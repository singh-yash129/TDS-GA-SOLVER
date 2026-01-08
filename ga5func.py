import pandas as pd
import json
import gzip
import re
import duckdb
from collections import defaultdict
from rapidfuzz import process, fuzz  # For city name clustering
from PIL import Image
import numpy as np
import os

import pandas as pd
import numpy as np
from datetime import datetime


def clean_and_calculate_margin(file_name):
    """
    Cleans sales data and calculates total margin for transactions before May 13, 2022,
    for the product 'Gamma' in France (FR), handling inconsistencies in country names,
    product names, and date formats.
    
    Parameters:
    file_path (str): Path to the Excel file.
    
    Returns:
    float: Total margin calculated as (Total Sales - Total Cost) / Total Sales
    """
    
    # Load the Excel file
    file_path=os.path.join(os.getcwd(),'tmp',file_name)
    df = pd.read_excel(file_path)
    
    # Standardize country names using fuzzy matching
    country_mapping = {"USA": "US", "U.S.A": "US", "US": "US", "France": "FR", "FRA": "FR"}
    
    def standardize_country(country):
        best_match = process.extractOne(country.strip(), country_mapping.keys())
        return country_mapping[best_match[0]] if best_match else country.strip()
    
    df["Country"] = df["Country"].astype(str).apply(standardize_country)
    
    # Convert date formats to a standard format (ISO 8601)
    def parse_date(date_str):
        for fmt in ("%m-%d-%Y", "%Y/%m/%d", "%Y-%m-%d"):
            try:
                return datetime.strptime(date_str, fmt).isoformat()
            except ValueError:
                continue
        return None
    
    df["Date"] = df["Date"].astype(str).apply(parse_date)
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Extract product name before the slash using fuzzy matching
    def extract_product_name(product):
        return product.split("/")[0].strip() if isinstance(product, str) else product
    
    df["Product"] = df["Product"].astype(str).apply(extract_product_name)
    
    # Clean Sales and Cost fields
    df["Sales"] = df["Sales"].astype(str).str.replace("USD", "").str.strip().astype(float)
    df["Cost"] = df["Cost"].astype(str).str.replace("USD", "").str.strip()
    df["Cost"] = pd.to_numeric(df["Cost"], errors='coerce')
    df["Cost"].fillna(df["Sales"] * 0.5, inplace=True)  # Assume cost is 50% of sales if missing
    
    # Apply filtering criteria
    cutoff_date = datetime(2022, 5, 13, 21, 49, 50)
    filtered_df = df[(df["Date"] <= cutoff_date) & (df["Product"] == "Gamma") & (df["Country"] == "FR")]
    
    # Calculate total margin
    total_sales = filtered_df["Sales"].sum()
    total_cost = filtered_df["Cost"].sum()
    total_margin = (total_sales - total_cost) / total_sales if total_sales != 0 else np.nan
    
    return total_margin

# Example usage
# margin = clean_and_calculate_margin("path_to_sales_data.xlsx")
# print(margin)


def count_unique_students(file_name):
    """
    Reads a text file, extracts unique student IDs, and counts them.
    
    Parameters:
    file_path (str): Path to the text file containing student data.
    
    Returns:
    int: Number of unique student IDs in the file.
    """
    unique_students = set()
    file_path=os.path.join(os.getcwd(),'tmp',file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            student_id = line.strip().split()[0]  # Assuming student ID is the first item in each line
            unique_students.add(student_id)
    
    return len(unique_students)

# Example usage
# unique_count = count_unique_students("path_to_student_data.txt")
# print(unique_count)


import gzip
import re
from datetime import datetime

def count_successful_get_requests(log_file_name):
    """
    Parses a gzipped Apache log file and counts the number of successful GET requests
    for pages under /tamilmp3/ made on Sundays between 10:00 and 14:59 in May 2024.
    
    Parameters:
    log_file (str): Path to the gzipped Apache log file.
    
    Returns:
    int: Number of successful GET requests meeting the criteria.
    """
    count = 0
    file_path=os.path.join(os.getcwd(),'tmp',log_file_name)
    # Define regex to parse log entries
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<time>.*?)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) \S+'
    )
    
    # Define filters
    date_format = "%d/%b/%Y:%H:%M:%S %z"
    
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                log_data = match.groupdict()
                
                # Parse datetime
                log_time = datetime.strptime(log_data["time"], date_format)
                
                # Check if it's Sunday, in May 2024, and within the time range
                if (log_time.year == 2024 and log_time.month == 5 and log_time.weekday() == 6
                        and 10 <= log_time.hour < 15):
                    
                    # Check if the request is a GET under /tamilmp3/
                    if log_data["method"] == "GET" and log_data["url"].startswith("/tamilmp3/"):
                        
                        # Check if the status code is successful (200-299)
                        if 200 <= int(log_data["status"]) < 300:
                            count += 1
    
    return count

