from subprocess import Popen, PIPE
import os
import re
import shodan
import requests
from urllib.parse import urlparse

# [2] download apk from device
def retrievePackage(package_name):
    command = ['adb', 'shell', 'pm', 'path', package_name]
    process = Popen(command, stdout=PIPE, stderr=True)
    output, error = process.communicate()
    location_pkg = output.decode('utf-8').replace('package:', '')
    return location_pkg

def pullApkToPackageFolder(directory, package_name, location_pkg):
    os.chdir(directory)
    if not os.path.exists(f'.\\analyzed_apks\\{package_name}'):
        os.makedirs(f'.\\analyzed_apks\\{package_name}')
    cmd = f'"adb pull {location_pkg} .\\analyzed_apks\\{package_name}"'.replace('\n','')
    os.system(cmd)
# [2] End

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
        # print(host)
        # print('IP: '+ str(host['ip']))
        # print('Organization: %s ' % host.get['org', 'n/a'])
        return host
    except shodan.APIError as error:
        print('Error: {}'.format(error))
# End Shodan Search
