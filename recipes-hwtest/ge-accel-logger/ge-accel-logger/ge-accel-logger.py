#!/usr/bin/python
# -*- coding: utf-8 -*-

# ge-accel-logger.py
#
# Read temperature and pressure from MMA8453
#
# Copyright (C) 2015 General Electric Company. All Rights Reserved.

import optparse
import glob
import sys
import time


class MMA8453:
    """Read the MMA8453 info through sysfs"""
    def __init__(self, bus, addr):
        sysfspath = "/sys/bus/i2c/devices/{0}-{1:04x}".format(
            bus, addr)
        with open("{0}/name".format(sysfspath)) as name:
            myname = name.readline().strip()
            if myname != "mma8453":
                raise RuntimeError("Device name mismatch")
        iionames = glob.glob("{0}/iio:device*".format(sysfspath))
        if len(iionames) == 0:
            raise RuntimeError("Can't find an IIO device")
        self.iioname = iionames[0]
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    
    def set_x(self, value):
        self.x = value

    def set_y(self, value):
        self.y = value

    def set_z(self, value):
        self.z = value

    axes = ( ("in_accel_x_raw", set_x),
             ("in_accel_y_raw", set_y),
             ("in_accel_z_raw", set_z) )

    def update(self):
        with open("{0}/in_accel_scale".format(self.iioname)) as scale_file:
            scale = float(scale_file.readline().strip())
        for (file_name, setter) in self.axes:
            with open("{0}/{1}".format(self.iioname, file_name)) as value_file:
                raw_val = int(value_file.readline().strip())
                setter(self, raw_val * scale)


class Params:
    """Command line parsing"""
    def __init__(self):
        parser = optparse.OptionParser(description=\
                                       "Read accelerometer values and store to file.",
                                       version="0.1")
        parser.add_option("-o", action="store", type="string",
                          dest="output", default="-",
                          help="output filename (use - for stdout)")
        parser.add_option("-p", "--period", action="store", type="int",
                          dest="period", default=60,
                          help="sampling period in seconds")
        parser.add_option("-s", "--singleshot", action="store_true",
                          dest="singleshot", default=False,
                          help="Single shot; don't repeat")
        (self.options, self.args) = parser.parse_args()

    def singleshot(self):
        return self.options.singleshot

    def output(self):
        return self.options.output

    def period(self):
        return self.options.period


class Sleeper:
    """Helper class to implement regular interval sleeping"""
    def __init__(self, period):
        self.period = period
        self.next_time = time.time() + period

    def wait(self):
        now = time.time();
        diff = self.next_time - now;
        if diff > 0:
            time.sleep(diff)
            self.next_time += self.period
        else:
            self.next_time = now + period


class Output:
    """Takes care of outputting to file"""
    def __init__(self, file):
        self.file = file

    def write_header(self):
        self.file.write("Time\tX\tY\tZ\n")

    def write_values(self, time, x, y, z):
        self.file.write("{0}\t{1}\t{2}\t{3}\n".format(time, x, y, z))


def main():
    params = Params()

    if params.output() == '-':
        ofile = sys.stdout
    else:
        ofile = open(params.output(), "w")

    MMA8453_I2C_BUS = 3
    MMA8453_I2C_DEV = 0x1C
    mma = MMA8453(MMA8453_I2C_BUS, MMA8453_I2C_DEV)

    output = Output(ofile)

    output.write_header()
    mma.update()
    output.write_values(time.time(), mma.x, mma.y, mma.z)

    if not params.singleshot():
        sleeper = Sleeper(params.period())
        while True:
            sleeper.wait()
            mma.update()
            output.write_values(time.time(), mma.x, mma.y, mma.z)


if __name__ == "__main__":
    main()
