---

## Backend README (ai_chatbot_api)

```markdown
# AI Chatbot Backend

This is the Django-based backend API for the AI Chatbot application. It provides endpoints for generating chatbot responses using OpenAI's API, and it stores conversation history in MongoDB. The backend also supports customizable chatbot tones and uses Django REST Framework and django-cors-headers for API management and CORS.

## Features

- **Chat API Endpoint:** Processes user messages, builds conversation context, and returns chatbot responses.
- **Custom Chatbot Tones:** Supports multiple tones (Angry, Depressed, Happy, Sarcastic, Random) that influence the chatbot’s personality.
- **Conversation Persistence:** Stores the conversation history in MongoDB using a composite key (`username_sessionid`) to uniquely identify each user session.
- **CORS Support:** Configured to allow cross-origin requests from your frontend.
- **Environment-Based Configuration:** Uses environment variables for sensitive settings (API keys, MongoDB URI, ALLOWED_HOSTS, etc.) via python-dotenv.

## Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- MongoDB database (e.g., [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))
- An OpenAI API key

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Niloy1010/ai_chatbot_api.git
   cd ai_chatbot_api
2. **Create and Activate a Virtual Environment:**

On Windows:

```bash
python -m venv env
.\env\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

3. **Environment Variables:**

Create a .env file in the project root with the following variables:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=mushroomchat-022417d141e7.herokuapp.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://mushroomchat.vercel.app
MONGO_URI=your-mongodb-uri
OPENAI_API_KEY=your-openai-api-key
```

Notes:
ALLOWED_HOSTS: List only hostnames/IP addresses (no protocol).
CORS_ALLOWED_ORIGINS: Must include the protocol (e.g., https://).
Replace the placeholders with your actual keys/URIs.

4. **Apply Migrations:**

```bash
python manage.py migrate
```

5. **Collect Static Files (if applicable):**

Ensure STATIC_ROOT is set in your settings.py (e.g., STATIC_ROOT = BASE_DIR / 'staticfiles') then run:

```bash
python manage.py collectstatic --noinput
```

6. **Run the Server Locally:**

```bash
python manage.py runserver
```

The API will be available at http://localhost:8000/api/chat/.
