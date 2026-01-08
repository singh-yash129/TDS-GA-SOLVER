# TDS Solver

## Project Description
This project is designed to make life easier for students enrolled in the Tools in Data Science course at IIT Madras’ Online Degree in Data Science. It provides an API that can automatically answer any of the graded assignment questions from the course.

## API Endpoint
The application exposes an API endpoint at:
```
https://your-app.vercel.app/api/
```

### Request
The endpoint accepts a POST request with the question and optional file attachments as multipart/form-data.

Example:
```sh
curl -X POST "https://your-app.vercel.app/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?" \
  -F "file=@abcd.zip"
```

### Response
The response is a JSON object with a single text (string) field: `answer`.

Example:
```json
{
  "answer": "1234567890"
}
```

## Deployment
Deploy your application to a public URL that can be accessed by anyone. You may use any platform, including Vercel.

## Submission
1. Create a new public GitHub repository.
2. Add an MIT LICENSE file.
3. Commit and push your code.
4. Submit your GitHub repository URL and your API endpoint URL in this [Google Form](https://forms.gle/6ZLCGEEHUHVK71Yu5).

## Evaluation
### Pre-requisites
- Your GitHub repository exists and is publicly accessible.
- Your GitHub repository has a LICENSE file with the MIT license.

### Scoring
- We will send 5 questions randomly chosen from the graded assignments above.
- Correct answers will be awarded 4 marks each.
- Your score will be the sum of the marks above. No normalization. What you get is what you get.