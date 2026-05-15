from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

# ─── 颜色系统 ───────────────────────────────────────────
C_NAVY    = RGBColor(0x1E, 0x3A, 0x5F)   # 深蓝（主色）
C_BLUE    = RGBColor(0x25, 0x63, 0xEB)   # 蓝色（强调）
C_LIGHT   = RGBColor(0xEF, 0xF6, 0xFF)   # 浅蓝底
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
C_GRAY    = RGBColor(0x64, 0x74, 0x8B)
C_LGRAY   = RGBColor(0xF1, 0xF5, 0xF9)
C_ACCENT  = RGBColor(0x06, 0xB6, 0xD4)   # 青色点缀
C_RED     = RGBColor(0xEF, 0x44, 0x44)
C_GREEN   = RGBColor(0x10, 0xB9, 0x81)

blank = prs.slide_layouts[6]  # 完全空白

def add_rect(slide, l, t, w, h, fill=None, line=None, line_w=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
        if line_w:
            shape.line.width = Pt(line_w)
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, l, t, w, h, size=18, bold=False, color=C_NAVY,
             align=PP_ALIGN.LEFT, italic=False, wrap=True):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    box.text_frame.word_wrap = wrap
    p = box.text_frame.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = "Microsoft YaHei"
    return box

def add_para(tf, text, size=14, bold=False, color=C_NAVY, align=PP_ALIGN.LEFT,
             space_before=0, indent=0):
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.level = indent
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Microsoft YaHei"
    return p

def clear_para(tf):
    """清空文本框第一个默认段落"""
    p = tf.paragraphs[0]
    p.runs[0].text = "" if p.runs else ""

def multi_text(slide, l, t, w, h, lines):
    """lines = [(text, size, bold, color, align, space_before)]"""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    box.text_frame.word_wrap = True
    first = True
    for item in lines:
        text, size, bold, color, align, sp = item
        if first:
            p = box.text_frame.paragraphs[0]
            first = False
        else:
            p = box.text_frame.add_paragraph()
        p.alignment = align
        p.space_before = Pt(sp)
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = "Microsoft YaHei"
    return box

def add_card(slide, l, t, w, h, title, body_lines, title_color=C_NAVY, bg=C_LGRAY):
    add_rect(slide, l, t, w, h, fill=bg)
    add_rect(slide, l, t, 0.04, h, fill=C_BLUE)
    add_text(slide, title, l+0.15, t+0.12, w-0.2, 0.35, size=13, bold=True, color=title_color)
    box = slide.shapes.add_textbox(Inches(l+0.15), Inches(t+0.5), Inches(w-0.2), Inches(h-0.6))
    box.text_frame.word_wrap = True
    first = True
    for line in body_lines:
        if first:
            p = box.text_frame.paragraphs[0]
            first = False
        else:
            p = box.text_frame.add_paragraph()
        p.space_before = Pt(2)
        run = p.add_run()
        run.text = line
        run.font.size = Pt(11)
        run.font.color.rgb = C_GRAY
        run.font.name = "Microsoft YaHei"


# ════════════════════════════════════════════════════════════════
# 第 1 页：封面
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)

# 深蓝背景
add_rect(s, 0, 0, 13.33, 7.5, fill=C_NAVY)
# 青色装饰条（左上角）
add_rect(s, 0, 0, 0.6, 7.5, fill=C_BLUE)
add_rect(s, 0.6, 0, 0.12, 7.5, fill=C_ACCENT)
# 右下装饰圆（用矩形代替）
add_rect(s, 9.5, 5.2, 4.5, 4.0, fill=RGBColor(0x15, 0x2C, 0x4E))

# 课程标签
add_text(s, "软件工程  课程设计汇报", 1.0, 1.2, 8, 0.5,
         size=14, color=C_ACCENT, bold=False)

# 主标题
multi_text(s, 1.0, 1.9, 11, 1.6, [
    ("智能房屋租赁系统", 44, True, C_WHITE, PP_ALIGN.LEFT, 0),
    ("Smart House Rental Platform", 18, False, RGBColor(0x93,0xC5,0xFD), PP_ALIGN.LEFT, 6),
])

