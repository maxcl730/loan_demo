# -*- coding: utf-8 -*-
import random
import string
import hashlib
from datetime import datetime
from database import db


class Member(db.Model):
    """Represents protected member."""
    __tablename__ = 'member'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    national_id = db.Column(db.String(20), nullable=False, default='', index=True)
    nickname = db.Column(db.String(50), nullable=False, default='')
    birthday = db.Column(db.String(20))
    mobile = db.Column(db.String(20), nullable=False, index=True)
    password = db.Column(db.String(50), nullable=False, default='')
    sex = db.Column(db.Integer, default=0)
    avatar = db.Column(db.String(200))
    salt = db.Column(db.String(32))
    reg_ip = db.Column(db.String(20))
    status = db.Column(db.Integer, nullable=False, default=0)
    blocked_info = db.Column(db.Text)
    language = db.Column(db.String(20))
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_time = db.Column(db.DateTime, default=datetime.now)
    credit_info = db.Column(db.Text)
    credit_address_e = db.Column(db.Text)  # E文地址信息
    credit_address_a = db.Column(db.Text)  # A文地址信息
    debit = db.relationship('Debit', backref="member", lazy='dynamic')
    applications = db.relationship('Application', backref="member", lazy='dynamic')
    """
    lazy: 指定sqlalchemy数据库什么时候加载数据
        select: 就是访问到属性的时候，就会全部加载该属性的数据
        joined: 对关联的两个表使用联接
        subquery: 与joined类似，但使用子子查询
        dynamic: 不加载记录，但提供加载记录的查询，也就是生成query对象
    """

    def __repr__(self):
        return "<Model Member `{}`>".format(self.nickname)

    def __str__(self):
        return self.nickname

    @property
    def sex_text(self):
        if self.sex == 1:
            # 可用
            sex_text = 'male'
        elif self.sex == 2:
            # 被禁
            sex_text = 'female'
        else:
            # 未知
            sex_text = 'Unknown'
        return sex_text

    @property
    def status_text(self):
        if self.status == 0:
            # 可用
            status_text = 'Available'
        elif self.status == 1:
            # 被禁
            status_text = 'Banned'
        else:
            # 未知
            status_text = 'Unknown'
        return status_text

    @property
    def gene_Salt(self):
        key_list = [random.choice((string.ascii_letters + string.digits)) for i in range(20)]
        return "".join(key_list)

    @property
    def gene_Token(self):
        m = hashlib.md5()
        temp = "%s-%s-%s" % (str(self.id), self.salt, self.status)
        m.update(temp.encode("utf-8"))
        return m.hexdigest()


class Debit(db.Model):
    __tablename__ = 'debit'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(50), autoincrement=True, nullable=False)
    number = db.Column(db.String(50), autoincrement=True, index=True, nullable=False)  # unique=True
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), unique=True, nullable=False)

    def __repr__(self):
        return "<Model Debit `{}`>".format(self.name)

    def __str__(self):
        return self.name + ' ' + self.number
