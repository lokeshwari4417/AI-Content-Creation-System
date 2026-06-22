# Installation Guide — AI Content Creation System

## System Requirements

| Requirement | Version |
|---|---|
| Python | 3.10 or higher |
| pip | Latest |
| Internet | Required (for OpenAI API) |
| OS | Windows 10+, macOS 12+, Ubuntu 20.04+ |

---

## Step-by-Step Installation

### Step 1 — Download the Project

Unzip `AI_Content_Creation_System.zip` to a folder of your choice, or clone from GitHub:

```bash
git clone https://github.com/yourusername/ai-content-creation-system.git
cd AI_Content_Creation_System
```

### Step 2 — Create a Virtual Environment

A virtual environment keeps project dependencies isolated from your global Python installation.

```bash
# Create the environment
python -m venv venv

# Activate on Windows (Command Prompt)
venv\Scripts\activate

# Activate on Windows (PowerShell)
venv\Scripts\Activate.ps1

# Activate on macOS / Linux
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal when it's active.

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `flask` — web framework
- `flask-sqlalchemy` — ORM for SQLite
- `openai` — OpenAI Python client
- `python-dotenv` — `.env` file loader
- `sqlalchemy` — database engine

### Step 4 — Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env        # macOS/Linux
copy .env.example .env      # Windows
```

Open `.env` in any text editor and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
SECRET_KEY=any-random-string-you-choose
```

> **Note:** The application runs in Demo Mode if `OPENAI_API_KEY` is missing or still set to the placeholder value.

### Step 5 — Run the Application

```bash
python app.py
```

Expected output:
```
✅ Database tables created successfully.
🚀 AI Content Creation System is running...
📍 Visit: http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

Open your browser and go to: **http://127.0.0.1:5000**

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Make sure the virtual environment is activated and `pip install -r requirements.txt` was run |
| `Port 5000 already in use` | Change the port in `app.py`: `app.run(port=5001)` |
| `OpenAI API error` | Check that your API key is correct and has available credits |
| `database.db` not created | Ensure you have write permissions in the project directory |
| Browser shows old styles | Hard-refresh with `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac) |

---

## Resetting the Database

To clear all history and start fresh:

```bash
# Delete the database file
rm database.db          # macOS/Linux
del database.db         # Windows

# Restart the app — it will recreate the table automatically
python app.py
```

---

## Production Deployment Notes

For deploying to a server (e.g., AWS EC2, Render, Railway):

1. Set `debug=False` in `app.py`
2. Use `gunicorn` instead of the Flask development server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
   ```
3. Set environment variables on the server instead of using a `.env` file
4. Use a reverse proxy (Nginx) in front of gunicorn for HTTPS
