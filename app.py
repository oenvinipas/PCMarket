from flask import Flask, request, redirect, render_template

app = Flask(__name__)

db = {
    "PC 1": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
    "PC 2": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
    "PC 3": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
    "PC 4": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
    "PC 5": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
    "PC 6": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
    "PC 7": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
    "PC 8": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
    "PC 9": ["Ryzen 9 3900X", "GeForce RTX 4080", "32GB DDR4 3200mhz", "980 Pro 2TB Internal SSD PCIE Gen 4x4 MVME", "https://m.media-amazon.com/images/I/81X8UMFt+RL.jpg"],
}


@app.get("/")
def get_all_listings_page():
    return render_template("index.html", db=db)


@app.get("/create")
def get_create_listing_page():
    return render_template("create.html")


@app.get("/login")
def get_account_login_page():
    return render_template("login.html")


@app.get("/signup")
def get_account_signup_page():
    return render_template("signup.html")


@app.get("/view/<int:listing_id>")
def get_view_of_listing(listing_id: int):
    # use listing_id to index through the dictionary "db" to get the PC Title then pass that instead of the listing_id
    return render_template("iso-view.html", listing_id=listing_id)


@app.get("/edit/<int:listing_id>")
def get_edit_page(listing_id: int):
    # use listing_id to index through the dictionary "db" to get the PC Title then pass that instead of the listing_id
    return render_template("edit.html", listing_id=listing_id)


@app.get("/account")
def get_account_page():
    return render_template("account.html")
