import time
import frida
import os
import functions_dast
import functions_sast
import functions_osint
import json
import utils
import sys
import fridauto_options

from xml.dom import minidom
from pathlib import Path

#setup FRIDA and Python
def my_message_handler(message, payload):
    print(message)
    print(payload)

device = frida.get_usb_device()
if(len(sys.argv)>1):
    package_name = sys.argv[1]
else:
    package_name = "com.example.maptmockapplication"
pid = device.spawn([package_name])
device.resume(pid)
time.sleep(1)
session = device.attach(pid)
with open("frida-functions.js") as f:
    script = session.create_script(f.read())
script.on("message", my_message_handler)
script.load()
# end setup  FRIDA and Python

print(r"""
███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗████████╗ ██████╗         ███╗   ███╗ █████╗ ████████╗███████╗
██╔════╝██╔══██╗██║██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗        ████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
█████╗  ██████╔╝██║██║  ██║███████║██║   ██║   ██║   ██║   ██║        ██╔████╔██║███████║   ██║   █████╗
██╔══╝  ██╔══██╗██║██║  ██║██╔══██║██║   ██║   ██║   ██║   ██║        ██║╚██╔╝██║██╔══██║   ██║   ██╔══╝
██║     ██║  ██║██║██████╔╝██║  ██║╚██████╔╝   ██║   ╚██████╔╝███████╗██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
""")
command = ""
options = {
    "1":"Exit",
    "2":"Enumerate & Change Activities",
    "3":"Enumerate Application Classes",
    "4":"Intercept SQLite Queries",
    "5":"Change Location",
}

options_str = '\n'.join(['[%s] %s' % (key, value) for (key, value) in options.items()])
arr_activities = []

while 1 == 1:
    print("[*] ******************************")
    print(options_str)
    print("[*] ******************************")
    command = input("[*] Enter command:")
    if command == "1":
        break
    if command == "2": # enumerate & change activities
        if not arr_activities:
            # retrieve activity
            dom = minidom.parse(f'.\\analyzed_apks\\{package_name}\\base\\AndroidManifest.xml')
            activities = dom.getElementsByTagName('activity')
            print(f"There are {len(activities)} activities:")
            for activity in activities:
                pkg_activity = activity.attributes["android:name"].value
                arr_activities.append(pkg_activity.split('.')[-1])
        if(len(arr_activities)>0):
            for (i, item) in enumerate(arr_activities, start=0):
                print("[" + str(i) + "]  "+item)
            print("["+str(i)+">] Go back")
            decod = input("[*] Enter the index of the activity that will be displayed: ")
            activity_ind = int(decod)
            if(activity_ind != 999):
                functions_dast.swap_activity(activity_ind, arr_activities, package_name)
    if command == "3":
        custom_search = input("Enable custom search? [Y/n]: ")
        if custom_search.lower() == "y":
            custom_word = input("Insert custom keyword: ")
            script.exports.enumerateApplicationClasses(custom_word)
        else:
            script.exports.enumerateApplicationClasses(package_name)# enumerate application classes
    if command == "4":
        script.exports.interceptSQLiteQueries()# intercept SQLite Queries
    if command == "5":
        latitude = input("latitude:")
        longitude = input("longitude:")
        script.exports.changeLocation(latitude, longitude)# Change Location



# if command == "8": # OSINT
#     strings_path = f'.\\analyzed_apks\\{package_name}\\base\\res\\values\\strings.xml'
#     if not os.path.exists(strings_path):
#         print("[*] The strings.xml file is not found or the apk was not pulled out.")
#     else:
#         print("[*] strings.xml found, retrieving all the urls/ips...")
#         if not os.path.exists(f'.\\osint_results\\{package_name}\\shodan'):
#             os.makedirs(f'.\\osint_results\\{package_name}\\shodan')
#         if not os.path.exists(f'.\\osint_results\\{package_name}\\virustotal'):
#             os.makedirs(f'.\\osint_results\\{package_name}\\virustotal')
#         if not os.path.exists(f'.\\osint_results\\{package_name}\\wbm'):
#             os.makedirs(f'.\\osint_results\\{package_name}\\wbm')
#         to_search = functions_osint.extractUrlsAndIpsFromFile(strings_path)
#         no_result = True
#         if(len(to_search["urls"])>0):
#             no_result = False
#             for url in to_search["urls"]:
#                 domain = functions_osint.extractDomainFromUrl(url)
#                 # shodan url
#                 json_shodan_path = f'.\\osint_results\\{package_name}\\shodan\\{domain}.json'
#                 if not os.path.exists(json_shodan_path):
#                     ip = functions_osint.shodanResolveDns(domain)
#                     json_result = functions_osint.shodanSearchIp(ip)
#                     utils.writeJsonFile(json_shodan_path, json_result)
#                 # vt url
#                 json_wbm_path = f'.\\osint_results\\{package_name}\\wbm\\{domain}.json'
#                 if not os.path.exists(json_wbm_path):
#                     wb_res = functions_osint.wbScan(url)
#                     json_result = wb_res
#                     utils.writeJsonFile(json_wbm_path, json_result)
#         if(len(to_search["ips"])>0):
#             no_result = False
#             for ip in to_search["ips"]:
#                 # shodan ip
#                 json_ipfile_path = f'.\\osint_results\\{package_name}\\shodan\\{ip}.json'
#                 if not os.path.exists(json_ipfile_path):
#                     json_result = functions_osint.shodanSearchIp(ip)
#                     open(json_ipfile_path, 'a').close()
#                     with open(json_ipfile_path, 'w') as outfile:
#                         json.dump(json_result, outfile, indent=4)
#                 # vt ip
#                 json_virustotal_path = f'.\\osint_results\\{package_name}\\virustotal\\{ip}.json'
#                 if not os.path.exists(json_virustotal_path):
#                     vt_res = functions_osint.vtScanUrl(ip)
#                     json_result = vt_res.__dict__
#                     utils.writeJsonFile(json_virustotal_path, json_result)
#         if(no_result):
#             print("[*] ip and domains not found.")


# if command == "9": # OLD Decode APK to java
#     print("[*]")
#     if not os.path.exists(f'.\\analyzed_apks\\{package_name}\\base.apk'):
#         print("[*] Please, run firstly [2] Retrieve APK from device.")
#     else:
#         if os.path.exists(f'.\\analyzed_apks\\{package_name}\\base-dex2jar.jar'):
#             decod = input("[*] Decoded files are already present, do you want to repeat the decoding process?[Y/n]")
#             if decod.lower() == "y":
#                 print("[*] Decoding apk to jar...")
#                 # [1] rename apk to zip
#                 if not os.path.exists(f'.\\analyzed_apks\\{package_name}\\base.zip'):
#                     name_file = f'.\\analyzed_apks\\{package_name}\\base.apk'
#                     to = f'.\\analyzed_apks\\{package_name}\\base.zip'
#                     utils.copyFile(name_file, to)
#                     functions_sast.decodeClassesToDex(to)
#                 #functions_sast.decodeApkToJar(package_name)
#         else:
#             print("[*] Decoding apk to jar...")
#             #functions_sast.decodeApkToJar(package_name)
#     print("[*]")
