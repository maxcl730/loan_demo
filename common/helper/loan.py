# -*- coding: utf-8 -*-
import json
from os import path as op
from dateutil.relativedelta import relativedelta
from sympy import solve
from sympy import abc


class MonthInstallment:
    """
    按月的分期付款计算，按月息为计息周期，一般常用的方式有等额本金和等额本息
    """

    def __init__(self, corpus, periods, y_rate, first_period_rate=1.0, method='A'):
        """
        .   @param corpus 本金.
        .   @param periods 期数 即还款一共分期几个月.
        .   @param y_rate 年化利率 我们一般以年化来讨论.
        .   @param first_period_rate 第一个周期月的倍率，恰好为整月时是1.
        """
        self.m_rate = y_rate / 12  # 月利率
        self.corpus = corpus  # 本金
        self.periods = periods  # 期数
        self.method = method  # 分期方式，默认为A：equal_amortization
        self.first_period_rate = first_period_rate  # 第一周期月的倍率
        self.m_corpus_return = corpus / periods  # 每期应还本金
        self.return_li = []  # 应还列表

    def info(self):
        if self.method == 'A':
            return "corpus:{},  terms:{},  apr:{:.4f}%, method:{}".format(self.corpus, self.periods, self.m_rate * 12, "Equal amortization")
        elif self.method == 'B':
            return "corpus:{},  terms:{},  apr:{:.4f}%, method:{}".format(self.corpus, self.periods, self.m_rate * 12, "Equal principle payment")

    @staticmethod
    def loan_policy():
        # 返回小贷规则
        json_path = op.dirname(op.abspath(__file__)) + "/../../main/loan_policy.json"
        with open(json_path) as f:
            policy = json.load(f, encoding='utf8')
        if type(policy) is dict:
            return policy
        else:
            return None

    def equal_amortization(self):
        """
        等额本息，比较常用，似乎是贷款的默认计算方式，无论银行还是网贷主要应用等额本息
        方法A
        """
        left_ = self.corpus * (1 + self.m_rate) ** self.first_period_rate - abc.x  # 剩余应还本息，这里先计算第一个月
        for i in range(1, self.periods):
            left_ = left_ * (1 + self.m_rate) - abc.x  # abc.x为未知数：每月应还金额，注意到等额本息每期金额是一样的
        return_x = solve(left_, [abc.x])  # 解方程剩余应还金额为0，求得未知数abc.x
        self.return_li = [round(return_x[0] * 100)/100.0 for x in range(self.periods)]
        return self.return_li

    def equal_principle_payment(self):
        """
        等额本金
        方法B
        """
        return_interest_li, left_ = [], self.corpus
        for i in range(self.periods):
            return_interest_li += [left_ * self.m_rate]  # 每期对应的利息，注意等额本金是每期都把利息还完了
            left_ -= self.m_corpus_return  # 剩余应还本息，相当于只考虑本金部分每期应还的部分
        return_interest_li[0] *= self.first_period_rate  # 对第一个月的应还利息做first_period_rate的修正
        self.return_li = [round((x + self.m_corpus_return) * 100)/100.0 for x in return_interest_li]
        return self.return_li

    def installments(self, start_date):
        # 格式化每月的费用
        # 从起始日开始，每一个月还款一次
        if self.method == 'A':
            fee_list = self.equal_amortization()
        elif self.method == 'B':
            fee_list = self.equal_principle_payment()
        else:
            return None
        installments_detail = list()
        for i in range(0, self.periods):
            installments_detail.append({
                'sequence': i+1,
                'date': start_date + relativedelta(months=i+1),
                'fee': fee_list[i]
            })
        return installments_detail
