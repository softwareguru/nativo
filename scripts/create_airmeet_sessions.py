# Script to create the session content files for Hugo from a csv file.

def main():
    import csv, sys, os, json, requests
    from slugify import slugify
    
    airmeet_id = ""

    if len(sys.argv) < 2:
        print("Not enough arguments")
        sys.exit()
    elif len(sys.argv) == 2:
        airmeet_id = sys.argv[1]
        source_file = "sessions.csv"
    else:
        airmeet_id = sys.argv[1]
        source_file = sys.argv[2]

    token = get_token()

    with open(source_file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            data = {}
            data['sessionTitle'] = row['title']
            data['sessionStartTime'] = make_timestamp(row['time_start'])
            data['hostEmail'] = row['host_email']

            speakers = row['speakers'].split(", ")
            time_end = row['time_end']
            abstract = row['description']

            url = f"https://api-gateway-prod.us.airmeet.com/prod/airmeet/{airmeet_id}/session"
            headers = { 'X-Airmeet-Access-Token': token, 'Content-Type': 'application/json' }
            json_data = json.dumps(data)
            print(json_data)
            r = requests.post(url, headers=headers, data=json.dumps(data))
            print(r.text)
                       

def get_token():
    from dotenv import load_dotenv
    import os, requests
    
    load_dotenv()

    access_key = os.getenv("AIRMEET_ACCESS_KEY")
    secret_key = os.getenv("AIRMEET_SECRET_KEY")

    if not access_key:
        raise Exception("AIRMEET_ACCESS_KEY missing as env variable")

    if not secret_key:
        raise Exception("AIRMEET_SECRET_KEY missing as env variable")

    url = "https://api-gateway-prod.us.airmeet.com/prod/auth"
    headers = { 'X-Airmeet-Access-Key': access_key, 'X-Airmeet-Secret-Key' : secret_key, 'Content-Type': 'application/json' }
    r = requests.post(url, headers=headers)

    return r.json().get('token')

def make_timestamp(strtime):
    from dateutil.parser import parse
    import time

    pd = parse(strtime)
    result = int(time.mktime(pd.timetuple())*1000)
    print (f"{strtime} is {result}")
    return result



if __name__ == "__main__": 
	main() 

