import requests
from bs4 import BeautifulSoup
import numpy as np

proxy_sites = [
    'https://free-proxy-list.net/',
    'https://www.us-proxy.org/',
    "https://hidemy.name/en/proxy-list/",
]

proxy_sites2 = [
    "https://openproxy.space/free-proxy-list",
]


def get_proxies(s):
    print(s)

    main = s
    r = requests.get(main)
    soup = BeautifulSoup(r.text, 'html.parser')
    tds = soup.find_all('table')[0].find_all("td")

    proxies = []

    for i in range(len(tds) // 8):
        proxy = tds[i * 8].getText().strip() + ":" + tds[i * 8 + 1].getText().strip()
        proxies.append(proxy)

    return proxies

def get_proxies2(s):
    print(s)

    main = s
    r = requests.get(main)
    soup = BeautifulSoup(r.text, 'html.parser')
    tds = soup.find_all('table')[0].find_all("td")

    proxies = []

    for i in range(len(tds) // 8):
        proxy = tds[i * 8 + 1].getText().strip() + ":" + tds[i * 8 + 2].getText().strip()
        proxies.append(proxy)

    return proxies


proxies = []
for site in proxy_sites:
    proxies.extend(get_proxies(site))
for site in proxy_sites2:
    proxies.extend(get_proxies2(site))

proxies = list(set(proxies))

np.random.shuffle(proxies)

proxies_str = '\n'.join(proxies)

with open('scraped_proxies.txt', 'a') as f:
    f.write(proxies_str)
