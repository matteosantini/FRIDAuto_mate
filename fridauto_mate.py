import time
import frida
import os
import functions_dast
import functions_sast
import functions_osint
import json
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
    print("[*] **********************************************************************************")
    print("[*] Current Package: "+ package_name)
    print("[*] **********************************************************************************")
    print(options_str)
    print("[*] **********************************************************************************")
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
