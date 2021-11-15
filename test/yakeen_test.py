# -*- coding: utf-8 -*-
from suds.client import Client
from suds.sudsobject import asdict
from suds import WebFault
from suds.transport import TransportError
import sys
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)

sap_url = "https://yakeen-piloting.eserve.com.sa/Yakeen4Gccpay/Yakeen4Gccpay?wsdl"

myheaders = dict(username='Gccpay_PILOT_USR', password='Gccpay@39077')
yk_client = Client(sap_url)
yk_client.set_options(soapheaders=myheaders)
#print(yk_client)

#response = yk_client.service.getCitizenInfo()
#print(response)

citizenInfoRequest = yk_client.factory.create("citizenInfoRequest")
nin = '1081383117'
birthday = '12-1414'
citizenInfoRequest.chargeCode = 'PILOT'
citizenInfoRequest.dateOfBirth = birthday # '1997-11-01'
citizenInfoRequest.nin = nin  # '1101193801'
citizenInfoRequest.password = 'Gccpay@39077'
citizenInfoRequest.userName = 'Gccpay_PILOT_USR'
citizenInfoRequest.referenceNumber = 'loan'


getCitizenInfo_request_string = \
"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:yak="http://yakeenforgccpay.yakeen.elm.com/">
     <soapenv:Header>
     </soapenv:Header>
     <soapenv:Body>
          <yak:getCitizenInfo>
               <CitizenInfoRequest>
                    <userName>Gccpay_PILOT_USR</userName>
                    <password>Gccpay@39077</password>
                    <chargeCode>PILOT</chargeCode>
                    <nin>{}</nin>
                    <dateOfBirth>{}</dateOfBirth>
                    <referenceNumber>loan</referenceNumber>
               </CitizenInfoRequest>
          </yak:getCitizenInfo>
     </soapenv:Body>
</soapenv:Envelope>"""

#print(getCitizenInfo_request_string)
#yk_client.service.getCitizenInfo(citizenInfoRequest)
try:
        yk_client.service.getCitizenInfo(__inject={'msg':bytes(getCitizenInfo_request_string.format(nin,birthday), encoding='utf-8')})
except (WebFault, TransportError) as e:
        print(e)


#response = yk_client.service.getAlienInfoByIqama()
#print(response)

getAlienInfoByIqamaRequest = yk_client.factory.create("getAlienInfoByIqama")
iqamaNumber = '2475836777'
birthday = '08-1983'
getAlienInfoByIqamaRequest.chargeCode = 'PILOT'
getAlienInfoByIqamaRequest.dateOfBirth = birthday  # '1997-11-01'
getAlienInfoByIqamaRequest.iqamaNumber = iqamaNumber # '1101193801'
getAlienInfoByIqamaRequest.password = 'Gccpay@39077'
getAlienInfoByIqamaRequest.userName = 'Gccpay_PILOT_USR'
getAlienInfoByIqamaRequest.referenceNumber = 'loan'


getAlienInfoByIqama_request_string = \
"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:yak="http://yakeenforgccpay.yakeen.elm.com/">
     <soapenv:Header>
     </soapenv:Header>
     <soapenv:Body>
          <yak:getAlienInfoByIqama>
               <AlienInfoByIqamaRequest>
                    <userName>Gccpay_PILOT_USR</userName>
                    <password>Gccpay@39077</password>
                    <chargeCode>PILOT</chargeCode>
                    <iqamaNumber>{}</iqamaNumber>
                    <dateOfBirth>{}</dateOfBirth>
                    <referenceNumber>loan</referenceNumber>
               </AlienInfoByIqamaRequest>
          </yak:getAlienInfoByIqama>
     </soapenv:Body>
</soapenv:Envelope>"""

#print(getAlienInfoByIqama_request_string)
#yk_client.service.getAlienInfoByIqama(getAlienInfoByIqamaRequest)
try:
        yk_client.service.getAlienInfoByIqama(__inject={'msg':bytes(getAlienInfoByIqama_request_string.format(iqamaNumber,birthday), encoding='utf-8')})
except (WebFault,TransportError) as e:
        print(e)