import ooi.immutables as oi
import os
import re
import requests
import time
import wget
import xarray as xr

class ARCHIVED():
    def __init__(self):
        self.payload = {}
        self.payload['format'] = 'application/netcdf'
    
    def set_request_times(self,begin_date='2010-01-01',begin_time='00:00:00',
                          end_date='2040-12-31',end_time='23:59:59'):
        self.payload['beginDT'] = begin_date + 'T' + begin_time + '.000Z'
        self.payload['endDT'] = end_date + 'T' + end_time + '.999Z'
    
    def submit_request(self,request_tuple):
        snims = '/'.join(request_tuple) #(site,node,instrument,method,stream)
        url = '/'.join((oi.base_url,oi.sensor_url,snims))       
        request = requests.get(url,params=self.payload)  
        if request.status_code == requests.codes.ok:
            e = round(request.elapsed.total_seconds(),3) #Elapsed       
            print('It took {}s to submit the request to OOINet.'.format(e))    
            return request
        else:
            print('HTTP Status Code: {}'.format(request.status_code))
            print('Request Error. Reason: {}'.format(request.reason))
            exit()
       
    def check_request_status(self,request):
        info = request.json()
        async_url = [url for url in info['allURLs'] if 'async' in url].pop()
        status_url = '/'.join((async_url,'status.txt'))
        i = 0 #Elapsed time iterator.
        while True:
            status = requests.get(status_url)
            if status.status_code == requests.codes.ok:
                print('\n')
                s = i*10
                print('Done! Request took {} seconds to complete.'.format(s))
                return info
            else:
                i = i + 1
                print('.',end='')
                time.sleep(10)
    
    def get_thredds(self,request):
        info = self.check_request_status(request)
        catalog_url=[u for u in info['allURLs'] if 'catalog' in u].pop()
        html_text = requests.get(catalog_url).text
        parts = re.findall('dataset=(ooi/.*?[0-9]\.nc)',html_text)
        thredds = [part + "#fillmismatch" for part in parts]
        return thredds
    
    def download_data(self,thredds,directory):       
        os.chdir(directory) #Set directory.
        if isinstance(thredds,str):
            thredds = [thredds]
        ncs = ['/'.join((oi.fileserver_url,thredd)) for thredd in thredds]
        paired = []
        requested = []
        for nc in ncs:
            r = re.findall("ooi/.*?-.*?-.*?-([0-9][0-9]-.*?)-",nc).pop()
            p = re.findall("deployment.*?_.*?-.*?-([0-9][0-9]-.*?)-",nc).pop()
            requested.append(r)
            paired.append(p)
        r = set(requested).pop()
        p = [i for i in set(paired) if r not in i]
        if p != []:
            p = p.pop()
            requested_ncs = [nc for nc in ncs if p not in nc]
        else:
            requested_ncs = ncs
        filepaths = []
        for nc in requested_ncs:
            filename = wget.download(nc)
            filepaths.append('/'.join((directory,filename)))
        return filepaths            
    
    def import_data(self,filepaths):
        if isinstance(filepaths,str):
            filepaths = [filepaths]
        ds = xr.open_mfdataset(filepaths,concat_dim='obs',combine='nested')
        return ds
        
    def check_for_downloads(self,request_tuple,directory):
        inst_files = self.get_filepaths(request_tuple,directory)
        if inst_files == []:
            return False
        else:
            return True
    
    def get_filepaths(self,request_tuple,directory):
        files = os.listdir(directory)
        inst_files = [f for f in files if '-'.join((request_tuple)) in f]
        return inst_files
