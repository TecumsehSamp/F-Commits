from google.cloud import bigquery
from unidecode import unidecode
import datetime
import json

client = bigquery.Client()
# You need to specify your Google API key in an ENV variable, client doesn't work if no key is found.

d = []
swearwords = [""]

def GetData():

    todaydate = datetime.date.today()
    yesterday = todaydate - datetime.timedelta(1)

    dataset_id1 = '`githubarchive.day.'+ yesterday.isoformat() + '` '
    dataset_id1 = dataset_id1.replace("-", "")
    query = (
        'SELECT TO_JSON_STRING(payload) AS json_row FROM' + dataset_id1 + ' '
        'WHERE type = "PushEvent"'
        'Limit 2000')
    query_job = client.query(
        query,
        location='US')
    return(query_job)



def Search(query_job):
    
    for json_row in query_job: 
        loadjson = json.loads(json_row['json_row'])
        loadjsontwice = json.loads(loadjson)
        commit = loadjsontwice['commits']

        for i in commit:
            message = unidecode((i['message']))
            d.append(i['message'])
            f = open("dump.txt", "a")
            f.write(message)
            for swear in swearwords:
                if swear in message:
                    f3 = open("swearing.txt", "a")
                    f3.write("\n Swear: " + message + "\n URL: " + i['url'] )
            



thing = GetData()
Search(thing)
