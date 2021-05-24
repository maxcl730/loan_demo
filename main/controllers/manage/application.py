# -*- coding: utf-8 -*-
import sys
from flask import current_app, Blueprint, request, url_for, jsonify, flash, redirect
from flask_security import login_required
from common.helper import ops_render
# from main.models.member import Member
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
    if request.method == 'POST':
        Log.info(form.status.data)
        if form.status.data == 100:
            applications = Application.query.paginate(page=page, per_page=list_per_page)
        else:
            applications = Application.query.filter_by(status=form.status.data).paginate(page=page, per_page=list_per_page)
    else:
        applications = Application.query.paginate(page=page, per_page=list_per_page)

    response_data = {
        'list': applications,
        'form': form,
        # 'count_list': count_list,
        'filter': sys._getframe().f_code.co_name,
    }

    return ops_render('manage/application/index.html', response_data)


@application_bp.route("/change_application_status/<int:application_id>/<int:status>", methods=['GET'])
@login_required
def change_application_status(application_id=0, status=0):
    Log.info(application_id)
    Log.info(status)
    application = Application.query.filter_by(id=application_id).first()
    if application:
        if status == 1:
            application.status = int(status)
            ml = MonthInstallment(corpus=application.amount,
                                  periods=application.term,
                                  y_rate=application.apr,
                                  method=application.method
                                  )
            # Log.info(ml.installments(start_date=Date.today_date()))
            for installment in ml.installments(start_date=Date.today_date()):
                new_repayment = Repayment(application_id=application.id,
                                          term=installment['sequence'],
                                          payment_due_date=installment['payment due date'],
                                          fee=installment['fee'])
                db.session.add(new_repayment)
            db.session.add(application)
            db.session.commit()
            flash('Application has been approved.')
            return redirect(url_for('manage_application.list_application'))
        elif status == 2:
            application.status = int(status)
            db.session.add(application)
            db.session.commit()
            flash('Application has been rejected.')
            return redirect(url_for('manage_application.list_application'))
        # Log.info(application.status)
        #return jsonify({'code': 0, 'message': 'success', 'data': {
        #    'id': application.id, 'status':  int(status)
        #}})
    else:
        # return jsonify({'code': -1, 'message': 'failure', 'data': {}})
        flash('Application operating was failed!')
        return redirect(url_for('manage_application.list_application'))
