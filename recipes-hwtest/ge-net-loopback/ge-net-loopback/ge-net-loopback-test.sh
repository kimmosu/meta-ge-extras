#!/bin/sh

# ge-net-loopback-test.sh
# eth0 and eth1 loopback testing

# IP addresses for eth0 & eth1
IP0=192.168.1.10
IP1=192.168.2.10

# Fake IP addresses for routing
IP00=192.168.101.10
IP11=192.168.102.10

PROGNAME=$0
RUNTIME=60

usage() {
    cat <<EOF
Usage: $PROGNAME [-t n] [--help]
   -t, --time       : set the running time in seconds (default=$RUNTIME)
                      (to continue forever, use -t 0)
   -h, --help       : print this usage information
EOF
    exit
}

# Check command line
while [ ! -z "$1" ] ; do
    case "$1" in
	-h|--help) usage ;;
	-t|--time) RUNTIME=$2; shift ;;
	*) echo "Unknown argument $1" ; usage ;;
    esac
    shift
done

cleanup() {
    ifdown eth0 >/dev/null 2>&1
    ifconfig eth0 down
    ifdown eth1 >/dev/null 2>&1
    ifconfig eth1 down
    iptables -t nat -F
    arp -d $IP00
    arp -d $IP11
}

fail() {
   echo $*
   cleanup
   exit 1
}

# Cleanup to be safe
cleanup

# Get MAC addresses
MAC0=`cat /sys/class/net/eth0/address`
MAC1=`cat /sys/class/net/eth1/address`

[ ! -z "${MAC0}" ] || fail "Failed to get MAC address for eth0!"
[ ! -z "${MAC1}" ] || fail "Faled to get MAC address for eth1!"

# Configure interfaces
ifconfig eth0 ${IP0} || fail "Unable to configure eth0!"
ifconfig eth1 ${IP1} || fail "Unable to configure eth1!"

# Set up NAT
iptables -t nat -A POSTROUTING -s ${IP0} -d ${IP11} -j SNAT --to-source ${IP00} && \
iptables -t nat -A POSTROUTING -s ${IP1} -d ${IP00} -j SNAT --to-source ${IP11} && \
iptables -t nat -A PREROUTING -d ${IP00} -j DNAT --to-destination ${IP0} && \
iptables -t nat -A PREROUTING -d ${IP11} -j DNAT --to-destination ${IP1}
[ $? -eq 0 ] || fail "Error setting up NAT tables!"

# Add cross routing to fake addresses:
ip route add ${IP11} dev eth0 && \
arp -i eth0 -s ${IP11} ${MAC1} && \
ip route add ${IP00} dev eth1 && \
arp -i eth1 -s ${IP00} ${MAC0} && \
[ $? -eq 0 ] || fail "Error setting up cross routing!"

# Now run iperf
start-stop-daemon -S -x /usr/bin/iperf -- -B ${IP0} -s -D
iperf -B ${IP1} -c ${IP00} -t ${RUNTIME} -i 10
killall -QUIT iperf

cleanup
