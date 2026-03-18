from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.house import House
from models.order import Order

house_bp = Blueprint('house', __name__)


@house_bp.route('/list')
def list_houses():
    page = request.args.get('page', 1, type=int)
    city = request.args.get('city', '')
    district = request.args.get('district', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 99999, type=float)
    house_type = request.args.get('house_type', '')

    query = House.query.filter_by(status=1)
    if city:
        query = query.filter_by(city=city)
    if district:
        query = query.filter_by(district=district)
    if house_type:
        query = query.filter_by(house_type=house_type)
    query = query.filter(House.price >= min_price, House.price <= max_price)

    pagination = query.order_by(House.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('house/list.html', pagination=pagination, houses=pagination.items)


@house_bp.route('/<int:house_id>')
def detail(house_id):
    house = House.query.get_or_404(house_id)
    return render_template('house/detail.html', house=house)


@house_bp.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    if not current_user.is_landlord():
        flash('只有房东才能发布房源', 'warning')
        return redirect(url_for('index'))
    if request.method == 'POST':
        house = House(
            title=request.form.get('title'),
            description=request.form.get('description'),
            price=float(request.form.get('price', 0)),
            area=float(request.form.get('area', 0)),
            rooms=int(request.form.get('rooms', 1)),
            halls=int(request.form.get('halls', 1)),
            bathrooms=int(request.form.get('bathrooms', 1)),
            address=request.form.get('address'),
            city=request.form.get('city'),
            district=request.form.get('district'),
            house_type=request.form.get('house_type'),
            tags=request.form.get('tags'),
            floor=request.form.get('floor', type=int),
            total_floor=request.form.get('total_floor', type=int),
            landlord_id=current_user.id,
            status=0  # 待审核
        )
        db.session.add(house)
        db.session.commit()
        flash('房源已提交，等待审核', 'success')
        return redirect(url_for('user.my_houses'))
    return render_template('house/publish.html')


@house_bp.route('/<int:house_id>/book', methods=['POST'])
@login_required
def book(house_id):
    house = House.query.get_or_404(house_id)
    if house.status != 1:
        flash('该房源当前不可预约', 'warning')
        return redirect(url_for('house.detail', house_id=house_id))

    order = Order(
        house_id=house_id,
        tenant_id=current_user.id,
        visit_date=request.form.get('visit_date'),
        message=request.form.get('message')
    )
    db.session.add(order)
    db.session.commit()
    flash('预约成功！等待房东确认', 'success')
    return redirect(url_for('user.orders'))
