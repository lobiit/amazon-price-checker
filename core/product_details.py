import requests

# Structure payload.
payload = {
'source': 'amazon',
'url': 'https://www.amazon.com/dp/B098FKXT8L',
'parse': True
}

# Get response
response = requests.request(
'POST',
'https://realtime.oxylabs.io/v1/queries',
auth=('USERNAME', 'PASSWORD'),
json=payload,
)

# Print prettified response to stdout.
print(response.json())