# -*- coding: utf-8 -*-
import requests
import json
import sys
import os.path as op
from pprint import pprint

# ROOT_PATH = 'http://127.0.0.1:5000'
ROOT_PATH = 'https://api.salaf.sa'


def test_member_login(national_id, password):
    url = ROOT_PATH + "/api/v1/member/login"
    params = {
        'national_id': national_id,
        'password': password,
    }
    # print(url)
    # headers = {"Content-Type": "application/text"}
    r = requests.post(url, data=params,)
    r.encoding = 'utf-8'
    return r.json()


def test_member_register(user_info):
    url = ROOT_PATH + "/api/v1/member/register"
    # print(url)
    # headers = {"Content-Type": "application/text"}
    r = requests.post(url, data=user_info,)
    r.encoding = 'utf-8'
    return r.json()


def test_user_auth(auth_info):
    url = ROOT_PATH + "/api/v1/member/auth?uid={}&token={}".format(auth_info['uid'], auth_info['token'])
    # headers = {"Content-Type": "application/text"}
    #r = requests.post(url, data=params,)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def test_user_info(auth_info):
    url = ROOT_PATH + "/api/v1/member/info?uid={}&token={}".format(auth_info['uid'], auth_info['token'])
    #r = requests.post(url, data=params,)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def test_user_debit(auth_info, debit_info):
    url = ROOT_PATH + "/api/v1/member/debit?uid={}&token={}".format(auth_info['uid'], auth_info['token'])
    #r = requests.post(url, data=params,)
    r = requests.post(url, data=debit_info,)
    r.encoding = 'utf-8'
    return r.json()


def test_user_apply(auth_info, application_info):
    url = ROOT_PATH + "/api/v1/loan/application?uid={}&token={}".format(auth_info['uid'], auth_info['token'])
    #r = requests.post(url, data=params,)
    r = requests.post(url, data=application_info,)
    r.encoding = 'utf-8'
    return r.json()


def test_user_applications_get(auth_info):
    url = ROOT_PATH + "/api/v1/loan/application?uid={}&token={}".format(auth_info['uid'], auth_info['token'])
    #r = requests.post(url, data=params,)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def test_user_applications_get_by_id(auth_info, application_id):
    url = ROOT_PATH + "/api/v1/loan/application?uid={}&token={}&application_id={}".format(auth_info['uid'], auth_info['token'], application_id)
    #r = requests.post(url, data=params,)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def test_loan_policy():
    url = ROOT_PATH + "/api/v1/loan/policy"
    #r = requests.post(url, data=params,)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def test_loan_products_list(auth_info):
    url = ROOT_PATH + "/api/v1/loan/products_list?uid={}&token={}".format(auth_info['uid'], auth_info['token'])
    #r = requests.post(url, data=params,)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def test_installments():
    url = ROOT_PATH + "/api/v1/loan/installment_detail?amount=10000&term=6&apr=5.3&method=A"
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def test_installments_new(auth_info, product_id):
    url = ROOT_PATH + "/api/v1/loan/product_installments?uid={}&token={}&product_id={}".format(auth_info['uid'], auth_info['token'], product_id)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def test_repayment(auth_info, application_id, sequence):
    url = ROOT_PATH + "/api/v1/loan/repayment?uid={}&token={}".format(auth_info['uid'], auth_info['token'])
    params = {
        'application_id': application_id,
        'sequence': sequence,
    }
    r = requests.post(url, data=params)
    r.encoding = 'utf-8'
    return r.json()


def test_repayment_list(auth_info):
    url = ROOT_PATH + "/api/v1/loan/repayment_list?uid={}&token={}".format(auth_info['uid'], auth_info['token'])
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.json()


def post_image(filename=''):
    # url = 'http://127.0.0.1:5000/api/v1/upload'
    url = ROOT_PATH + "/manage/summernote"
    (filepath, tempfilename) = op.split(filename);
    if len(tempfilename) > 1:
        files = {
            'file': (tempfilename, open(filename, 'rb'), 'image/png', {})
        }
        res = requests.request("POST", url, data={'width': 0, 'height': 0}, files=files)
        print(res.text)


if __name__ == '__main__':
    #fn = sys.argv[1]
    #post_image(fn)

    user_info1 = {
        'national_id': '1081383137',
        'password': '123456',
        'mobile': '13911155577',
        'language': 'English',
        'birthday': '06/06/1414',
    }

    user_info2 = {
        'national_id': '2175836777',
        'password': '123456',
        'mobile': '13911155577',
        'language': 'English',
        'birthday': '06/06/1995',
    }

    """
    user_info = {
        'national_id': '20210522',
        'password': 'helloworld',
        'mobile': '13911155577',
        'language': 'zh_CN',
        'birthday': '11/01/1999',
    }
    """
    debit_info = {
        'name': 'James1 Hardan',
        'number': '9191372910211'
    }


    application_info = {
        # 'amount': 10000,
        # 'term': 6,
        # 'apr': 5.5,
        # 'method': 'A'
        'product_id': 9
    }
    user_token = test_member_register(user_info1)
    # user_token = test_member_login(user_info['national_id'], user_info['password'])
    pprint(user_token)
    #user_token = test_user_auth(user_token['data'])
    #pprint(user_token)
    #resp_data = test_user_info(user_token['data'])
    #pprint(resp_data)
    #resp_data = test_user_debit(user_token['data'], debit_info)
    #pprint(resp_data)
    #resp_data = test_loan_policy()
    #pprint(resp_data)
    #resp_data = test_installments()
    #pprint(resp_data)



    #resp_data = test_loan_products_list(user_token['data'])
    #pprint(resp_data)
    #for product in resp_data['data']['products']:
    #    resp_data = test_installments_new(user_token['data'], product['id'])
    #    pprint(resp_data)

    #resp_data = test_user_apply(user_token['data'], application_info)
    #pprint(resp_data)
    #resp_data = test_user_applications_get(user_token['data'])
    #pprint(resp_data)
    #for application in resp_data['data']['applications']:
    #    resp_data = test_user_applications_get_by_id(user_token['data'], application_id=application['id'])
    #    pprint(resp_data)

    #resp_data = test_repayment(user_token['data'], application_id=3, sequence=1)
    #pprint(resp_data)
    """
    user_token = {
        'code': 0,
        'data': {
            'token': 'dba0c87473f2e7461d5b702ff6f25f3e',
            'uid': 2,
        }
    }
    """
    #resp_data = test_repayment_list(user_token['data'])
    #pprint(resp_data)
