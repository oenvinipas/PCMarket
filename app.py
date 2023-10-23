from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.get("/")
def get_all_listings_page():
    return render_template('index.html')

@app.get('/create')
def get_create_listing_page():
    return render_template('create.html')

@app.get('/login')
def get_account_login_page():
    return render_template('login.html')

@app.get('/signup')
def get_account_signup_page():
    return render_template('signup.html')

@app.get('/view/<int:listing_id>')
def get_view_of_listing(listing_id: int):
    # use listing_id to index through the dictionary "db" to get the PC Title then pass that instead of the listing_id
    return render_template('iso-view.html', listing_id=listing_id)

@app.get('/edit/<int:listing_id>')
def get_edit_page(listing_id: int):
    # use listing_id to index through the dictionary "db" to get the PC Title then pass that instead of the listing_id
    return render_template('edit.html', listing_id=listing_id)

@app.get('/account')
def get_account_page():
    return render_template('account.html')