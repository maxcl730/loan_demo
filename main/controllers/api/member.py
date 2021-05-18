# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource, fields
from .parser import member_login_parser, uid_token_parser, member_register_parser, member_info_post_parser, \
    member_debit_parser
from common.http import Http
from common.helper.member import check_token
from database import db
from main.models.member import Member, Debit
from common import Log


class MemberAvatar(fields.Raw):
    def format(self, value):
        return value.avatar


class MemberNickname(fields.Raw):
    def format(self, value):
        return value.nickname


class MemberLoginApi(Resource):
    def post(self):
        """
        会员登录
        调用接口需要提供 National_id/Password, 返回Token和uid。
        ---
        tags:
          - 会员接口
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
                  description: 用户密码.
                  example: "helloworld"
        responses:
          200:
            description: 返回Token和Uid
            examples:
              json: {'token': 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0NzcyMjY0MCwiZXhwIjoxNTQ3NzIyOTQwfQ.eyJpZCI6IjVjMzgzNTNkNmZlYmJiMDcyNTE0OGE1OCJ9._BjoZS8TMAifNik21hO6xpSVyHXEzRDmMrmWiRVgx0s', 'uid':123}

        """

        data_format = {
            'uid': fields.Integer,
            'token': fields.String,
        }
        # 用户验证（返回uid、signature)
        args = member_login_parser.parse_args()
        member = Member.query.filter_by(national_id=args['national_id']).first()
        if member:
            member.salt = member.gene_Salt
            db.session.add(member)
            db.session.commit()
            uid = str(member.id)
            token = member.gene_Token
            return Http.gen_success_response(data={'uid': str(uid), 'token': token}, data_format=data_format)
        else:
            return Http.gen_failure_response(code=-1, message='Member does not exist.')

        #if member.status == 2:
            # 会员已被禁用
        #    return Http.gen_failure_response(message="Member has been blocked.")


class MemberAuthApi(Resource):
    def get(self):
        """
        会员验证
        使用uid和token验证当前用户是否有效
        ---
        tags:
          - 会员接口
        parameters:
          - name: uid
            in: query
            required: true
            description: 用户id
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
            description: code=0为正常，返回uid(用户id)和AccessToken，每次用户访问登录接口Token会更新；code不等于0请查看message中的错误信息。
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
        会员信息注册
        会员信息注册，National_ID/Mobile/Password
        ---
        tags:
          - 会员接口
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
                  description: 电话.
                  example: "111000222333"
                password:
                  type: string
                  description: 用户密码.
                  example: "hello_world"
                language:
                  type: string
                  description: 用户语言
                  example: "en_US"
                birthday:
                  type: string
                  description: 用户出生日期
                  example: "dd/mm/yyyy"
        responses:
          200:
            description: code=0为正常，返回uid(用户id)和AccessToken，每次用户访问登录接口Token会更新；code不等于0请查看message中的错误信息。
            examples:
              json: {'code': 0, "message": "Success", 'data': {'uid':'5c3a15126febbb06f576384b', 'token':'feee62378cc104e14e628e0048325103'}}
        """
        data_format = {
            'uid': fields.Integer,
            'token': fields.String,
        }
        args = member_register_parser.parse_args()
        #try:
        member = Member.query.filter_by(national_id=args['national_id']).first()
        if member:
            member.mobile = args['mobile']
            member.password = args['password']
            member.language = args.get('language', '')
            member.birthday = args.get('birthday', '')
            member.nickname = args.get('nickname', '')
            member.sex = args.get('sex', '')
            db.session.add(member)
        else:
            new_member = Member(
                national_id=args['national_id'],
                mobile=args['mobile'],
                password=args['password'],
                birthday=args.get('birthday', ''),
                language=args.get('language', 'en_US'),
                nickname=args.get('nickname', ''),
                sex=args.get('sex', 0),
                reg_ip=request.remote_addr
            )
            db.session.add(new_member)
        member = Member.query.filter_by(national_id=args['national_id']).first()
        member.salt = member.gene_Salt
        uid = str(member.id)
        db.session.add(member)
        db.session.commit()
        token = member.gene_Token
        return Http.gen_success_response(data={'uid': str(uid), 'token': token}, data_format=data_format)
        #except Exception as e:
        #    db.session.rollback()
        #    return Http.gen_failure_response(message=e.__str__())


class MemberInfoApi(Resource):
    def get(self):
        """
        获取会员信息
        获取昵称、头像、性别、状态、数等个人信息
        ---
        tags:
          - 会员接口
        parameters:
          - name: uid
            in: query
            required: true
            description: 用户id
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
              code=0为正常，返回用户信息；code不等于0请查看message中的错误信息；
              nickname:用户昵称；
              sex： 0 未知，1 男，2 女；
              status： 1 正常 ，2 禁用；
              point： 剩余试用次数。
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
        #if member_debit is None:

        return Http.gen_success_response(data={
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
        更新会员信息， 注册新会员信息
        更新会员密码、手机号、nickname、性别、语言等
        ---
        tags:
          - 会员接口
        parameters:
          - name: uid
            in: query
            required: true
            description: 用户id
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
                  description: 昵称.
                  example: "iloveu"
                password:
                  type: string
                  description: password.
                  example: "3uihfaefeDAFAa34fAFA"
                mobile:
                  type: string
                  description: 手机号
                  example: "91030219421"
                sex:
                  type: int
                  description: 性别
                  example: "1-男；2-女；0-未知"
                language:
                  type: string
                  description: 语言
                  example: "zh_CN, en_US"
        responses:
          200:
            description: code=0为正常，返回成功；code不等于0请查看message中的错误信息；
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
        更新会员借记卡
        更新会员借记卡信息：账户名、卡号
        ---
        tags:
          - 会员接口
        parameters:
          - name: uid
            in: query
            required: true
            description: 用户id
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
                  description: 账号名
                  example: "James Harden"
                number:
                  type: string
                  description: 账号
                  example: "623192012395821021"
        responses:
          200:
            description: code=0为正常，返回成功；code不等于0请查看message中的错误信息；
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