# 分割线
add_rect(s, 1.0, 3.65, 5.5, 0.04, fill=C_BLUE)

# 副信息
multi_text(s, 1.0, 3.85, 9, 2.5, [
    ("基于 Flask + SQLAlchemy 构建的 B/S 架构多角色租房平台", 13, False, RGBColor(0xCB,0xD5,0xE1), PP_ALIGN.LEFT, 0),
    ("", 8, False, C_WHITE, PP_ALIGN.LEFT, 0),
    ("支持租客找房、房东发布、管理员审核全流程", 13, False, RGBColor(0xCB,0xD5,0xE1), PP_ALIGN.LEFT, 0),
])

# 页码
add_text(s, "01", 12.4, 6.9, 0.8, 0.4, size=11, color=RGBColor(0x47,0x6A,0x9A))


# ════════════════════════════════════════════════════════════════
# 第 2 页：项目背景与目标
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_WHITE)
add_rect(s, 0, 0, 13.33, 1.15, fill=C_NAVY)
add_rect(s, 0, 1.15, 13.33, 0.06, fill=C_BLUE)

add_text(s, "项目背景与目标", 0.5, 0.28, 8, 0.65, size=24, bold=True, color=C_WHITE)
add_text(s, "Background & Objectives", 0.5, 0.75, 8, 0.35, size=11, color=RGBColor(0x93,0xC5,0xFD))
add_text(s, "02", 12.4, 6.9, 0.8, 0.4, size=11, color=C_GRAY)

# 背景文字
add_text(s, "随着城镇化进程加快，房屋租赁需求持续增长，传统中介模式存在信息不透明、流程繁琐等痛点。"
         "本项目旨在构建一套线上租赁平台，实现房源信息化管理与多角色协同工作流。",
         0.5, 1.45, 12.3, 0.8, size=13, color=C_GRAY)

# 三个目标卡片
goals = [
    ("找房便捷", C_BLUE, ["租客可按城市、类型、价格", "关键词多维度搜索房源", "在线预约看房一键完成"]),
    ("房源管理", C_GREEN, ["房东自主发布、管理房源", "实时查看预约申请", "支持下架与重新上架"]),
    ("平台监管", RGBColor(0xF5,0x9E,0x0B), ["管理员审核房源信息", "查看全部房源与订单", "强制下架违规内容"]),
]
for i, (title, color, items) in enumerate(goals):
    x = 0.5 + i * 4.27
    add_rect(s, x, 2.45, 4.0, 4.6, fill=C_LGRAY)
    add_rect(s, x, 2.45, 4.0, 0.06, fill=color)
    add_text(s, title, x+0.2, 2.6, 3.6, 0.45, size=16, bold=True, color=color)
    box = s.shapes.add_textbox(Inches(x+0.2), Inches(3.2), Inches(3.6), Inches(3.6))
    box.text_frame.word_wrap = True
    first = True
    for item in items:
        p = box.text_frame.paragraphs[0] if first else box.text_frame.add_paragraph()
        first = False
        p.space_before = Pt(4)
        r = p.add_run()
        r.text = "•  " + item
        r.font.size = Pt(12)
        r.font.color.rgb = C_GRAY
        r.font.name = "Microsoft YaHei"


# ════════════════════════════════════════════════════════════════
# 第 3 页：需求分析（用例）
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_WHITE)
add_rect(s, 0, 0, 13.33, 1.15, fill=C_NAVY)
add_rect(s, 0, 1.15, 13.33, 0.06, fill=C_BLUE)

add_text(s, "需求分析", 0.5, 0.28, 8, 0.65, size=24, bold=True, color=C_WHITE)
add_text(s, "Requirements Analysis — User Roles & Use Cases", 0.5, 0.75, 10, 0.35, size=11, color=RGBColor(0x93,0xC5,0xFD))
add_text(s, "03", 12.4, 6.9, 0.8, 0.4, size=11, color=C_GRAY)

