import json

import requests
import time

from data_news_produser.service import save_json_to_mongo

EVENT_REGISTRY_URL = "http://localhost:5000/articles?page="

GROQ_API_KEY = "xai-iBBJMOrJmGRrcJiwwcvCg4gn7s4DyQ9uJuVYq5lz1nBxKn7KN6To2IiEZm9deaapHIqvXFYBW8vVly7P"
GROQ_API_URL = "https://api.x.ai/v1/chat/completions"
OPENCAGE_API_KEY = "bfa11842d84d477ebc17255c97c2cc3a"


response_format_groq = {
    "type": "json_schema",
    "json_schema": {
        "name": "news_classification",
        "schema": {
            "type": "object",
            "properties": {
                "classification": {
                    "type": "string",
                    "enum": [
                        "Current terrorism event",
                        "Past terrorism event",
                        "Other news event"
                    ]
                },
                "location": {
                    "type": "string",
                    "description": "The location where the event occurred",
                    "longitude": "float",
                    "latitude" : "float"
                }
            },
            "required": ["classification", "location"],
            "additionalProperties": False
        },
        "strict": True
    }
}



def fetch_articles(page):

    response = requests.get(f"{EVENT_REGISTRY_URL}{page}")
    if response.status_code == 200:

        return response.json().get('articles')
    else:
        print(f"Error fetching articles: {response.status_code}")
        return []


def classify_news_article(article_content):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    payload = {
        "messages": [
            {"role": "system",
             "content":"You are an assistant classifying news articles into categories and locations"},
            {"role": "user", "content": f"This is a news article: {article_content}"}
        ],
        "model": "grok-2-1212",
        "stream": False,
        "temperature": 0,
        "response_format": response_format_groq
    }
    # Send the request
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    # Check for successful response
    if response.status_code == 200:
        try:
            response_json = response.json()
            return response_json
        except json.JSONDecodeError:
            print("Failed to decode JSON response")
            return None
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None


def get_location(name):
    # API Key של OpenCage Geocoder (תוכל להנפיק מפתח API ב- https://opencagedata.com/)


    # כתובת ה-API של OpenCage
    url = f"https://api.opencagedata.com/geocode/v1/json?q={name}&key={OPENCAGE_API_KEY}"

    # שלח את הבקשה ל-API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # אם נמצאו תוצאות גיאוקודינג, מחזירים את ה-lon וה-lat
        if data["results"]:
            location = data["results"][0]["geometry"]
            lon = location["lng"]
            lat = location["lat"]
            return {"lon": lon, "lat": lat}
        else:
            print(f"No geolocation data found for {name}.")
            return {"lon": 0.0, "lat": 0.0}
    else:
        print(f"Error fetching geolocation data: {response.status_code}")
        return {"lon": 0.0, "lat": 0.0}




# התהליך המרכזי
def main():
    articles_page = 1
    while True:
        print(f"Fetching articles for page {articles_page}...")
        articles = fetch_articles(articles_page)
        if not articles:
            break
        results = articles.get("results")

        for article in results[:10]:
            body = article.get("body", "")
            location = article.get("source", {}).get("title", "Unknown Location")
            #get first words from body

            classification = classify_news_article(body[:300])
            content = classification['choices'][0]['message']['content']

            # המרת התוכן למילון
            parsed_content = json.loads(content)

            # יצירת אובייקט JSON חדש
            result = {
                'country': parsed_content.get('location', ''),
                'category': parsed_content.get('classification', ''),
                'body': body

            }
            location_ll = get_location(result['country'])
            result['lon'] = location_ll['lon']
            result['lat'] = location_ll['lat']
            save_json_to_mongo(result)



        articles_page += 1
        time.sleep(120)


if __name__ == "__main__":
    main()
