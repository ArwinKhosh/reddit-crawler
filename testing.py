import os

# File list in specified folder
file_list = os.listdir("data")

# Strip JSON extension
for file in file_list:
    print(file.split('.')[0])


 file = open("submissions.json","a")

 json.dumps(object,sort_keys=True,ensure_ascii=True),file=file