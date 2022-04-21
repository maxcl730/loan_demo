# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource, fields
from .parser import member_login_parser, uid_token_parser, member_register_parser, member_info_post_parser, \
    member_debit_parser
from common.http import Http
from common.helper.member import check_token
from database import db
from flask import current_app
from main.models.member import Member, Debit
from common.helper.credit import YakeenCredit
import json


class MemberAvatar(fields.Raw):
    def format(self, value):
        return value.avatar


class MemberNickname(fields.Raw):
    def format(self, value):
        return value.nickname


class MemberLoginApi(Resource):
    def post(self):
        """
        Login
        Require:  National_id/Password;  return: Token/uid。
        ---
        tags:
          - Member
        parameters:
          - name: body
            in: body
            required: true
            schema:
              required:
                - national_id
                - password
              properties:
                national_id:
                  type: string
                  description: National_id.
                  example: "19230192"
                password:
                  type: string
                  description: password.
                  example: "helloworld"
        responses:
          200:
            description: return Token and Uid
            examples:
              json: {'token': 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0NzcyMjY0MCwiZXhwIjoxNTQ3NzIyOTQwfQ.eyJpZCI6IjVjMzgzNTNkNmZlYmJiMDcyNTE0OGE1OCJ9._BjoZS8TMAifNik21hO6xpSVyHXEzRDmMrmWiRVgx0s', 'uid':123}

        """

        data_format = {
            'uid': fields.Integer,
            'token': fields.String,
        }
        # 用户验证（返回uid、signature)
        args = member_login_parser.parse_args()
        member = Member.query.filter_by(national_id=args['national_id'], password=args['password']).first()
        if member:
            member.salt = member.gene_Salt
            db.session.add(member)
            db.session.commit()
            uid = str(member.id)
            token = member.gene_Token
            return Http.gen_success_response(data={'uid': str(uid), 'token': token}, data_format=data_format)
        else:
            return Http.gen_failure_response(code=-1, message='Member does not exist or password is incorrect.')

        #if member.status == 2:
            # 会员已被禁用
        #    return Http.gen_failure_response(message="Member has been blocked.")


class MemberAuthApi(Resource):
    def get(self):
        """
        Authorized
        Verify uid and token or renew token.
        ---
        tags:
          - Member
        parameters:
          - name: uid
            in: query
            required: true
            description: user id
            schema:
              type: string
          - name: token
            in: query
            required: true
            description: AccessToken
            schema:
              type: string
        responses:
          200:
            description: code=0 success，return uid and AccessToken，Token will be refreshed at request；code<> 0 failed.
            examples:
              json: {'code': 0, "message": "Success", 'data': {'uid':'5c3a15126febbb06f576384b', 'token':'feee62378cc104e14e628e0048325103'}}
        """
        data_format = {
            'uid': fields.Integer,
            'token': fields.String,
        }
        # 用户验证（返回uid、signature)
        args = uid_token_parser.parse_args()
        try:
            member = check_token(uid=args['uid'], token=args['token'], fake=False)
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())

        # 调用此接口后会更新Token
        member.salt = member.gene_Salt
        db.session.add(member)
        db.session.commit()
        uid = str(member.id)
        token = member.gene_Token
        return Http.gen_success_response(data={'uid': str(uid), 'token': token}, data_format=data_format)


class MemberRegisterApi(Resource):
    def post(self):
        """
        Register
        Require: National_ID/Mobile/Password
        ---
        tags:
          - Member
        parameters:
          - name: body
            in: body
            required: true
            schema:
              required:
                - national_id
                - password
              properties:
                national_id:
                  type: string
                  description: National_id.
                  example: "19230192"
                mobile:
                  type: string
                  description: mobile.
                  example: "111000222333"
                password:
                  type: string
                  description: password.
                  example: "hello_world"
                language:
                  type: string
                  description: language
                  example: "en_US"
                birthday:
                  type: string
                  description: birthday
                  example: "dd/mm/yyyy"
        responses:
          200:
            description: code=0 success，return uid and AccessToken，Token will be refreshed at request；code<> 0 failed.
            examples:
              json: {'code': 0, "message": "Success", 'data': {'uid':'5c3a15126febbb06f576384b', 'token':'feee62378cc104e14e628e0048325103'}}
        """
        data_format = {
            'uid': fields.Integer,
            'token': fields.String,
        }
        args = member_register_parser.parse_args()
        member = Member.query.filter_by(national_id=args['national_id']).first()
        if member:
            # 返回用户已存在
            return Http.gen_failure_response(code=2, message="National/Resident id has been registered.")
        else:
            if current_app.config['CREDIT_VERIFY']:
                # 调用征信接口查询用户信息
                credit = YakeenCredit(national_id=args['national_id'], birthday=args['birthday'])
                member_credit_info = credit.verify_member_info()
                if not member_credit_info:
                    # 用户征信信息异常，返回错误
                    return Http.gen_failure_response(code=2, message="Failed to query credit information.")

                # 用户征信信息正常，继续注册
                # 用户地址信息
                member_address = credit.verify_member_address()
                # return Http.gen_failure_response(code=2, message="Failed to query credit information.")
            else:
                member_credit_info = None
                member_address = dict()

            new_member = Member(
                national_id=args['national_id'],
                mobile=args['mobile'],
                password=args['password'],
                birthday=args.get('birthday', ''),
                language=args.get('language', 'en_US'),
                nickname=args.get('nickname', ''),
                sex=args.get('sex', 0),
                reg_ip=request.remote_addr,
                credit_info=json.dumps(member_credit_info),
                credit_address_e=json.dumps(member_address.get('English')) if member_address.get('English', None) else None,
                credit_address_a=json.dumps(member_address.get('Arabic')) if member_address.get('Arabic', None) else None,
                credit_address_e_count=0 if member_address.get('English', None) else 1,
                credit_address_a_count=0 if member_address.get('Arabic', None) else 1
                # credit_address_e=None,
                # credit_address_e_count=1,
                # credit_address_a=None,
                # credit_address_a_count=1
            )
            db.session.add(new_member)
            member = Member.query.filter_by(national_id=args['national_id']).first()
            member.salt = member.gene_Salt
            uid = str(member.id)
            db.session.add(member)
            db.session.commit()
            token = member.gene_Token
            return Http.gen_success_response(data={'uid': str(uid), 'token': token}, data_format=data_format)


