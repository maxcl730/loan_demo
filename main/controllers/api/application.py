# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource, fields
from main.models.application import Application
from main.models.loan import Repayment
from database import db
from .parser import application_post_parser, application_get_parser
from common.helper.member import check_token
from common.helper.loan import MonthInstallment
from common.helper.mapping import TimestampValue
from common.http import Http
from common.date import Date
from common import Log


class MemberAvatar(fields.Raw):
    def format(self, value):
        return value.avatar


class MemberNickname(fields.Raw):
    def format(self, value):
        return value.nickname


class MemberCreatedTimeStamp(fields.Raw):
    def format(self, value):
        return Date.datetime_toTimestamp(value.created_time)


class LoanApplicationApi(Resource):
    def get(self):
        """
        贷款申请列表
        贷款申请列表
        ---
        tags:
          - 贷款申请接口
        parameters:
          - name: uid
            in: query
            description: 用户id
            schema:
              type: string
          - name: token
            in: query
            description: AccessToken
            schema:
              type: string
          - name: application_id
            in: query
            required: False
            description: 贷款id，如为空则查询所有该用户的贷款申请
            schema:
              type: int
        responses:
          200:
            description:
              code=0为正常，返回首页内容；code不等于0请查看message中的错误信息；</br>
              数据项：</br>
              applications_number - 总申请数</br>
              applications:申请数组
              {id:申请id，nickname:用户昵称，avatar:用户头像，content:申请内容，created_time:申请时间}
            examples:
              json: {'code': 0, "message": "Success", 'data': { }}

        """
        args = application_get_parser.parse_args()
        try:
            member = check_token(uid=args['uid'], token=args['token'])
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())
        if args.get("application_id", None) is None:
            # 获取所有贷款申请
            data_format = {
                'applications_count': fields.Integer,
                'applications': fields.List(fields.Nested({
                    'id': fields.Integer,
                    'amount': fields.Integer,
                    'term': fields.Integer,
                    'apr': fields.Float,
                    'status': fields.Integer,
                    'status_text': fields.String,
                    'created_time': TimestampValue(attribute='created_time'),
                    'updated_time': TimestampValue(attribute='created_time')
                })),
            }
            applications = member.applications.all()
            data = {
                'applications': applications,
                'applications_count': len(applications),
                'installments': None,
            }
        else:
            data_format = {
                'application': fields.Nested({
                    'id': fields.Integer,
                    'amount': fields.Integer,
                    'term': fields.Integer,
                    'apr': fields.Float,
                    'status': fields.Integer,
                    'status_text': fields.String,
                    'created_time': TimestampValue(attribute='created_time'),
                    'updated_time': TimestampValue(attribute='created_time')
                }),
                'installments': fields.List(
                    fields.Nested({
                        'term': fields.Integer,
                        'payment_due_date': TimestampValue(attribute='payment_due_date'),
                        'fee': fields.Float,
                        'paid_status': fields.Integer,
                        'status_text': fields.String
                    })
                )
            }
            # 获取指定的贷款申请
            application = member.applications.filter_by(id=args['application_id']).first()
            if application:
                installments = Repayment.query.filter_by(application_id=args['application_id']).order_by(Repayment.term).all()
            else:
                installments = None
            data = {
                'application': application,
                'installments': installments,
            }

        return Http.gen_success_response(data=data, data_format=data_format)

    def post(self):
        """
        会员申请贷款
        申请贷款，需要提交：amount/term/apr/method
        ---
        tags:
          - 贷款申请接口
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
              required:
                - amount
                - term
                - apr
              properties:
                amount:
                  type: int
                  description: 贷款总额
                  example: 10000
                term:
                  type: int
                  description: 分期数
                  example: 6
                apr:
                  type: float
                  description: 年利率
                  example: 5.3
                method:
                  type: string
                  description: 还款方式, 默认是A-Equal_Amortization
                  example: A/B
        responses:
          200:
            description: code=0为正常，返回成功；code不等于0请查看message中的错误信息；
            examples:
              json: {'code': 0, 'message':'SUCCESS', 'data':{}}

        """
        # 验证token
        args = application_post_parser.parse_args()
        try:
            member = check_token(uid=args['uid'], token=args['token'])
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())
        # 校验参数
        policy = MonthInstallment.loan_policy()
        if policy['amount']['min'] <= args['amount'] <= policy['amount']['max'] and args['term'] in policy['term'] and args['apr'] in policy['apr']:
            new_application = Application(
                amount=args['amount'],
                term=args['term'],
                apr=args['apr'],
                method=args.get('method', 'A'),
                member_id=member.id
            )
            db.session.add(new_application)
            db.session.commit()
            return Http.gen_success_response()
        return Http.gen_failure_response(message='Illegal application.')
