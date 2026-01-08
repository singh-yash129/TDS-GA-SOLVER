import os
import json
import zipfile
import hashlib
import requests
import subprocess
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
from Prebuilt import gunc
from github import Github


def get_vscode_version():
    return gunc('q-vs-code-version')

def make_http_request(email):
    url = f"https://httpbin.org/get?email={email}"
    response = requests.get(url)
    return response.json()

def run_npx_command(file_name):
    file_path = os.path.join(os.getcwd(), 'tmp', file_name)
    command = f"npx -y prettier@3.4.2 {file_path} | sha256sum"
    return subprocess.getoutput(command)



def count_wednesdays(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return sum(1 for d in pd.date_range(start, end) if d.weekday() == 2)

def extract_csv_from_zip(zip_filename):
    zip_path = os.path.join(os.getcwd(),"tmp", zip_filename)  # Assume the ZIP file is in /tmp
    extract_path = os.path.join(os.getcwd(),"tmp", "extracted")  # Extract inside /tmp/extracted
    os.makedirs(extract_path, exist_ok=True)  # Ensure the directory exists

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)  # Extract files into /tmp/extracted

    csv_file_path = os.path.join(extract_path, "extract.csv")  # Expected CSV file path

    if not os.path.exists(csv_file_path):
        return f"Error: {csv_file_path} not found!"

    df = pd.read_csv(csv_file_path)
    
    if "answer" not in df.columns:
        return "Error: Column 'answer' not found in CSV!"

    return df["answer"].iloc[0]  # Return the first value from the "answer" column




def sort_json(file_name) :
    # Parse the JSON string into a Python object (list of dictionaries)
    json_data=os.path.join(os.getcwd,'tmp',file_name)
    data = json.loads(json_data)
    
    # Sort the list of dictionaries by 'age' and 'name'
    sorted_data = sorted(data, key=lambda x: (x["age"], x["name"]))
    
    # Return the sorted data as a JSON string (minified)
    return json.dumps(sorted_data, separators=(",", ":"))


def multi_cursor_to_json(file_name):
    file_path=os.path.join(os.getcwd(),'tmp',file_name)
    data = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if "=" in line:
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()
    
    json_output = json.dumps(data, indent=4)
    return json_output
    return json.dumps(input_text.splitlines())

def extract_hidden_value(file_name):
    with open(os.path.join(os.getcwd,'tmp',file_name),'r') as file:
        html_content=file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find("input", {"type": "hidden"})["value"]

def sum_css_values(file_name):
    with open(os.path.join(os.getcwd,'tmp',file_name),'r') as file:
        html_content=file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    return sum(int(div["data-value"]) for div in soup.find_all("div", class_="foo"))

def process_encoded_files(zip_filename, symbols):
    # Define paths
    zip_path = os.path.join(os.getcwd(), "tmp", zip_filename)  # Assume the ZIP file is in /tmp
    extract_path = os.path.join(os.getcwd(), "tmp", "data")  # Extract inside /tmp/replace
    os.makedirs(extract_path, exist_ok=True)  # Ensure the directory exists
    
    # Extract ZIP file contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    total = 0
    for file in Path(extract_path).glob("*.csv"):
        df = pd.read_csv(file, encoding='utf-8', names=["symbol", "value"])
        total += df[df["symbol"].isin(symbols)]["value"].sum()
    return total

def use_github(repo_name, github_username,email):
    os.system(f"git clone https://github.com/{github_username}/{repo_name}.git")
    os.chdir(repo_name)
    
    email_data = {"email": email}
    with open("email.json", "w") as file:
        json.dump(email_data, file, indent=4)
    
    os.system("git add email.json")
    os.system("git commit -m 'Add email.json file'")
    os.system("git push origin main")
    
    return(f"File pushed successfully. Check it at: https://github.com/{github_username}/{repo_name}/blob/main/email")


