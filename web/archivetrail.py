import requests
from bs4 import BeautifulSoup
import PyPDF2
import pytesseract
from PIL import Image
from io import BytesIO

# Base URL for the API
base_url = "https://archive.org/services/search/v1"

# Define the endpoint
endpoint = "/scrape"

# Construct the full URL
url = base_url + endpoint

# Define parameters for the GET request (modify as needed)
params = {
    'q': 'DeepLearning',  # Search for documents related to SYNCOIN
    'fields': 'identifier,title,creator,date'  # Fields you want to retrieve
}

# Make the GET request
response = requests.get(url, params=params)

# Function to fetch text content
def fetch_text_content(text_file_url):
    text_response = requests.get(text_file_url)
    if text_response.status_code == 200:
        soup = BeautifulSoup(text_response.content, 'html.parser')
        return soup.get_text(separator=' ')
    else:
        print(f"Failed to fetch text content from {text_file_url}. Status code:", text_response.status_code)
        return None

# Function to fetch PDF content
def fetch_pdf_content(pdf_file_url):
    pdf_response = requests.get(pdf_file_url)
    if pdf_response.status_code == 200:
        pdf_reader = PyPDF2.PdfFileReader(pdf_response.content)
        content = ""
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            content += page.extractText()
        return content
    else:
        print(f"Failed to fetch PDF content from {pdf_file_url}. Status code:", pdf_response.status_code)
        return None

# Function to fetch text content from images using OCR
def fetch_image_content(image_file_url):
    image_response = requests.get(image_file_url)
    if image_response.status_code == 200:
        img = Image.open(BytesIO(image_response.content))
        text = pytesseract.image_to_string(img)
        return text
    else:
        print(f"Failed to fetch image content from {image_file_url}. Status code:", image_response.status_code)
        return None

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print("Search Results:", data)  # Print the entire response data for debugging
    
    # Extract search results
    search_results = data.get('items', [])
    print("Number of search results:", len(search_results))  # Print the number of search results
    
    if not search_results:
        print("No documents found related to SYNCOIN.")
    else:
        # Loop through search results
        for result in search_results:
            identifier = result.get('identifier')
            if identifier:
                print(f"Fetching content for identifier: {identifier}")
                
                # Fetch metadata
                metadata_url = f"https://archive.org/metadata/{identifier}"
                metadata_response = requests.get(metadata_url)
                if metadata_response.status_code == 200:
                    metadata = metadata_response.json()
                    files = metadata.get('files', [])
                    
                    # Check content type and fetch content accordingly
                    content_fetched = False
                    for file in files:
                        if file['format'] == 'Text':
                            text_file_url = f"https://archive.org{file['name']}"
                            content = fetch_text_content(text_file_url)
                            if content:
                                content_fetched = True
                                print(f"Content (text) for identifier: {identifier}\n")
                                print(content[:500])  # Print the first 500 characters of the content
                                break
                        elif file['format'] == 'PDF':
                            pdf_file_url = f"https://archive.org{file['name']}"
                            content = fetch_pdf_content(pdf_file_url)
                            if content:
                                content_fetched = True
                                print(f"Content (PDF) for identifier: {identifier}\n")
                                print(content[:500])  # Print the first 500 characters of the content
                                break
                        elif file['format'] == 'Image':
                            image_file_url = f"https://archive.org{file['name']}"
                            content = fetch_image_content(image_file_url)
                            if content:
                                content_fetched = True
                                print(f"Content (image OCR) for identifier: {identifier}\n")
                                print(content[:500])  # Print the first 500 characters of the content
                                break
                        else:
                            print(f"Skipping {file['format']} content for identifier: {identifier}")
                    
                    if not content_fetched:
                        print(f"No text, PDF, or image content found for identifier: {identifier}")
                    
                else:
                    print(f"Failed to fetch metadata for {identifier}. Status code:", metadata_response.status_code)
            else:
                print("No identifier found in search results.")
else:
    print("Failed to fetch data. Status code:", response.status_code)
