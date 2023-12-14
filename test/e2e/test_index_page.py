from app import db
from models import Computer


def test_get_index_page(test_app):
    response = test_app.get("/")
    data = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "" in data


def test_get_index_page_with_listings(test_app):
    computers = Computer.query.all()    
    
    response = test_app.get("/")
    data = response.data.decode("utf-8")
    assert response.status_code == 200
    for computer in computers:
        assert computer.name in data
        assert computer.cpu in data
        assert computer.gpu in data
        assert computer.ram in data