class MemberInfoApi(Resource):
    def get(self):
        """
        Information query
        Return nickname/ avatar/ gender / status etc.
        ---
        tags:
          - Member
        parameters:
          - name: uid
            in: query
            required: true
            description: user id
            schema:
              type: string
          - name: token
            in: query
            required: true
            description: AccessToken
            schema:
              type: string
        responses:
          200:
            description:
              code=0 success，return user info；code<>0 please check error message；
            examples:
              json: {'code': 0, "message": "Success", 'data': {'nickname':'logan', 'national_id':'1304124123', 'sex':1, 'status':1, 'mobile':'11222333444', 'language':'en_US'}}

        """
        data_format = {
            'nickName': fields.String,
            'national_id': fields.String,
            'mobile': fields.String,
            'sex': fields.Integer,
            'language': fields.String,
            'birthday': fields.String,
            'status': fields.Integer,
            'debit': fields.Nested({
                'name': fields.String,
                'number': fields.String
            })
        }
        args = uid_token_parser.parse_args()
        # 验证token
        try:
            member = check_token(uid=args['uid'], token=args['token'], fake=False)
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())

        # Log.info("{}, {}".format(effective_invitation.sum('current_point'), effective_helper.sum('helper_point')))

        member_debit = member.debit.first()
        if member_debit is None:
            member_debit = {'name': None, 'number': None}

        return Http.gen_success_response(
            data={
                    'nickName': member.nickname,
                    'national_id': member.national_id,
                    'sex': member.sex,
                    'language': member.language,
                    'birthday': member.birthday,
                    'status': member.status,
                    'debit': member_debit
                    },
            data_format=data_format
        )

    def post(self):
        """
        Information update
        Include password/ mobile /nickname/ gender / language etc.
        ---
        tags:
          - Member
        parameters:
          - name: uid
            in: query
            required: true
            description: user id
            schema:
              type: string
          - name: token
            in: query
            required: true
            description: AccessToken
            schema:
              type: string
          - name: body
            in: body
            required: true
            schema:
              properties:
                nickname:
                  type: string
                  description: nickname
                  example: "iloveu"
                password:
                  type: string
                  description: password.
                  example: "3uihfaefeDAFAa34fAFA"
                mobile:
                  type: string
                  description: mobile
                  example: "91030219421"
                sex:
                  type: int
                  description: gender
                  example: "1-male；2-female；0-unknown"
                language:
                  type: string
                  description: language
                  example: "zh_CN, en_US"
        responses:
          200:
            description: code=0 ,success ；code<> 0 failed；
            examples:
              json: {'code': 0, 'message':'SUCCESS', 'data':{}}

        """
        # 提交更新会员信息
        args = member_info_post_parser.parse_args()
        # 验证token
        try:
            member = check_token(uid=args['uid'], token=args['token'])
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())

        member.sex = args.get('sex', member.sex)
        member.nickName = args.get('nickName', member.nickname)
        member.mobile = args.get('mobile', member.mobile)
        member.language = args.get('language', member.language)
        member.birthday = args.get('birthday', member.birthday)
        member.nickname = args.get('nickname', member.birthday)
        db.session.add(member)
        db.session.commit()

        return Http.gen_success_response()


class MemberDebitApi(Resource):
    def post(self):
        """
        Member debit update
        Require: name and number
        ---
        tags:
          - Member
        parameters:
          - name: uid
            in: query
            required: true
            description: user id
            schema:
              type: string
          - name: token
            in: query
            required: true
            description: AccessToken
            schema:
              type: string
          - name: body
            in: body
            required: true
            schema:
              properties:
                name:
                  type: string
                  description: Name
                  example: "James Harden"
                number:
                  type: string
                  description: Account number
                  example: "623192012395821021"
        responses:
          200:
            description: code=0 ,success ；code<> 0 failed；
            examples:
              json: {'code': 0, 'message':'SUCCESS', 'data':{}}

        """
        args = member_debit_parser.parse_args()
        # 验证token
        try:
            member = check_token(uid=args['uid'], token=args['token'])
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())

        member_debit = member.debit.first()
        if member_debit is None:
            new_debit = Debit(member_id=member.id, name=args['name'], number=args['number'])
            db.session.add(new_debit)
            db.session.commit()
        else:
            member_debit.name = args['name']
            member_debit.number = args['number']
            db.session.add(member_debit)
            db.session.commit()

        return Http.gen_success_response()
