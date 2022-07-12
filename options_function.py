from subprocess import Popen, PIPE
import os
import re

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
    # opening and reading the file
    with open(strings_path) as file:
        for line in file:
                urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', line)
                ips = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                if(len(urls)>0):
                    print(urls)
                if(len(ips)>0):
                    print(ips)
# End retrieve all urls
