**Project Structure**

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


*Responsibilities*
app.py — creates Flask app and registers routes.
database/mongodb.py — creates MongoDB connection and exposes collections.
routes/prompt_routes.py — contains API endpoints and request validation.
services/prompt_service.py — fetches prompt templates.
services/openai_service.py — communicates with OpenAI.
.env — stores secrets/configuration.
requirements.txt — Python dependencies.    


1. Prerequisites:-
    Install or create:
    Python 3.10+
    MongoDB Atlas account
    OpenAI API key
    Git (optional)
    Postman or Thunder Client (optional)
    MongoDB does not need to be installed locally. This project uses MongoDB Atlas.
   
3. MongoDB Atlas Setup:-
    Create a Cluster
    Create a free MongoDB Atlas cluster, for example:
    Cluster0
    Create a Database User
    Example:
       Username: aishwarychaurasia9_db_user
       Password: <KdEJxI*********>
       Get Connection String
       Go to:
       Cluster
       → Connect
       → Drivers
       → Python

        The URI will look similar to: mongodb+srv://aishwarychaurasia9_db_user:<password>@cluster0.xxxxx.mongodb.net/?appName=Cluster0

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
Input:
Explain REST API.

Final prompt:
You are an expert in education domain. Answer the following: Explain REST API.

history Collection
Every request/response pair is stored.


4. Environment Variables:-
        Create .env in the project root:
        MONGO_URI=mongodb+srv://aishwarychaurasia9_db_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?appName=Cluster0
        MONGO_DB_NAME=flask_ai_db
        OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        OPENAI_MODEL=YOUR_MODEL_NAME

5. Create Virtual Environment:-
        From the project directory:
        python -m venv venv
        Activate it: .env\Scripts\Activate.ps1

6. Install Dependencies:-
        python -m pip install flask pymongo python-dotenv openai
        Or:
        python -m pip install -r requirements.txt

7. Run the Application:-
        Make sure the virtual environment is active.
        python app.py
        Or explicitly:
        .env\Scripts\python.exe app.py

            Expected:
            * Serving Flask app 'app'
            * Debug mode: on
            * Running on http://127.0.0.1:5000

            Keep this terminal open.

8. Test Flask:-
        If the project contains the test route:
        GET /test
        Open: http://127.0.0.1:5000/test

9. API 1 — Single Prompt:-

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

