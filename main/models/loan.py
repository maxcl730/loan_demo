# -*- coding: utf-8 -*-
from datetime import datetime
from database import db


class Repayment(db.Model):
    """Represents protected member."""
    __tablename__ = 'repayment'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    # member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False, index=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False, index=True)
    paid_status = db.Column(db.Integer, default=0, nullable=False)  # 0-未还款， 1-已还款
    sequence = db.Column(db.Integer, nullable=False)
    payment_due_date = db.Column(db.DateTime, nullable=False)
    fee = db.Column(db.Float, default=0, nullable=False)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_time = db.Column(db.DateTime, default=datetime.now)
    __table_args__ = (
        #  联合索引
        db.UniqueConstraint('application_id', 'sequence', name='uix_application_sequence'),
        # db.Index('application_id', 'sequence')
    )

    @property
    def status_text(self):
        if self.paid_status == 0:
            if self.payment_due_date < datetime.now():
                text = 'overdue'  # 逾期
            else:
                text = 'undue'  # 待还款
        else:
            text = 'paid-up'  # 已还清

        return text

    def __repr__(self):
        return "<Model Repayment `{}`>".format(self.id)

    def __str__(self):
        return self.id


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    amount = db.Column(db.Integer, default=0, nullable=False)
    terms = db.Column(db.Integer, default=0, nullable=False)  # months
    fees = db.Column(db.Float, default=0, nullable=False)
    fee_payment = db.Column(db.SMALLINT, default=0, nullable=False)  # 1:pre-paid, 2: post-paid
    rate_per_month = db.Column(db.Float, default=0, nullable=False)
    available = db.Column(db.SMALLINT, default=0, nullable=False)  # 0: unavailable, 1: available
    applications_count = db.Column(db.Integer, default=0, nullable=False)
    applications = db.relationship('Application', backref="product", lazy='dynamic')
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_time = db.Column(db.DateTime, default=datetime.now)

    @property
    def available_text(self):
        if self.available == 0:
            text = 'No'  # 逾期
        else:
            text = 'Yes'  # 待还款

        return text

    @property
    def fee_payment_text(self):
        if self.fee_payment == 1:
            text = 'pre-paid'
        elif self.fee_payment == 2:
            text = 'post-paid'
        else:
            text = 'unknown'
        return text

    def __repr__(self):
        return "<Model Production `{}`>".format(self.id)

    def __str__(self):
        return self.id
