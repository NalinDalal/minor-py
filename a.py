from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re


def analyze_js(js_content):
    # Simple analysis to check for suspicious patterns
    suspicious_patterns = [
        "eval(",
        "document.write(",
        "new Function(",
        "setTimeout(",
        "setInterval(",
    ]
    found_patterns = [
        pattern for pattern in suspicious_patterns if pattern in js_content
    ]
    if found_patterns:
        print(f"Suspicious patterns found: {found_patterns}")
    else:
        print("No suspicious patterns detected.")


def simple_crawler(url):
    try:
        # Send HTTP request to the URL
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully fetched: {url}\n")

            # Print HTML response length
            html_length = len(response.text)
            print(f"HTML Response Length: {html_length} characters\n")

            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract and print the title of the page
            title = soup.title.text if soup.title else "No title found"
            print(f"Page Title: {title}\n")

            # Check for JSON responses (if applicable)
            print("Checking for JSON responses:")
            json_links = [
                script["src"]
                for script in soup.find_all("script", src=True)
                if script["src"].endswith(".json")
            ]
            for json_link in json_links:
                json_url = urljoin(url, json_link)
                try:
                    json_response = requests.get(json_url).json()
                    print(f"JSON Response from {json_url}: {json_response}\n")
                except Exception as e:
                    print(f"Failed to fetch/parse JSON from {json_url}: {e}\n")

            # Check for JavaScript files
            print("Analyzing JavaScript files:")
            js_links = [
                script["src"]
                for script in soup.find_all("script", src=True)
                if script["src"].endswith(".js")
            ]
            for js_link in js_links:
                js_url = urljoin(url, js_link)
                try:
                    js_response = requests.get(js_url)
                    if js_response.status_code == 200:
                        print(f"Analyzing JavaScript file: {js_url}")
                        analyze_js(js_response.text)
                    else:
                        print(f"Failed to fetch JavaScript file: {js_url}")
                except Exception as e:
                    print(f"Error fetching JS file: {js_url}: {e}")

        else:
            print(f"Error: Failed to fetch {url} - Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Test
if __name__ == "__main__":
    sample_url = "https://www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd=_home-customer&nav=1/loading.php?"
    simple_crawler(sample_url)
