# -*- coding: utf-8 -*-
from werkzeug.datastructures import FileStorage
from flask_restful import reqparse

# 分期明细参数解析器
installments_detail_parser = reqparse.RequestParser()
installments_detail_parser.add_argument(
    'amount',
    type=int,
    required=True,
    location=['args', 'form'],
    help="Amount is required!"
)
installments_detail_parser.add_argument(
    'term',
    type=int,
    required=True,
    location=['args', 'form'],
    help="Term is required!"
)
installments_detail_parser.add_argument(
    'apr',
    type=float,
    required=True,
    location=['args', 'form'],
    help="Apr is required!"
)
installments_detail_parser.add_argument(
    'method',
    type=str,
    required=True,
    location=['args', 'form'],
    help="Method is required!"
)

# 系统接口参数解析器
member_login_parser = reqparse.RequestParser()
member_login_parser.add_argument(
    'national_id',
    type=str,
    required=True,
    location=['args', 'form'],
    help="Member's national_id is required!"
)
member_login_parser.add_argument(
    'password',
    type=str,
    required=True,
    location=['args', 'form'],
    help="Password is required!"
)

# 会员注册参数解析器
member_register_parser = reqparse.RequestParser()
member_register_parser.add_argument(
    'national_id',
    type=str,
    required=True,
    location=['args', 'form', 'json'],
    help="<national_id> is required!"
)
member_register_parser.add_argument(
    'mobile',
    type=str,
    required=False,
    location=['args', 'form', 'json'],
    # help="<mobile> is required!"
)
member_register_parser.add_argument(
    'password',
    type=str,
    required=True,
    location=['args', 'form', 'json'],
    help="<password> is required!"
)
member_register_parser.add_argument(
    'birthday',
    type=str,
    required=True,
    location=['args', 'form', 'json'],
    # help="<password> is required!"
)
member_register_parser.add_argument(
    'sex',
    type=str,
    required=False,
    location=['args', 'form', 'json'],
    # help="<password> is required!"
)
member_register_parser.add_argument(
    'nickname',
    type=str,
    required=False,
    location=['args', 'form', 'json'],
    # help="<password> is required!"
)
member_register_parser.add_argument(
    'language',
    type=str,
    required=False,
    location=['args', 'form', 'json'],
    # help="<password> is required!"
)

uid_token_parser = reqparse.RequestParser()
uid_token_parser.add_argument(
    'uid',
    type=str,
    required=True,
    location=['args', 'form'],
    help="<uid> is required!"
)
uid_token_parser.add_argument(
    'token',
    type=str,
    required=True,
    location=['args', 'form'],
    help="<token> is required!"
)

# 分页参数
pagination_get_perser = uid_token_parser.copy()
pagination_get_perser.add_argument(
    'page',
    type=int,
    location=['args', 'form'],
)
pagination_get_perser.replace_argument(
    'uid',
    type=str,
    location=['args', 'form', 'json'],
)
pagination_get_perser.replace_argument(
    'token',
    type=str,
    location=['args', 'form', 'json'],
)

member_info_post_parser = member_register_parser.copy()
member_info_post_parser.remove_argument('national_id')
# member_info_post_parser.remove_argument('password')

# 更新会员debit信息
member_debit_parser = uid_token_parser.copy()
member_debit_parser.add_argument(
    'name',
    type=str,
    required=True,
    location=['form', 'json'],
    help="Member's debit name"
)
member_debit_parser.add_argument(
    'number',
    type=str,
    required=True,
    location=['form', 'json'],
    help="Member's debit name"
)

# 用户查看产品分期明细
product_installments_get_parser = uid_token_parser.copy()
product_installments_get_parser.add_argument(
    'product_id',
    type=int,
    required=True,
    location=['args', 'form', 'json'],
    # help='Application_id is required.'
)

# 用户申请试用
application_get_parser = uid_token_parser.copy()
application_get_parser.add_argument(
    'application_id',
    type=int,
    required=False,
    location=['args', 'form', 'json'],
    # help='Application_id is required.'
)

# amount/term/apr/method
application_post_parser = uid_token_parser.copy()
application_post_parser.add_argument(
    'product_id',
    type=int,
    required=True,
    location=['form', 'json'],
    help="Application's amount is required."
)

# 还款参数
loan_repayment_parser = uid_token_parser.copy()
loan_repayment_parser.add_argument(
    'application_id',
    type=int,
    required=True,
    location=['form', 'json'],
    help="Application id"
)
loan_repayment_parser.add_argument(
    'sequence',
    type=int,
    required=True,
    location=['form', 'json'],
    help="Term sequence."
)

# 上传图片接口
upload_post_parser = uid_token_parser.copy()
upload_post_parser.add_argument(
    'file',
    type=FileStorage,
    location='files',
    required=True,
    help='<file> is required.'
)
upload_post_parser.add_argument(
    'width',
    type=int,
    location=['args', 'form', 'json'],
)
upload_post_parser.add_argument(
    'height',
    type=int,
    location=['args', 'form', 'json'],
)