roles = [
    ("租  客", C_BLUE, [
        "注册 / 登录账号",
        "浏览 / 搜索房源",
        "查看房源详情",
        "提交看房预约",
        "管理个人预约记录",
        "取消预约申请",
    ]),
    ("房  东", C_GREEN, [
        "注册房东账号",
        "发布 / 编辑房源",
        "上传房源封面图",
        "查看收到的预约",
        "确认 / 拒绝预约",
        "下架 / 重新上架",
    ]),
    ("管理员", RGBColor(0xF5,0x9E,0x0B), [
        "查看平台统计数据",
        "审核待上架房源",
        "通过 / 拒绝审核",
        "查看全部房源列表",
        "强制下架违规房源",
        "管理所有订单信息",
    ]),
]
for i, (role, color, funcs) in enumerate(roles):
    x = 0.45 + i * 4.27
    # 角色标题条
    add_rect(s, x, 1.4, 4.0, 0.55, fill=color)
    add_text(s, role, x, 1.43, 4.0, 0.5, size=16, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    # 功能列表
    for j, fn in enumerate(funcs):
        y = 2.08 + j * 0.77
        add_rect(s, x, y, 4.0, 0.65, fill=C_LGRAY if j % 2 == 0 else C_WHITE)
        add_rect(s, x, y, 0.04, 0.65, fill=color)
        add_text(s, fn, x+0.15, y+0.12, 3.8, 0.45, size=12, color=C_NAVY)


# ════════════════════════════════════════════════════════════════
# 第 4 页：系统架构
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_WHITE)
add_rect(s, 0, 0, 13.33, 1.15, fill=C_NAVY)
add_rect(s, 0, 1.15, 13.33, 0.06, fill=C_BLUE)

add_text(s, "系统架构设计", 0.5, 0.28, 8, 0.65, size=24, bold=True, color=C_WHITE)
add_text(s, "System Architecture — MVC + Blueprint", 0.5, 0.75, 10, 0.35, size=11, color=RGBColor(0x93,0xC5,0xFD))
add_text(s, "04", 12.4, 6.9, 0.8, 0.4, size=11, color=C_GRAY)

# 左侧：架构分层图
layers = [
    ("表现层 Presentation", C_BLUE,    "Jinja2 模板 + Bootstrap 5 + Bootstrap Icons"),
    ("控制层 Controller",   C_ACCENT,   "Flask Blueprint（auth / house / user / admin）"),
    ("服务层 Service",      C_GREEN,    "业务逻辑 · 图片处理（Pillow）· 权限校验"),
    ("数据层 Data",         RGBColor(0xF5,0x9E,0x0B), "SQLAlchemy ORM + Flask-Migrate + PostgreSQL"),
]
for i, (name, color, desc) in enumerate(layers):
    y = 1.5 + i * 1.3
    add_rect(s, 0.4, y, 7.0, 1.1, fill=color)
    add_text(s, name, 0.55, y+0.1, 6.8, 0.45, size=13, bold=True, color=C_WHITE)
    add_text(s, desc, 0.55, y+0.55, 6.8, 0.45, size=11, color=RGBColor(0xE0,0xF2,0xFE))
    if i < len(layers) - 1:
        add_text(s, "▼", 3.6, y+1.05, 0.8, 0.25, size=10, color=C_GRAY, align=PP_ALIGN.CENTER)

# 右侧：目录结构
add_rect(s, 7.8, 1.4, 5.1, 5.7, fill=C_LGRAY)
add_rect(s, 7.8, 1.4, 5.1, 0.42, fill=C_NAVY)
add_text(s, "项目目录结构", 7.9, 1.43, 5.0, 0.38, size=12, bold=True, color=C_WHITE)

tree = [
    ("app.py             应用入口 & 工厂函数", 0),
    ("extensions.py      db / login / migrate", 0),
    ("requirements.txt   依赖清单", 0),
    ("models/", 0),
    ("  user.py   house.py   order.py", 1),
    ("routes/", 0),
    ("  auth.py   house.py", 1),
    ("  user.py   admin.py", 1),
    ("templates/         Jinja2 模板", 0),
    ("static/img/uploads 上传图片", 0),
]
box = s.shapes.add_textbox(Inches(7.95), Inches(1.95), Inches(4.8), Inches(5.0))
box.text_frame.word_wrap = False
first = True
for line, lvl in tree:
    p = box.text_frame.paragraphs[0] if first else box.text_frame.add_paragraph()
    first = False
    p.space_before = Pt(3)
    r = p.add_run()
    r.text = ("  " if lvl else "") + line
    r.font.size = Pt(10.5)
    r.font.color.rgb = C_NAVY if lvl == 0 else C_GRAY
    r.font.name = "Consolas"


