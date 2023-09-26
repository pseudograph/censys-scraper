import time

from censys.search import CensysHosts
import requests
import sys

API_URL = "https://www.censys.io/api/v1"



class Server:
    def __init__(self, ip, port, type):
        self.ip = ip
        self.port = port
        self.type = type


def extractKey(content: str, target: str, shiftLeft: int, length: int) -> str:
    middleIndex = content.find(f"{target}")
    startIndex = middleIndex - shiftLeft
    return content[startIndex: startIndex + length]


if __name__ == '__main__':
    UID: str = sys.argv[1]
    SECRET: str = sys.argv[2]
    TARGET: str = sys.argv[3]
    SHIFT_LEFT: int = int(sys.argv[4])
    LENGTH: int = int(sys.argv[5])
    h = CensysHosts(UID, SECRET)

    servers = []
    keys = []
    print('Querying API...')
    query = h.search(f"services.http.response.body: *{TARGET}*", per_page=100, pages=100)
    for page in query:
        for host in page:
            for service in host["services"]:
                if service["service_name"] == 'HTTP':
                    servers.append(Server(ip=host["ip"], port=service["port"], type='http'))
                elif service["service_name"] == 'HTTPS':
                    servers.append(Server(ip=host["ip"], port=service["port"], type='https'))

    print(f"Query complete. {len(servers)} IPs retrieved.")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    for server in servers:
        try:
            response = requests.get(f"{server.type}://{server.ip}:{server.port}/", headers=headers, timeout=10)
            key = ''
            key = extractKey(response.content.decode('UTF-8'), TARGET, SHIFT_LEFT, LENGTH)
            if len(key) == 0:
                continue
            print(f"{server.ip}:{server.port} : {key}")
            keys.append(key)
        except Exception as error:
            print(f"{server.ip}:{server.port} : {error}")

    for key in keys:
        if len(key) > 0:
            print(key)

