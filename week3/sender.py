import socket
import struct

PORT = 9999
IFACE = b"eth0"  # Ép gửi qua card eth0

def bind_to_device(sock):
    """Hàm ép socket gắn vào interface cụ thể trên Linux"""
    try:
        SO_BINDTODEVICE = getattr(socket, 'SO_BINDTODEVICE', 25)
        sock.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, IFACE)
    except Exception as e:
        print(f"[-] Cảnh báo: Không thể bind socket vào {IFACE.decode()}: {e}")
        print("    Vui lòng chạy chương trình bằng quyền root/sudo!")

def send_packet(ip_version, mode, default_ip):
    print(f"\n" + "="*45)
    print(f" CẤU HÌNH GỬI {mode.upper()} ({'IPv4' if ip_version == 4 else 'IPv6'}) ".center(45, "-"))
    
    # 1. Tùy chọn thay đổi IP đích bằng hàm input()
    print(f"[*] Địa chỉ {mode} gợi ý: {default_ip}")
    target_ip = input(f"[?] Nhập địa chỉ {mode} bạn muốn gửi đến (Nhấn Enter để dùng gợi ý): ").strip()
    if not target_ip:
        target_ip = default_ip

    # 2. Tùy chọn thay đổi nội dung thông điệp
    message = input("[?] Nhập nội dung thông điệp (Nhấn Enter để dùng mặc định): ").strip()
    if not message:
        message = f"Day la thong diep {mode} ({'IPv4' if ip_version == 4 else 'IPv6'}) gui qua {IFACE.decode()}!"

    # 3. Tiến hành gửi gói tin
    try:
        if ip_version == 4:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bind_to_device(sock)
            
            # Cấu hình TTL nếu là Multicast IPv4
            if mode == "Multicast":
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
                
            sock.sendto(message.encode('utf-8'), (target_ip, PORT))
            
        elif ip_version == 6:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            bind_to_device(sock)
            
            # Cấu hình Hops nếu là Multicast IPv6
            if mode == "Multicast":
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 2)
                import struct
                iface_idx = socket.if_nametoindex(IFACE.decode('utf-8'))
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, struct.pack('@I', iface_idx))
                
            sock.sendto(message.encode('utf-8'), (target_ip, PORT))
            
        print(f"\n[+] ĐÃ GỬI THÀNH CÔNG!")
        print(f"    Giao diện xuất : {IFACE.decode()}")
        print(f"    Chế độ gửi     : {mode}")
        print(f"    Đích đến       : {target_ip}:{PORT}")
        print(f"    Nội dung       : {message}\n")
        
    except Exception as e:
        print(f"\n[-] LỖI GỬI GÓI TIN: {e}\n")
    finally:
        if 'sock' in locals():
            sock.close()

def main_menu():
    while True:
        print("\n" + "="*45)
        print(" MENU LỰA CHỌN PHƯƠNG THỨC GỬI (SOCKET) ".center(45))
        print("="*45)
        print("  1. IPv4 - Gửi Unicast")
        print("  2. IPv4 - Gửi Multicast")
        print("  3. IPv4 - Gửi Anycast")
        print("-" * 45)
        print("  4. IPv6 - Gửi Unicast")
        print("  5. IPv6 - Gửi Multicast")
        print("  6. IPv6 - Gửi Anycast")
        print("-" * 45)
        print("  0. Thoát chương trình")
        print("="*45)
        
        choice = input("Vui lòng chọn (0-6): ").strip()
        
        # Các IP mặc định dưới đây chỉ là gợi ý, người dùng sẽ được hỏi lại bằng input()
        if choice == '1':
            send_packet(ip_version=4, mode="Unicast", default_ip="192.168.69.160")
        elif choice == '2':
            send_packet(ip_version=4, mode="Multicast", default_ip="224.1.1.1")
        elif choice == '3':
            send_packet(ip_version=4, mode="Anycast", default_ip="1.1.1.1") 
        elif choice == '4':
            send_packet(ip_version=6, mode="Unicast", default_ip="fe80::1")
        elif choice == '5':
            send_packet(ip_version=6, mode="Multicast", default_ip="ff02::1")
        elif choice == '6':
            send_packet(ip_version=6, mode="Anycast", default_ip="2001:db8::1")
        elif choice == '0':
            print("Thoát chương trình. Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại!")

if __name__ == "__main__":
    main_menu()