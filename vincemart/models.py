from vincemart import db
from vincemart import bcrypt
from vincemart import login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    budget = db.Column(db.Float)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def get_id(self):
        return (self.user_id)
    
class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_image = db.Column(db.String(255), nullable=False)
    image1 = db.Column(db.String(100), nullable=False)
    image2 = db.Column(db.String(100), nullable=False)
    image3 = db.Column(db.String(100), nullable=False)
    image4 = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.now)
    brand = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('Users', backref='products')

class Specifications(db.Model):
    spec_id = db.Column(db.Integer, primary_key=True)
    announced = db.Column(db.Text)
    status = db.Column(db.Text)
    dimensions = db.Column(db.Text)
    weight = db.Column(db.Text)
    build = db.Column(db.Text)
    SIM = db.Column(db.Text)
    type = db.Column(db.Text)
    size = db.Column(db.Text)
    resolution = db.Column(db.Text)
    protection = db.Column(db.Text)
    OS = db.Column(db.Text)
    chipset = db.Column(db.Text)
    CPU = db.Column(db.Text)
    GPU = db.Column(db.Text)
    card_slot = db.Column(db.Text)
    internal = db.Column(db.Text)
    main_camera_type = db.Column(db.Text)
    main_camera_features = db.Column(db.Text)
    main_camera_video = db.Column(db.Text)
    selfie_camera_type = db.Column(db.Text)
    selfie_camera_features = db.Column(db.Text)
    selfie_camera_video = db.Column(db.Text)
    loudspeaker = db.Column(db.Text)
    _3_5mm_jack = db.Column(db.Text)
    WLAN = db.Column(db.Text)
    bluetooth = db.Column(db.Text)
    positioning = db.Column(db.Text)
    NFC = db.Column(db.Text)
    radio = db.Column(db.Text)
    USB = db.Column(db.Text)
    sensors = db.Column(db.Text)
    battery_type = db.Column(db.Text)
    charging = db.Column(db.Text)
    colors = db.Column(db.Text)
    models = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    product = db.relationship('Products', backref='specifications')
