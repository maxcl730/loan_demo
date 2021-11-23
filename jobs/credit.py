# -*- coding: utf-8 -*-
import os
from main import create_app
from main.models.member import Member
from common import Log

# Get the ENV from os environment
env = os.environ.get('FLASK_ENV', 'development')
# Create the app instance via Factory method
FLASK_APP = create_app(env.lower())


def fix_user_address(**kwargs):
    # 完善用户地址信息
    with FLASK_APP.app_context():
        Log.info('Fix user address.')
        pass
