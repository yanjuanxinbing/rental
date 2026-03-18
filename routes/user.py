from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.house import House
from models.order import Order

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')


@user_bp.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(tenant_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('user/orders.html', orders=orders)


@user_bp.route('/my-houses')
@login_required
def my_houses():
    houses = House.query.filter_by(landlord_id=current_user.id).order_by(House.created_at.desc()).all()
    # 房东看自己发布的房子收到的预约
    incoming = []
    for h in houses:
        incoming += h.orders.filter_by(status=0).all()
    return render_template('user/my_houses.html', houses=houses, incoming=incoming)


@user_bp.route('/order/<int:order_id>/confirm', methods=['POST'])
@login_required
def confirm_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.house.landlord_id != current_user.id:
        flash('无权操作', 'danger')
        return redirect(url_for('user.my_houses'))
    order.status = 1
    db.session.commit()
    flash('已确认预约', 'success')
    return redirect(url_for('user.my_houses'))


@user_bp.route('/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.tenant_id != current_user.id and order.house.landlord_id != current_user.id:
        flash('无权操作', 'danger')
        return redirect(url_for('index'))
    order.status = 3
    db.session.commit()
    flash('已取消', 'info')
    return redirect(url_for('user.orders'))
