import requests

headers = {
    'authority': 'www.reddit.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,no;q=0.7',
    'cookie': 'csv=1; edgebucket=PoBrCYPmOlUDYePXEu; reddaid=UPVMLYXZT6E7HAIB; __gads=ID=20a9e1e231db2933:T=1586714846:S=ALNI_MYo-pjd3eeMQIF7PYefObCkKj7hxQ; eu_cookie_v2=3; loid=0000000000672uvug0.2.1586714779982.Z0FBQUFBQmVvX3RYSFZfaDdEZWJfeHN5TGZOSmR4MkxBd3RhLXNveXNIN3Fycm5RVU96cmszWmRHMy1TS19NS2JtclZtQ2xlX0lXMGJMVjFmWlFDVkxxekcyeHk0b0xnYW5DeUY3UkZ6a0FER3VhNWtabjBfUk1ZU0lJeWZCYlh0ZDdYTnFYWUc5cDg; d2_token=3.1f7524bf19ae24d3fc68ad516c2740bb56d5423cbce7081812ed29a3f04bd728.eyJhY2Nlc3NUb2tlbiI6Ii1zamxwVHBJNzJ4YXIyTHI4TXhjM3hDNlVReDQiLCJleHBpcmVzIjoiMjAyMC0wNC0yNVQxMjozNjoyNC4wMDBaIiwibG9nZ2VkT3V0Ijp0cnVlLCJzY29wZXMiOlsiKiIsImVtYWlsIl19; recent_srs=t5_32g5k^%^2Ct5_2vlls^%^2Ct5_2u3sb^%^2Ct5_2revo^%^2Ct5_2sjey^%^2Ct5_2r36m^%^2Ct5_2qh4p^%^2Ct5_2u9xs^%^2Ct5_2rmj5^%^2C; session_tracker=RWgPV1TxwIAJXtFpEf.0.1612049072721.Z0FBQUFBQmdGZXF4VVd4Rmp0a01LVUZpMGZxWVB3dmRuRDc3RGZxWkM5RHFkeGdxdHh0RlZ4dlcwQXpYcTd0MjYxb2I3OVNvcjg2WndHR3pESTlZQVluZ0xtMHNLRW5LNlphYjlSZ1JSWUlKM29iSDJUSlBJWDBOSEtwLUQ2QURRai0weWtaX2ZQNy0',
}

response = requests.get('https://www.reddit.com/r/europe/top/.json', headers=headers)

json_response = response.json()

json_entries = json_response['data']['children']

json_entries[0]['data']['permalink']