import os

# File list in specified folder
file_list = os.listdir("data")

# Strip JSON extension
for file in file_list:
    print(file.split('.')[0])


 file = open("submissions.json","a")

 json.dumps(object,sort_keys=True,ensure_ascii=True),file=file




 #---------------------------------------------------

 

elif created_utc_date in days_exist:
    file.close() 

    oldest_created_utc_date = epoch_to_gmt(oldest_created_utc,1)
    while oldest_created_utc_date not in days_exist:
        file = open(f"data/comments_by_date/{oldest_created_utc_date}.json","a")
        oldest_created_utc = gmt_to_epoch(oldest_created_utc_date)
        if created_utc > oldest_created_utc:
            file.close() 

    oldest_created_utc = gmt_to_epoch(epoch_to_gmt(oldest_created_utc,1))
    break
