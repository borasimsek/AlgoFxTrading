import requests
import constants.defs as defs

class OandaAPI:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
                                    "Authorization": f"Bearer {defs.API_KEY}",
                                    "Content-Type": "application/json"})
    
    def make_request(self, url, verb = 'get',code = 200, params = None, data = None, headers = None):
        full_url = f"{defs.OANDA_URL}/{url}"
        try:
            response = None
            if verb == 'get':
                response = self.session.get(full_url, params = params, data=data, headers=headers)
            if response == None:
                return False, {'error': 'Invalid verb'}
            if response.status_code == code:
                return True, response.json()
            else:
                return False, {'error': response.json()}
        except Exception as e:
            return False, {'error': str(e)}
    
    def get_account_ep(self,ep,data_key):
        url = f"accounts/{defs.ACCOUNT_ID}/{ep}"
        ok, data = self.make_request(url)
        if ok and data_key in data:
            return data[data_key]
        else:
            print("Error get_account_ep(): ", data)
            return None
        
    def get_account_summary(self):
        return self.get_account_ep('summary','account')
    
    def get_account_instruments(self):
        return self.get_account_ep('instruments','instruments')