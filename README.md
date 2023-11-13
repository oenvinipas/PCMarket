# PCMarket
This website is going to be built in Flask using Jinja, HTML, and Bootstrap. This is a website where users can auction or purchase PCs/parts.

## Getting Started

### Environment

To work with this code, you should create a virtual environment to work out of:

1) To create a virtual environment, simply run the below command in your terminal 

```
python -m venv [branch_name]
```

2) Once this has been completed, you need to activate your virtual environment:

- On Windows:

```
source venv/Scripts/Activate
```

- On macOS

```
source venv/bin/activate
```

3) After activating your environment, install the required dependencies by running the below command:

```
pip install -r requirements.txt
```

## Structure 

### templates

- Contains all of our HTML pages
    - `_template.html` - base template that every html page in our project is built off
        - Contains the navbar and footer
    - `index.html` - Home Screen
    - `account.html` - Account details page
    - `create.html` - Creating listing page
    - `edit.html` - Edit listing page
    - `iso-view.html` - Single Listing View / Isolation View
    - `login.html` - Login page
    - `signup.html` - Signup page 

### app.py

- All of our backend code

### static

- Contains static files we reference in code 
    - Logo