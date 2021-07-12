# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DecimalField, SelectField, RadioField, TextAreaField,  SubmitField, PasswordField
from wtforms_components import DateTimeField, DateRange, Email
from wtforms.validators import DataRequired, Required, Length, EqualTo, NumberRange
# from flask_wtf.file import FileRequired, FileAllowed
from common.helper.mapping import STATUS, RUNNING_STATUS_WITH_APPLICATION


class CustomForm(Form):
    class Meta(Form.Meta):
        """
        重写render_field，实现Flask-Bootstrap与render_kw的class并存
        """

        def render_field(self, field, render_kw):
            other_kw = getattr(field, 'render_kw', None)
            if other_kw is not None:
                class1 = other_kw.get('class', None)
                class2 = render_kw.get('class', None)
                if class1 and class2:
                    render_kw['class'] = class2 + ' ' + class1
                render_kw = dict(other_kw, **render_kw)
            return field.widget(field, **render_kw)


class ProductForm(CustomForm):
    amount = IntegerField(label='Amount',
                          validators=[DataRequired(), NumberRange(min=100, max=50000)],
                          default=300,
                          render_kw={
                              "class": 'input-sm',
                              "type": 'number',
                              "step": '100',
                              # "readonly": 'True'
                          })
    terms = IntegerField(label='Terms',
                         validators=[DataRequired(), NumberRange(min=1, max=120)],
                         default=3,
                         render_kw={
                            "class": 'input-sm',
                            "type": 'number'
                         })
    fees = DecimalField(label='Fees',
                        places=2,
                        default=0,
                        validators=[DataRequired(), NumberRange(min=0)],
                        render_kw={
                            "class": 'input-sm',
                            "type": 'number',
                            "step": '0.01',
                        })
    fee_payment = RadioField('fee_payment',
                             choices=[(1, 'pre-paid'), (2, 'post-paid')],
                             validators=[DataRequired()],
                             coerce=int,
                             default=1,
                             )

    rate_per_month = DecimalField(label='Rate/Month',
                                  places=2,
                                  default=0,
                                  validators=[DataRequired(), NumberRange(min=0)],
                                  render_kw={
                                      "class": 'input-sm',
                                      "type": "number",
                                      "step": "0.01",
                                  })
    available = RadioField('available',
                           choices=[(0, 'No'), (1, 'Yes')],
                           coerce=int,
                           default=0,
                           )
    submit = SubmitField('Submit',
                         render_kw={
                             'class': 'btn btn-info'
                         })


class MemberSearchForm(CustomForm):
    """
    status = SelectField(label='Status',
                         coerce=int,
                         choices=STATUS,
                         render_kw={
                             "class": 'input-sm',
                             "style": '"width: 90px"'
                         })
    """
    mobile = StringField('Mobile',
                         render_kw={
                             "class": 'input-sm'
                         })
    national_id = StringField('National ID',
                           render_kw={
                               "class": 'input-sm'
                           })
    created_time_begin = DateTimeField('Created at (from)',
                                       validators=[DateRange(
                                            min=datetime(2019, 1, 1),
                                            max=datetime(2029, 12, 12)
                                       )],
                                       format='%Y-%m-%d',
                                       render_kw={
                                           "placeholder": "begin",
                                           "class": "input-sm",
                                           "type": "input",
                                           "autocomplete": "off",
                                       })
    created_time_end = DateTimeField('to',
                                     validators=[DateRange(
                                           min=datetime(2019, 1, 1),
                                           max=datetime(2029, 12, 12)
                                     )],
                                     format='%Y-%m-%d',
                                     render_kw={
                                         "placeholder": "end",
                                         "class": "input-sm",
                                         "type": "input",
                                         "autocomplete": "off",
                                     })


class BlockedMemberSearchForm(CustomForm):
    nickname = StringField('昵称',
                           render_kw={
                               "class": 'input-sm'
                           })
    username = StringField('姓名',
                           render_kw={
                               "class": 'input-sm'
                           })


class EditRuleForm(CustomForm):
    content = TextAreaField('规则说明',
                            validators=[Required()],
                            render_kw={
                                'class': 'form-control',
                                'rows': '15'
                            })
    submit = SubmitField('提交',
                         render_kw={
                             'class': 'btn btn-info'
                         })


class ApplicationSearchForm(CustomForm):
    national_id = StringField('用户昵称',
                     render_kw={
                         "class": 'input-sm',
                       })
    mobile = StringField('手机号',
                         render_kw={
                             "class": 'input-sm'
                         })
    # 申请状态
    status = SelectField('申请状态',
                        coerce=int,
                        choices=RUNNING_STATUS_WITH_APPLICATION,
                        render_kw={
                          "class": 'input-sm',
                          "style": '"width: 90px"'
                        })
    created_time_begin = DateTimeField('开始时间',
                                       validators=[DateRange(
                                           min=datetime(2019, 1, 1),
                                           max=datetime(2029, 12, 12)
                                       )],
                                       format='%Y-%m-%d',
                                       render_kw={
                                           "placeholder": "Begin",
                                           "class": "input-sm",
                                           "type": "input",
                                           "autocomplete": "off",
                                       })
    created_time_end = DateTimeField('结束时间',
                                     validators=[DateRange(
                                         min=datetime(2019, 1, 1),
                                         max=datetime(2029, 12, 12)
                                     )],
                                     format='%Y-%m-%d',
                                     render_kw={
                                         "placeholder": "End",
                                         "class": "input-sm",
                                         "type": "input",
                                         "autocomplete": "off",
                                     })


class UserForm(CustomForm):
    email = StringField(label='Email',
                        validators=[DataRequired(message="邮箱不能为空"), Email(message="邮箱格式不正确")],
                        description='用户使用邮箱登录管理系统',
                        render_kw={
                            "required": "1",
                            "placeholder": "输入邮箱",
                            "class": "form-control",
                            "type": "input",
                            },
                        )
    name = StringField(label='姓名',
                       validators=[DataRequired(), Length(min=1, max=30)],
                       render_kw={
                            "required": "1",
                            "placeholder": "输入姓名",
                            "class": "form-control",
                            "type": "input",
                            },
                       )
    passwd = PasswordField(label='密码',
                           validators=[DataRequired(message="密码不能为空")],
                           render_kw={
                               "required": "1",
                               "placeholder": "输入密码",
                               "class": "form-control",
                               "type": "password",
                               },
                           )
    confirm_passwd = PasswordField(label='确认密码',
                                   validators=[DataRequired(message="确认密码不能为空"), EqualTo('passwd',message="两次密码不一致")],
                                   render_kw={
                                       "required": "1",
                                       "placeholder": "再次输入密码",
                                       "class": "form-control",
                                       "type": "password",
                                       },
                           )
    submit = SubmitField('提交',
                         render_kw={
                             'class': 'btn btn-info'
                         })


class UserPasswdForm(CustomForm):
    passwd = PasswordField(label='密码',
                           validators=[DataRequired(message="密码不能为空")],
                           render_kw={
                               "required": "1",
                               "placeholder": "输入密码",
                               "class": "form-control",
                               "type": "password",
                               },
                           )
    confirm_passwd = PasswordField(label='确认密码',
                                   validators=[DataRequired(message="确认密码不能为空"), EqualTo('passwd',message="两次密码不一致")],
                                   render_kw={
                                       "required": "1",
                                       "placeholder": "再次输入密码",
                                       "class": "form-control",
                                       "type": "password",
                                       },
                           )
    submit = SubmitField('提交',
                         render_kw={
                             'class': 'btn btn-info'
                         })
