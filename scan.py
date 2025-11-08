import socket

# NOTE: listen on port 1337 with netcat: nc -l 1337


def get_ssh_banner(host: str, port: int = 22, timeout: float = 2.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            banner = s.recv(1024).decode().strip()
            return banner if banner else None
    except (TimeoutError, ConnectionRefusedError, UnicodeDecodeError):
        return None


def get_http_server(host: str, port: int = 80, timeout: float = 2.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            # Send a minimal HTTP HEAD request
            s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
            response = s.recv(4096).decode()
            # Look for the 'Server:' header in the response
            for line in response.split("\r\n"):
                if line.lower().startswith("server:"):
                    return line.split(":", 1)[1].strip()
            return None
    except (TimeoutError, ConnectionRefusedError, UnicodeDecodeError):
        return None


def scan(ip_target, port_target):
    if port_target == 22:
        # test with 172.65.251.78:22
        data = get_ssh_banner(ip_target, port_target, 3.0)
        if data:
            print(data)
            return

    if port_target in (80, 443, 8080):
        # example with 104.21.5.178:80
        data = get_http_server(ip_target, port_target, 3.0)
        if data:
            print(data)
            return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(3)
            s.connect((ip_target, port_target))
            print("OK")
        except (TimeoutError, ConnectionRefusedError, OSError) as e:
            print(e)


def scan_range(ip_target, port_start, port_end):
    """
    Scanne une plage de ports sur une IP cible

    Args:
        ip_target: L'adresse IP à scanner
        port_start: Port de début (0-65535)
        port_end: Port de fin (0-65535)
    """
    print(f"\n=== Scan de {ip_target} - Ports {port_start} à {port_end} ===\n")

    for port in range(port_start, port_end + 1):
        print(f"Scanning port {port}...", end=" ")
        scan(ip_target, port)

    print(f"\n=== Scan terminé ===")