# ════════════════════════════════════════════════════════════════
# 第 5 页：数据库设计
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_WHITE)
add_rect(s, 0, 0, 13.33, 1.15, fill=C_NAVY)
add_rect(s, 0, 1.15, 13.33, 0.06, fill=C_BLUE)

add_text(s, "数据库设计", 0.5, 0.28, 8, 0.65, size=24, bold=True, color=C_WHITE)
add_text(s, "Database Design — 3 Core Entities & Relationships", 0.5, 0.75, 10, 0.35, size=11, color=RGBColor(0x93,0xC5,0xFD))
add_text(s, "05", 12.4, 6.9, 0.8, 0.4, size=11, color=C_GRAY)

tables = [
    ("users（用户表）", C_BLUE, [
        "id            主键",
        "username      用户名（唯一）",
        "email         邮箱（唯一）",
        "password_hash 哈希密码",
        "phone         联系电话",
        "role          角色 0租客/1房东/2管理员",
        "created_at    注册时间",
    ]),
    ("houses（房源表）", C_GREEN, [
        "id            主键",
        "title         标题",
        "price         月租金",
        "area          面积㎡",
        "rooms/halls/bathrooms  户型",
        "city / district / address 位置",
        "house_type    整租/合租",
        "cover_img     封面图片",
        "status        0审核中/1上架/3下架",
        "landlord_id   → users.id",
    ]),
    ("orders（预约表）", RGBColor(0xF5,0x9E,0x0B), [
        "id            主键",
        "house_id      → houses.id",
        "tenant_id     → users.id",
        "visit_date    看房时间",
        "message       租客留言",
        "status        0待确认/1已确认/3已取消",
        "created_at    提交时间",
    ]),
]
for i, (title, color, fields) in enumerate(tables):
    x = 0.35 + i * 4.35
    add_rect(s, x, 1.4, 4.1, 0.5, fill=color)
    add_text(s, title, x+0.1, 1.42, 3.9, 0.45, size=13, bold=True, color=C_WHITE)
    for j, f in enumerate(fields):
        yy = 1.9 + j * 0.54
        add_rect(s, x, yy, 4.1, 0.5, fill=C_LGRAY if j % 2 == 0 else C_WHITE)
        add_text(s, f, x+0.15, yy+0.08, 3.9, 0.38, size=10, color=C_NAVY)

# 关系说明
add_rect(s, 0.35, 7.0, 12.6, 0.35, fill=C_LIGHT)
add_text(s, "关系：users(1) ─── houses(N)   ·   users(1) ─── orders(N)   ·   houses(1) ─── orders(N)",
         0.5, 7.03, 12.4, 0.3, size=11, color=C_BLUE, align=PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# 第 6 页：核心功能展示
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_WHITE)
add_rect(s, 0, 0, 13.33, 1.15, fill=C_NAVY)
add_rect(s, 0, 1.15, 13.33, 0.06, fill=C_BLUE)

add_text(s, "核心功能展示", 0.5, 0.28, 8, 0.65, size=24, bold=True, color=C_WHITE)
add_text(s, "Core Features — End-to-End Rental Workflow", 0.5, 0.75, 10, 0.35, size=11, color=RGBColor(0x93,0xC5,0xFD))
add_text(s, "06", 12.4, 6.9, 0.8, 0.4, size=11, color=C_GRAY)

