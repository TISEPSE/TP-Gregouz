import argparse
import ipaddress

from scan import scan, scan_range


def valid_ipv4_address(value):
    try:
        ipaddress.IPv4Address(value)
        return value
    except ipaddress.AddressValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid IPv4 address.")


def valid_port(value):
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer.")

    if not (0 <= port <= 65535):
        raise argparse.ArgumentTypeError(
            f"{port} is not a valid port number (0-65535)."
        )
    return port


def valid_port_range(value):
    """
    Valide une plage de ports au format 'start-end' (ex: 20-80)
    """
    try:
        start, end = value.split('-')
        start_port = valid_port(start)
        end_port = valid_port(end)

        if start_port > end_port:
            raise argparse.ArgumentTypeError(
                f"Le port de début ({start_port}) doit être inférieur ou égal au port de fin ({end_port})."
            )

        return (start_port, end_port)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{value} n'est pas un format de range valide. Utilisez le format 'start-end' (ex: 20-80)."
        )


parser = argparse.ArgumentParser(
    description="Scanner de ports pour une adresse IP"
)
parser.add_argument(
    "-i", "--ip", type=valid_ipv4_address, required=True, help="L'adresse IP v4 cible"
)
parser.add_argument(
    "-p", "--port", nargs="+", type=valid_port, help="Le(s) port(s) cible(s) (0-65535)"
)
parser.add_argument(
    "-r", "--range", type=valid_port_range, help="Plage de ports à scanner (ex: 20-80)"
)
args = parser.parse_args()

# Vérifier qu'au moins --port ou --range est spécifié
if not args.port and not args.range:
    parser.error("Vous devez spécifier au moins --port ou --range")

# Vérifier que --port et --range ne sont pas utilisés ensemble
if args.port and args.range:
    parser.error("Vous ne pouvez pas utiliser --port et --range en même temps")

# Exécuter le scan
if args.range:
    start_port, end_port = args.range
    scan_range(args.ip, start_port, end_port)
else:
    print(f"port = {args.port}, ip = {args.ip}")
    for port in args.port:
        scan(args.ip, port)