# -*- coding: utf-8 -*-
import sys
from flask import current_app, Blueprint, request, url_for, jsonify, flash, redirect
from flask_security import login_required
from common.helper import ops_render
from database import db
from main.models.loan import Product
from main.form import ProductForm
from common import Log

product_bp = Blueprint('manage_product', __name__,)


@product_bp.route("/list_product", methods=['GET'])
@product_bp.route("/list_product/<int:page>", methods=['GET'])
@login_required
def list_product(page=1):
    list_per_page = current_app.config['MANAGEMENT_LIST_PER_PAGE']
    form = ProductForm()
    products = Product.query.paginate(page=page, per_page=list_per_page)

    response_data = {
        'list': products,
        'form': form,
        # 'count_list': count_list,
        'filter': sys._getframe().f_code.co_name,
    }

    return ops_render('manage/product/index.html', response_data)


@product_bp.route("/add_product", methods=['POST'])
@login_required
def add_product():
    form = ProductForm()
    if request.method == 'POST' and form.validate():
        amount = form.amount.data
        terms = form.terms.data
        fees = form.fees.data
        fee_payment = form.fee_payment.data
        rate_per_month = form.rate_per_month.data

        new_product = Product(
            amount=amount,
            terms=terms,
            fees=fees,
            fee_payment=fee_payment,
            rate_per_month=rate_per_month
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Add new product successful.')
    else:
        flash('Add new product failed.')

    return redirect(url_for('manage_product.list_product'))


@product_bp.route("/delete_product/<int:product_id>", methods=['GET'])
@login_required
def delete_product(product_id=0):
    if product_id > 0:
        Product.query.filter_by(id=product_id).delete()
        db.session.commit()

        flash('Delete product successful.')
    return redirect(url_for('manage_product.list_product'))


@product_bp.route("/edit_product/<int:product_id>", methods=['GET'])
@login_required
def edit_product(product_id=0):
    form = ProductForm()
    product = None
    if product_id > 0:
        product = Product.query.filter_by(id=product_id).first()
        form.available.default = product.available
        form.fee_payment.default = product.fee_payment
        form.process()
        form.amount.data = product.amount
        form.terms.data = product.terms
        form.fees.data = product.fees
        form.rate_per_month.data = product.rate_per_month

    response_data = {
        'product': product,
        'form': form,
    }

    return ops_render('manage/product/edit.html', response_data)


@product_bp.route("/update_product/<int:product_id>", methods=['POST'])
@login_required
def update_product(product_id=0):
    form = ProductForm()
    if product_id > 0:
        product = Product.query.filter_by(id=product_id).first()
        if product and request.method == 'POST':
            if product.applications_count == 0 and form.validate():
                product.amount = form.amount.data
                product.terms = form.terms.data
                product.fees = form.fees.data
                product.fee_payment = form.fee_payment.data
                product.rate_per_month = form.rate_per_month.data
                product.available = form.available.data
                db.session.add(product)
                db.session.commit()
            else:
                product.available = form.available.data
                db.session.add(product)
                db.session.commit()
            flash('Update product successful.')
        else:
            flash('Update product failed.')
    return redirect(url_for('manage_product.list_product'))

