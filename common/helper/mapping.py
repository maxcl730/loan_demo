# -*- coding: utf-8 -*-
from flask_restful import fields
from common.date import Date

SEX = [
    (0, 'Unknown'),
    (1, 'male'),
    (2, 'female'),
]

STATUS = [(100, 'all'),
          (1, 'active'),
          (2, 'banned')]

RUNNING_STATUS_WITH_APPLICATION = [
    (100, 'All'),
    (0, 'Pending'),
    (1, 'Approved'),
    (2, 'Rejected')
]

PUBLISH_STATUS = [
    (100, '全部'),
    (0, '未发布'),
    (1, '已发布'),
    (2, '发布申请名单'),
]


class TimestampValue(fields.Raw):
    def format(self, value):
        return Date.datetime_toTimestamp(value)
