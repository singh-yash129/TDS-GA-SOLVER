from fastapi import FastAPI, File, Form, UploadFile, HTTPException
import pandas as pd
import zipfile
import io
import os
import requests
import json
import ga1func, ga2func, ga3func, ga4func, ga5func
from prompt import prompt,TASK_FUNCTIONS


# Initialize FastAPI app
app = FastAPI()

# Set your AIPROXY_TOKEN
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"


TASK_IMPLEMENTATIONS = {
    "get_vscode_version": ga1func.get_vscode_version,
    "count_wednesdays": ga1func.count_wednesdays,
    "run_npx_command": ga1func.run_npx_command,
    "make_http_request": ga1func.make_http_request,
    "extract_csv_from_zip": ga1func.extract_csv_from_zip,
    "sort_json": ga1func.sort_json,
    "multi_cursor_to_json": ga1func.multi_cursor_to_json,
    "extract_hidden_value": ga1func.extract_hidden_value,
    "sum_css_values": ga1func.sum_css_values,
    "process_encoded_files": ga1func.process_encoded_files,
    "use_github": ga1func.use_github,
    "replace_text_in_files": ga1func.replace_text_in_files,
    "list_large_files": ga1func.list_large_files,
    "move_and_rename_files": ga1func.move_and_rename_files,
    "compare_files": ga1func.compare_files,
    "sql_ticket_sales": ga1func.sql_ticket_sales,
    "find_git_repo_size": ga1func.find_git_repo_size,
    "check_file_integrity": ga1func.check_file_integrity,
    "extract_all_text_from_html": ga1func.extract_all_text_from_html,
    "generate_markdown": ga2func.generate_markdown,
    "compress_image": ga2func.compress_image,
    "deploy_github_pages": ga2func.deploy_github_pages,
    "google_colab_test": ga2func.google_colab_test,
    "image_library_colab": ga2func.image_library_colab,
    "deploy_vercel_api": ga2func.deploy_vercel,
    "create_github_action": ga2func.create_github_action,
    "push_docker_image": ga2func.push_docker_image,
    "run_fastapi_server": ga2func.run_fastapi_server,
    "run_llamafile": ga2func.run_llamafile,
    "analyze_sentiment": ga3func.analyze_sentiment,
    "generate_addresses": ga3func.generate_addresses,
    "extract_invoice_text": ga3func.extract_invoice_text,
    "generate_text_embeddings": ga3func.generate_text_embeddings,
    "LLM_say_yes":ga3func.LLM_say_yes,
    "llm_token":ga3func.llm_token,
    "count_ducks_on_page6": ga4func.count_ducks_on_page6,
    "fetch_low_rated_movies": ga4func.fetch_low_rated_movies,
    "fetch_wikipedia_outline": ga4func.fetch_wikipedia_outline,
    "get_weather_forecast": ga4func.get_weather_forecast,
    "get_max_latitude": ga4func.get_max_latitude,
    "get_hn_go_post": ga4func.get_hn_go_post,
    "get_newest_berlin_github_user": ga4func.get_newest_berlin_github_user,
    "generate_github_action": ga4func.generate_github_action,
    "extract_student_marks": ga4func.extract_student_marks,
    "pdf_to_markdown": ga4func.pdf_to_markdown,
    "clean_and_calculate_margin": ga5func.clean_and_calculate_margin,
    "count_unique_students": ga5func.count_unique_students,
    "count_successful_get_requests": ga5func.count_successful_get_requests,
    "top_data_consumer": ga5func.top_data_consumer,
    "clean_and_aggregate_sales": ga5func.clean_and_aggregate_sales,
    "count_key_occurrences": ga5func.count_key_occurrences,
    "reconstruct_image": ga5func.reconstruct_image,
    "calculate_average_temperature": ga5func.calculate_average_temperature,
    "extract_emails_from_text": ga5func.extract_emails_from_text,
    'extract_transcript':ga5func.extract_transcript,
    'most_similar_embedding':ga3func.most_similar_embedding,
    'extract_text_from_image':ga3func.extract_text_from_image,
   
}


# Function mapping


# Function to call respective task function (dummy implementation)
def execute_task(task_name, **kwargs):

        function = TASK_IMPLEMENTATIONS.get(task_name)
        if function:
            return function(**kwargs)  # ✅ Call actual function
        return "Unknown task"
# with open('ans.json', 'r', encoding='utf-8') as file:
#     data = json.load(file) 
# def gunc(req):
#     return data[req]
# item_list = list(data.keys())
UPLOAD_DIR='tmp'
os.makedirs(UPLOAD_DIR, exist_ok=True)
@app.post("/api/")
async def answer_question(question: str = Form(...), file: UploadFile = File(None)):
    
#     prompt = f'''You are an awesome task assistant. Your sole responsibility is to return exactly one item name in any given condition and item name is most similar to the question. The item name must be selected from the provided list.

# Key instructions:
# 1. The item name must be chosen from the list provided: {item_list}.
# 2. You should not output any words other than the item name.
# 3. The output must strictly follow JSON format, as shown below:
# ```json
# {{
#     "function": "item_name_here"
# }}
# '''

    try:
        saved_file_path = None
        saved_file=False
        if file:
            saved_file=True
            if isinstance(file.filename, str) and file.filename.strip():
    # Ensure the filename does not contain invalid characters
                saved_file_path = os.path.join(os.getcwd(),UPLOAD_DIR, file.filename)
                print(saved_file_path)
            else:
                raise ValueError("Invalid or empty file name.")
            
            # Check if the file already exists, and delete the old one if so
            if os.path.exists(saved_file_path):
                os.remove(saved_file_path)
                print(f"Existing file {saved_file_path} deleted.")

            # Save the new file to the 'upload' directory
            with open(saved_file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            print(f"File saved at: {saved_file_path}")

        headers = {
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "system", "content": prompt},{"role": "user","content":f'Question{question}'}]
        }
        response = requests.post(AIPROXY_URL, json=data, headers=headers)
        response_json = response.json()
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response_json.get("error", "Unknown error"))




        ai_response = response_json["choices"][0]["message"]["content"].strip()

        if ai_response.startswith("```json"):
            ai_response = ai_response.replace("```json", "").replace("```", "").strip()
        # If GPT-4o Mini suggests a function call, execute it
        print(ai_response)
        try:
            parsed_response = json.loads(ai_response)
            if "function" in parsed_response and parsed_response["function"] in TASK_FUNCTIONS:
                task_name = parsed_response["function"]
                task_params = parsed_response.get("parameters", {})
        
                if 'file_name' in task_params:
                    task_params['file_name'] = file.filename
                elif 'zip_filename' in task_params:    
                    task_params['zip_filename']=file.filename
                elif 'log_file_name' in task_params:
                    task_params['log_file_name']=file.filename
                elif 'scrambled_image' in task_params:
                    task_params['scrambled_image']=file.filename
                elif 'mapping_file_name' in task_params:
                    task_params['mapping_file_name']=file.filename

                elif 'image_file' in task_params:
                    task_params['image_file']=file.filename              
                print(task_params)
              
                return {"answer": execute_task(task_name,**task_params)}
        except json.JSONDecodeError:
            pass  # If response isn't JSON, assume it's a direct answer
        
        return {"answer": ai_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

