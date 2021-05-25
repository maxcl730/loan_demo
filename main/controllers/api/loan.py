# -*- coding: utf-8 -*-
import json
from flask import jsonify
from flask_restful import Resource, fields
from main.models.loan import Repayment
from main.models.application import Application
# from main.models.member import Member
from common.helper.member import check_token
from .parser import loan_repayment_parser, installments_detail_parser, uid_token_parser
from common.http import Http
from common.date import Date
from database import db
from common.helper.loan import MonthInstallment
from common.helper.mapping import TimestampValue
from common import Log
# from sqlalchemy import and_, or_


class LoanPolicyApi(Resource):
    def get(self):
        # 返回小贷规则
        policy = MonthInstallment.loan_policy()
        if policy:
            data = {
                'code': 0,
                'message': 'Success',
                'data': policy
            }
            return jsonify(data)
        else:
            return Http.gen_failure_response(message='Loading loan policy failure.')


class InstallmentsDetailApi(Resource):
    def get(self):
        """
        获取贷款分期数据
        根据贷款额度、分期、方法获取贷款明细
        ---
        tags:
          - Loan接口
        parameters:
          - name: amount
            in: query
            required: true
            description: 贷款额度
            schema:
              type: int
          - name: term
            in: query
            required: true
            description: 分期数
            schema:
              type: int
          - name: apr
            in: query
            required: true
            description: 年利率
            schema:
              type: float
          - name: method
            in: query
            required: true
            description: 还款方式 A or B
            schema:
              type: int
        responses:
          200:
            description: code=0为正常，返回uid(用户id)和AccessToken，每次用户访问登录接口Token会更新；code不等于0请查看message中的错误信息。
            examples:
              json: {'code': 0, "message": "Success", 'data': {'uid':'5c3a15126febbb06f576384b', 'token':'feee62378cc104e14e628e0048325103'}}
        """
        data_format = {
            'installments': fields.List(
                fields.Nested({
                    'sequence': fields.Integer,
                    'payment due date': fields.String,
                    'fee': fields.Float
                }))
        }
        args = installments_detail_parser.parse_args()
        # 计算分期还款明细
        policy = MonthInstallment.loan_policy()
        # 校验参数
        if policy['amount']['min'] <= args['amount'] <= policy['amount']['max'] and args['term'] in policy['term'] and args['apr'] in policy['apr']:
            ml = MonthInstallment(corpus=args['amount'],
                                  periods=args['term'],
                                  y_rate=args['apr']/100,
                                  method=args['method'])
            Log.info(ml.info())
            installments_detail = ml.installments(start_date=Date.today_date())
            if installments_detail:
                return Http.gen_success_response(data={"installments": installments_detail}, data_format=data_format)
            else:
                return Http.gen_failure_response(message='Arguments error!')
        return Http.gen_failure_response(message='Arguments error!')


class RepaymentListApi(Resource):
    def get(self):
        """
        还款列表接口
        还款列表接口
        ---
        tags:
          - Loan接口
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
            description: code=0为正常，返回成功；code不等于0请查看message中的错误信息；
            examples:
              json: {'code': 0, 'message':'SUCCESS', 'data':{}}

        """
        # 用户验证（返回uid、signature)
        args = uid_token_parser.parse_args()
        try:
            member = check_token(uid=args['uid'], token=args['token'], fake=False)
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())

        #repayments = Repayment.query.outerjoin(Application).filter(Application.member_id == member.id, Repayment.paid_status == 1)

        repayments = db.session.query(Repayment.application_id,
                        Repayment.sequence,
                        Repayment.updated_time,
                        Repayment.fee,
                        Application.amount,
                        Application.created_time,
                        Application.term).join(Application,
                        Repayment.application_id == Application.id).filter(Application.member_id == member.id,
                                                                           Repayment.paid_status == 1).all()
        data = list()
        for rep in repayments:
            # Log.info(rep.keys())
            data.append({
                'application_id': rep.application_id,
                'sequence': rep.sequence,
                'fee': rep.fee,
                'updated_time': rep.updated_time,
                'amount': rep.amount,
                'application_created_time': rep.created_time,
                'term': rep.term
            })

        data_format = {
            'repayments': fields.List(
                fields.Nested({
                    'application_id': fields.Integer,
                    'sequence': fields.Integer,
                    'fee': fields.Float,
                    'updated_time': TimestampValue(attribute='updated_time'),
                    'amount': fields.Integer,
                    'application_created_time': TimestampValue('application_created_time'),
                    'term': fields.Integer
                }))
        }
        #return Http.gen_success_response()
        return Http.gen_success_response(data={'repayments': data}, data_format=data_format)


class RepaymentApi(Resource):
    def post(self):
        """
        还款接口
        还款接口，需要提交：application_id/sequence
        ---
        tags:
          - Loan接口
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
                - application_id
                - sequence
              properties:
                application_id:
                  type: int
                  description: 申请id
                  example: 132
                sequence:
                  type: int
                  description: 分期序号
                  example: 132
        responses:
          200:
            description: code=0为正常，返回成功；code不等于0请查看message中的错误信息；
            examples:
              json: {'code': 0, 'message':'SUCCESS', 'data':{}}

        """
        args = loan_repayment_parser.parse_args()
        # 验证token
        try:
            member = check_token(uid=args['uid'], token=args['token'], fake=False)
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())

        # Log.info(args)
        repayment = Repayment.query.filter_by(application_id=args['application_id'], sequence=args['sequence']).first()
        repayment.paid_status = 1
        db.session.add(repayment)
        db.session.commit()
        # Log.info(repayment.paid_status)
        return Http.gen_success_response()


