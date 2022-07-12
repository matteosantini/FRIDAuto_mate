import time
import frida
import os
from xml.dom import minidom
from pathlib import Path
import functions_dast
import functions_sast
import functions_osint
import shodan
import json

# retrieve json configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# init shodan api
SHODAN_API_KEY = config["api_key_shodan"]
api_shodan = shodan.Shodan(SHODAN_API_KEY)

#setup FRIDA and Python
def my_message_handler(message, payload):
    print(message)
    print(payload)

device = frida.get_usb_device()
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
    "2":"Retrieve APK from device",
    "3":"Decode APK",
    "4":"Enumerate & Change Activities",
    "5":"Enumerate Application Classes",
    "6":"Intercept SQLite Queries",
    "7":"Change Location",
    "8":"OSINT",
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
    if command == "2": # retrieve apk from device
        print("[*]")
        print("[*] Retrieving package location...")
        location_pkg = functions_sast.retrievePackage(package_name)
        print("[*] Package location: " + location_pkg)
        print("[*] Pulling apk into /analyzed_apks")
        functions_sast.pullApkToPackageFolder(os.path.dirname(__file__), package_name, location_pkg)
        print(f"[*] APK saved in {os.path.dirname(__file__)}\\analyzed_apks\\{package_name}")
        print("[*]")
    if command == "3": # B. apktool decode → access to manifest
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
    if command == "4": # enumerate & change activities
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
    if command == "5":
        custom_search = input("Enable custom search? [Y/n]: ")
        if custom_search.lower() == "y":
            custom_word = input("Insert custom keyword: ")
            script.exports.enumerateApplicationClasses(custom_word)
        else:
            script.exports.enumerateApplicationClasses(package_name)# enumerate application classes
    if command == "6":
        script.exports.interceptSQLiteQueries()# intercept SQLite Queries
    if command == "7":
        latitude = input("latitude:")
        longitude = input("longitude:")
        script.exports.changeLocation(latitude, longitude)# Change Location
    if command == "8": # OSINT
        strings_path = f'.\\analyzed_apks\\{package_name}\\base\\res\\values\\strings.xml'
        if not os.path.exists(strings_path):
            print("[*] The strings.xml file is not found or the apk was not pulled out.")
        else:
            print("[*] strings.xml found, retrieving all the urls/ips...")
            to_search = functions_osint.extractUrlsAndIpsFromFile(strings_path)
            no_result = True
            if(len(to_search["urls"])>0):
                no_result = False
                if not os.path.exists(f'.\\osint_results\\{package_name}\\shodan'):
                    os.makedirs(f'.\\osint_results\\{package_name}\\shodan')
                for url in to_search["urls"]:
                    domain = functions_osint.extractDomainFromUrl(url)
                    json_domainfile_path = f'.\\osint_results\\{package_name}\\shodan\\{domain}.json'
                    if not os.path.exists(json_domainfile_path):
                        ip = functions_osint.shodanResolveDns(api_shodan, SHODAN_API_KEY, domain)
                        json_result = functions_osint.shodanSearchIp(api_shodan, ip)
                        open(json_domainfile_path, 'a').close()
                        with open(json_domainfile_path, 'w') as outfile:
                            json.dump(json_result, outfile, indent=4)
            if(len(to_search)>0):
                no_result = False
                if not os.path.exists(f'.\\osint_results\\{package_name}\\shodan'):
                        os.makedirs(f'.\\osint_results\\{package_name}\\shodan')
                for ip in to_search["ips"]:
                    json_ipfile_path = f'.\\osint_results\\{package_name}\\shodan\\{ip}.json'
                    if not os.path.exists(json_ipfile_path):
                        json_result = functions_osint.shodanSearchIp(api_shodan, ip)
                        open(json_ipfile_path, 'a').close()
                        with open(json_ipfile_path, 'w') as outfile:
                            json.dump(json_result, outfile, indent=4)
            if(no_result):
                print("[*] ip and domains not found.")
