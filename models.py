from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    
    def __init__(self, email: str, password: str, first_name: str) -> None:
        self.email = email
        self.password = password
        self.first_name = first_name
class Computer(db.Model):
    __tablename__ = "computer"
    
    computer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), default="computer")
    description = db.Column(db.String(255), default="-")
    price = db.Column(db.String(255), nullable=False)
    case = db.Column(db.String(255), default="-")
    motherboard = db.Column(db.String(255), default="-")
    cpu = db.Column(db.String(255), default="-")
    gpu = db.Column(db.String(255), default="-")
    ram = db.Column(db.String(255), default="-")
    memory = db.Column(db.String(255), default="-")
    fans = db.Column(db.String(255), default="-")
    power_supply = db.Column(db.String(255), default="-")
    condition = db.Column(db.String(255), default="-")
    rgb = db.Column(db.Boolean, default=False)

    def __init__(self, name: str, description: str, price: str, case: str, motherboard: str, cpu: str, gpu: str, ram: str, memory: str, fans: str, power_supply: str, condition: str, rgb: bool) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.case = case
        self.motherboard = motherboard
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.memory = memory
        self.fans = fans
        self.power_supply = power_supply
        self.condition = condition
        self.rgb = rgb
        
class Posts(db.Model):
    __tablename__ = "posts"
    
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    computer_id = db.Column(db.Integer, db.ForeignKey("computer.computer_id"), nullable=False)
    top_bidder = db.Column(db.Integer, db.ForeignKey("users.user_id")) 
    bid_count = db.Column(db.Integer, default=0)
    bid_days = db.Column(db.Integer, default=0)
    
    time_created = datetime.now()
    
    user = db.relationship("User", foreign_keys=[user_id], backref="user_posts", lazy=True)
    computer = db.relationship("Computer", backref="posts", lazy=True)
    bidder = db.relationship("User", foreign_keys=[top_bidder], backref="bid_posts", lazy=True)
    
    def __init__(self, user_id: int, computer_id: int, bid_days: int) -> None:
        self.user_id = user_id
        self.computer_id = computer_id
        self.bid_days = bid_days
        
class Comments(db.Model):
    __tablename__ = "comments"
    
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    
    post = db.relationship("Posts", backref="comments", lazy=True)
    user = db.relationship("User", backref="comments", lazy=True)
    
    def __init__(self, user_id: int, post_id: int, comment: str) -> None:
        self.user_id = user_id
        self.post_id = post_id
        self.comment = comment