features = [
    ("房源浏览与搜索", C_BLUE, [
        "首页展示最新 8 套上架房源",
        "按城市快捷筛选入口",
        "关键词搜索（标题/城市/标签）",
        "侧边栏多维度过滤（类型/价格）",
    ]),
    ("房源发布审核", C_GREEN, [
        "房东填写完整房源信息",
        "上传封面图（自动 letterbox 处理）",
        "提交后进入审核队列",
        "管理员一键通过或拒绝",
    ]),
    ("预约看房流程", C_ACCENT, [
        "租客选择意向日期时间",
        "填写看房留言（可选）",
        "房东收到通知并确认 / 拒绝",
        "租客可随时取消待确认预约",
    ]),
    ("房东房源管理", RGBColor(0xF5,0x9E,0x0B), [
        "查看全部自有房源与状态",
        "已上架房源可一键下架",
        "下架后可重新提交审核",
        "待确认预约集中展示处理",
    ]),
    ("管理员后台", RGBColor(0x8B,0x5C,0xF6), [
        "统计面板：用户/房源/订单数",
        "Tab 分类：待审核/已上架/全部",
        "已上架房源可强制下架",
        "一键通过 / 拒绝待审核房源",
    ]),
    ("账号权限体系", C_NAVY, [
        "注册时选择租客或房东身份",
        "管理员账号后台预置，不开放注册",
        "登录后动态显示对应功能菜单",
        "越权操作返回错误提示",
    ]),
]
for i, (title, color, items) in enumerate(features):
    col = i % 3
    row = i // 3
    x = 0.4 + col * 4.27
    y = 1.45 + row * 2.85
    add_rect(s, x, y, 4.1, 2.6, fill=C_LGRAY)
    add_rect(s, x, y, 4.1, 0.06, fill=color)
    add_text(s, title, x+0.15, y+0.12, 3.8, 0.38, size=13, bold=True, color=color)
    box = s.shapes.add_textbox(Inches(x+0.15), Inches(y+0.55), Inches(3.8), Inches(1.9))
    box.text_frame.word_wrap = True
    first = True
    for item in items:
        p = box.text_frame.paragraphs[0] if first else box.text_frame.add_paragraph()
        first = False
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = "  " + item
        r.font.size = Pt(11)
        r.font.color.rgb = C_GRAY
        r.font.name = "Microsoft YaHei"


# ════════════════════════════════════════════════════════════════
# 第 7 页：技术栈与关键实现
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_WHITE)
add_rect(s, 0, 0, 13.33, 1.15, fill=C_NAVY)
add_rect(s, 0, 1.15, 13.33, 0.06, fill=C_BLUE)

add_text(s, "技术栈与关键实现", 0.5, 0.28, 8, 0.65, size=24, bold=True, color=C_WHITE)
add_text(s, "Tech Stack & Key Implementation Details", 0.5, 0.75, 10, 0.35, size=11, color=RGBColor(0x93,0xC5,0xFD))
add_text(s, "07", 12.4, 6.9, 0.8, 0.4, size=11, color=C_GRAY)

# 左：技术栈表格
techs = [
    ("后端框架", "Flask 3.x",           "轻量级 Python Web 框架，Blueprint 模块化"),
    ("ORM",    "SQLAlchemy 3.x",       "声明式数据模型，支持 SQLite / PostgreSQL"),
    ("迁移",   "Flask-Migrate",        "基于 Alembic，数据库版本管理"),
    ("认证",   "Flask-Login",          "会话管理、登录保护、角色权限装饰器"),
    ("图片",   "Pillow",               "封面图 letterbox 处理，统一 800×400"),
    ("前端",   "Bootstrap 5 + Jinja2", "响应式布局，服务端渲染模板"),
    ("部署",   "Gunicorn + PostgreSQL","生产 WSGI 服务器，云数据库"),
]
add_rect(s, 0.4, 1.4, 7.8, 0.42, fill=C_NAVY)
add_text(s, "技术分类", 0.55, 1.43, 2.0, 0.36, size=11, bold=True, color=C_WHITE)
add_text(s, "技术选型", 2.45, 1.43, 2.5, 0.36, size=11, bold=True, color=C_WHITE)
add_text(s, "说明", 4.95, 1.43, 3.3, 0.36, size=11, bold=True, color=C_WHITE)
for i, (cat, tech, note) in enumerate(techs):
    y = 1.82 + i * 0.67
    bg = C_LGRAY if i % 2 == 0 else C_WHITE
    add_rect(s, 0.4, y, 7.8, 0.65, fill=bg)
    add_text(s, cat,  0.55, y+0.12, 1.8, 0.42, size=11, color=C_GRAY)
    add_text(s, tech, 2.45, y+0.12, 2.4, 0.42, size=11, bold=True, color=C_BLUE)
    add_text(s, note, 4.95, y+0.12, 3.2, 0.42, size=10, color=C_GRAY)

