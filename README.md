# ✦ AI Content Creation System

> An industry-oriented Generative AI web application that produces high-quality content using advanced prompt engineering and OpenAI GPT-3.5-Turbo.

---

## 📌 Project Overview

The **AI Content Creation System** is a full-stack web application built with **Python Flask** and the **OpenAI API**. Users can generate five types of professional content — blog posts, social media posts, marketing emails, product descriptions, and advertisement copy — by simply selecting parameters and clicking a button. All generated content is saved to a **SQLite** database and can be searched, previewed, and downloaded.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 5 Content Types | Blog Post, Social Media, Marketing Email, Product Description, Advertisement |
| 5 Tones | Professional, Friendly, Casual, Marketing, Educational |
| 3 Lengths | Short (~200 w), Medium (~500 w), Long (~1000 w) |
| Prompt Engineering | Separate, structured prompt templates per content type |
| Content History | SQLite + SQLAlchemy ORM, with search and delete |
| Export | Download any content as a `.txt` file |
| Demo Mode | Works without an API key (shows placeholder output) |
| Responsive UI | Mobile-friendly dark-themed interface |

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (custom properties, CSS Grid), Vanilla JavaScript (Fetch API)
- **Backend**: Python 3.10+, Flask 3.x, Flask Blueprints
- **AI**: OpenAI Python SDK (GPT-3.5-Turbo)
- **Database**: SQLite via SQLAlchemy ORM
- **Environment**: python-dotenv

---

## 📁 Folder Structure

```
AI_Content_Creation_System/
├── app.py                        # App factory & entry point
├── requirements.txt
├── .env.example                  # Environment variable template
├── README.md
├── database.db                   # Auto-created on first run
├── static/
│   ├── css/style.css
│   └── js/script.js
├── templates/
│   ├── layout.html               # Base template
│   ├── index.html                # Generator page
│   └── history.html              # History page
├── models/
│   └── content_model.py          # SQLAlchemy ORM model
├── prompts/
│   └── prompt_templates.py       # Prompt engineering module
├── routes/
│   └── content_routes.py         # Flask Blueprint (all routes)
└── docs/
    ├── Project_Report.md
    └── Installation_Guide.md
```

---

## ⚙️ Quick Start

```bash
# 1. Clone / unzip the project
cd AI_Content_Creation_System

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Open .env and add your OPENAI_API_KEY

# 5. Run the application
python app.py
# Open http://127.0.0.1:5000
```

---

## 🔑 Adding Your OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new secret key
3. Open the `.env` file and replace the placeholder:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

4. Restart the Flask server — real AI content will now be generated.

---

## 📸 Screenshots

| Page | Description |
|---|---|
| `/` Generator | Dark-themed form with content type dropdown, topic/audience inputs, tone selector, and length radio cards |
| Output Panel | Generated content displayed with copy and download actions |
| `/history` | Card grid of all past generations with search, expand, download, and delete |

---

## 🧑‍💻 Author

**T. Lokeshwari**  
B.E. Computer Science & Engineering (AI/ML Specialisation)  
Agni College of Technology, Chennai  
Team Innoventors
