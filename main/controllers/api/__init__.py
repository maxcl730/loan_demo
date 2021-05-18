# -*- coding: utf-8 -*-
from .member import MemberLoginApi, MemberAuthApi, MemberRegisterApi, MemberInfoApi, MemberDebitApi
from .loan import LoanPolicyApi, InstallmentsDetailApi
from .application import LoanApplicationApi
#from .homepage import HomepageApi


def api_setup(api=None):
    if not api:
        return False

    api.add_resource(
        MemberLoginApi,
        '/member/login',
        endpoint='api_member_login'
    )

    api.add_resource(
        MemberAuthApi,
        '/member/auth',
        endpoint='api_member_auth'
    )

    api.add_resource(
        MemberRegisterApi,
        '/member/register',
        endpoint='api_member_register'
    )

    api.add_resource(
        MemberInfoApi,
        '/member/info',
        endpoint='api_member_info'
    )

    api.add_resource(
        MemberDebitApi,
        '/member/debit',
        endpoint='api_member_debit'
    )

    api.add_resource(
        LoanPolicyApi,
        '/loan/policy',
        endpoint='api_loan_policy'
    )

    api.add_resource(
        InstallmentsDetailApi,
        '/loan/installment_detail',
        endpoint='api_loan_installment_detail'
    )

    api.add_resource(
        LoanApplicationApi,
        '/loan/application',
        endpoint='api_loan_application'
    )
