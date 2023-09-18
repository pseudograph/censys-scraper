import time

from censys.search import CensysHosts
import requests
import sys

API_URL = "https://www.censys.io/api/v1"

h = CensysHosts()


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

    ips = []
    keys = []
    print('Querying API...')
    query = h.search(f"services.http.response.body: *{TARGET}*", per_page=100, pages=100)
    for page in query:
        for host in page:
            print(host["ip"])
            ips.append(host["ip"])
    print(f"Query complete. {len(ips)} IPs retrieved.")

    for ip in ips:
        url = f"https://search.censys.io/hosts/{ip}/data/json"
        page = requests.get(url)
        key = ''
        attempts = 0
        while len(key) == 0 and attempts < 5:
            key = extractKey(page.content.decode('UTF-8'), TARGET, SHIFT_LEFT, LENGTH)
            if len(key) > 0:
                break
            time.sleep(1)
            attempts += 1
        print(f"{ip} : {key}")
        keys.append(key)

    for key in keys:
        if len(key) > 0:
            print(key)