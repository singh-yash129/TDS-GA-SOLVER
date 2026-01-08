import httpx
import requests
import bs4
from bs4 import BeautifulSoup
import json

from datetime import datetime
                # to convert API to json format

from urllib.parse import urlencode

# to parse the webpage

import pandas as pd
import re                     # regular expression operators


WIKI_BASE_URL = "https://en.wikipedia.org/wiki/"


# Task 1: ESPN Cricinfo - Count Ducks on Page 6
def count_ducks_on_page6():
    url = "https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page=6;template=results;type=batting"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    duck_column = [int(td.text) for td in soup.select("td[data-stat='0']")]
    return sum(duck_column)

# Task 2: IMDb - Movies Rated 2 to 5
def fetch_low_rated_movies():

    url = "https://www.imdb.com/search/title/?user_rating=2.0,5.0&count=25"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = soup.select('.ipc-metadata-list-summary-item')

        movie_data = []

        for index, movie in enumerate(movies):
            if index >= 25:
                break  # Stop after collecting 25 movies
        
            title_element = movie.select_one('.ipc-title__text')
            year_element = movie.select_one('.dli-title-metadata-item')
            rating_element = movie.select_one('.ipc-rating-star--rating')
            link_element = movie.select_one('.ipc-title-link-wrapper')
        
            title = title_element.text.strip() if title_element else 'N/A'
            year = year_element.text.strip() if year_element else 'N/A'
            rating = rating_element.text.strip() if rating_element else 'N/A'
        
        # Extract IMDb ID from the href attribute
            id_match = link_element['href'].split('/')[2] if link_element and 'href' in link_element.attrs else 'N/A'
        
            movie_data.append({"id": id_match, "title": title, "year": year, "rating": rating})

    # Print extracted movie data as JSON
        return (json.dumps(movie_data, indent=2))



# Task 3: Wikipedia API - Extract Headings
def fetch_wikipedia_page(country: str) -> str:
    url = WIKI_BASE_URL + country.replace(" ", "_")
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.text

def extract_headings(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    
    markdown_outline = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])  # Extract heading level from tag name
        title = heading.text.strip()
        markdown_outline += "#" * level + f" {title}\n\n"
    
    return markdown_outline

def fetch_wikipedia_outline(country: str):
    html_content = fetch_wikipedia_page(country)
    if not html_content:
        return {"error": "Country not found or unable to fetch Wikipedia page."}
    
    markdown_outline = extract_headings(html_content)
    return {"country": country, "outline": markdown_outline}

# Task 4: BBC Weather API - Islamabad Forecast
import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
from datetime import datetime
from urllib.parse import urlencode

def get_weather_forecast(country):
    test_city = country
    location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
        'api_key': os.getenv('WEATHER_API'),
        's': test_city,
        'stack': 'aws',
        'locale': 'en',
        'filter': 'international',
        'place-types': 'settlement,airport,district',
        'order': 'importance',
        'a': 'true',
        'format': 'json'
    })

    result = requests.get(location_url).json()

    # ✅ Check if results exist before accessing them
    if 'response' not in result or 'results' not in result['response'] or 'results' not in result['response']['results'] or not result['response']['results']['results']:
        return json.dumps({"error": "Location not found"}, indent=2)

    location_id = result['response']['results']['results'][0]['id']
    url = f'https://www.bbc.com/weather/{location_id}'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # ✅ Check if elements exist before processing
    daily_high_values = soup.find_all('span', attrs={'class': 'wr-day-temperature__high-value'})
    daily_low_values  = soup.find_all('span', attrs={'class': 'wr-day-temperature__low-value'})
    daily_summary = soup.find('div', attrs={'class': 'wr-day-summary'})

    if not daily_high_values or not daily_low_values or not daily_summary:
        return json.dumps({"error": "Weather data not found"}, indent=2)

    daily_summary_list = re.findall('[a-zA-Z][^A-Z]*', daily_summary.text)
    datelist = pd.date_range(datetime.today(), periods=len(daily_high_values)).tolist()
    datelist = [datelist[i].date().strftime('%y-%m-%d') for i in range(len(datelist))]

    weather_data = {datelist[i]: daily_summary_list[i] for i in range(len(datelist))}

    return json.dumps(weather_data, indent=2)




# Task 5: Nominatim API - Max Latitude of Lima

def get_max_latitude(area):
    from geopy.geocoders import Nominatim

    locator = Nominatim(user_agent="myGeocoder")

    location = locator.geocode(area)