# Example usage
# successful_requests = count_successful_get_requests("path_to_apache_logs.gz")
# print(successful_requests)

import gzip
import re
from datetime import datetime
from collections import defaultdict

def top_data_consumer(log_file_name):
    """
    Parses a gzipped Apache log file to find the IP address that downloaded the most data
    from /malayalammp3/ on 2024-05-15.
    
    Parameters:
    log_file (str): Path to the gzipped Apache log file.
    
    Returns:
    tuple: (Top IP address, total bytes downloaded)
    """
    ip_data_usage = defaultdict(int)
    log_file=os.path.join(os.getcwd(),'tmp',log_file_name)
    # Define regex to parse log entries
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<time>.*?)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\S+)'
    )
    
    # Define filters
    date_format = "%d/%b/%Y:%H:%M:%S %z"
    target_date = datetime(2024, 5, 15).date()
    
    with gzip.open(log_file, 'rt', encoding='utf-8') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                log_data = match.groupdict()
                
                # Parse datetime
                log_time = datetime.strptime(log_data["time"], date_format)
                
                # Check if it's the target date
                if log_time.date() == target_date:
                    
                    # Check if the request is under /malayalammp3/
                    if log_data["url"].startswith("/malayalammp3/"):
                        
                        # Parse response size, ignoring '-' values
                        size = int(log_data["size"]) if log_data["size"].isdigit() else 0
                        ip_data_usage[log_data["ip"]] += size
    
    # Identify the top data-consuming IP
    top_ip = max(ip_data_usage, key=ip_data_usage.get, default=None)
    
    return top_ip, ip_data_usage.get(top_ip, 0)

# Example usage
# top_ip, total_bytes = top_data_consumer("path_to_apache_logs.gz")
# print(f"Top IP: {top_ip}, Total Bytes: {total_bytes}")


def clean_and_aggregate_sales(file_name):
    file_path=os.path.join(os.getcwd(),'tmp',file_name)
    """
    Reads a dataset, clusters city names using fuzzy matching, filters relevant sales entries,
    and aggregates total units sold for each clustered city.
    
    Parameters:
    file_path (str): Path to the CSV dataset containing sales data.
    
    Returns:
    dict: Dictionary mapping clustered city names to total units of 'Mouse' sold where units >= 77.
    """
    # Load dataset
    df = pd.read_csv(file_path)
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()
    
    # Filter sales entries (Product == 'Mouse' & Units Sold >= 77)
    filtered_df = df[(df['product'].str.strip().str.lower() == 'mouse') & (df['units_sold'] >= 77)]
    
    # Cluster city names using fuzzy matching
    unique_cities = list(filtered_df['city'].unique())
    city_clusters = {}
    
    for city in unique_cities:
        match, score = process.extractOne(city, city_clusters.keys(), scorer=fuzz.token_sort_ratio)
        if score > 85:  # Threshold for clustering similar names
            city_clusters[match].append(city)
        else:
            city_clusters[city] = [city]
    
    # Create a mapping of city names to their cluster representatives
    city_mapping = {city: cluster for cluster, cities in city_clusters.items() for city in cities}
    
    # Normalize city names in the dataset
    filtered_df['city'] = filtered_df['city'].map(city_mapping)
    
    # Aggregate sales by clustered city
    city_sales = filtered_df.groupby('city')['units_sold'].sum().to_dict()
    
    return city_sales

# Example usage
# sales_by_city = clean_and_aggregate_sales("path_to_sales_data.csv")
# print(f"Units of Mouse sold in Delhi: {sales_by_city.get('Delhi', 0)}")

import json

def calculate_total_sales(file_name):
    file_path=os.path.join(os.getcwd(),'tmp',file_name)
    """
    Reads a JSON file containing sales data, extracts and sums up the sales values,
    while handling missing or incomplete data.
    
    Parameters:
    file_path (str): Path to the JSON file containing sales data.
    
    Returns:
    float: Total sales value across all entries.
    """
    total_sales = 0.0
    
    # Load JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract and sum sales values
    for entry in data:
        if 'sales' in entry and isinstance(entry['sales'], (int, float)):
            total_sales += entry['sales']
    
    return total_sales

# Example usage
# total_sales = calculate_total_sales("path_to_sales_data.json")
# print(f"Total Sales Value: {total_sales}")


import json

def count_key_occurrences(file_name, target_key='OI'):
    file_path=os.path.join(os.getcwd(),'tmp',file_name)
    """
    Reads a large, deeply nested JSON log file and counts occurrences of a specified key.
    
    Parameters:
    file_path (str): Path to the JSON log file.
    target_key (str): The key to count occurrences of.
    
    Returns:
    int: Total number of times the key appears in the JSON structure.
    """
    def recursive_count(data):
        count = 0
        if isinstance(data, dict):
            count += sum(1 for key in data.keys() if key == target_key)
            for key, value in data.items():
                count += recursive_count(value)
        elif isinstance(data, list):
            for item in data:
                count += recursive_count(item)
        return count
    
    try:
        # Load JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return 0
    except FileNotFoundError:
        print("Error: File not found.")
        return 0
    
    return recursive_count(data)

