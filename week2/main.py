from md_fw_declare import *
from md_fw_menu import *

TEST_CASES = {
    "1": {
        "title": "VALID_PACKET",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6, dst=VALID_DST_IPv6) /
            TCP(sport=VALID_SPORT, dport=VALID_DPORT) /
            payload_default
        )
    },
    "2": {
        "title": "INVALID_SRC_IPv6",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=INVALID_SRC_IPv6, dst=VALID_DST_IPv6) /
            TCP(sport=VALID_SPORT, dport=VALID_DPORT) /
            payload_default
        )
    },
    "3": {
        "title": "INVALID_DST_IPv6",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=INVALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT)/
            payload_default
        )
    },
    "4": {
        "title": "VALID_DST_Multicast",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_Multicast)/
            ICMPv6EchoRequest() /
            payload_default
        )
    },
    "5": {
            "title": "INVALID_DST_Multicast",
            "packet": (
                Ether(src=SRC_MAC, dst=DST_MAC) /
                dot1q /
                IPv6(src=VALID_SRC_IPv6,dst=INVALID_DST_Multicast)/
                ICMPv6EchoRequest() /
                payload_default
            )
    },
    "6": {
        "title": "INVALID_TCP_DPORT",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=INVALID_DPORT)/
            payload_default
        )
    },
    "7": {
        "title": "INVALID_TCP_SPORT",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=INVALID_SPORT,dport=VALID_DPORT)/
            payload_default
        )
    },
    "8": {
        "title": "VALID_UDP_PORT",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            UDP(sport=VALID_SPORT,dport=VALID_DPORT)/
            payload_default
        )
    },
    "9": {
        "title": "INVALID_UDP_DPORT",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            UDP(sport=VALID_SPORT,dport=INVALID_DPORT)/
            payload_default
        )
    },
    "10": {
            "title": "INVALID_UDP_SPORT",
            "packet": (
                Ether(src=SRC_MAC, dst=DST_MAC) /
                dot1q /
                IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
                UDP(sport=INVALID_SPORT,dport=VALID_DPORT)/
                payload_default
            )
    },
    "11": {
        "title": "TC-11: Invalid VLAN Tag (Dot1Q)",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            Dot1Q(vlan=INVALID_VLAN_ID) /
            IPv6(src=VALID_SRC_IPv6, dst=VALID_DST_IPv6) /
            TCP(sport=VALID_SPORT, dport=VALID_DPORT) /
            "TEST_FIREWALL_VLAN_FILTER"
        )
    },
    "12": {
        "title": "TC-12: Untagged Packet (No 802.1Q)",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            IPv6(src=VALID_SRC_IPv6, dst=VALID_DST_IPv6) /
            TCP(sport=VALID_SPORT, dport=VALID_DPORT) /
            "TEST_FIREWALL_UNTAGGED_PACKET"
        )
    },
    "13": {
        "title": "TC-13: Invalid Ethernet Src MAC",
        "packet": (
            Ether(src=INVALID_SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6, dst=VALID_DST_IPv6) /
            TCP(sport=VALID_SPORT, dport=VALID_DPORT) /
            "TEST_FIREWALL_INVALID_SRC_MAC"
        )
    },
    "14": {
        "title": "VALID_ICMPV6_ECHO_REQUEST",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            ICMPv6EchoRequest(id=0x1234,seq=1,data=payload_default)
        )
    },
    "15": {
        "title": "TC-15: Invalid Next Header (SCTP = 132)",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6, dst=VALID_DST_IPv6, nh=132) /
            Raw(load="TEST_FIREWALL_INVALID_NEXT_HEADER_SCTP")
        )
    },
    "16": {
        "title": "INVALID_TCP_FLAGS_NULL",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x00)/
            payload_default
        )
    },
    "17a": {
        "title": "INVALID_TCP_FLAGS_SYN_FIN",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x03)/
            payload_default
        )
    },
    "17b": {
        "title": "INVALID_TCP_FLAGS_SYN_RST",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x06)/
            payload_default
        )
    },
    "17c": {
        "title": "INVALID_TCP_FLAGS_FIN_RST",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x05)/
            payload_default
        )
    },
    "17d": {
        "title": "INVALID_TCP_FLAGS_FIN_ONLY",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x01)/
            payload_default
        )
    },
    "17e": {
        "title": "INVALID_TCP_FLAGS_XMAS",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x29)/
            payload_default
        )
    },
    "17f": {
        "title": "INVALID_TCP_FLAGS_ALL",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x3F)/
            payload_default
        )
    },
    "17g": {
        "title": "INVALID_TCP_FLAGS_SYN_FIN_PSH",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x0B)/
            payload_default
        )
    },
    "17h": {
        "title": "INVALID_TCP_FLAGS_SYN_FIN_RST",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x07)/
            payload_default
        )
    },
    "17i": {
        "title": "INVALID_TCP_FLAGS_URG_ONLY",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x20)/
            payload_default
        )
    },
    "17j": {
        "title": "INVALID_TCP_FLAGS_PSH_URG",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x28)/
            payload_default
        )
    },
    "17k": {
        "title": "UNSOLICITED_TCP_FLAGS_SYN_ACK",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x12)/
            payload_default
        )
    },
    "17l": {
        "title": "UNSOLICITED_TCP_FLAGS_FIN_ACK",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x11)/
            payload_default
        )
    },
    "17m": {
        "title": "VALID_TCP_FLAGS_SYN_ONLY",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT,flags=0x02)/
            payload_default
        )
    },
    "18": {
        "title": "EMPTY_PAYLOAD",
        "packet": (
            Ether(src=SRC_MAC, dst=DST_MAC) /
            dot1q /
            IPv6(src=VALID_SRC_IPv6,dst=VALID_DST_IPv6)/
            TCP(sport=VALID_SPORT,dport=VALID_DPORT)/
            payload_empty
        )
    },

}
PKT_Default_Receive = None

def select_test_case():
    """Select packet from TEST_CASES"""
    global PKT_Default_Receive

    print("\n========== Test Cases ==========")
    for tc_id, tc in TEST_CASES.items():
        print(f"{tc_id:>4} : {tc['title']}")
    print("================================")

    case = input("Enter Test Case ID: ").strip()

    if case not in TEST_CASES:
        print(f"[ERROR] Test Case '{case}' does not exist.")
        return False

    PKT_Default_Receive = TEST_CASES[case]["packet"]

    print(f"\nSelected: {case} - {TEST_CASES[case]['title']}")
    return True


def print_infor():
    global PKT_Default_Receive

    if PKT_Default_Receive is None:
        print("Please select a Test Case first.")
        return

    print("\n---------- Packet Information ----------")
    PKT_Default_Receive.show()


def send_packet():
    global PKT_Default_Receive

    if PKT_Default_Receive is None:
        print("Please select a Test Case first.")
        return

    try:
        print("\nSending packet...")
        PKT_Default_Receive.show()
        sendp(PKT_Default_Receive, iface=IFACE, count=7, inter=0.01)
        print("Packet sent successfully.")
    except Exception as ex:
        print("Error:", ex)

def print_menu():
    print("""
========== MENU ==========
1. Select Test Case
2. Show Packet
3. Send Packet
0. Exit
==========================
""")
    return input("Choice: ")


def main():
    while True:
        try:
            choice = print_menu()

            if choice == "1":
                select_test_case()

            elif choice == "2":
                print_infor()

            elif choice == "3":
                send_packet()

            elif choice == "0":
                print("Bye!")
                break

            else:
                print("Invalid choice.")

        except KeyboardInterrupt:
            print("\nBye!")
            break


if __name__ == "__main__":
    main()