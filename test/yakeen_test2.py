# -*- coding: utf-8 -*-
from suds.client import Client
from suds import WebFault
#from suds.sudsobject import asdict
#from suds.transport import TransportError
import json
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.INFO)

sap_url = "https://yakeen-piloting.eserve.com.sa/Yakeen4Gccpay/Yakeen4Gccpay?wsdl"

myheaders = dict(username='Gccpay_PILOT_USR', password='Gccpay@39077')
yk_client = Client(sap_url)
yk_client.set_options(timeout=20)
#yk_client.set_options(soapheaders=myheaders)
#print(yk_client)
#sys.exit()
#print("#"*80)
user_info = dict()
user_address_info = dict()

nin = '1081383117'
birthday = '12-1414'
citizenInfoRequest = yk_client.factory.create("citizenInfoRequest")
citizenInfoRequest.chargeCode = 'PILOT'
citizenInfoRequest.dateOfBirth = birthday  # '1997-11-01'
citizenInfoRequest.nin = nin  # '1101193801'
citizenInfoRequest.password = 'Gccpay@39077'
citizenInfoRequest.userName = 'Gccpay_PILOT_USR'
citizenInfoRequest.referenceNumber = 'loan'
try:
    rs_CitizenInfo = yk_client.service.getCitizenInfo(citizenInfoRequest)
    user_info.clear()
    for key in rs_CitizenInfo.__keylist__:
        user_info[key] = rs_CitizenInfo[key]
    print("#" * 150)
    # print(user_info)
    print(json.dumps(user_info))
    print("#" * 150)
except WebFault as e:
    print(e.__str__())

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
try:
    rs_CitizenAddressInfo = yk_client.service.getCitizenAddressInfo(citizenAddressInfoRequest)
    user_address_info.clear()
    print("#"*150)
    for key in rs_CitizenAddressInfo.__keylist__:
        if isinstance(rs_CitizenAddressInfo[key], list):
            user_address_detail = list()
            for v in rs_CitizenAddressInfo[key]:
                if hasattr(v, '__keylist__') and hasattr(v, '__iter__'):
                    user_address_detail.append({add_key: v[add_key] for add_key in v.__keylist__})
            user_address_info[type(v).__name__] = user_address_detail
        else:
            user_address_info[key] = rs_CitizenAddressInfo[key]
    print(json.dumps(user_address_info))
    # print(user_address_info)
    print("#"*150)
except WebFault as e:
    print(e)

getAlienInfoByIqamaRequest = yk_client.factory.create("alienInfoByIqamaRequest")
iqamaNumber = '2475836777'
birthday = '08-1983'
getAlienInfoByIqamaRequest.chargeCode = 'PILOT'
getAlienInfoByIqamaRequest.dateOfBirth = birthday  # '1997-11-01'
getAlienInfoByIqamaRequest.iqamaNumber = iqamaNumber  # '1101193801'
getAlienInfoByIqamaRequest.password = 'Gccpay@39077'
getAlienInfoByIqamaRequest.userName = 'Gccpay_PILOT_USR'
getAlienInfoByIqamaRequest.referenceNumber = 'loan'
try:
    rs_AlienInfo = yk_client.service.getAlienInfoByIqama(getAlienInfoByIqamaRequest)
    user_info.clear()
    for key in rs_AlienInfo.__keylist__:
        user_info[key] = rs_AlienInfo[key]
    print("#"*150)
    # print(user_info)
    print(json.dumps(user_info))
    print("#"*150)
except WebFault as e:
    print(e)

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
try:
    rs_AlienAddressInfo = yk_client.service.getAlienAddressInfo(getAlienAddressInfoRequest)
    user_address_info.clear()
    print("#"*150)
    for key in rs_AlienAddressInfo.__keylist__:
        if isinstance(rs_AlienAddressInfo[key], list):
            user_address_detail = list()
            for v in rs_AlienAddressInfo[key]:
                if hasattr(v, '__keylist__') and hasattr(v, '__iter__'):
                    user_address_detail.append({add_key: v[add_key] for add_key in v.__keylist__})
            user_address_info[type(v).__name__] = user_address_detail
        else:
            user_address_info[key] = rs_AlienAddressInfo[key]
    print(json.dumps(user_address_info))
    # print(user_address_info)
    print("#"*150)
except WebFault as e:
    print(e)
