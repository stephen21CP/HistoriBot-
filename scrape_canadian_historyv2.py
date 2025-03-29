import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Dictionary containing Canadian history resources
canadian_history_resources = {
    "canadian_history_events": "https://www.thecanadianencyclopedia.ca/en/timeline/100-great-events-in-canadian-history",
    "Canadian_Acts_Treaties": "https://www.thecanadianencyclopedia.ca/en/timeline/acts-and-treaties",
    "2SLGBTQ+_History": "https://www.thecanadianencyclopedia.ca/en/timeline/lgbtq2",
    "canadian_science": "https://www.thecanadianencyclopedia.ca/en/timeline/science",
    "asia_canada": "https://www.thecanadianencyclopedia.ca/en/timeline/asia-canada",
    "black_history": "https://www.thecanadianencyclopedia.ca/en/timeline/black-history",
    "first_nations": "https://www.thecanadianencyclopedia.ca/en/timeline/first-nations",
    "indigenous_suffrage": "https://www.thecanadianencyclopedia.ca/en/timeline/indigenous-suffrage",
    "voting_rights": "https://www.thecanadianencyclopedia.ca/en/timeline/voting-rights-in-canada",
    "confederation": "https://www.thecanadianencyclopedia.ca/en/timeline/confederation",
    "alberta": "https://www.thecanadianencyclopedia.ca/en/timeline/alberta",
    "british_columbia": "https://www.thecanadianencyclopedia.ca/en/timeline/british-columbia",
    "manitoba": "https://www.thecanadianencyclopedia.ca/en/timeline/manitoba",
    "new_brunswick": "https://www.thecanadianencyclopedia.ca/en/timeline/new-brunswick",
    "newfoundland": "https://www.thecanadianencyclopedia.ca/en/timeline/newfoundland-and-labrador",
    "nova_scotia": "https://www.thecanadianencyclopedia.ca/en/timeline/nova-scotia",
    "northwest": "https://www.thecanadianencyclopedia.ca/en/timeline/northwest-territories",
    "nunavut": "https://www.thecanadianencyclopedia.ca/en/timeline/nunavut",
    "ontario": "https://www.thecanadianencyclopedia.ca/en/timeline/ontario",
    "pei": "https://www.thecanadianencyclopedia.ca/en/timeline/prince-edward-island",
    "quebec": "https://www.thecanadianencyclopedia.ca/en/timeline/quebec",
    "saskatchewan": "https://www.thecanadianencyclopedia.ca/en/timeline/saskatchewan",
    "yukon": "https://www.thecanadianencyclopedia.ca/en/timeline/yukon"
}

# Set the headers to include a User-Agent (simulate a real browser request)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

urls = ["https://www.thecanadianencyclopedia.ca/en/timelines",]
url = urls[0]
pages = []
soup_list = []
not_last_page = True
pagenumber = 0

# helper function to pull the urls for all of the timeline pages from the source
# and pass them into the parsePage function to parse them into txt files
def getUrls():
    global not_last_page
    global pagenumber
    current_url = urls[-1]
    page = requests.get(current_url, headers=headers)
    
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            # creates a list of all timeline urls on this page
            timeline_links = [s.find('a')['href'] for s in soup.find_all('div', {'class': 'callout-item__container'})]
            pages.append(timeline_links)
            for i, link in enumerate(timeline_links):
                parsePage(link, i)
            # print(timeline_links)
        except AttributeError:
            print("No timelines found on this page.")
            not_last_page = False
        try:
            next_link = soup.find('a', {'rel': 'next'})['href']
            next_page = urljoin(current_url, next_link)
            pagenumber = pagenumber + 1
            print(f"Next page found: {next_page}")
            if next_page not in urls:
                urls.append(next_page)
            else:
                not_last_page = False
        except AttributeError:
            print("No next page found.")
            not_last_page = False
    else:
        print(f"Failed to retrieve {current_url} (Status code: {page.status_code})")

# Loop through each category and URL
# for category, url in canadian_history_resources.items():
# converted to a helper to parse individual pages after they're checked 
# takes the url of the page and a "category" to name the txt file
# writes to a txt file and returns the page's soup object
def parsePage(url, category):
    print(f"Fetching data from: {url} ({category})")

    # Send a GET request to fetch the page content with headers
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all timeline entries
        timeline_items = soup.find_all('li', class_='timeline-list__item')

        # Extract event details
        events = []
        for item in timeline_items:
            title = item.find('p', class_='timeline-title')
            date = item.find('p', class_='timeline-date uppercase')
            description = item.find('p', class_='timeline-description')

            if title and description:
                event_data = {
                    "title": title.get_text(strip=True),
                    "date": date.get_text(strip=True) if date else "No date available",
                    "description": description.get_text(strip=True)
                }
                events.append(event_data)

        # Write events to a file named after the category
        file_name = str(category) + "_" + str(pagenumber) + ".txt"
        with open(file_name, 'w', encoding='utf-8') as f:
            for idx, event in enumerate(events, start=1):
                f.write(f"Item {idx}: {event['title']}\n")
                f.write(f"Date: {event['date']}\n")
                f.write(f"Description: {event['description']}\n")
                f.write("-" * 80 + "\n")  # Separator for readability

        print(f"Data saved to {file_name} ({len(events)} items)\n")
    else:
        print("Page", url, "returned incorrect status code")


while not_last_page:
    getUrls()
print(pages)

print("All URLs collected:", urls)

for i, url in enumerate(urls):
    parsePage(url, i)