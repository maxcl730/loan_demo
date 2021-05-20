# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from flask import current_app, Blueprint, request, abort, jsonify, flash, redirect
from flask_security import login_required
from common.helper import ops_render
from main.models.member import Member
from database import db
from main.models.application import Application
from main.models.loan import Repayment
from main.form import ApplicationSearchForm
from common.helper.loan import MonthInstallment
from common.date import Date
from common import Log

application_bp = Blueprint('manage_application', __name__,)


@application_bp.route("/list_application", methods=['GET', 'POST'])
@application_bp.route("/list_application/<int:page>", methods=['GET', 'POST'])
@login_required
def list_application(page=1):
    list_per_page = current_app.config['MANAGEMENT_LIST_PER_PAGE']
    form = ApplicationSearchForm()
    applications = Application.query.paginate(page=page, per_page=list_per_page)

    response_data = {
        'list': applications,
        'form': form,
        # 'count_list': count_list,
        'filter': sys._getframe().f_code.co_name,
    }

    return ops_render('manage/application/index.html', response_data)


@application_bp.route("/change_application_status", methods=['POST'])
@login_required
def change_application_status():
    data = request.get_json()
    application = Application.query.filter_by(id=data.get('id', 0)).first()
    if application:
        if data.get('status') == '1':
            application.status = int(data.get('status'))
            ml = MonthInstallment(corpus=application.amount,
                                  periods=application.term,
                                  y_rate=application.apr,
                                  method=application.method
                                  )
            # Log.info(ml.installments(start_date=Date.today_date()))
            for installment in ml.installments(start_date=Date.today_date()):
                new_repayment = Repayment(application_id=application.id,
                                          term=installment['sequence'],
                                          payment_due_date=installment['date'],
                                          fee=installment['fee'])
                db.session.add(new_repayment)
            db.session.add(application)
            db.session.commit()
        elif data.get('status') == '2':
            application.status = int(data.get('status'))
            db.session.add(application)
            db.session.commit()
        # Log.info(application.status)
        return jsonify({'code': 0, 'message': 'success', 'data': {}})
    else:
        return jsonify({'code': -1, 'message': 'failure', 'data': {}})
