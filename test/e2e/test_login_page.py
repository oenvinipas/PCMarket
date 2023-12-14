from models import User
from app import db, bcrypt


def test_get_login_page(test_app):
    response = test_app.get("/login")
    data = response.data.decode("utf-8")

    assert response.status_code == 200


def test_get_account_page_after_login(test_app):
    hashed_password = bcrypt.generate_password_hash("12345").decode("utf-8")
    user = User("quandale@gmail.com", hashed_password, "Quandale", "Dingle")
    db.session.add(user)
    db.session.commit()

    response = test_app.post(
        "/login",
        data={"email": "quandale@gmail.com", "password": "12345"},
        follow_redirects=True,
    )
    data = response.data.decode()

    assert response.status_code == 200
    assert "Quandale" in data
    assert "Welcome to PCMarket!" in data

    user_to_delete = User.query.filter_by(first_name="Quandale").first()
    db.session.delete(user_to_delete)
    db.session.commit()


def test_login_functionality(test_app):
    hashed_password = bcrypt.generate_password_hash("12345").decode("utf-8")
    user = User("quandale2@gmail.com", hashed_password, "Quandale2", "Dingle")
    db.session.add(user)
    db.session.commit()

    response = test_app.post(
        "/login",
        data={"email": "quandale2@gmail.com", "password": "12345"},
        follow_redirects=False,
    )
    data = response.data.decode()

    assert response.status_code == 302

    user_to_delete = User.query.filter_by(first_name="Quandale2").first()
    db.session.delete(user_to_delete)
    db.session.commit()
    
