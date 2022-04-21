# -*- coding: utf-8 -*-
from flask import current_app
from flask_restful import Resource, fields
from main.models.application import Application
from main.models.loan import Product, Repayment
from database import db
from .parser import application_post_parser, application_get_parser
from common.helper.member import check_token
from common.helper.loan import MonthInstallment
from common.helper.mapping import TimestampValue
from decimal import Decimal
from common.http import Http
from common.date import Date
from common import Log


class ProductValue(fields.Raw):
    def format(self, value):
        return value


class LoanApplicationApi(Resource):
    def get(self):
        """
        Application list
        Application list (The specific application or all of user)
        ---
        tags:
          - Application
        parameters:
          - name: uid
            in: query
            description: user id
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
            description: Application id. If not provided, all applications of user will be return.
            schema:
              type: int
        responses:
          200:
            description:
              code=0 success；code<> 0 failed.</br>
              数据项：</br>
              applications_number - Total of applications</br>
              applications:detail information.
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
                    'amount': ProductValue(attribute='product.amount'),
                    'terms': ProductValue(attribute='product.terms'),
                    'fees': ProductValue(attribute='product.fees'),
                    'fee_payment': ProductValue(attribute='product.fee_payment_text'),
                    'rate_per_month': ProductValue(attribute='product.rate_per_month'),
                    'status': fields.Integer,
                    'status_text': fields.String,
                    'created_time': TimestampValue(attribute='created_time'),
                    'updated_time': TimestampValue(attribute='updated_time')
                })),
            }
            applications = member.applications.order_by(Application.updated_time.desc()).all()
            data = {
                'applications': applications,
                'applications_count': len(applications),
                'installments': None,
            }
        else:
            data_format = {
                'application': fields.Nested({
                    'id': fields.Integer,
                    'amount': ProductValue(attribute='product.amount'),
                    'terms': ProductValue(attribute='product.terms'),
                    'fees': ProductValue(attribute='product.fees'),
                    'fee_payment':ProductValue(attribute='product.fee_payment_text'),
                    'rate_per_month': ProductValue(attribute='product.rate_per_month'),
                    'status': fields.Integer,
                    'status_text': fields.String,
                    'created_time': TimestampValue(attribute='created_time'),
                    'updated_time': TimestampValue(attribute='updated_time')
                }),
                'installments': fields.List(
                    fields.Nested({
                        'sequence': fields.Integer,
                        'payment_due_date': TimestampValue(attribute='payment_due_date'),
                        'fee': fields.Float,
                        'paid_status': fields.Integer,
                        'status_text': fields.String
                    })
                )
            }
            # 获取指定的贷款申请
            installments = None
            application = member.applications.filter_by(id=args['application_id']).first()
            if application:
                if application.status == 1:
                    installments = Repayment.query.filter_by(application_id=args['application_id']).order_by(Repayment.sequence).all()

            data = {
                'application': application,
                'installments': installments,
            }

        return Http.gen_success_response(data=data, data_format=data_format)

    def post(self):
        """
        Loan apply
        Loan apply，require：amount/term/apr/method
        ---
        tags:
          - Application
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
              required:
                - product_id
              properties:
                product_id:
                  type: int
                  description: product_id
                  example: 9
        responses:
          200:
            description: code=0 success；code<> 0 failed.
            examples:
              json: {'code': 0, 'message':'SUCCESS', 'data':{}}

        """
        # 验证token
        args = application_post_parser.parse_args()
        try:
            member = check_token(uid=args['uid'], token=args['token'])
        except Exception as e:
            return Http.gen_failure_response(message=e.__str__())

        product = Product.query.filter_by(id=args['product_id']).first()
        if product:
            ml = MonthInstallment(corpus=product.amount,
                                  periods=product.terms,
                                  y_rate=product.rate_per_month * 12 / 100,
                                  method='A')
            # Log.info(ml.info())
            installments_detail = ml.installments(start_date=Date.today_date())
            if installments_detail:
                if product.fee_payment == 2:
                    installments_detail[-1]['fee'] = Decimal(installments_detail[-1]['fee'] + product.fees).quantize(Decimal("0.00"))

                new_application = Application(
                    product_id=args['product_id'],
                    member_id=member.id
                )
                db.session.add(new_application)
                product.applications_count = product.applications_count + 1
                db.session.add(product)
                db.session.commit()
                return Http.gen_success_response()

        return Http.gen_failure_response(message='Illegal apply.')
