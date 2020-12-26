import ooi.immutables as oi
from ooi.archived import ARCHIVED
import os

data_dir = 'C:/Users/Ian/Documents/GitHub/ooi-python/annotations/data'
ims = [
       oi.CE01ISSP_CTDPF,oi.CE02SHSP_CTDPF,oi.CE06ISSP_CTDPF,oi.CE07SHSP_CTDPF,
       oi.CE01ISSP_DOSTA,oi.CE02SHSP_DOSTA,oi.CE06ISSP_DOSTA,oi.CE07SHSP_DOSTA,
       oi.CE01ISSP_FLORT,oi.CE02SHSP_FLORT,oi.CE06ISSP_FLORT,oi.CE07SHSP_FLORT,
       oi.CE01ISSP_NUTNR,oi.CE02SHSP_NUTNR,oi.CE06ISSP_NUTNR,oi.CE07SHSP_NUTNR,
       oi.CE01ISSP_VELPT,oi.CE02SHSP_VELPT,oi.CE06ISSP_VELPT,oi.CE07SHSP_VELPT,
       oi.CE01ISSP_SPKIR,oi.CE02SHSP_SPKIR,oi.CE06ISSP_SPKIR,oi.CE07SHSP_SPKIR,
       oi.CE01ISSP_PARAD,oi.CE02SHSP_PARAD,oi.CE06ISSP_PARAD,oi.CE07SHSP_PARAD,
       ]
for im in ims:
    m2m = ARCHIVED()
    ddir = os.path.join(data_dir,im[0],im[2])
    os.makedirs(ddir,exist_ok=True)    
    if m2m.check_for_downloads(im,ddir) is True:
        print('Files already exist. Continuing...')
        continue
    m2m.set_request_times()    
    r = m2m.submit_request(im)
    i = m2m.get_thredds(r)
    files = m2m.download_data(i,ddir)
    
