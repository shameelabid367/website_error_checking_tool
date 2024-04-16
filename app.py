from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client['error']
collection = db['links']

error_codes = [404,]

def crawl_and_check_errors(url):
    error_links = []
    try:
        # Check if the URL has a scheme, if not, add a default scheme (e.g., "https://")
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "https://" + url

        response = requests.get(url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links from the page
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        # Check each linked page for errors
        for link in links:
            # Skip "mailto" links
            if link.startswith('mailto:') or link.startswith('javascript'):
                continue
            
            # Use urljoin to handle relative URLs
            absolute_link = urljoin(url, link)
            link_response = requests.get(absolute_link, verify=False)

            try:
                
                link_response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code in error_codes:
                    error_links.append({'url': absolute_link, 'error': (e.response.status_code)})
                # else:
                #     error_links.append({'url': 'non-::'+absolute_link, 'error': str(e)})

    except requests.exceptions.HTTPError as e:
        if e.response.status_code in error_codes:
                    error_links.append({'url': url, 'error': (e.response.status_code)})
    
    return error_links
        # return [{'url': url, 'error': str(e)}]

def save_to_mongodb(url, error_links):
    existing_document = collection.find_one({'url': url})

    if existing_document:
        # If the document exists, update it
        collection.update_one({'url': url}, {'$set': {'error_links': error_links}})
    else:
        # If the document doesn't exist, insert a new one
        collection.insert_one({'url': url, 'error_links': error_links})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        error_li = crawl_and_check_errors(url)
        
        # Save the data to MongoDB
        if len(error_li) > 0:
            save_to_mongodb(url, error_li)

        return render_template('index.html', url=url, error_links=error_li)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         url = request.form.get('url')
#         error_links = crawl_and_check_errors(url)
#         return render_template('index.html', url=url, error_links=error_links)

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
