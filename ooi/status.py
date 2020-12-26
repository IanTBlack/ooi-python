import requests

def ooinet():
    '''A function that issues a request to OOINet to check its status.
    return -- True if OOINet is up, False if OOINet is down
    '''       
    response = requests.get('https://ooinet.oceanobservatories.org')
    e = round(response.elapsed.total_seconds(),2) #Elapsed       
    print('It took {}s to receive a response from OOINet.'.format(e))     
    if response.status_code == requests.codes.ok:
        print('OOINet is up and A-Okay!')
        return True
    else:
        print('HTTP Status Code: {}'.format(response.status_code))
        print('OOINet is not available at the moment.')       
        return False

