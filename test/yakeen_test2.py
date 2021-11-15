# -*- coding: utf-8 -*-
from suds.client import Client
#from suds.sudsobject import asdict
#from suds import WebFault
#from suds.transport import TransportError
import sys
import json
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.INFO)

sap_url = "https://yakeen-piloting.eserve.com.sa/Yakeen4Gccpay/Yakeen4Gccpay?wsdl"

myheaders = dict(username='Gccpay_PILOT_USR', password='Gccpay@39077')
yk_client = Client(sap_url)
#yk_client.set_options(soapheaders=myheaders)
#print(yk_client)
#sys.exit()
#print("#"*80)

citizenInfoRequest = yk_client.factory.create("citizenInfoRequest")
nin = '1081383117'
birthday = '12-1414'
citizenInfoRequest.chargeCode = 'PILOT'
citizenInfoRequest.dateOfBirth = birthday # '1997-11-01'
citizenInfoRequest.nin = nin  # '1101193801'
citizenInfoRequest.password = 'Gccpay@39077'
citizenInfoRequest.userName = 'Gccpay_PILOT_USR'
citizenInfoRequest.referenceNumber = 'loan'

rs_CitizenInfo = yk_client.service.getCitizenInfo(citizenInfoRequest)
user_info = dict()
for key in rs_CitizenInfo.__keylist__:
    user_info[key] = rs_CitizenInfo[key]
print("#"*200)
#print(user_info)
print(json.dumps(user_info))
print("#"*200)

citizenAddressInfoRequest = yk_client.factory.create("citizenAddressInfoRequest")
nin = '1081383117'
birthday = '12-1414'
citizenAddressInfoRequest.chargeCode = 'PILOT'
citizenAddressInfoRequest.dateOfBirth = birthday  # '1997-11-01'
citizenAddressInfoRequest.nin = nin  # '1101193801'
citizenAddressInfoRequest.password = 'Gccpay@39077'
citizenAddressInfoRequest.userName = 'Gccpay_PILOT_USR'
citizenAddressInfoRequest.referenceNumber = 'loan'
citizenAddressInfoRequest.addressLanguage = 'E'

rs_CitizenAddressInfo = yk_client.service.getCitizenAddressInfo(citizenAddressInfoRequest)
#print(rs_CitizenAddressInfo)
user_address_info = dict()
print("#"*200)
for key in rs_CitizenAddressInfo.__keylist__:
    user_address_info[key] = rs_CitizenAddressInfo[key]
    if isinstance(user_address_info[key], list):
        for v in user_address_info[key]:
            user_address_info[type(v).__name__] = list()
            user_address_detail = dict()
            if hasattr(v, '__keylist__') and hasattr(v, '__iter__'):
                user_address_detail = {add_key: v[add_key] for add_key in v.__keylist__}
                #user_address_detail['class'] = type(v).__name__
                user_address_info[type(v).__name__].append(user_address_detail)
#print(rs_CitizenAddressInfo)
print(json.dumps(user_address_info))
#print(user_address_info)
print("#"*200)

getAlienInfoByIqamaRequest = yk_client.factory.create("alienInfoByIqamaRequest")
iqamaNumber = '2475836777'
birthday = '08-1983'
getAlienInfoByIqamaRequest.chargeCode = 'PILOT'
getAlienInfoByIqamaRequest.dateOfBirth = birthday  # '1997-11-01'
getAlienInfoByIqamaRequest.iqamaNumber = iqamaNumber  # '1101193801'
getAlienInfoByIqamaRequest.password = 'Gccpay@39077'
getAlienInfoByIqamaRequest.userName = 'Gccpay_PILOT_USR'
getAlienInfoByIqamaRequest.referenceNumber = 'loan'

rs_AlienInfo = yk_client.service.getAlienInfoByIqama(getAlienInfoByIqamaRequest)
user_info = dict()
for key in rs_AlienInfo.__keylist__:
    user_info[key] = rs_AlienInfo[key]
print("#"*200)
#print(user_info)
print(json.dumps(user_info))
print("#"*200)

getAlienAddressInfoRequest = yk_client.factory.create("alienAddressInfoRequest")
iqamaNumber = '2475836777'
birthday = '08-1983'
getAlienAddressInfoRequest.chargeCode = 'PILOT'
getAlienAddressInfoRequest.dateOfbirth = birthday  # '1997-11-01'
getAlienAddressInfoRequest.iqamaNumber = iqamaNumber  # '1101193801'
getAlienAddressInfoRequest.password = 'Gccpay@39077'
getAlienAddressInfoRequest.userName = 'Gccpay_PILOT_USR'
getAlienAddressInfoRequest.referenceNumber = 'loan'
getAlienAddressInfoRequest.addressLanguage = 'E'

rs_AlienAddressInfo = yk_client.service.getAlienAddressInfo(getAlienAddressInfoRequest)
user_address_info = dict()
print("#"*200)
for key in rs_AlienAddressInfo.__keylist__:
    user_address_info[key] = rs_AlienAddressInfo[key]
    if isinstance(user_address_info[key], list):
        for v in user_address_info[key]:
            user_address_info[type(v).__name__] = list()
            user_address_detail = dict()
            if hasattr(v, '__keylist__') and hasattr(v, '__iter__'):
                user_address_detail = {add_key: v[add_key] for add_key in v.__keylist__}
                #user_address_detail['class'] = type(v).__name__
                user_address_info[type(v).__name__].append(user_address_detail)
#print(json.dumps(user_address_info))
print(json.dumps(user_address_info))
print("#"*200)
