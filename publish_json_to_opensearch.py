import requests
import csv

# URL of our OpenSearch instance
url = 'https://localhost:9200/games_index/_doc/'

# Our OpenSearch credentials
credentials = ('admin', 'GHAILENEmark11994**')

# Read CSV data into a Python data structure
with open('computer_games.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = [row for row in reader]

# If data is a dictionary (i.e., single CSV object), wrap it in a list
if isinstance(data, dict):
    data = [data]

# For each document...
for doc in data:
    # POST the document as JSON to the OpenSearch instance, using our credentials
    response = requests.post(url, json=doc, auth=credentials, verify=False)

    # Print the response from OpenSearch
    print(response.json())