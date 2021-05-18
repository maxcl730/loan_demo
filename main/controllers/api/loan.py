# -*- coding: utf-8 -*-
import json
from flask import jsonify
from flask_restful import Resource, fields
from common.http import Http
from common.date import Date
from common.helper.loan import MonthInstallment
from .parser import installments_detail_parser


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
                    'date': fields.String,
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
            installments_detail = ml.installments(start_date=Date.today_date())
            if installments_detail:
                return Http.gen_success_response(data={"installments": installments_detail}, data_format=data_format)
            else:
                return Http.gen_failure_response(message='Arguments error!')
        return Http.gen_failure_response(message='Arguments error!')


class RepaymentApi(Resource):
    def post(self):
        """
        还款接口
        还款接口，需要提交：amount/term/apr/method
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
        pass
