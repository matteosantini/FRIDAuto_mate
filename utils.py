import json

def writeJsonFile(file_path, json_content):
    open(file_path, 'a').close()
    with open(file_path, 'w') as outfile:
        json.dump(json_content, outfile, indent=4)
