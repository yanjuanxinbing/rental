"""
演示数据初始化脚本
运行: python seed.py
账号:
  管理员  admin    / admin123
  房东    landlord / demo123
  租客    tenant   / demo123
"""
from app import create_app
from extensions import db
from models.user import User
from models.house import House
from models.order import Order
from datetime import datetime

app = create_app()

HOUSES = [
    dict(
        title='朝阳区阳光里 精装两居 近地铁',
        description='南北通透，采光极佳。精装修，家电齐全，拎包入住。小区环境优美，距地铁6号线步行5分钟。\n\n房间配置：主卧带衣柜，次卧朝南，客厅宽敞明亮。厨房独立，配备冰箱、洗衣机、空调。',
        price=5800, area=78.0, rooms=2, halls=1, bathrooms=1,
        floor=8, total_floor=18, address='朝阳区阳光里小区8号楼',
        city='北京', district='朝阳区', house_type='整租',
        tags='近地铁,电梯房,精装修,拎包入住', status=1,
    ),
    dict(
        title='海淀区中关村 合租次卧 适合在校生',
        description='中关村核心区域，周边商业配套完善，超市、餐厅林立。合租三室，独立次卧，公用客厅、厨房。宽带100M，适合学生或上班族。',
        price=2200, area=15.0, rooms=1, halls=1, bathrooms=1,
        floor=3, total_floor=6, address='海淀区中关村南大街合租公寓',
        city='北京', district='海淀区', house_type='合租',
        tags='近高校,宽带,近商圈', status=1,
    ),
    dict(
        title='浦东新区陆家嘴 江景三居 豪华装修',
        description='坐拥黄浦江景，陆家嘴金融核心地带。三居室豪华装修，落地窗观江景，品质家具家电全配。地铁2号线直达，出行便捷。',
        price=18000, area=130.0, rooms=3, halls=2, bathrooms=2,
        floor=22, total_floor=35, address='浦东新区滨江大道888号',
        city='上海', district='浦东新区', house_type='整租',
        tags='江景房,豪华装修,近地铁,电梯房', status=1,
    ),
    dict(
        title='静安区南京西路 精品一居 交通便利',
        description='上海市中心黄金地段，南京西路商圈步行可达。一居室精装，适合单身白领。楼下地铁站直达全城，周边餐饮丰富。',
        price=6500, area=42.0, rooms=1, halls=1, bathrooms=1,
        floor=11, total_floor=24, address='静安区愚园路精品公寓',
        city='上海', district='静安区', house_type='整租',
        tags='市中心,精装修,近地铁', status=1,
    ),
    dict(
        title='天河区珠江新城 写字楼旁 两居室',
        description='珠江新城CBD核心，上班族首选。两室一厅精装修，南向采光好。小区有游泳池、健身房等配套设施，物业管理完善。',
        price=7200, area=88.0, rooms=2, halls=1, bathrooms=1,
        floor=15, total_floor=30, address='天河区华夏路珠江新城豪庭',
        city='广州', district='天河区', house_type='整租',
        tags='CBD核心,精装修,带健身房,电梯房', status=1,
    ),
    dict(
        title='福田区华强北 合租主卧 含水电',
        description='深圳华强北电子商圈，地铁1号线、7号线双地铁覆盖。合租主卧带独卫，房间宽敞，含水电网费。适合年轻创业者和上班族。',
        price=3500, area=20.0, rooms=1, halls=1, bathrooms=1,
        floor=6, total_floor=12, address='福田区华强北路创业公寓',
        city='深圳', district='福田区', house_type='合租',
        tags='双地铁,含水电,近商圈', status=1,
    ),
    dict(
        title='西湖区文一路 学区房 三室两厅',
        description='杭州热门学区房，紧邻文一路名校群。三室两厅精装，面积宽敞，适合家庭居住。小区绿化率高，环境安静，地铁3号线步行8分钟。',
        price=9500, area=115.0, rooms=3, halls=2, bathrooms=2,
        floor=5, total_floor=11, address='西湖区文一路花园小区',
        city='杭州', district='西湖区', house_type='整租',
        tags='学区房,近地铁,精装修,家庭适合', status=1,
    ),
    dict(
        title='锦江区春熙路 时尚一居 闹中取静',
        description='春熙路商圈旁，购物娱乐一步到位。精装一居室，现代风格装修，配备智能家居系统。小区有24小时安保，安全有保障。',
        price=4200, area=50.0, rooms=1, halls=1, bathrooms=1,
        floor=9, total_floor=20, address='锦江区红星路春熙公寓',
        city='成都', district='锦江区', house_type='整租',
        tags='近春熙路,智能家居,精装修', status=1,
    ),
]

with app.app_context():
    db.create_all()

    if User.query.filter_by(username='admin').first():
        print('演示数据已存在，跳过初始化。')
    else:
        admin = User(username='admin', email='admin@demo.com', role=2)
        admin.set_password('admin123')

        landlord = User(username='landlord', email='landlord@demo.com', role=1, phone='13800138000')
        landlord.set_password('demo123')

        tenant = User(username='tenant', email='tenant@demo.com', role=0, phone='13900139000')
        tenant.set_password('demo123')

        db.session.add_all([admin, landlord, tenant])
        db.session.flush()

        for h in HOUSES:
            house = House(landlord_id=landlord.id, **h)
            db.session.add(house)

        db.session.flush()

        first_house = House.query.filter_by(landlord_id=landlord.id).first()
        if first_house:
            order = Order(
                house_id=first_house.id,
                tenant_id=tenant.id,
                visit_date=datetime(2026, 5, 20, 14, 0),
                message='您好，我对这套房子很感兴趣，方便周二下午看房吗？',
                status=0,
            )
            db.session.add(order)

        db.session.commit()
        print('演示数据初始化完成！')
        print('  管理员：admin / admin123')
        print('  房东：  landlord / demo123')
        print('  租客：  tenant / demo123')
