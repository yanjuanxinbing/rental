from extensions import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    visit_date = db.Column(db.DateTime)                  # 预约看房时间
    start_date = db.Column(db.DateTime)                  # 租期开始
    end_date = db.Column(db.DateTime)                    # 租期结束
    status = db.Column(db.Integer, default=0)
    # 0=待确认 1=已确认(看房) 2=租约生效 3=已取消 4=已完成
    message = db.Column(db.Text)                         # 租客留言
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def status_text(self):
        return {
            0: '待确认', 1: '已确认', 2: '租约生效', 3: '已取消', 4: '已完成'
        }.get(self.status, '未知')

    def __repr__(self):
        return f'<Order {self.id}>'
