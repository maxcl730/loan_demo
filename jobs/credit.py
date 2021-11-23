# -*- coding: utf-8 -*-
import os
from main import create_app
from main.models.member import Member
from main.models.loan import Product, Repayment
from common import Log
import time

# Get the ENV from os environment
env = os.environ.get('FLASK_ENV', 'development')
# Create the app instance via Factory method
FLASK_APP = create_app(env.lower())


def fix_user_address(**kwargs):
    # 完善用户地址信息
    with FLASK_APP.app_context():
        Log.info('Fix user address.')

        members = Member.query.filter(Member.credit_address_a==None).all()
        for member in members:
            print(member.national_id)

        time.sleep(5)
        members = Member.query.filter(Member.credit_address_e==None).all()
        for member in members:
            print(member.national_id)

        Log.info('done.')
