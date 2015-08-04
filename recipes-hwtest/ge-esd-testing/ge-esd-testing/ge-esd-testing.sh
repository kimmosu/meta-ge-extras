#!/bin/sh
init_hw() {
    echo Taking down network interfaces...
    for i in eth0 eth1 wlan0; do ifdown $i; done
    echo Bringing networn interfaces back up..
    for i in eth0 eth1 wlan0; do ifup $i; done
    echo configuring WLAN...
    wpa_cli <<EOF
add_network
set_network 1 ssid "$wpa_ssid"
set_network 1 psk "$wpa_psk"
select_network 1
quit
EOF
    echo Fetching IP address for WLAN...
    udhcpc -i wlan0
}

check_hw() {
    echo Pinging gateway through all interfaces...
    for i in eth0 eth1 wlan0; do ping -I $i $gateway_ip -c 3; done
    echo Reading MPL3115
    cat /sys/class/i2c-dev/i2c-4/device/4-0060/iio\:device1/in_temp_raw
    cat /sys/class/i2c-dev/i2c-4/device/4-0060/iio\:device1/in_temp_scale
    cat /sys/class/i2c-dev/i2c-4/device/4-0060/iio\:device1/in_pressure_raw
    cat /sys/class/i2c-dev/i2c-4/device/4-0060/iio\:device1/in_pressure_scale
}

wpa_ssid="Bx60_TEST"
wpa_psk="1234567890"
gateway_ip="192.168.0.254"

action="help"
while [ "x$1" != "x" ] ; do
    case $1 in
	init)
	    action="init"
	    ;;
	check)
	    action="check"
	    ;;
	help)
	    action="help"
	    ;;
	*)
	    echo "Unknown command $1" ; action="help"
	    ;;
    esac
    shift
done

case $action in
init)
	init_hw
	;;
check)
	check_hw
	;;
help)
	echo "usage: $0 init|check|help"
esac
