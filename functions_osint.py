import re
import shodan
import requests
import vt
import json

from urllib.parse import urlparse

# retrieve json configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# init shodan api
SHODAN_API_KEY = config["api_key_shodan"]
api_shodan = shodan.Shodan(SHODAN_API_KEY)

# init virustotal api
VT_API_KEY = config["api_key_virustotal"]
client = vt.Client(VT_API_KEY)

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

def shodanResolveDns(domain):
    try:
            dns_resolve = 'https://api.shodan.io/dns/resolve?hostnames=' + domain + '&key=' + SHODAN_API_KEY
            resolved = requests.get(dns_resolve)
            host_ip = resolved.json()[domain]
            return host_ip
    except shodan.APIError as error:
            print('Error: {}'.format(error))

def shodanSearchIp(ip):
    try:
        host = api_shodan.host(ip)
        return host
    except shodan.APIError as error:
        print('Error: {}'.format(error))

# virustotal search
def vtScanUrl(url):
    url_id = vt.url_id(url)
    url = client.get_object("/urls/{}", url_id)
    return url

    
