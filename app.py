import os, requests
from dotenv import load_dotenv
from flask import Flask, abort, request, redirect, render_template, session, flash
from models import db, User, Computer, Posts, Comments
from flask_bcrypt import Bcrypt
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

app.secret_key = os.getenv("DB_SECRET_KEY", "potato")
app.permanent_session_lifetime = timedelta(minutes=30)
imgBBapi_key = os.getenv("imgBB_api_key")

db.init_app(app)
bcrypt = Bcrypt()
bcrypt.init_app(app)

@app.context_processor
def inject_data():
    session_first_name = session.get("first_name", "Guest")
    session_user_id = session.get("user_id", 0)
    return {
        "session_first_name": session_first_name,
        "session_user_id": session_user_id,
    }


@app.get("/")
def get_all_listings_page():
    # Add the logic to create card view of each computer that was posted (Home Page)
    Computa = Computer.query.all()
    return render_template("index.html", Computa=Computa)


@app.get("/create")
def get_create_listing_page():
    return render_template("create.html")

@app.post("/create")
def process_create_listing():
    if "image" not in request.files:
        flash("No image provided", "error")
        abort(400)

    file = request.files["image"]

    if file.filename == "":
        flash("No selected file", "error")
        abort(400)

    imgbb_url = "https://api.imgbb.com/1/upload"
    files = {"image": (file.filename, file.read())}
    params = {"key": imgBBapi_key}

    response = requests.post(imgbb_url, files=files, params=params)

    if response.status_code == 200:
        image_url = response.json()["data"]["url"]

        # Get other form data
        description = request.form.get("description")
        name = request.form.get("name")
        price = request.form.get("price")
        case = request.form.get("computer_case")
        motherboard = request.form.get("motherboard")
        cpu = request.form.get("cpu")
        gpu = request.form.get("gpu")
        ram = request.form.get("ram")
        memory = request.form.get("memory")
        fans = request.form.get("fans")
        power_supply = request.form.get("power_supply")
        condition = request.form.get("condition")
        rgb = request.form.get("rgb") == "True"

        new_computer = Computer(
            name,
            description,
            image_url,
            price,
            case,
            motherboard,
            cpu,
            gpu,
            ram,
            memory,
            fans,
            power_supply,
            condition,
            rgb,
        )

        db.session.add(new_computer)
        db.session.commit()
        new_post = Posts(session["user_id"], new_computer.computer_id)
        db.session.add(new_post)
        db.session.commit()

        return redirect("/")
    else:
        error_message = response.text
        flash(f"Image upload failed: {error_message}", "error")
        # return render_template("error.html", error=error_message)
        return redirect("/create")

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
        return redirect("/login")

    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        return redirect("/login")

    if not bcrypt.check_password_hash(existing_user.password, raw_password):
        return redirect("/login")
    # first_name = existing_user.first_name

    session["email"] = email
    session["first_name"] = existing_user.first_name
    session["user_id"] = existing_user.user_id
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
    if (
        raw_password != raw_re_password
        or not email
        or not raw_password
        or not first_name
    ):
        abort(400)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        abort(400)

    hashed_password = bcrypt.generate_password_hash(raw_password, 12).decode()
    new_user = User(email, hashed_password, first_name)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/login")


@app.get("/view/<int:listing_id>")
def get_view_of_listing(listing_id: int):
    # post_id and computer_id (listing_id in this case) need to be the same number or else post is None
    post = Posts.query.get_or_404(listing_id)
    listing_computer_id = post.computer_id
    Computa = Computer.query.filter_by(computer_id=listing_computer_id).first()
    return render_template(
        "iso-view.html",
        Computa=Computa,
        post=post,
    )


@app.get("/edit/<int:listing_id>")
def get_edit_page(listing_id: int):
    # post_id and computer_id (listing_id in this case) need to be the same number or else post is None
    post = Posts.query.get_or_404(listing_id)
    if "user_id" not in session or session["user_id"] != post.user_id:
        abort(401)

    computa = Computer.query.filter_by(computer_id=listing_id).first()
    return render_template(
        "edit.html",
        listing_id=listing_id,
        current_price=computa.price,
        current_case=computa.case,
        current_motherboard=computa.motherboard,
        current_cpu=computa.cpu,
        current_gpu=computa.gpu,
        current_ram=computa.ram,
        current_memory=computa.memory,
        current_fans=computa.fans,
        current_power_supply=computa.power_supply,
        current_condition=computa.condition,
        current_rgb=computa.rgb,
        current_description=computa.description,
    )


@app.post("/edit/<int:listing_id>")
def update_listing(listing_id: int):
    # post_id and computer_id (listing_id in this case) need to be the same number or else post is None
    post = Posts.query.get_or_404(listing_id)
    if "user_id" not in session or session["user_id"] != post.user_id:
        abort(401)

    computa = Computer.query.filter_by(computer_id=listing_id).first()

    updated_price = request.form.get("price")
    updated_case = request.form.get("computer_case")
    updated_motherboard = request.form.get("motherboard")
    updated_cpu = request.form.get("cpu")
    updated_gpu = request.form.get("gpu")
    updated_ram = request.form.get("ram")
    updated_memory = request.form.get("memory")
    updated_fans = request.form.get("fans")
    updated_power_supply = request.form.get("power_supply")
    updated_condition = request.form.get("condition")
    updated_rgb = request.form.get("rgb") == "True"
    updated_description = request.form.get("description")

    computa.price = updated_price
    computa.case = updated_case
    computa.motherboard = updated_motherboard
    computa.cpu = updated_cpu
    computa.gpu = updated_gpu
    computa.ram = updated_ram
    computa.memory = updated_memory
    computa.fans = updated_fans
    computa.power_supply = updated_power_supply
    computa.condition = updated_condition
    computa.rgb = updated_rgb
    computa.description = updated_description

    db.session.commit()

    return redirect(f"/view/{listing_id}")


@app.get("/account")
def get_account_page(): 
    if session.get('first_name') == None:
        return redirect('/login')
    else:
        return render_template("account.html")


@app.post("/logout")
def logout():
    del session["email"]
    del session["first_name"]
    del session["user_id"]
    return redirect("/")

@app.post("/delete/<int:listing_id>")
def delete_listing(listing_id: int):
    post = Posts.query.get_or_404(listing_id)
    if "user_id" not in session or session["user_id"] != post.user_id:
        abort(401)

    computa = Computer.query.filter_by(computer_id=listing_id).first()

    db.session.delete(post)
    db.session.delete(computa)
    db.session.commit()
    return redirect("/")
  
@app.post("/create-comment/<int:listing_id>")
def create_comment(listing_id):
    comment = request.form.get('comment')
    user_id = session['user_id']

    new_comment = Comments(user_id=user_id, post_id=listing_id, comment=comment)
    
    db.session.add(new_comment)
    db.session.commit()
    return redirect(f"/view/{listing_id}")