def replace_text_in_files(zip_filename):
    # Define paths
    zip_path = os.path.join(os.getcwd(), "tmp", zip_filename)  # Assume the ZIP file is in /tmp
    extract_path = os.path.join(os.getcwd(), "tmp", "replace")  # Extract inside /tmp/replace
    os.makedirs(extract_path, exist_ok=True)  # Ensure the directory exists
    
    # Extract ZIP file contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Replace text in each file and calculate the hash
    sha256_hash = hashlib.sha256()
    for file in Path(extract_path).rglob("*"):  # Ensure proper directory traversal
        if file.is_file():
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            with open(file, "w", encoding="utf-8") as f:
                f.write(content.replace("IITM", "IIT Madras"))
            # Update the hash with the file content
            sha256_hash.update(content.encode("utf-8"))
    
    # Return the SHA-256 hash in hexadecimal format
    return sha256_hash.hexdigest()


def list_large_files(zip_filename, min_size, date):
    zip_path = os.path.join(os.getcwd(), "tmp", zip_filename)  # Assume the ZIP file is in /tmp
    extract_path = os.path.join(os.getcwd(), "tmp", "list")  # Extract inside /tmp/replace
    os.makedirs(extract_path, exist_ok=True)  # Ensure the directory exists
    
    # Extract ZIP file contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    total_size = 0
    for file in Path(extract_path).rglob("*"):
        if file.is_file() and file.stat().st_size >= min_size and datetime.fromtimestamp(file.stat().st_mtime) >= date:
            total_size += file.stat().st_size
    return total_size

def move_and_rename_files(zip_filename):
    zip_path = os.path.join(os.getcwd(), "tmp", zip_filename)  # Assume the ZIP file is in /tmp
    extract_path = os.path.join(os.getcwd(), "tmp", "move")  # Extract inside /tmp/replace
    os.makedirs(extract_path, exist_ok=True)  # Ensure the directory exists
    
    # Extract ZIP file contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    for file in Path(extract_path).rglob("*"):
        if file.is_file():
            new_name = ''.join(str(int(c) + 1) if c.isdigit() else c for c in file.name)
            file.rename(Path(extract_path) / new_name)
    return subprocess.getoutput(f"grep . {extract_path}/* | LC_ALL=C sort | sha256sum")


def compare_files(zip_filename):
    # Define paths
    zip_path = os.path.join(os.getcwd(), "tmp", zip_filename)  # Assume the ZIP file is in /tmp
    extract_path = os.path.join(os.getcwd(), "tmp", "compare")  # Extract inside /tmp/compare
    os.makedirs(extract_path, exist_ok=True)  # Ensure the directory exists
    
    # Extract ZIP file contents
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # List all text files in the extracted path
    text_files = [file for file in Path(extract_path).glob("*.txt")]

    # Ensure there are exactly two text files to compare
    if len(text_files) != 2:
        raise ValueError("Expected exactly 2 text files in the ZIP archive.")
    
    # Read file contents
    with open(text_files[0], 'r', encoding="utf-8") as file_a, open(text_files[1], 'r', encoding="utf-8") as file_b:
        lines_a = file_a.readlines()
        lines_b = file_b.readlines()
    
    # Count differing lines
    if len(lines_a) != len(lines_b):
        raise ValueError("Files have different numbers of lines.")
    
    differing_lines = sum(1 for line_a, line_b in zip(lines_a, lines_b) if line_a != line_b)
    
    return differing_lines

# Example call:
# print(compare_files("example.zip"))

def sql_ticket_sales(file_name):
    db_path=os.path.join(os.getcwd(), "tmp", file_name)
    conn = sqlite3.connect(db_path)
    query = "SELECT SUM(units * price) FROM tickets WHERE LOWER(type) = 'gold'"
    result = conn.execute(query).fetchone()[0]
    conn.close()
    return result

def find_git_repo_size(repo_name):
    repo_path=os.path.join(os.getcwd(),'tmp',repo_name)
    return subprocess.getoutput(f"du -sh {repo_path}")

def check_file_integrity(file_name):
    file_path=os.path.join(os.getcwd,'tmp',file_name)
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def extract_all_text_from_html(file_name):
    file_path=os.path.join(os.getcwd,'tmp',file_name)
    with open(file_path, 'r') as file:
        html_content=file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=" ").strip()
