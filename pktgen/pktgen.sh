#! /bin/sh

modprobe pktgen

PKTGEND=1                 # number of CPU's - 1
CLONE_SKB="clone_skb 1"   # how many copys of each packet
PKT_SIZE="pkt_size 0"    # Size of the generated packet
COUNT="count 1000000"     # How many packets per thread to send
DELAY="delay 000"         # delay between packets
INTERFACE="eth1"          # which interface to generate the packets on
MAC="00:00:00:00:00:00"   # MAC address of the targets interface

function pgset() {
    local result

    echo $1 > $PGDEV

    result=`cat $PGDEV | grep -F "Result: OK:"`
    if [ "$result" = "" ]; then
         cat $PGDEV | grep -F Result:
    fi
}

function pg() {
    echo inject > $PGDEV
    cat $PGDEV
}

# Config Start Here -----------------------------------------------------------

remove_all()
{
 # thread config
 for i in `seq 0 $PKTGEND`;do
  PGDEV=/proc/net/pktgen/kpktgend_"$i"
  pgset "rem_device_all"
 done
}

remove_all

for i in `seq 0 $PKTGEND`;do
 PGDEV=/proc/net/pktgen/kpktgend_"$i"
 pgset "add_device $INTERFACE@$i"
done

# device config
#

for i in `seq 0 $PKTGEND`;do
 PGDEV=/proc/net/pktgen/$INTERFACE@$i
 echo "Configuring $PGDEV"
 pgset "$COUNT"
 pgset "$CLONE_SKB"
 pgset "$PKT_SIZE"
 pgset "$DELAY"
 pgset "flag QUEUE_MAP_CPU"
 pgset "flag IPDST_RND"
 pgset "flag FLOW_SEQ"
 pgset "dst 1.1.1.2"
 pgset "flows 2048"
 pgset "flowlen 30"
 #pgset "dst_mac $MAC"
 pgset "dst_port 80"
 pgset "udp_dst_min 1"
 pgset "udp_dst_max 65535"
 pgset "src_min 10.0.0.1"
 pgset "src_max 10.0.0.254"
done

# Time to run
PGDEV=/proc/net/pktgen/pgctrl

echo "Running... ctrl^C to stop"
pgset "start"
echo "Done"

grep pps /proc/net/pktgen/*
