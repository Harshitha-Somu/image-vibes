
# 🎵🖼️ Image Vibes

**Image Vibes** is an AI-powered web app that generates creative captions for images and recommends music based on the mood detected in faces. It combines advanced computer vision and emotion recognition models with music APIs to create an engaging multimedia experience.

---

## 🚀 Features

- 📤 Upload any image
- 📝 Generate smart captions using **BLIP-2**
- 😊 Detect emotion using **Keywords in generated caption**
- 🎶 Recommend music using **Last.fm API**
- 🔐 Environment variables for API security
- 🧪 Includes test scripts for key modules

---

## 🧠 Technologies Used

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python (Flask)
- **AI Models:** 
  - [BLIP-2](https://huggingface.co/Salesforce/blip2) (image captioning)
- **Music API:** [Last.fm API](https://www.last.fm/api)
- **Database:** SQLite


---

## ⚙️ Getting Started

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/Harshitha-Somu/image-vibes.git
cd image-vibes
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add `.env` File

Create a `.env` file in the root directory and add:

```
OPENAI_API_KEY=your_openai_key
LASTFM_API_KEY=your_lastfm_key
```

> ⚠️ Make sure `.env` is listed in `.gitignore`

### 5️⃣ Run the App

```bash
python app.py
```

Open your browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📂 Project Structure

```
image-vibes/
├── static/               # CSS, images, etc.
├── templates/            # HTML files
├── utils/                # Caption & mood detection logic
├── app.py                # Main Flask app
├── firebase_config.py    # Firebase integration
├── requirements.txt      # Dependencies
├── your_database.db      # SQLite database
├── .env                  # API keys (ignored in Git)
└── .gitignore            # Git ignored files
```

---

## 🧪 Tests

Run test scripts to verify image captioning and face detection:

```bash
python test_caption_imports.py
python test_deepface.py
```

---

## 👩‍💻 Developed By

**Harshitha Somu**  
🔗 [GitHub](https://github.com/Harshitha-Somu) • 💼 [LinkedIn](https://www.linkedin.com/in/harshitha-somu-2a2843317?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

---

## 📃 License

This project is open-sourced under the [MIT License](LICENSE).
