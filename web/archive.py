import requests



# # Base URL for the API
base_url = "https://archive.org/services/search/v1"

# Define the endpoint
endpoint = "/scrape"

# Construct the full URL
url = base_url + endpoint

# Define parameters for the GET request (modify as needed)
params = {
    'q': 'Machine Learning',  # Replace 'search term' with your actual search query
    'fields': 'identifier,title,creator,date'  # Fields you want to retrieve
    
}

# Make the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # print("Search Results:", data)
else:
    print("Failed to fetch data. Status code:", response.status_code)



