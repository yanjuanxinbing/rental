from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.house import House
from models.user import User
from models.order import Order

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('需要管理员权限', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_houses': House.query.count(),
        'pending_houses': House.query.filter_by(status=0).count(),
        'total_orders': Order.query.count(),
    }
    pending = House.query.filter_by(status=0).all()
    return render_template('admin/dashboard.html', stats=stats, pending=pending)


@admin_bp.route('/house/<int:house_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_house(house_id):
    house = House.query.get_or_404(house_id)
    house.status = 1
    db.session.commit()
    flash(f'《{house.title}》已通过审核', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/house/<int:house_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_house(house_id):
    house = House.query.get_or_404(house_id)
    house.status = 3
    db.session.commit()
    flash(f'《{house.title}》已拒绝', 'warning')
    return redirect(url_for('admin.dashboard'))
