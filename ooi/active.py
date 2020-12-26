import ooi.immutables as oi
import datetime
import requests

class ACTIVE():
    def __init__(self):
        self.payload = {}
        self.payload['format'] = 'application/json'
    
    def set_request_limits(self,seconds=60*60*3,limit=1000):
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = datetime.timedelta(seconds = seconds)
        past = (now-delta).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        self.payload['beginDT'] = past
        self.payload['limit'] = limit

    def get_nrt_data(self,request_tuple):      
        snims = '/'.join(request_tuple)
        url = '/'.join((oi.base_url,oi.sensor_url,snims))         
        request = requests.session().get(url,params=self.payload)            
        if request.status_code == requests.codes.ok:
            self._print_elapsed(request)
            return request.json()
        else:
            print('HTTP Status Code: {}'.format(request.status_code))
            print('Request Error. Reason: {}'.format(request.reason))
            return False
    
    def _print_elapsed(self,request):
        elapsed = round(request.elapsed.total_seconds(),3)
        msg = "It took {} seconds to receive a response from OOINet."
        print(msg.format(elapsed))
    