# Example usage
# occurrences = count_key_occurrences("path_to_logs.json", "OI")
# print(f"Occurrences of 'OI' as a key: {occurrences}")
import duckdb

def get_high_quality_posts(file_name):
    db_path=os.path.join(os.getcwd(),'tmp',file_name)
    """
    Connects to the DuckDB database, retrieves post IDs of posts made after
    2025-02-03T01:22:01.112Z with at least one comment having exactly 5 useful stars,
    and returns them sorted in ascending order.
    
    Parameters:
    db_path (str): Path to the DuckDB database file.
    
    Returns:
    list: Sorted list of post IDs meeting the criteria.
    """
    query = """
    SELECT post_id
    FROM social_media
    WHERE timestamp >= '2025-02-03T01:22:01.112Z'
    AND REGEXP_MATCHES(comments, '"useful"\s*:\s*5')
    ORDER BY post_id;
    """
    
    con = duckdb.connect(db_path)
    result = con.execute(query).fetchall()
    con.close()
    
    return [row[0] for row in result]


import os
import base64
import subprocess
import json
import requests

def extract_transcript(youtube_url, start_time, end_time, model_size='base'):
    """
    Downloads the audio from a YouTube video, extracts the specified segment,
    and transcribes it using Google Gemini API.

    Parameters:
    youtube_url (str): The URL of the YouTube video.
    start_time (float): The start time in seconds.
    end_time (float): The end time in seconds.
    model_size (str): The size of the Whisper model to use (default: 'base').

    Returns:
    str: The transcribed text of the extracted audio segment.
    """
    # Define the output audio file
    audio_file = "audio_clip.mp3"
    
    # Download the audio using yt-dlp
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio',
    }
    
    # Run yt-dlp to download the audio
    subprocess.run(['yt-dlp', '--format', 'bestaudio', '--postprocessor-args', '-vn', '-acodec', 'mp3', '--output', audio_file, youtube_url])

    # Encode the audio file in base64
    with open(audio_file, "rb") as audio_file_obj:
        audio_base64 = base64.b64encode(audio_file_obj.read()).decode('utf-8')

    # Send a request to Google Gemini API for transcription
    headers = {
        "X-Goog-API-Key": os.getenv("GOOGLE_API_KEY"),
        "Content-Type": "application/json",
    }

    # Prepare the data payload
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "audio/mp3",
                            "data": audio_base64
                        }
                    },
                    {"text": "Transcribe this"}
                ]
            }
        ]
    }

    # Make the request to Google Gemini API
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:streamGenerateContent?alt=sse",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        # Process the response
        result = response.json()
        
        # Extract the transcribed text from the response
        transcript = result.get('contents', [])[0].get('parts', [])[0].get('text', "")
        return transcript
    else:
        # Handle errors
        print(f"Error: {response.status_code}, {response.text}")
        return None

    # Clean up the downloaded audio file
    os.remove(audio_file)



def calculate_average_temperature(file_name):

    json_file=os.path.join(os.getcwd(),'tmp',file_name)
    with open(json_file, 'r') as f:
        data = json.load(f)
    temperatures = [entry['temperature'] for entry in data if 'temperature' in entry]
    return sum(temperatures) / len(temperatures) if temperatures else None

def extract_emails_from_text(file_name):
    file_path=os.path.join(os.getcwd(),'tmp',file_name)
    with open(file_path, 'r') as f:
        text = f.read()
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return set(emails)

from PIL import Image
import json
import io

def reconstruct_image(scrambled_image, mapping_file_name):
    scrambled_image_path=os.path.join(os.getcwd(),'tmp',scrambled_image)
    mapping_file_path=os.path.join(os.getcwd(),'tmp',mapping_file_name)
    # Load the scrambled image
    scrambled_image = Image.open(scrambled_image_path)
    width, height = scrambled_image.size
    piece_size = width // 5  # Since it's a 5x5 grid
    
    # Load the mapping file
    with open(mapping_file_path, 'r') as f:
        mapping = json.load(f)
    
    # Create a blank image for the reconstructed output
    reconstructed_image = Image.new('RGB', (width, height))
    
    # Reassemble the image using the mapping file
    for piece in mapping:
        original_row, original_col = piece["original"]
        current_row, current_col = piece["current"]
        
        # Extract the current piece from the scrambled image
        box = (current_col * piece_size, current_row * piece_size, 
               (current_col + 1) * piece_size, (current_row + 1) * piece_size)
        piece_image = scrambled_image.crop(box)
        
        # Paste it into the correct position in the reconstructed image
        new_position = (original_col * piece_size, original_row * piece_size)
        reconstructed_image.paste(piece_image, new_position)
    
    # Return the reconstructed image as a binary response
    img_byte_arr = io.BytesIO()
    reconstructed_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()


