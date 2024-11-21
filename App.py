from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import requests
import os

# Flask app setup
app = Flask(__name__)# Add this to a .env file for security
bcrypt = Bcrypt(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///users.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Hugging Face Endpoint
HF_ENDPOINT = os.getenv("HF_ENDPOINT", "https://b3xeyjvju03lme3x.us-east-1.aws.endpoints.huggingface.cloud")
API_KEY = os.getenv("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", "hf_dummy_key")  # Replace with your actual API key

# Default generation parameters
BASE_PARAMS = {
    'do_sample': True,
    'top_k': 50,
    'top_p': 0.95,
    'temperature': 0.8,
    'repetition_penalty': 1.1,
    'no_repeat_ngram_size': 4,
    'num_beams': 2,
    'early_stopping': True,
    'length_penalty': 1.2,
    'bad_words_ids': None,
    'min_length': 10,
    'use_cache': True,
}

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Decorator for login-required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route("/")
def home():
    """Home page."""
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Successfully logged in!", "success")
            return redirect(url_for("homechat"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration page."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("register"))

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account successfully created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    """Logout and clear session."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    """User dashboard."""
    return render_template("dashboard.html")

@app.route("/generate", methods=["POST"])
@login_required
def generate():
    """
    Interact with the Hugging Face model.
    Expects a JSON payload with 'input_text' and optional 'params'.
    """
    try:
        # Get input from request
        data = request.get_json()
        input_text = data.get("input_text", "").strip()
        custom_params = data.get("params", {})

        if not input_text:
            return jsonify({"error": "Input text cannot be empty."}), 400

        # Merge default and custom parameters
        generation_params = {**BASE_PARAMS, **custom_params, "inputs": input_text}

        # Make a request to the Hugging Face endpoint
        response = requests.post(
            HF_ENDPOINT,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=generation_params,
        )
        
        # Handle Hugging Face response
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("generated_text", "")
            return jsonify({"input": input_text, "output": generated_text})
        else:
            return jsonify({"error": "Error from Hugging Face API", "details": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
