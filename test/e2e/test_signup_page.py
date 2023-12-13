from models import User
from app import db


def test_get_signup_page(test_app):
    response = test_app.get("/signup")
    data = response.data.decode("utf-8")

    assert response.status_code == 200


def test_get_login_page_after_signup(test_app):
    response = test_app.post(
        "/signup",
        data={
            "first_name": "McDonald",
            "email": "mcdonald@gmail.com",
            "password": "12345",
            "re-password": "12345",
        },
        follow_redirects=True,
    )
    data = response.data.decode()

    assert response.status_code == 200

    user_to_delete = User.query.filter_by(first_name="McDonald").first()
    db.session.delete(user_to_delete)
    db.session.commit()


def test_signup_functionality(test_app):
    response = test_app.post(
        "/signup",
        data={
            "first_name": "Mickey",
            "email": "mickey@gmail.com",
            "password": "12345",
            "re-password": "12345",
        },
        follow_redirects=False,
    )
    data = response.data.decode()

    assert response.status_code == 302

    user_to_delete = User.query.filter_by(first_name="Mickey").first()
    db.session.delete(user_to_delete)
    db.session.commit()