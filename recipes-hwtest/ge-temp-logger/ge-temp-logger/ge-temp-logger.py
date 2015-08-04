#!/usr/bin/python
# -*- coding: utf-8 -*-

# ge-temp-logger.py
#
# Read temperature and pressure from MPL3115
#
# Copyright (C) 2015 General Electric Company. All Rights Reserved.

import optparse
import glob
import sys
import time

class MPL3115:
    """Read the MPL3115 info through sysfs"""
    def __init__(self, bus, addr):
        sysfspath = "/sys/bus/i2c/devices/{0}-{1:04x}".format(
            bus, addr)
        with open("{0}/name".format(sysfspath)) as name:
            myname = name.readline().strip()
            if myname != "mpl3115":
                raise RuntimeError("Device name mismatch")
        iionames = glob.glob("{0}/iio:device*".format(sysfspath))
        if len(iionames) == 0:
            raise RuntimeError("Can't find an IIO device")
        self.iioname = iionames[0]
        self.temperature = -273.15
        self.pressure = 0.0

    def update(self):
        self.read_temperature(self.iioname)
        self.read_pressure(self.iioname)

    def read_temperature(self, iiopath):
        with open("{0}/in_temp_raw".format(iiopath)) as raw_temp:
            val = int(raw_temp.readline().strip())
        with open("{0}/in_temp_scale".format(iiopath)) as temp_scale:
            scale = float(temp_scale.readline().strip())
        self.temperature = val * scale

    def read_pressure(self, iiopath):
        with open("{0}/in_pressure_raw".format(iiopath)) as raw_pressure:
            val = int(raw_pressure.readline().strip())
        with open("{0}/in_pressure_scale".format(iiopath)) as pressure_scale:
            scale = float(pressure_scale.readline().strip())
        self.pressure = val * scale

class Params:
    """Command line parsing"""
    def __init__(self):
        parser = optparse.OptionParser(description=\
                                       "Read temperature and pressure values and store to file.",
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
        self.file.write("Time\tTemp\tPressure\n")

    def write_values(self, time, temp, pressure):
        self.file.write("{0}\t{1}\t{2}\n".format(time,temp,pressure))

def main():

    params = Params()

    if params.output() == '-':
        ofile = sys.stdout
    else:
        ofile = open(params.output(), "w")

    MPL_I2C_BUS = 4
    MPL_I2C_DEV = 0x60
    mpl = MPL3115(MPL_I2C_BUS, MPL_I2C_DEV)

    output = Output(ofile)

    output.write_header()
    mpl.update()
    output.write_values(time.time(), mpl.temperature, mpl.pressure)

    if not params.singleshot():
        sleeper = Sleeper(params.period())
        while True:
            sleeper.wait()
            mpl.update()
            output.write_values(time.time(), mpl.temperature, mpl.pressure)


if __name__ == "__main__":
    main()
