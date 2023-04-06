import requests
import json
from datetime import datetime
import time
import os

# Set your API key and organization ID
api_key = 'YOUR API KEY GOES HERE'
org_id = 'YOUR ORG ID GOES HERE'

# Set the interval for API calls in seconds
interval = 60

# Set the maximum number of API call responses to keep in the log
max_responses = 2

# Initialize an empty list to store the API call responses
responses = []

while True:
    # Set the endpoint URL
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/uplinks/statuses"

    # Set the headers with the API key and content type
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json"
    }

    # Make the GET request and save the response to a variable
    response = requests.get(url, headers=headers)

    # Convert the response to JSON format
    json_data = json.loads(response.text)

    # Get the current date and time
    current_time = datetime.now().strftime("%H:%M %d/%m/%Y")

    # Append the formatted output to the responses list
    formatted_response = []
    for device in json_data:
        serial = device["serial"]
        for uplink in device["uplinks"]:
            interface = uplink["interface"]
            status = uplink["status"]
            if status == "not connected":
                status = "not_connected"
            formatted_response.append(f"{current_time} {serial} {interface} {status}")
    responses.append(formatted_response)

    # Remove the oldest API call response if the maximum number of responses is exceeded
    if len(responses) > max_responses:
        responses.pop(0)

    # Save the responses to a log.txt file
    with open("log.txt", "w") as f:
        for response in responses:
            f.write('\n'.join(response) + '\n')

    # Wait for the specified interval before running the script again
    time.sleep(interval)

    # Clear the log.txt file if it contains more than the last two minutes of API call responses
    if len(responses) > 1:
        os.remove("log.txt")
        open("log.txt", "w").close()