import time
import frida
import os

def my_message_handler(message, payload):
    print(message)
    print(payload)


device = frida.get_usb_device()
package_name = "com.example.maptmockapplication"
pid = device.spawn([package_name]) #
device.resume(pid)
time.sleep(1)  # Without it Java.perform silently fails
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
    "2":"Enumerate Activities",
    "3":"Change Activity By Index",
    "4":"Enumerate Loaded Classes",
    "5": "Intercept SQLite Queries"
}
options_str = '\n'.join(['[%s] %s' % (key, value) for (key, value) in options.items()])
while 1 == 1:
    print(options_str)
    command = input("Enter command:")
    if command == "1":
        break
    elif command == "2":
        script.exports.enumerateActivities(package_name, 1)
    elif command == "3":
        activity_ind = input("Enter the index of the activity that will be displayed: ")
        script.exports.goToActivity(package_name, activity_ind)
        os.chdir("C:\platform-tools")
        os.system('"adb shell input keyevent 3"') # home button
        os.system(f'"adb shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"')
    elif command == "4":
        script.exports.enumerateLoadedClasses() #todo ricerca classe
    elif command == "5":
        script.exports.interceptSQLiteQueries()
