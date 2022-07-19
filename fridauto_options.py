import functions_sast
import os
import subprocess
from xml.dom import minidom
import re

def retrieveApk(package_name):
    print("[*]")
    print("[*] Retrieving package location...")
    location_pkg = functions_sast.retrievePackage(package_name)
    print("[*] Package location: " + location_pkg)
    print("[*] Pulling apk into /analyzed_apks")
    functions_sast.pullApkToPackageFolder(os.path.dirname(__file__), package_name, location_pkg)
    print(f"[*] APK saved in {os.path.dirname(__file__)}\\analyzed_apks\\{package_name}")
    print("[*]")

def decodeApkToSmali(package_name):
    print("[*]")
    if not os.path.exists(f'.\\analyzed_apks\\{package_name}\\base.apk'):
        print("[*] Please, run firstly [2] Retrieve APK from device.")
    else:
        if os.path.exists(f'.\\analyzed_apks\\{package_name}\\base'):
            decod = input("[*] Decoded files are already present, do you want to repeat the decoding process?[Y/n]")
            if decod.lower() == "y":
                print("[*] Decoding apk...")
                functions_sast.decodeApk(package_name)
        else:
            print("[*] Decoding apk...")
            functions_sast.decodeApk(package_name)
    print("[*]")

def retrieveBaseInformationAPK(package_name):
    infos_ret = {}
    infos_ret["permissions"]  = []
    infos_ret["pkg"]  = package_name
    # informations
    strings_path = f''
    cmd = f'aapt d --values badging .\\analyzed_apks\\{package_name}\\base.apk'
    cmd_res = subprocess.check_output(cmd, shell=True)
    infos = cmd_res.decode('utf-8')
    # permissions
    print('asdf')
    for line in infos.split('\n'):
        permission = re.findall("^uses-permission: name='(.*?)\'", line)
        if(len(permission)>0):
            infos_ret['permissions'].append(permission[0])
        versionName = re.findall("versionName=\'(.*?)\'", line)
        if(len(versionName)>0):
            infos_ret['versionName'] = versionName[0]
        applicationLabel = re.findall("^application-label:'(.*?)\'", line)
        if(len(applicationLabel)>0):
            infos_ret['applicationLabel'] = applicationLabel[0]
        # native_code = re.findall("^native-code:'(.*?)\'", line)
        # if(len(applicationLabel)>0):
        #     infos_ret['applicationLabel'] = applicationLabel[0]
    return infos_ret
