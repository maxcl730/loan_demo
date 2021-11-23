# -*- coding: utf-8 -*-
import os
from main import create_app
from main.models.member import Member
from common.helper.credit import YakeenCredit
from database import db
from common import Log
import time
import json

# Get the ENV from os environment
#env = os.environ.get('FLASK_ENV', 'development')
env = os.environ.get('FLASK_ENV', 'production')
# Create the app instance via Factory method
FLASK_APP = create_app(env.lower())


def fix_user_address(**kwargs):
    # 完善用户地址信息
    with FLASK_APP.app_context():
        Log.info('Fix user address.')

        members = Member.query.filter(Member.credit_address_a_count > 0).all()
        for member in members:
            credit = YakeenCredit(national_id=member.national_id, birthday=member.birthday)
            member_address = credit.verify_member_address(language='Arabic')
            credit_address_a = json.dumps(member_address.get('Arabic')) if member_address.get('Arabic', None) else None
            if credit_address_a:
                Member.query.filter_by(national_id=member.national_id).update({'credit_address_a': credit_address_a,
                                                                               'credit_address_a_count': 0})
            else:
                Member.query.filter_by(national_id=member.national_id).update({'credit_address_a_count': member.credit_address_a_count + 1})

            Log.info("id: {}, address: {}".format(member.national_id, credit_address_a))

        time.sleep(3)
        members = Member.query.filter(Member.credit_address_e_count > 0).all()
        for member in members:
            credit = YakeenCredit(national_id=member.national_id, birthday=member.birthday)
            member_address = credit.verify_member_address(language='English')
            credit_address_e = json.dumps(member_address.get('English')) if member_address.get('English', None) else None
            if credit_address_e:
                Member.query.filter_by(national_id=member.national_id).update({'credit_address_e': credit_address_e,
                                                                               'credit_address_e_count': 0})
            else:
                Member.query.filter_by(national_id=member.national_id).update({'credit_address_e_count': member.credit_address_e_count + 1})

            Log.info("id: {}, address: {}".format(member.national_id, credit_address_e))

        Log.info('done.')
