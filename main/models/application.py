from database import db
from datetime import datetime


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    status = db.Column(db.Integer, default=0, nullable=False)
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    created_time = db.Column(db.DateTime, default=datetime.now)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, index=True)
    repayment = db.relationship('Repayment', backref="application", lazy='dynamic')

    #__mapper_args__ = {
    #    "order_by": created_time.desc()
    #}

    @property
    def status_text(self):
        if self.status == 0:
            # 待审批
            status_text = 'Pending'
        elif self.status == 1:
            # 申请通过
            status_text = 'Approved'
        elif self.status == 2:
            # 申请通过
            status_text = 'Rejected'
        else:
            # 未知
            status_text = 'Unknown'
        return status_text

    def __repr__(self):
        return "<Model Application `{}`>".format(self.id)

    def __str__(self):
        return self.id

