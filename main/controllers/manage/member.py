# -*- coding: utf-8 -*-
# from datetime import datetime, timedelta
from flask import current_app, Blueprint, request, abort, url_for, flash, redirect
from flask_security import login_required
from database import db
from common.helper import ops_render
from common.helper.mapping import STATUS
from main.models.member import Member
from main.models.application import Application
from main.form import MemberSearchForm, BlockedMemberSearchForm
from common import Log

member_bp = Blueprint('manage_member', __name__,)


@member_bp.route("/list_member", methods=['GET', 'POST'])
@member_bp.route("/list_member/<int:page>", methods=['GET', 'POST'])
@login_required
def list_member(page=1):
    list_per_page = current_app.config['MANAGEMENT_LIST_PER_PAGE']
    form = MemberSearchForm()
    members = Member.query
    if request.method == 'POST':
        if form.national_id.data:
            members = members.filter_by(national_id=form.national_id.data)
        if form.mobile.data:
            members = members.filter_by(mobile=form.mobile.data)
        if form.created_time_begin.data:
            members = members.filter(Member.created_time >= form.created_time_begin.data)
        if form.created_time_end.data:
            members = members.filter(Member.created_time <= form.created_time_end.data)

    members = members.paginate(page=page, per_page=list_per_page)

    count_list = dict()
    for member in members.items:
        application_count = db.session.query(Application).filter_by(member_id=member.id).count()
        count_list[member.id.__str__()] = [application_count, ]
        # Log.info("{}  {}  {}".format(application_count, success_application_count, report_count))
    response_data = {
        'list': members,
        'form': form,
        'status_mapping': STATUS,
        'count_list': count_list,
    }
    return ops_render('manage/member/index.html', response_data)


@member_bp.route("/blocked_member", methods=['GET', 'POST'])
@member_bp.route("/blocked_member/<int:page>", methods=['GET', 'POST'])
@login_required
def blocked_member(page=1):
    list_per_page = current_app.config['MANAGEMENT_LIST_PER_PAGE']
    form = BlockedMemberSearchForm()
    if request.method == 'POST':
        if form.nickname.data and len(form.nickname.data) > 0:
            members = Member.query.filter_by(nickname=form.nickname.data).paginate(page=page, per_page=list_per_page)
        else:
            members = Member.query.paginate(page=page, per_page=list_per_page)
    else:
        members = Member.query.paginate(page=page, per_page=list_per_page)

    response_data = {
        'list': members,
        'form': form,
    }
    return ops_render('manage/member/blocked.html', response_data)


@member_bp.route("/enable_member/<string:uid>", methods=['GET'])
@login_required
def enable_member(uid=None):
    # ?????????????????????????????????
    if uid and len(uid) == 24:
        Member.query.filter(id=uid).update(status=0)
        flash('?????????????????????!')
        return redirect(url_for('manage_member.blocked_member'))
    else:
        abort(404)