# 右：关键实现要点
add_rect(s, 8.5, 1.4, 4.4, 5.7, fill=C_LIGHT)
add_rect(s, 8.5, 1.4, 4.4, 0.42, fill=C_BLUE)
add_text(s, "关键实现要点", 8.62, 1.43, 4.2, 0.36, size=12, bold=True, color=C_WHITE)

points = [
    ("应用工厂模式", "create_app() + Blueprint 注册，便于扩展和测试"),
    ("图片 Letterbox", "Pillow 等比缩放后居中裁白边，统一显示规格"),
    ("角色权限装饰器", "@login_required + is_admin()/is_landlord() 多级控制"),
    ("安全输入处理", "注册 role 上限=1，数字字段安全转换防 500 错误"),
    ("演示数据种子", "seed.py 一键初始化三种角色 + 8 套样本房源"),
]
for i, (pt, desc) in enumerate(points):
    y = 1.95 + i * 1.0
    add_rect(s, 8.55, y, 0.3, 0.3, fill=C_BLUE)
    add_text(s, pt,   8.95, y-0.02, 3.8, 0.36, size=12, bold=True, color=C_NAVY)
    add_text(s, desc, 8.95, y+0.32, 3.8, 0.5,  size=10, color=C_GRAY)


# ════════════════════════════════════════════════════════════════
# 第 8 页：演示账号与测试流程
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_WHITE)
add_rect(s, 0, 0, 13.33, 1.15, fill=C_NAVY)
add_rect(s, 0, 1.15, 13.33, 0.06, fill=C_BLUE)

add_text(s, "演示账号与测试流程", 0.5, 0.28, 9, 0.65, size=24, bold=True, color=C_WHITE)
add_text(s, "Demo Accounts & Test Workflow", 0.5, 0.75, 10, 0.35, size=11, color=RGBColor(0x93,0xC5,0xFD))
add_text(s, "08", 12.4, 6.9, 0.8, 0.4, size=11, color=C_GRAY)

# 演示账号
accounts = [
    ("管理员", "admin", "admin123", C_RED,   "审核房源 / 查看统计 / 强制下架"),
    ("房东",   "landlord", "demo123", C_GREEN, "管理房源 / 确认预约 / 下架上架"),
    ("租客",   "tenant",   "demo123", C_BLUE,  "浏览搜索 / 预约看房 / 管理预约"),
]
add_rect(s, 0.4, 1.45, 12.5, 0.42, fill=C_NAVY)
for i, label in enumerate(["角色", "用户名", "密码", "主要操作"]):
    xs = [0.55, 2.0, 3.9, 5.8]
    add_text(s, label, xs[i], 1.48, 2.0, 0.36, size=12, bold=True, color=C_WHITE)

for i, (role, user, pwd, color, ops) in enumerate(accounts):
    y = 1.87 + i * 0.68
    add_rect(s, 0.4, y, 12.5, 0.65, fill=C_LGRAY if i % 2 == 0 else C_WHITE)
    add_rect(s, 0.4, y, 0.04, 0.65, fill=color)
    add_text(s, role, 0.55, y+0.14, 1.4, 0.38, size=13, bold=True, color=color)
    add_text(s, user, 2.0,  y+0.14, 1.8, 0.38, size=12, color=C_NAVY)
    add_text(s, pwd,  3.9,  y+0.14, 1.8, 0.38, size=12, color=C_NAVY)
    add_text(s, ops,  5.8,  y+0.14, 7.0, 0.38, size=11, color=C_GRAY)

