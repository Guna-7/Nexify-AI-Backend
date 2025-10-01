

## 🐍 **Backend (Django) – `README.md`**

````text
# AI Chat App Backend – Django + DRF + GROQ

This is the backend of a Fullstack AI Chat Application built with Django, Django REST Framework, and integrated with OpenAI's GPT-4 model. It provides a RESTful API for managing chat messages and communicating with the GPT-4 API.

## ⚙️ Tech Stack
- Python 3.x
- Django
- Django REST Framework
- Groq

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-chat-backend.git
cd ai-chat-backend
````

### 2. Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your OpenAI API Key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_openai_api_key_here
```

You can also use `python-decouple` or Django settings directly to manage your API key.

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start the Server

```bash
python manage.py runserver
```
