# 智能房屋租赁系统

基于 Flask 的房屋租赁平台，软件工程课程项目。

## 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库
python app.py   # 首次运行会自动 db.create_all()

# 3. 访问
# http://127.0.0.1:5000
```

## 项目结构

```
rental/
├── app.py              # 入口，create_app 工厂函数
├── extensions.py       # db / login_manager / migrate
├── requirements.txt
├── models/
│   ├── user.py         # 用户模型（租客/房东/管理员）
│   ├── house.py        # 房源模型
│   └── order.py        # 预约订单模型
├── routes/
│   ├── auth.py         # 注册 / 登录 / 退出
│   ├── house.py        # 房源列表 / 详情 / 发布 / 预约
│   ├── user.py         # 个人中心 / 我的预约 / 我的房源
│   └── admin.py        # 管理后台（审核房源）
├── templates/
│   ├── base.html       # 公共导航 + flash 消息
│   ├── index.html      # 首页
│   ├── auth/           # 登录 / 注册
│   ├── house/          # 列表 / 详情 / 发布
│   ├── user/           # 个人中心 / 预约 / 房源管理
│   └── admin/          # 管理后台
└── static/
    └── img/uploads/    # 房源图片上传目录
```

## 角色权限

| 角色 | 注册时选择 | 权限 |
|------|-----------|------|
| 租客 | role=0 | 浏览、搜索、预约看房 |
| 房东 | role=1 | 租客权限 + 发布房源、管理预约 |
| 管理员 | 手动设置 role=2 | 全部权限 + 审核房源 |

> 管理员账号需在数据库手动将 role 字段改为 2，或在 shell 中执行：
> ```python
> from app import create_app; from extensions import db; from models.user import User
> app = create_app()
> with app.app_context():
>     u = User.query.filter_by(username='你的用户名').first()
>     u.role = 2; db.session.commit()
> ```

## 主要功能

- 用户注册/登录（Flask-Login，bcrypt 密码哈希）
- 房源发布与审核流程（房东发布 → 管理员审核 → 上架）
- 多条件筛选搜索（城市/类型/价格区间）
- 分页展示
- 预约看房（租客预约 → 房东确认/拒绝）
- 管理后台（数据统计 + 房源审核）
