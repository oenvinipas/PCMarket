import os
from dotenv import load_dotenv
from flask import Flask, abort, request, redirect, render_template, session
from models import db, User, Computer, Posts, Comments
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.secret_key = os.getenv("DB_SECRET_KEY", "potato")

db.init_app(app)
bcrypt = Bcrypt()
bcrypt.init_app(app)

# db = {
#     "PC 1": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
#     "PC 2": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
#     "PC 3": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
#     "PC 4": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
#     "PC 5": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
#     "PC 6": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
#     "PC 7": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
#     "PC 8": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
#     "PC 9": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
# }


@app.context_processor
def inject_data():
    session_first_name = session.get('first_name', "Guest")
    return {"session_first_name": session_first_name}


@app.get("/")
def get_all_listings_page():
    #Add the logic to create card view of each computer that was posted (Home Page)
    Computa = Computer.query.all()
    return render_template("index.html", Computa = Computa)


@app.get("/create")
def get_create_listing_page():
    return render_template("create.html")


@app.get("/login")
def get_account_login_page():
    if "email" in session:
        return redirect("/account")
    return render_template("login.html")


@app.post("/login")
def process_login_request():
    raw_password = request.form.get("password")
    email = request.form.get("email")
    if not raw_password or not email:
        abort(401)

    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        abort(401)

    if not bcrypt.check_password_hash(existing_user.password, raw_password):
        abort(401)
    
    # first_name = existing_user.first_name

    session["email"] = email
    session["first_name"] = existing_user.first_name
    return redirect("/account")


@app.get("/signup")
def get_account_signup_page():
    if "email" in session:
        return redirect("/account")
    return render_template("signup.html")


@app.post("/signup")
def process_signup_request():
    raw_password = request.form.get("password")
    raw_re_password = request.form.get("re-password")
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    if raw_password != raw_re_password or not email or not raw_password or not first_name:
        abort(400)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        abort(400)

    hashed_password = bcrypt.generate_password_hash(raw_password, 12).decode()
    new_user = User(email, hashed_password, first_name)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/login")


# TODO: Integrate with database
@app.get("/view/<int:listing_id>")
def get_view_of_listing(listing_id: int):
    # pc_name = f"PC {listing_id}"
    # if pc_name not in db:
    #     abort(404)

    # pc_specs = db[pc_name]
    # pc_image = pc_specs[-1]  # image URL is the last element in the list
    # return render_template("iso-view.html", pc_name=pc_name, pc_specs=pc_specs, pc_image=pc_image)
    return render_template("iso-view.html")


@app.get("/edit/<int:listing_id>")
def get_edit_page(listing_id: int):
    # use listing_id to index through the dictionary "db" to get the PC Title then pass that instead of the listing_id
    return render_template("edit.html", listing_id=listing_id)


@app.get("/account")
def get_account_page():
    if "email" not in session:
        abort(401)
    return render_template("account.html")


@app.post("/logout")
def logout():
    del session["email"]
    del session["first_name"]
    return redirect("/")
