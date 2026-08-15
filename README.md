Project Structure

flask-ai-prompt-api/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── database/
│   ├── __init__.py
│   └── mongodb.py
│
├── routes/
│   ├── __init__.py
│   └── prompt_routes.py
│
└── services/
    ├── __init__.py
    ├── prompt_service.py
    └── openai_service.py


Responsibilities
app.py — creates Flask app and registers routes.
database/mongodb.py — creates MongoDB connection and exposes collections.
routes/prompt_routes.py — contains API endpoints and request validation.
services/prompt_service.py — fetches prompt templates.
services/openai_service.py — communicates with OpenAI.
.env — stores secrets/configuration.
requirements.txt — Python dependencies.    


1. Prerequisites

Install or create:
Python 3.10+
MongoDB Atlas account
OpenAI API key
Git (optional)
Postman or Thunder Client (optional)
MongoDB does not need to be installed locally. This project uses MongoDB Atlas.

2. MongoDB Atlas Setup

Create a Cluster
Create a free MongoDB Atlas cluster, for example:
Cluster0
Create a Database User
Example:

Username:
aishwarychaurasia9_db_user
Password:
<KdEJxIzK5VSL1HOX>
Never commit this password.

Configure Network Access

In Atlas:

Security
→ Network Access
→ Add IP Address
→ Add My Current IP Address

Get Connection String

Go to:

Cluster0
→ Connect
→ Drivers
→ Python

The URI will look similar to:

mongodb+srv://aishwarychaurasia9_db_user:<password>@cluster0.xxxxx.mongodb.net/?appName=Cluster0

3. MongoDB Database Structure
Database:
flask_ai_db
Collections:

flask_ai_db
├── prompts
└── history

prompts Collection

Required document:

{
  "_id": "Education_Prompt",
  "template": "You are an expert in education domain. Answer the following: {{userInput}}"
}

The {{userInput}} placeholder is replaced at runtime.

For example:

Template:
You are an expert in education domain. Answer the following: {{userInput}}

Input:
Explain REST API.

Final prompt:
You are an expert in education domain. Answer the following: Explain REST API.

history Collection

Every request/response pair is stored.

Example:

{
  "userInput": "Explain REST API.",
  "prompt": "You are an expert in education domain. Answer the following: Explain REST API.",
  "response": "A REST API is..."
}

The history collection can be created automatically when the first record is inserted.

4. Environment Variables

Create .env in the project root:

MONGO_URI=mongodb+srv://aishwarychaurasia9_db_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?appName=Cluster0
MONGO_DB_NAME=flask_ai_db

OPENAI_API_KEY=YOUR_OPENAI_API_KEY
OPENAI_MODEL=YOUR_MODEL_NAME

Replace the placeholders with real values.

Never commit .env.

Recommended .gitignore:

.env
venv/
.venv/
__pycache__/
*.pyc
.vscode/

5. Create Virtual Environment

From the project directory:

python -m venv venv

Activate it:

.env\Scripts\Activate.ps1

You should see:

(venv)

If PowerShell blocks activation:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Then activate again.

6. Install Dependencies

python -m pip install flask pymongo python-dotenv openai

Or:

python -m pip install -r requirements.txt

A basic requirements.txt can contain:

Flask
pymongo
python-dotenv
openai

7. Run the Application

Make sure the virtual environment is active.

python app.py

Or explicitly:

.env\Scripts\python.exe app.py

Expected:

* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000

Keep this terminal open.

8. Test Flask

If the project contains the test route:

GET /test

Open:

http://127.0.0.1:5000/test

Expected:

{
  "message": "Prompt route is working"
}

A 404 at / is normal if no / route has been defined.

9. API 1 — Single Prompt

Endpoint

POST /api/prompt

URL:

http://127.0.0.1:5000/api/prompt

Header:

Content-Type: application/json

Request:

{
  "userInput": "How much should I score in each subject to pass CA final?"
}

Processing Flow

Client
  ↓
Validate userInput
  ↓
Fetch Education_Prompt from MongoDB
  ↓
Replace {{userInput}}
  ↓
Call OpenAI
  ↓
Save request/response to history
  ↓
Return JSON

Expected response:

{
  "response": "..."
}

10. Test Single Prompt with PowerShell

Keep Flask running in one terminal.

Open a second terminal:

Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/prompt" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"userInput":"Explain what a REST API is in simple terms."}'

11. Test Single Prompt with Postman

Create:

POST http://127.0.0.1:5000/api/prompt

Select:

Body
→ raw
→ JSON

Use:

{
  "userInput": "Explain what a REST API is in simple terms."
}

Click Send.

12. API 2 — Batch Prompt Processing

Endpoint

POST /api/prompts/batch

URL:

http://127.0.0.1:5000/api/prompts/batch

Request:

{
  "userInputs": [
    "Explain REST API.",
    "What is normalization in databases?",
    "What is the difference between HTML and CSS?"
  ]
}

Expected response:

{
  "responses": [
    "Answer to question 1...",
    "Answer to question 2...",
    "Answer to question 3..."
  ]
}

The response order must match the input order.

13. Batch Concurrency

The batch endpoint should not process requests like:

Question 1 → wait → Question 2 → wait → Question 3

Instead, the AI calls should run concurrently:

             ┌── OpenAI request 1
             ├── OpenAI request 2
Batch ───────┼── OpenAI request 3
             └── OpenAI request N

A ThreadPoolExecutor can be used for concurrent I/O-bound OpenAI calls.

For example:

with ThreadPoolExecutor(max_workers=min(5, len(user_inputs))) as executor:
    responses = list(executor.map(process_one, user_inputs))

executor.map() preserves the order of the input iterable, so:

input[0] → response[0]
input[1] → response[1]
input[2] → response[2]

even if the underlying calls finish in a different order.

14. API Validation

Missing input

Request:

{}

Response:

{
  "error": "userInput is required"
}

Use HTTP status:

400 Bad Request

Invalid batch input

Request:

{
  "userInputs": "hello"
}

Response:

{
  "error": "userInputs must be a list"
}

15. Common Errors

ModuleNotFoundError: No module named 'openai'

Run:

.env\Scripts\python.exe -m pip install openai

localhost:27017 connection refused

The application is trying to use a local MongoDB server.

When using Atlas, MONGO_URI must start with:

mongodb+srv://

not:

mongodb://localhost:27017

Check:

MONGO_URI=mongodb+srv://...

MONGO_DB_NAME is None

Make sure .env contains:

MONGO_DB_NAME=flask_ai_db

and that .env is in the project root.

Restart Flask after changing .env.

Education_Prompt not found

Check:

Database: flask_ai_db
Collection: prompts
Document _id: Education_Prompt

404 Not Found

Check the method and URL.

GET  /test
POST /api/prompt
POST /api/prompts/batch

Opening a POST endpoint in a browser sends GET, so use Postman, Thunder Client, or PowerShell.

16. Security

Never hard-code:

MongoDB password

MongoDB URI containing credentials

OpenAI API key

Use:

MONGO_URI=...
OPENAI_API_KEY=...

And ensure:

.env

is ignored by Git.

If a secret is accidentally committed, rotate/revoke it.

17. Git Setup

Initialize:

git init

Check:

git status

Make sure .env is not listed.

Then:

git add .
git commit -m "Initial Flask AI Prompt API"