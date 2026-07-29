import socket
import struct
import ipaddress
import select
import sys

PORT = 9999
IFACE = "enp1s0"  # Ép chặt vào interface này

def bind_to_device(sock, iface_name):
    """Ép socket gắn vào một card mạng cụ thể (Linux only)"""
    try:
        SO_BINDTODEVICE = getattr(socket, 'SO_BINDTODEVICE', 25)
        # Interface name phải được chuyển sang dạng bytes
        sock.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, iface_name.encode('utf-8'))
    except PermissionError:
        print(f"[-] LỖI QUYỀN TRUY CẬP: Không thể ép socket vào {iface_name}.")
        print("    Vui lòng chạy chương trình bằng quyền root (sudo python3 ...)")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Lỗi khi bind device {iface_name}: {e}")
        sys.exit(1)

def setup_receiver(mcast_ip_str):
    sockets = []
    
    # 1. Khởi tạo Socket IPv4
    try:
        sock_v4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_v4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bind_to_device(sock_v4, IFACE) # Ép vào enp1s0
        sock_v4.bind(('0.0.0.0', PORT))
        sockets.append(sock_v4)
        print(f"[*] Đang lắng nghe IPv4 (Unicast/Anycast) trên cổng {PORT}, card {IFACE}")
    except Exception as e:
        print(f"[-] Lỗi tạo socket IPv4: {e}")

    # 2. Khởi tạo Socket IPv6
    try:
        sock_v6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock_v6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bind_to_device(sock_v6, IFACE) # Ép vào enp1s0
        sock_v6.bind(('::', PORT))
        sockets.append(sock_v6)
        print(f"[*] Đang lắng nghe IPv6 (Unicast/Anycast) trên cổng {PORT}, card {IFACE}")
    except Exception as e:
        print(f"[-] Lỗi tạo socket IPv6: {e}")

    # 3. Xử lý gia nhập nhóm Multicast
    if mcast_ip_str:
        try:
            ip_obj = ipaddress.ip_address(mcast_ip_str)
            if not ip_obj.is_multicast:
                print(f"[-] Cảnh báo: {mcast_ip_str} không phải là địa chỉ Multicast!")
            else:
                if ip_obj.version == 4:
                    # Gửi bản tin IGMP Join (IPv4) qua enp1s0
                    mreq = struct.pack("4sl", socket.inet_aton(mcast_ip_str), socket.INADDR_ANY)
                    sock_v4.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                    print(f"[+] Đã gửi IGMP Join, gia nhập nhóm IPv4: {mcast_ip_str}")
                    
                elif ip_obj.version == 6:
                    # Gửi bản tin MLD Join (IPv6) qua enp1s0
                    # Lấy chính xác ID của card enp1s0
                    iface_idx = socket.if_nametoindex(IFACE)
                    mreq = socket.inet_pton(socket.AF_INET6, mcast_ip_str) + struct.pack('@I', iface_idx)
                    sock_v6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
                    print(f"[+] Đã gửi MLD Join, gia nhập nhóm IPv6: {mcast_ip_str}")
        except ValueError:
            print(f"[-] IP không hợp lệ: {mcast_ip_str}")

    return sockets

def main():
    print("="*50)
    print(f" BỘ NHẬN THÔNG ĐIỆP (ÉP CARD {IFACE.upper()}) ".center(50))
    print("="*50)
    
    print("[*] Gợi ý IP Multicast: IPv4 (vd: 224.1.1.1), IPv6 (vd: ff02::1)")
    mcast_target = input("[?] Nhập IP Multicast muốn gia nhập (Bỏ trống nếu chỉ nhận Unicast): ").strip()
    print("-" * 50)
    
    # Thiết lập các socket lắng nghe
    active_sockets = setup_receiver(mcast_target)
    
    if not active_sockets:
        print("[-] Không có socket nào hoạt động. Thoát chương trình.")
        return

    print(f"\n[*] Hệ thống đang chờ nhận thông điệp trên {IFACE}...")
    print("[*] Bấm Ctrl+C để thoát.\n")

    try:
        while True:
            # select chờ dữ liệu đến từ bất kỳ socket nào
            readable, _, _ = select.select(active_sockets, [], [])
            
            for sock in readable:
                data, addr = sock.recvfrom(1024)
                msg = data.decode('utf-8', errors='ignore')
                
                print(f"[+] Nhận được tin nhắn từ: {addr[0]}")
                print(f"    Giao diện: {IFACE}")
                print(f"    Nội dung: {msg}\n")
                
    except KeyboardInterrupt:
        print("\n[*] Đã đóng bộ nhận.")
    finally:
        for sock in active_sockets:
            sock.close()

if __name__ == "__main__":
    main()