import os

def swap_activity(activity_ind, arr_activities, package_name):
    if activity_ind < len(arr_activities):
        activity = arr_activities[activity_ind]
        print(f"adb shell am start -n {package_name}/.{activity}")
        os.system(f"adb shell am start -n {package_name}/.{activity}")
