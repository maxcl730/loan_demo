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
    term = db.Column(db.Integer, nullable=False)
    payment_due_date = db.Column(db.DateTime, nullable=False)
    fee = db.Column(db.Float, default=0, nullable=False)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_time = db.Column(db.DateTime, default=datetime.now)
    __table_args__ = (
        #  联合索引
        db.UniqueConstraint('application_id', 'term', name='uix_application_term'),
        # db.Index('application_id', 'term')
    )

    @property
    def status_text(self):
        if self.paid_status == 0:
            if self.payment_due_date < datetime.now():
                text = 'overdue'  # 逾期
            else:
                text = 'obligated'  # 待还款
        else:
            text = 'paid-up'  # 已还清

        return text

    def __repr__(self):
        return "<Model Repayment `{}`>".format(self.id)

    def __str__(self):
        return self.id
