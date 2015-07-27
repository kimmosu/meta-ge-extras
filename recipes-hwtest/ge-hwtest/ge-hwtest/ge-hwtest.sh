#!/bin/sh
usage()
{
    echo "Usage: $0 [testname]"
    echo
    echo "Supported testnames:"
    echo "  dhrystone   -- launch the dhrystone tester in a loop"
    echo "  dhrystone2  -- launch two dhrystone testers in parallel"
    echo "  linpack     -- launch the linpack test in a loop"
    echo "  linpack2    -- launch two linpack tests in parallel"
    echo "  dhry_lin    -- launch dhrystone and linpack in parallel"
    exit 1
}

if [ $# -ne 1 ] ; then
    usage $0
fi

start_subprocess()
{
    xterm -e sh -c "$*" &
    PIDS="$PIDS $!"
}

start_dhrystone()
{
    start_subprocess "while true; do echo 100000000 | dhry ; done"
}

start_linpack()
{
    start_subprocess "while true; do echo 8000 | linpack ; done"
}

PIDS=""
case $1 in
    dhrystone)
	start_dhrystone
	;;
    dhrystone2)
	start_dhrystone
	start_dhrystone
	;;
    linpack)
	start_linpack
	;;
    linpack2)
	start_linpack
	start_linpack
	;;
    dhry_lin)
	start_dhrystone
	start_linpack
	;;
    *)
	usage $0
	;;
esac

read -p "Press enter to exit:" line

for pid in $PIDS ; do
    kill $pid
done
