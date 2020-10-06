# Parses content.json as changes all file names to their matching Firebase URLs
# Check out content.json for the very specific format needed.

from db import FirebaseHelper
import json

helper = FirebaseHelper()
directory = "Content/"

with open('content.json') as f:
    m = json.load(f)

path = directory + m["id"] + "/" + m["cover_image"]
m["cover_image"] = helper.get_url(path)

for stage in m["stages"]:
    if "image" in stage:
        path = directory + m["id"] + "/" + stage["image"]
        stage["image"] = helper.get_url(path)
    if "audio" in stage:
        path = directory + m["id"] + '/' + stage["audio"]
        stage["audio"] = helper.get_url(path)
    if "options" in stage:
        for k, v in stage["options"].items():
            path = directory + m["id"] + '/' + v
            stage["options"][k] = helper.get_url(path)

helper.create_content(m)
# s = json.dumps(m)
# f = open("dict.json", "w")
# f.write(s)
# f.close()
