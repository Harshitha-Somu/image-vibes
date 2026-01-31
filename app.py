import os
from flask import Flask, render_template, request, session, redirect, url_for,flash
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Load the BLIP captioning model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


# Route for homepage
@app.route("/")
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template("index.html", username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)








# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# Route for handling image upload and caption/music generation
@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]
    if file.filename == "":
        return "No selected file", 400

    if file:
        filename = file.filename
        filepath = os.path.join("static/uploads", filename)

        # Save uploaded image
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)

        # Generate caption
        caption = generate_caption(filepath)

        # Detect mood
        mood = detect_mood(caption)

        # Recommend music
        songs = get_music(mood)

        return render_template("result.html", caption=caption, image_path=filepath, mood=mood, songs=songs)


# Generate caption using BLIP
def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


# Simple mood detection
def detect_mood(caption):
    caption = caption.lower()
    if "happy" in caption or "smile" in caption:
        return "Happy"
    elif "sad" in caption or "lonely" in caption:
        return "Sad"
    elif "sunset" in caption or "love" in caption:
        return "Romantic"
    elif "party" in caption or "dance" in caption:
        return "Energetic"
    else:
        return "Calm"


# Music recommendation based on mood
def get_music(mood):
    music_library = {
        "Happy": ["Happy - Pharrell Williams", "Best Day of My Life - American Authors"],
        "Sad": ["Someone Like You - Adele", "Fix You - Coldplay"],
        "Romantic": ["Perfect - Ed Sheeran", "All of Me - John Legend"],
        "Energetic": ["Can't Stop - Red Hot Chili Peppers", "Titanium - David Guetta ft. Sia"],
        "Calm": ["Weightless - Marconi Union", "Bloom - ODESZA"]
    }
    return music_library.get(mood, ["Let It Be - The Beatles"])




'''@app.route('/register', methods=['POST'])
def register():
    # Get form data
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Example validation
    if password != confirm_password:
        return "Passwords do not match"  # Replace with flash and return template in real app

    # Save user logic here...

    session['username'] = username  # Log user in
    return redirect(url_for('index'))'''

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "Passwords do not match"
            return render_template('login.html', error=error, show_register=True)

        hashed_password = generate_password_hash(password)

        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            username=username,
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('index'))

        except IntegrityError:
            db.session.rollback()
            error = "Email or username already registered"

    return render_template('login.html', error=error, show_register=True)







@app.route('/profile')
def profile():
    return render_template('profile.html')

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
