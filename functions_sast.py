from subprocess import Popen, PIPE
import os

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

# [3] Decode apk
def decodeApk(package_name):
    os.chdir(os.path.dirname(__file__)+f'\\analyzed_apks\\{package_name}')
    cmd = '"apktool d -f base.apk"'
    os.system(cmd)
