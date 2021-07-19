# -*- coding: utf-8 -*-
import sys
from flask import current_app, Blueprint, request, url_for, jsonify, flash, redirect
from flask_security import login_required
from common.helper import ops_render
from main.models.member import Member
from database import db
from main.models.application import Application
from main.models.loan import Repayment
from main.form import ApplicationSearchForm
from common.helper.loan import MonthInstallment
from decimal import Decimal
from common.date import Date
from common import Log

application_bp = Blueprint('manage_application', __name__,)


@application_bp.route("/list_application", methods=['GET', 'POST'])
@application_bp.route("/list_application/<int:page>", methods=['GET', 'POST'])
@login_required
def list_application(page=1):
    list_per_page = current_app.config['MANAGEMENT_LIST_PER_PAGE']
    form = ApplicationSearchForm()
    applications = Application.query.join(Member).order_by(Application.updated_time.desc())
    Log.info(page)
    if request.method == 'POST':
        if form.national_id.data:
            applications = applications.filter(Member.national_id == form.national_id.data)
        if form.mobile.data:
            applications = applications.filter(Member.mobile == form.mobile.data)

        if form.created_time_begin.data:
            applications = applications.filter(Application.created_time >= form.created_time_begin.data)
        if form.created_time_end.data:
            applications = applications.filter(Application.created_time <= form.created_time_end.data)
        if form.status.data != 100:
            applications = applications.filter(Application.status == form.status.data).order_by(Application.updated_time.desc())
        else:
            applications = applications.order_by(Application.updated_time.desc())

    applications_paged = applications.paginate(page=page, per_page=list_per_page)
    response_data = {
        'list': applications_paged,
        'form': form,
        'product_id': 0,
        # 'count_list': count_list,
        'filter': sys._getframe().f_code.co_name,
    }
    Log.info(response_data)
    return ops_render('manage/application/index.html', response_data)


@application_bp.route("/filter_application/<int:product_id>", methods=['GET'])
@login_required
def filter_application(product_id=0):
    applications = Application.query.filter_by(product_id=product_id).order_by(Application.updated_time.desc()).paginate()
    response_data = {
        'list': applications,
        'product_id': product_id,
    }

    return ops_render('manage/application/index.html', response_data)


@application_bp.route("/change_application_status/<int:application_id>/<int:status>", methods=['GET'])
@login_required
def change_application_status(application_id=0, status=0):
    application = Application.query.filter_by(id=application_id).first()
    if application:
        if status == 1:
            application.status = int(status)
            ml = MonthInstallment(corpus=application.product.amount,
                                  periods=application.product.terms,
                                  y_rate=application.product.rate_per_month * 12 / 100,
                                  method='A'
                                  )
            # Log.info(ml.info())
            # Log.info(ml.installments(start_date=Date.today_date()))
            installments_detail = ml.installments(start_date=Date.today_date())
            if installments_detail:
                if application.product.fee_payment == 2:
                    installments_detail[-1]['fee'] = Decimal(installments_detail[-1]['fee'] + application.product.fees).quantize(Decimal("0.00"))

            for installment in installments_detail:
                new_repayment = Repayment(application_id=application.id,
                                          sequence=installment['sequence'],
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


@application_bp.route("/view_repayment/<int:application_id>", methods=['GET'])
@login_required
def view_repayment(application_id=0):
    list_per_page = current_app.config['MANAGEMENT_LIST_PER_PAGE']
    repayments = Repayment.query.filter_by(application_id=application_id).paginate(page=1, per_page=list_per_page)
    if repayments:
        response_data = {
            'list': repayments,
        }
    else:
        response_data = {
            'list': None,
        }
    return ops_render('manage/application/repayment.html', response_data)
