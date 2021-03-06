from revenues import db
from sqlalchemy import func


class User(db.Model):
    __tablename__ = 'USER'
    openid = db.Column(db.String(28), primary_key=True, nullable=False, comment='用户表主键值，用于索引，字串由微信生成，对于同一小程序，不同微信用户的openid不相同')
    registration_date = db.Column(db.DateTime, default=func.now(), nullable=False, comment='用户账户申请日期,新用户申请账户时生成')
    role = db.Column(db.Integer, nullable=False, server_default='0', comment='用户类型, 0=志愿者, 1=视障人士,新用户申请账户时设定')
    name = db.Column(db.String(100), default='志愿者', comment='用户姓名,用户申请账户时输入，可更新')
    real_name = db.Column(db.String(100), comment='用户真实姓名,用户申请证书时输入，可更新')
    id_type = db.Column(db.String(100), default='身份证', comment='证件类型：身份证；护照；驾驶证等,用户申请证书时输入，可更新')
    idcard = db.Column(db.String(18), unique=True, comment='用户18位身份证号,用户申请账户时输入，可选')
    idcard_verified = db.Column(db.Integer, server_default='0', comment='身份证号验证标识位，0=未验证，1=已验证,待引用')
    disabled_id = db.Column(db.String(60), unique=True, comment='视障人士残疾人证号,视障人士申请账户时输入')
    disabled_id_verified = db.Column(db.Integer, server_default='0', comment='残疾人证号验证标识位，0=未验证，1=已验证,待引用')
    phone = db.Column(db.String(16), nullable=False, unique=True, comment='用户联系电话,用户申请账户时输入，可更新')
    phone_verified = db.Column(db.Integer, server_default='0', nullable=False, comment='联系电话验证标识位，0=未验证，1=已验证,用户申请账户时需先认证联系电话')
    email = db.Column(db.String(32), unique=True, comment='用户邮箱')
    email_verified = db.Column(db.Integer, server_default='0', comment='用户邮箱验证标识位，0=未验证，1=已验')
    contact = db.Column(db.String(16), comment='用户备用联系电话,用户申请账户时输入，可选，可更新')
    gender = db.Column(db.String(1), nullable=False, server_default='无', comment='用户性别，"男"或者"女",用户申请账户时输入，可更新')
    birth = db.Column(db.DateTime, nullable=False, comment='用户生日,用户申请账户时输入，可更新')
    address = db.Column(db.String(80), server_default='无', comment='用户联系地址,用户申请账户时输入，可更新')
    emergent_contact = db.Column(db.String(8), comment='视障人士紧急联系人姓名,视障人士申请账户时输入，可更新')
    emergent_contact_phone = db.Column(db.String(16), comment='视障人士紧急联系人联系电话,视障人士申请账户时输入，可更新')
    activities_joined = db.Column(db.Integer, server_default='0', nullable=False, comment='微信端显示活动参加次数，以及根据次数计算参加时长,待定')
    remark = db.Column(db.String(255), server_default='无', comment='用户备注,用户申请账户时输入')
    audit_status = db.Column(db.Integer, server_default='0', nullable=False, comment='用户注册申请的审核状态,0=进行中, 1=已通过, -1=被拒绝,2=导入数据,管理员审核注册用户时更新')
    push_status = db.Column(db.Integer, server_default='0', nullable=False, comment='???')
    recipient_name = db.Column(db.String(100), comment='证书收件人姓名,用户申请证书时输入，可更新')
    recipient_address = db.Column(db.String(80), comment='证书收件人地址,用户申请账户时输入，可更新')
    recipient_phone = db.Column(db.String(16), comment='证书收件人电话,用户申请账户时输入，可更新')
    avatar_url = db.Column(db.String(300), nullable=False, comment='用户微信头像地址链接')