# 测试流程
add_text(s, "推荐演示流程", 0.5, 4.3, 5, 0.4, size=14, bold=True, color=C_NAVY)
steps = [
    ("Step 1", "游客身份浏览首页 → 按城市快捷筛选 → 关键词搜索房源 → 查看房源详情",      C_BLUE),
    ("Step 2", "租客登录 → 进入房源详情 → 填写预约时间和留言 → 提交预约",              C_GREEN),
    ("Step 3", "房东登录 → 个人中心 → 我的房源 → 查看待确认预约 → 点击确认",           RGBColor(0xF5,0x9E,0x0B)),
    ("Step 4", "管理员登录 → 管理后台 → 统计面板 → 审核新提交房源 → 通过 / 拒绝",      C_RED),
]
for i, (step, desc, color) in enumerate(steps):
    y = 4.82 + i * 0.62
    add_rect(s, 0.4, y, 1.1, 0.52, fill=color)
    add_text(s, step, 0.4, y+0.09, 1.1, 0.38, size=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(s, desc, 1.65, y+0.1, 11.1, 0.38, size=11, color=C_GRAY)
    if i < len(steps)-1:
        add_text(s, "▼", 0.82, y+0.5, 0.3, 0.25, size=9, color=C_GRAY, align=PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# 第 9 页：总结与展望
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
add_rect(s, 0, 0, 13.33, 7.5, fill=C_NAVY)
add_rect(s, 0, 0, 0.6, 7.5, fill=C_BLUE)
add_rect(s, 0.6, 0, 0.12, 7.5, fill=C_ACCENT)

add_text(s, "09", 12.4, 6.9, 0.8, 0.4, size=11, color=RGBColor(0x47,0x6A,0x9A))

multi_text(s, 1.0, 0.6, 11, 0.9, [
    ("总结与展望", 32, True, C_WHITE, PP_ALIGN.LEFT, 0),
    ("Summary & Future Work", 14, False, RGBColor(0x93,0xC5,0xFD), PP_ALIGN.LEFT, 4),
])
add_rect(s, 1.0, 1.6, 5.0, 0.04, fill=C_BLUE)

# 已完成
add_rect(s, 1.0, 1.8, 5.2, 5.3, fill=RGBColor(0x15,0x2C,0x4E))
add_rect(s, 1.0, 1.8, 5.2, 0.45, fill=C_GREEN)
add_text(s, "已完成功能", 1.1, 1.83, 5.0, 0.38, size=13, bold=True, color=C_WHITE)
done = [
    "多角色注册登录与权限体系",
    "房源发布 / 审核 / 上下架完整流程",
    "关键词 + 多维度房源搜索",
    "在线预约看房全流程",
    "管理员后台统计与房源管控",
    "演示数据一键初始化",
    "生产级 Gunicorn 部署配置",
]
box = s.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.0), Inches(4.5))
box.text_frame.word_wrap = True
first = True
for item in done:
    p = box.text_frame.paragraphs[0] if first else box.text_frame.add_paragraph()
    first = False
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "✓  " + item
    r.font.size = Pt(12)
    r.font.color.rgb = C_GREEN
    r.font.name = "Microsoft YaHei"

# 未来展望
add_rect(s, 6.6, 1.8, 5.9, 5.3, fill=RGBColor(0x15,0x2C,0x4E))
add_rect(s, 6.6, 1.8, 5.9, 0.45, fill=C_ACCENT)
add_text(s, "未来展望", 6.7, 1.83, 5.7, 0.38, size=13, bold=True, color=C_WHITE)
todo = [
    "在线签约与电子合同模块",
    "支付宝 / 微信支付集成",
    "地图选址与周边配套展示",
    "即时通讯（租客与房东对话）",
    "房源评分与租客评价体系",
    "移动端响应式优化 / 小程序",
]
box2 = s.shapes.add_textbox(Inches(6.7), Inches(2.35), Inches(5.7), Inches(4.5))
box2.text_frame.word_wrap = True
first = True
for item in todo:
    p = box2.text_frame.paragraphs[0] if first else box2.text_frame.add_paragraph()
    first = False
    p.space_before = Pt(5)
    r = p.add_run()
    r.text = "→  " + item
    r.font.size = Pt(12)
    r.font.color.rgb = C_ACCENT
    r.font.name = "Microsoft YaHei"


# ────────────────────────────────────────────────────────────────
# 保存
# ────────────────────────────────────────────────────────────────
prs.save("智能房屋租赁系统_汇报PPT.pptx")
print("PPT 已生成：智能房屋租赁系统_汇报PPT.pptx")
