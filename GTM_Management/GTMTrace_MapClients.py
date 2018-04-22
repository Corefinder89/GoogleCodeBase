import requests, json, os

path = os.path.dirname (os.path.realpath (__file__))
config_file_path = os.path.join (path, 'client_secrets.json')

# Get configurations from the client_secrets.json file
def get_config():
    try:
        with open (config_file_path, 'r') as file:
            config = json.loads(file.read ( ))

        return config
    except IOError as e:
        print e

# Get refresh access token after 3600sec and use the access token to hit the API
def refresh_access_tokens():
    config = get_config ()

    # Get client data for
    for client_config in config:
        # Payload data from client secret configurations
        payload = {
            'client_id': client_config['client_id'],
            'client_secret': client_config['client_secret'],
            'refresh_token': client_config['refresh_token'],
            'grant_type': 'refresh_token'
        }

        # Header parameters
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Get response status
        response = requests.post('https://accounts.google.com/o/oauth2/token', data=payload, headers=headers)

        # if response status from the API is 200, store the response data in a response object
        if response.status_code == 200:
            response = response.json()

            app_config = get_config()

            for client_config in app_config:
                if client_config['client_id'] == client_config['client_id']:
                    client_config['access_token'] = response['access_token']

            with open(config_file_path, 'w') as file:
                file.write(json.dumps(app_config))

def write_data_as_csv(dict):
    csv = open("GA1.csv","a")
    for key in dict.keys():
        acc_name = key
        acc_id = dict[key]
        row = acc_name + "," + acc_id + "\n"
        csv.write(row)

def get_client_list(config):
    access_token = config['access_token']

    headers = {
        'Authorization': 'Bearer {}'.format (access_token)
    }

    response = requests.get ('https://content.googleapis.com/tagmanager/v1/accounts', headers=headers)

    response_data = response.json()

    csv = open ("GA1.csv", "w")
    columnTitleRow = "name, accountId\n"
    csv.write (columnTitleRow)
    csv.close()

    for ent in response_data['accounts']:
        acct_dict = {ent['name']:ent['accountId']}
        write_data_as_csv(acct_dict)

refresh_access_tokens()

config = get_config()

for parse_config in config:
    get_client_list(parse_config)
