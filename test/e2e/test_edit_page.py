# from app import db, app
# from models import User, Computer, Posts
# from flask import session

# def test_get_edit_page(test_app):
#     user = User("test@gmail.com", "password", "Test", "Last")
#     db.session.add(user)
#     db.session.commit()

#     computer = Computer("Test Computer", "Description", "image_url", "1000", "Case", "Motherboard", "CPU", "GPU", "8GB", "512GB", "Fans", "Power Supply", "New", False)
#     db.session.add(computer)
#     db.session.commit()

#     with test_app as client:
#         with client.session_transaction() as sess:
#             sess["email"] = "test@gmail.com"
#             sess["first_name"] = "Test"
#             sess["user_id"] = user.user_id

#         response = client.get(f"/edit/{computer.computer_id}")
#         data = response.data.decode("utf-8")

#         assert response.status_code == 200
#         assert "Edit Computer Details" in data
#         assert computer.name in data
#         assert computer.cpu in data
#         assert computer.gpu in data

#     user_to_delete = User.query.filter_by(email="test@gmail.com").first()
#     db.session.delete(user_to_delete)
#     db.session.commit()

# def test_update_listing(test_app):
#     user = User("test@gmail1.com", "password", "Test", "Last")
#     db.session.add(user)
#     db.session.commit()

#     computer = Computer("Test Computer", "Description", "image_url", "1000", "Case", "Motherboard", "CPU", "GPU", "8GB", "512GB", "Fans", "Power Supply", "New", False)
#     db.session.add(computer)
#     db.session.commit()

#     with test_app as client:
#         with client.session_transaction() as sess:
#             sess["email"] = "test@gmail1.com"
#             sess["first_name"] = "Test"
#             sess["user_id"] = user.user_id

#         new_price = "1200"
#         response = client.post(f"/edit/{computer.computer_id}", data={"price": new_price})
#         updated_computer = Computer.query.filter_by(computer_id=computer.computer_id).first()

#         assert response.status_code == 302
#         assert updated_computer.price == new_price
        
#     user_to_delete = User.query.filter_by(email="test@gmail1.com").first()
#     db.session.delete(user_to_delete)
#     db.session.commit()
