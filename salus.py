import requests
import xmltodict
import pprint


HOST = 'https://salus-api.arrayent.com:8081'

class SalusAPI:

    def __init__(self, credentials):
        self._token = None
        self._device_info = None
        self._device = None
        self._credentials = credentials

    def credentials(self):
        return {
            'appId': 1097,
            'name': self._credentials['username'],
            'password': self._credentials['password_hash']
        }

    def request_url_to(self, page, params = {}):
        qs = params
        if self._token is None:
            qs.update(self.credentials())
        else:
            qs.update(self._token)

        url = f'{HOST}/zdk/services/zamapi/{page}'

        return requests.get(url, params = qs).text

    def login(self):
        login_body = self.request_url_to('userLogin')
        login_response = xmltodict.parse(login_body)['ns1:userLoginResponse']
        self._token = {
            'userId': login_response['userId'],
            'secToken': login_response['securityToken']
        }

        devices_body = self.request_url_to('getDeviceList')
        device_list = xmltodict.parse(devices_body)['ns1:getDeviceListResponse']['devList']
        self._device = {
            'devId': device_list['devId'],
            'deviceTypeId': device_list['typeId']
        }
        self._device_info = None

    def device_info(self, attr_id):
        if self._device_info is None:
            body = self.request_url_to('getDeviceAttributesWithValues', self._device)
            self._device_info = xmltodict.parse(body).get('ns1:getDeviceAttributesWithValuesResponse')
        attribute = [at for at in self._device_info['attrList'] if at['id'] == str(attr_id)]
        if len(attribute) > 0:
            return attribute[0]['value']
        return None

    def refresh_device_info(self):
        body = self.request_url_to('getDeviceAttributesWithValues', self._device)
        new_device_info = xmltodict.parse(body).get('ns1:getDeviceAttributesWithValuesResponse')
        if not new_device_info:
            print(new_device_info)
            return False
        else:
            self._device_info = new_device_info
            return True

    def online(self):
        return self.device_info(386) == 1

    def device(self):
        return {
            'contactable': not self.device_info(307) == 3200,
            'currentTemperature': float(self.device_info(306)) / 100,
            'targetTemperature': float(self.device_info(307)) / 100,
            'status': 'on' if self.device_info(309) == '1' else 'off',
            'online': self.device_info(386) == '1'
        }

    def update_device(self, payload):
        params = self._device
        params.update(payload)
        response_body = self.request_url_to('setMultiDeviceAttributes2', params)
        return xmltodict.parse(response_body).get('ns1:setMultiDeviceAttributes2Response')

    def set_temperature(self, temp):
        payload = {
            'name1': 'A85',
            'value1': int(round(temp, 1) * 100),
            'name2': 'A88',
            'value2': '1'
        }

        return self.update_device(payload)

