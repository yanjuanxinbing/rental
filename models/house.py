from extensions import db
from datetime import datetime


class House(db.Model):
    __tablename__ = 'houses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)          # 月租金
    area = db.Column(db.Float)                           # 面积 m²
    rooms = db.Column(db.Integer, default=1)             # 室
    halls = db.Column(db.Integer, default=1)             # 厅
    bathrooms = db.Column(db.Integer, default=1)         # 卫
    floor = db.Column(db.Integer)
    total_floor = db.Column(db.Integer)
    address = db.Column(db.String(256))
    city = db.Column(db.String(64))
    district = db.Column(db.String(64))
    house_type = db.Column(db.String(32))                # 整租/合租
    cover_img = db.Column(db.String(256), default='default_house.jpg')
    status = db.Column(db.Integer, default=0)            # 0=审核中 1=上架 2=已租出 3=下架
    tags = db.Column(db.String(256))                     # 逗号分隔，如"近地铁,电梯房"
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = db.relationship('Order', backref='house', lazy='dynamic')

    def get_tags(self):
        return self.tags.split(',') if self.tags else []

    def status_text(self):
        return {0: '审核中', 1: '出租中', 2: '已租出', 3: '已下架'}.get(self.status, '未知')

    def __repr__(self):
        return f'<House {self.title}>'
