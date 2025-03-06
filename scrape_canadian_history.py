import requests
from bs4 import BeautifulSoup

# Dictionary containing Canadian history resources
canadian_history_resources = {
    "canadian_history_events": "https://www.thecanadianencyclopedia.ca/en/timeline/100-great-events-in-canadian-history",
    "Canadian_Acts_Treaties": "https://www.thecanadianencyclopedia.ca/en/timeline/acts-and-treaties",
    "2SLGBTQ+_History": "https://www.thecanadianencyclopedia.ca/en/timeline/lgbtq2",
    "canadian_science": "https://www.thecanadianencyclopedia.ca/en/timeline/science"
}

# Set the headers to include a User-Agent (simulate a real browser request)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Loop through each category and URL
for category, url in canadian_history_resources.items():
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
        file_name = f"{category}.txt"
        with open(file_name, 'w', encoding='utf-8') as f:
            for idx, event in enumerate(events, start=1):
                f.write(f"Item {idx}: {event['title']}\n")
                f.write(f"Date: {event['date']}\n")
                f.write(f"Description: {event['description']}\n")
                f.write("-" * 80 + "\n")  # Separator for readability

        print(f"Data saved to {file_name} ({len(events)} items)\n")

    else:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}\n")