# -*- coding: utf-8 -*-
from suds.client import Client
from suds import WebFault
# from suds.sudsobject import asdict
# from suds.transport import TransportError
from flask import current_app
from concurrent.futures import ThreadPoolExecutor
from common import Log

# import logging
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.INFO)
# logging.getLogger('suds.transport').setLevel(logging.INFO)


class YakeenCredit:
    user_info = dict()
    user_address = {'Arabic': dict(), 'English': dict()}
    language_sign_map = {'A': 'Arabic', 'E': 'English'}
    executor = ThreadPoolExecutor(2)

    def __init__(self, national_id, birthday):
        self.yk_client = Client(current_app.config['YAKEEN_SOAP_URL'])
        self.yk_client.set_options(timeout=20)
        self.username = current_app.config['YAKEEN_SOAP_USERNAME']
        self.password = current_app.config['YAKEEN_SOAP_PASSWORD']
        self.chargecode = current_app.config['YAKEEN_SOAP_CHARGECODE']
        self.referenceNumber = current_app.config['YAKEEN_SOAP_REFERENCENUMBER']

        self.member_national_id = national_id
        self.member_birthday = birthday.replace('/', '-')[3:]

    def verify_member_info(self):
        # 获取会员信用信息
        # is it citizen or alien
        if self.member_national_id[0:1] == '1':
            # citizen
            # for test
            self.member_national_id = '1081383117'
            self.member_birthday = '12-1414'
            if self.citizen_info():
                return self.user_info
        elif self.member_national_id[0:1] == '2':
            # alien
            # for test
            self.member_national_id = '2475836777'
            self.member_birthday = '08-1983'
            if self.alien_info():
                return self.user_info
        else:
            # error national_id
            return None

    def verify_member_address(self):
        # 获取会员地址信息
        # is it citizen or alien
        if self.member_national_id[0:1] == '1':
            # citizen
            # for test
            self.member_national_id = '1081383117'
            self.member_birthday = '12-1414'
            self.citizen_address(language_sign='A')
            self.citizen_address(language_sign='E')
            return self.user_address
        elif self.member_national_id[0:1] == '2':
            # alien
            # for test
            self.member_national_id = '2475836777'
            self.member_birthday = '08-1983'
            self.alien_address(language_sign='A')
            self.alien_address(language_sign='E')
            return self.user_address
        else:
            # error national_id
            return None

    def citizen_info(self):
        self.user_info.clear()
        req = self.yk_client.factory.create("citizenInfoRequest")
        req.dateOfBirth = self.member_birthday
        req.nin = self.member_national_id
        req.chargeCode = self.chargecode
        req.password = self.password
        req.userName = self.username
        req.referenceNumber = self.referenceNumber
        try:
            rs = self.yk_client.service.getCitizenInfo(req)
            for key in rs.__keylist__:
                self.user_info[key] = rs[key]

            # Log.info(self.user_info)
            return True
        except WebFault as e:
            Log.warn(e.__str__())
            return False

    def citizen_address(self, language_sign='E'):
        self.user_address[self.language_sign_map[language_sign]].clear()
        req = self.yk_client.factory.create("citizenAddressInfoRequest")
        req.dateOfBirth = self.member_birthday
        req.nin = self.member_national_id
        req.chargeCode = self.chargecode
        req.password = self.password
        req.userName = self.username
        req.referenceNumber = self.referenceNumber
        req.addressLanguage = language_sign
        try:
            rs = self.yk_client.service.getCitizenAddressInfo(req)
            for key in rs.__keylist__:
                if isinstance(rs[key], list):
                    user_address_detail = list()
                    v = None
                    for v in rs[key]:
                        if hasattr(v, '__keylist__') and hasattr(v, '__iter__'):
                            user_address_detail.append({add_key: v[add_key] for add_key in v.__keylist__})
                    if v:
                        self.user_address[self.language_sign_map[language_sign]][type(v).__name__] = user_address_detail
                else:
                    self.user_address[self.language_sign_map[language_sign]][key] = rs[key]

            # Log.info(self.user_address)
            return True
        except WebFault as e:
            Log.warn(e.__str__())
            return False

    def alien_info(self):
        self.user_info.clear()
        req = self.yk_client.factory.create("alienInfoByIqamaRequest")
        req.dateOfBirth = self.member_birthday
        req.iqamaNumber = self.member_national_id
        req.chargeCode = self.chargecode
        req.password = self.password
        req.userName = self.username
        req.referenceNumber = self.referenceNumber
        try:
            rs = self.yk_client.service.getAlienInfoByIqama(req)
            for key in rs.__keylist__:
                self.user_info[key] = rs[key]

            # Log.info(self.user_info)
            return True
        except WebFault as e:
            Log.warn(e.__str__())
            return False

    def alien_address(self, language_sign='E'):
        self.user_address[self.language_sign_map[language_sign]].clear()
        req = self.yk_client.factory.create("alienAddressInfoRequest")
        req.dateOfbirth = self.member_birthday
        req.iqamaNumber = self.member_national_id
        req.chargeCode = self.chargecode
        req.password = self.password
        req.userName = self.username
        req.referenceNumber = self.referenceNumber
        req.addressLanguage = language_sign
        try:
            rs = self.yk_client.service.getAlienAddressInfo(req)
            for key in rs.__keylist__:
                if isinstance(rs[key], list):
                    user_address_detail = list()
                    v = None
                    for v in rs[key]:
                        if hasattr(v, '__keylist__') and hasattr(v, '__iter__'):
                            user_address_detail.append({add_key: v[add_key] for add_key in v.__keylist__})
                    if v:
                        self.user_address[self.language_sign_map[language_sign]][type(v).__name__] = user_address_detail
                else:
                    self.user_address[self.language_sign_map[language_sign]][key] = rs[key]

            # Log.info(self.user_address)
            return True
        except WebFault as e:
            Log.warn(e.__str__())
            return False
