import json

TASK_FUNCTIONS = {
    "check_file_integrity": ["file_name"],
    "compare_files": ["zip_filename"],
    "count_wednesdays": ["start_date", "end_date"],
    "extract_all_text_from_html": ["file_name"],
    "extract_csv_from_zip": ["zip_filename"],
    "extract_hidden_value": ["file_name"],
    "find_git_repo_size": ["repo_name"],
    "get_vscode_version": [],
  
    "list_large_files": ["zip_filename", "min_size", "date"],
    "make_http_request": ["email"],
    "move_and_rename_files": ["zip_filename"],
    "multi_cursor_to_json": ["input_text"],
    "process_encoded_files": ["zip_filename", "symbols"],
    "replace_text_in_files": ["zip_filename"],
    "run_npx_command": ["file_name"],
    "sort_json": ["file_name"],
    "sql_ticket_sales": ["db_name"],
    "sum_css_values": ["file_name"],
    "use_github": ["repo_name", "github_username","email"],
    "compress_image": ['file_name'],
    "create_github_action": ["repo_name", "github_username","email"],
    "deploy_github_pages": ["repo_name", "github_username","email"],
    "deploy_vercel": ["repo_name", "github_username",'file_name'],
    "generate_markdown": [],
    "google_colab_test": [],
    "image_library_colab": ['file_name'],
    "push_docker_image": ['docker_username','repo_name'],
    "run_fastapi_server": ['file_name'],
    "run_llamafile": ['file_name'],
    'most_similar_embedding':[],
    "analyze_sentiment": [],
  
    "extract_text_from_image": ["image_file"],
    "generate_addresses": [],
    "llm_token": ['file_name','model'],
 
 
    "generate_text_embeddings": [],
  
    'LLM_say_yes':[],

    "count_ducks_on_page6": [],
    "extract_student_marks": ["file_name",'filter_subject','filter_marks','from_page','to_page'],
    "fetch_low_rated_movies": [],
    "fetch_wikipedia_outline": ["country"],
    'get_high_quality_posts':['file_name'],
    "generate_github_action": [],
    "get_hn_go_post": ['points'],
    "get_weather_forecast": ["country"],
    "get_max_latitude": ['area'],
    "get_newest_berlin_github_user": [],
    "pdf_to_markdown": ["file_name"],
    'calculate_total_sales':['file_name'],
    "clean_and_aggregate_sales": ["file_name"],
    "calculate_average_temperature": ["file_name"],
    "clean_and_calculate_margin": ["file_name"],
    "count_key_occurrences": ["file_name",'target_key'],
    "count_successful_get_requests": ["log_file_name"],
    "count_unique_students": ["file_name"],
    "extract_emails_from_text": ["file_name"],
    "top_data_consumer": ["log_file_name"],

    'reconstruct_image':['scrambled_image','mapping_file_name'],
    'extract_transcript':['youtube_url','start_time','end_time','model_size']
}

prompt = f"""
You are an AI assistant trained to solve data science assignments efficiently. Given a user question, determine if:
1. The question can be answered directly with your knowledge.
2. The question requires executing a function from a predefined list.

**Rules:**
- If a function is needed, return a JSON object in this format:
  {{
      "function": "function_name",
      "parameters": {{ "param1": "value1", "param2": "value2" }}
  }}
- Only use function names from this list: {json.dumps(list(TASK_FUNCTIONS.keys()))}.
- Only use parameter keys corresponding to the respective function: {json.dumps(TASK_FUNCTIONS)}.
- Ensure all required parameters for the function are included.
- **Important:** Uploaded file names must remain unchanged (e.g., if the name is `q-csv-zip.zip`, it must remain `q-csv-zip.zip`).
- If the function does not require parameters, return `"parameters": {{}}`.
- **Do NOT answer in plain text** if a function is available.

**Example Outputs:**
1. **Direct Answer:**
   *User:* What is 2 + 2?
   *Response:* "4"

2. **Function Call Required:**
   *User:* "What is the output of 'code -s' in VS Code?"
   *Response:*  
   ```json
   {{
       "function": "get_vscode_version",
       "parameters": {{}}
   }}
   ```

3. **Function Call Required**
   *User:* "Download the provided README.md file and run 'npx -y prettier@3.4.2 README.md | sha256sum'."
   *Response:*  
   ```json
   {{
       "function": "run_npx_command",
       "parameters": {{
           "file_name": "README.md"
       }}
   }}
   ```

4. **Function Call Required**
   *User:* "Send an HTTPS request to 'https://httpbin.org/get' with the email parameter."
   *Response:*  
   ```json
   {{
       "function": "make_http_request",
       "parameters": {{
           "email": "example@example.com"
       }}
   }}
   ```

5. **Function Call Required:**  
   *User:* "Check the integrity of the file at 'some/path/to/file.txt'."
   *Response:*  
   ```json
   {{
       "function": "check_file_integrity",
       "parameters": {{
           "file_name": "file.txt"
       }}
   }}
   ```

"""