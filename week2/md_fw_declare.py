from scapy.all import *
from scapy.layers.inet import *
from scapy.layers.inet6 import *
from scapy.layers.l2 import Dot1Q
from random import randint
from netaddr import *
import binascii
import sys

import signal
from threading import Thread
from sqlalchemy import false 
# Interface
IFACE = "enp1s0"

PKT_COUNT = 5

# Scan Ports 
FROM_PORT = 1 
TO_PORT = 65536 

SRC_MAC = "2c:58:b9:8b:51:c2"
DST_MAC = "d8:3a:dd:a4:c0:75"
INVALID_SRC_MAC = "fa:fb:fc:fd:fe:ff"

VLAN_ID = 5
INVALID_VLAN_ID= 10
#IPv6s 
INVALID_DST_IPv6 = "fd22:9696:0123:0003::69"
INVALID_SRC_IPv6 = "fd22:ffff:0123:0003::99"

VALID_DST_IPv6 = "fd53:1234:5678:5::14"
VALID_SRC_IPv6 = "fd53:1234:5678:5::12"


VALID_DST_Multicast = "ff02::1" 
INVALID_DST_Multicast = "ff00::1"

# Ports 
VALID_SPORT = 65535 
VALID_DPORT = 80 
INVALID_DPORT = 65534 
INVALID_SPORT = 999

RANGE = (1000, 65535) 
pro_type = TCP 
# Layers 
dot1q = Dot1Q(vlan=VLAN_ID) 
# Payload 
payload_default ="Default"
payload_empty=""

PKT_Default_Receive = Ether(src=SRC_MAC, dst=DST_MAC)/dot1q/IPv6(src=VALID_SRC_IPv6, 
dst=VALID_DST_IPv6)/pro_type(sport=VALID_SPORT, dport=VALID_DPORT)/payload_default 
PKT_Default_Send = Ether(src=DST_MAC, dst=SRC_MAC)/dot1q/IPv6(src=VALID_DST_IPv6, 
dst=VALID_SRC_IPv6)/pro_type(sport=VALID_DPORT, dport=VALID_SPORT)/payload_default