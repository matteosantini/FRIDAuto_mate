import re
import shodan
import requests
from urllib.parse import urlparse

# Retrieve all urls
def extractUrlsAndIpsFromFile(strings_path):
    founded_list = {}
    founded_list["urls"]  = []
    founded_list["ips"] = []
    # opening and reading the file
    with open(strings_path) as file:
        for line in file:
                url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', line)
                ip = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                if(len(url)>0):
                    founded_list["urls"].append(url[0])
                if(len(ip)>0):
                    founded_list["ips"].append(ip[0])
    print(founded_list)
    return founded_list

# Shodan Search
def extractDomainFromUrl(url):
    return urlparse(url).netloc

def shodanResolveDns(api_shodan, SHODAN_API_KEY, domain):
    try:
            dns_resolve = 'https://api.shodan.io/dns/resolve?hostnames=' + domain + '&key=' + SHODAN_API_KEY
            resolved = requests.get(dns_resolve)
            host_ip = resolved.json()[domain]
            return host_ip
    except shodan.APIError as error:
            print('Error: {}'.format(error))

def shodanSearchIp(api, ip):
    try:
        host = api.host(ip)
        return host
    except shodan.APIError as error:
        print('Error: {}'.format(error))
