import time
import frida
import os
from xml.dom import minidom
from subprocess import Popen, PIPE
import re

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
    if command == "2": # download apk from device
        print("[*]")
        print("[*] Retrieving package location...")
        command = ['adb', 'shell', 'pm', 'path', package_name]
        process = Popen(command, stdout=PIPE, stderr=True)
        output, error = process.communicate()
        location_pkg = output.decode('utf-8').replace('package:', '')
        print("[*] Package location: " + location_pkg)
        print("[*] Pulling apk into /analyzed_apks")
        os.chdir(os.path.dirname(__file__))
        if not os.path.exists(f'.\\analyzed_apks\\{package_name}'):
            os.makedirs(f'.\\analyzed_apks\\{package_name}')
        cmd = f'"adb pull {location_pkg} .\\analyzed_apks\\{package_name}"'.replace('\n','')
        os.system(cmd)
        print(f"[*] APK saved in {os.path.dirname(__file__)}\\analyzed_apks\\{package_name}")
        print("[*]")
    if command == "3": # B. apktool decode → access to manifest
        print("[*]")
        if not os.path.exists(os.path.exists(f'.\\analyzed_apks\\{package_name}\\base.apk')):
            print("[*] Please, run firstly [2] Retrieve APK from device.")
        else:
            if os.path.exists(os.path.exists(f'.\\analyzed_apks\\{package_name}\\base')):
                decod = input("[*] Decoded files are already present, do you want to repeat the decoding process?[Y/n]")
                if decod.lower() == "y":
                    print("[*] Decoding apk...")
                    os.chdir(os.path.dirname(__file__)+f'\\analyzed_apks\\{package_name}')
                    cmd = '"apktool d base.apk"'
                    os.system(cmd)
            else:
                print("[*] Decoding apk...")
                os.chdir(os.path.dirname(__file__)+f'\\analyzed_apks\\{package_name}')
                cmd = '"apktool d base.apk"'
                os.system(cmd)
        print("[*]")
    if command == "4": # enumerate & change activities
        if not arr_activities:
            dom = minidom.parse(f'.\\analyzed_apks\\{package_name}\\base\\AndroidManifest.xml')
            activities = dom.getElementsByTagName('activity')
            print(f"There are {len(activities)} activities:")
            i = 1
            for activity in activities:
                pkg_activity = activity.attributes["android:name"].value
                arr_activities.append(pkg_activity.split('.')[-1])
                i += 1
            if i>1:
                for (i, item) in enumerate(arr_activities, start=0):
                    print("[" + str(i) + "]  "+item)
                decod = input("[*] Do you want to swap activity?[Y/n]")
                if decod.lower() == "y":
                    activity_ind = input("Enter the index of the activity that will be displayed: ")
                    activity_ind = int(activity_ind)
                    if activity_ind < len(arr_activities):
                        activity = arr_activities[activity_ind]
                        print(f"adb shell am start -n {package_name}/.{activity}")
                        os.system(f"adb shell am start -n {package_name}/.{activity}")
        else:
            for (i, item) in enumerate(arr_activities, start=0):
                print("[" + str(i) + "]  "+item)
            decod = input("[*] Do you want to swap activity?[Y/n]")
            if decod.lower() == "y":
                activity_ind = input("Enter the index of the activity that will be displayed: ")
                activity_ind = int(activity_ind)
                if activity_ind < len(arr_activities):
                    activity = arr_activities[activity_ind]
                    print(f"adb shell am start -n {package_name}/.{activity}")
                    os.system(f"adb shell am start -n {package_name}/.{activity}")
                    # am start -n com.example.maptmockapplication/.NotLinkableActivity -- start an activity in adb shell
    if command == "5":
        custom_search = input("Enable custom search? [Y/n]: ")
        if custom_search.lower() == "y":
            custom_word = input("Insert custom keyword: ")
            script.exports.enumerateApplicationClasses(custom_word)
        else:
            script.exports.enumerateApplicationClasses(package_name)
    if command == "6":
        script.exports.interceptSQLiteQueries()
    if command == "7":
        latitude = input("latitude:")
        longitude = input("longitude:")
        script.exports.changeLocation(latitude, longitude)