# Accessing the bounding box information.  Nominatim returns a string like
# "48.8534100,-2.3488000,48.8600000,-2.3330000".  We need to parse it.

    bounding_box_str = location.raw['boundingbox']
    bounding_box = [float(coord) for coord in bounding_box_str]

    max_latitude = max(bounding_box[0], bounding_box[1]) # boundingbox order: south, north, west, east


    return (f"The maximum latitude of the bounding box for {area} is: {max_latitude}")


# Task 6: Hacker News - Latest Go Post with 85+ Points
def get_hn_go_post(points):
    url = f"https://hnrss.org/newest?points={points}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Failed to retrieve data"
    
    soup = BeautifulSoup(response.text, 'xml')
    
    for item in soup.find_all("item"):
        link_tag = item.find("link")
        
        if link_tag:
            return link_tag.text
    
    return "No posts found with 85+ points"

# Task 7: GitHub API - Berlin Users with 140+ Followers
def get_newest_berlin_github_user():
    url = "https://api.github.com/search/users?q=location:Berlin+followers:>140&sort=joined&order=desc"
    response = requests.get(url).json()
    
    if 'items' not in response or not response['items']:
        return "No users found"
    
    newest_user = response['items'][0]
    newest_user=newest_user['login']
    user_url=f"https://api.github.com/users/{newest_user}"
    response = requests.get(user_url).json()

   
    created_at = response.get('created_at', "No creation date available")
    
    return created_at if created_at <= "2025-02-04T22:33:09Z" else "Ignoring ultra-new users"

# Task 8: GitHub Actions - Daily Commit
def generate_github_action():
    action_yaml = """
    name: Daily Commit
    on:
      schedule:
        - cron: '0 0 * * *'
    jobs:
      commit:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout
            uses: actions/checkout@v2
          - name: Make a commit (23f2004644@ds.study.iitm.ac.in)
            run: |
              date > update.txt
              git add update.txt
              git commit -m "Daily update"
              git push
    """
    return action_yaml
import os
# Task 9: PDF Parsing - Student Marks Analysis
 # PyMuPDF
import os

import os
import pandas as pd
import tabula

def extract_student_marks(file_name,filter_subject,from_page,to_page,filter_marks):
    # Get the path of the PDF
    pdf_path = os.path.join(os.getcwd(), 'tmp', file_name)
    
    # Check if the file exists
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{file_name}' does not exist.")
        return
    
    # Read the tables from the PDF
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
    
    # Initialize an empty list to store all DataFrames
    all_dfs = []
    
    # Iterate through each table and add a "Group" column based on the page number
    for i, table in enumerate(tables):
        # Add a "Group" column to the table
        table["Group"] = i + 1  # Group 1 for Page 1, Group 2 for Page 2, etc.
        # Append the table to the list
        all_dfs.append(table)
    
    # Combine all DataFrames into a single DataFrame
    df = pd.concat(all_dfs, ignore_index=True)
    
    # Rename columns for easier access (assuming the structure is consistent)
    df.columns = ["Maths", "Physics", "English", "Economics", "Biology", "Group"]
    
    # Convert marks to numerical data types
    df["Maths"] = pd.to_numeric(df["Maths"], errors="coerce")
    df["Physics"] = pd.to_numeric(df["Physics"], errors="coerce")
    df["English"] = pd.to_numeric(df["English"], errors="coerce")
    df["Economics"] = pd.to_numeric(df["Economics"], errors="coerce")
    df["Biology"] = pd.to_numeric(df["Biology"], errors="coerce")
    df["Group"] = pd.to_numeric(df["Group"], errors="coerce")
    
    # Drop rows with missing values (if any)
    df.dropna(inplace=True)
    
    # Display the first few rows of the combined DataFrame
    print("First few rows of the data:")
    print(df.head())
    
    # Display the data types of the columns
    print("\nData types of the columns:")
    print(df.dtypes)
    
    # Example of filtering: students with Physics marks >= 56 and Group number between 46 and 79
    filtered_df = df[(df[filter_subject] >= filter_marks) & (df["Group"].between(from_page, to_page))]
    print(filtered_df)
    
    # Calculate the total marks for Economics in the filtered DataFrame
    total_economics_marks = filtered_df[filter_subject].sum()
    # Corrected to "Economics"
    
    return int(total_economics_marks)




 # PyMuPDF
import os

def pdf_to_markdown(file_name):
    pdf_path = os.path.join(os.getcwd(), 'tmp', file_name)
 # Add text with Markdown formatting
    import pymupdf4llm
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text
