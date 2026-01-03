
from flask import Flask, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hospital_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# -------------------- Disease List (100+) --------------------
DISEASES = [
    "Diabetes","Hypertension","Asthma","Tuberculosis","Malaria","Dengue",
    "COVID-19","Influenza","Pneumonia","Bronchitis","Hepatitis A","Hepatitis B",
    "Hepatitis C","Typhoid","Cholera","Anemia","Migraine","Epilepsy",
    "Arthritis","Osteoporosis","Heart Disease","Stroke","Kidney Stones",
    "UTI","Gallstones","Peptic Ulcer","GERD","IBS","Crohn’s Disease",
    "Ulcerative Colitis","Eczema","Psoriasis","Acne","Conjunctivitis",
    "Cataract","Glaucoma","Sinusitis","Tonsillitis","Thyroid Disorder",
    "PCOS","Endometriosis","Depression","Anxiety","Bipolar Disorder",
    "Schizophrenia","ADHD","Autism","Alzheimer’s","Parkinson’s",
    "Leukemia","Lymphoma","Breast Cancer","Lung Cancer","Colon Cancer",
    "Cervical Cancer","Ovarian Cancer","Brain Tumor","HIV/AIDS","Rabies",
    "Tetanus","Measles","Mumps","Rubella","Chickenpox","Polio",
    "Leprosy","Sickle Cell Anemia","Thalassemia","Gout",
    "Rheumatoid Arthritis","Obesity","Sleep Apnea","Varicose Veins",
    "Hemorrhoids","Pancreatitis","Appendicitis","Hernia","Back Pain",
    "Sciatica","Frozen Shoulder","Carpal Tunnel Syndrome"
]

# -------------------- Database Model --------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # staff / doctor / patient

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# -------------------- Templates --------------------
login_page = """
<h2>Hospital Login</h2>
<form method="post">
  <input name="username" placeholder="Username" required><br><br>
  <input type="password" name="password" placeholder="Password" required><br><br>
  <button type="submit">Login</button>
</form>
<a href="/register">Register</a>
"""

register_page = """
<h2>Register</h2>
<form method="post">
  <input name="username" placeholder="Username" required><br><br>
  <input type="password" name="password" placeholder="Password" required><br><br>
  <select name="role">
    <option value="staff">Staff</option>
    <option value="doctor">Doctor</option>
    <option value="patient">Patient</option>
  </select><br><br>
  <button type="submit">Register</button>
</form>
<a href="/">Back to Login</a>
"""

dashboard_page = """
<h2>{{ role|capitalize }} Dashboard</h2>
<p>Welcome, {{ user }}</p>

<h3>Diseases ({{ diseases|length }})</h3>
<ul>
{% for d in diseases %}
  <li>{{ d }}</li>
{% endfor %}
</ul>

<a href="/logout">Logout</a>
"""

# -------------------- Routes --------------------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/dashboard")
    return render_template_string(login_page)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        hashed = generate_password_hash(request.form["password"])
        user = User(
            username=request.form["username"],
            password=hashed,
            role=request.form["role"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template_string(register_page)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template_string(
        dashboard_page,
        user=current_user.username,
        role=current_user.role,
        diseases=DISEASES
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# -------------------- Run --------------------
if __name__ == "__main__":
    app.run(debug=True)
