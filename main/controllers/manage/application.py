# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from flask import current_app, Blueprint, request, abort, jsonify, flash, redirect
from flask_security import login_required
from common.helper import ops_render
from main.models.member import Member
from main.models.application import Application
from main.form import ApplicationSearchForm
from common import Log

application_bp = Blueprint('manage_application', __name__,)
