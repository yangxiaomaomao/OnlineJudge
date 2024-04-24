import requests
from os.path import dirname, realpath
import sys
requests.packages.urllib3.disable_warnings()

test_dir = dirname(realpath(__file__))
timeout = 2
scores = {
    "http_301":None,
    "https_200":None,
    "http_200":None,
    "http_404":None,
    "http_in_dir":None,
    "http_range1":None,
    "http_range2":None
}
print(1)
#http 301
try:
    r = requests.get('http://10.0.0.1/index.html', allow_redirects=False, timeout = timeout)
    scores["http_301"] = (r.status_code == 301 and r.headers['Location'] == 'https://10.0.0.1/index.html')
except:
    scores["http_301"] = False
print(2)
# https 200 OK
try: 
    r = requests.get('https://10.0.0.1/index.html', verify=False, timeout = timeout)
    scores["https_200"] = (r.status_code == 200 and open(test_dir + '/../index.html', 'rb').read() == r.content)
except: 
    scores["https_200"] = False
print(3)
# http 200 OK
try:
    r = requests.get('http://10.0.0.1/index.html', verify=False, timeout = timeout)
    scores["http_200"] = (r.status_code == 200 and open(test_dir + '/../index.html', 'rb').read() == r.content)
except:
    scores["http_200"] = False
print(4)
# http 404
try:
    r = requests.get('http://10.0.0.1/notfound.html', verify=False, timeout = timeout)
    scores["http_404"] = (r.status_code == 404)
except:
    scores["http_404"] = False
print(5)
# file in directory
try:
    r = requests.get('http://10.0.0.1/dir/index.html', verify=False, timeout = timeout)
    scores["http_in_dir"] = (r.status_code == 200 and open(test_dir + '/../index.html', 'rb').read() == r.content)
except:
    scores["http_in_dir"] = False
print(6)
# http range 100-200
try:
    headers = { 'Range': 'bytes=100-200' }
    r = requests.get('http://10.0.0.1/index.html', headers=headers, verify=False, timeout = timeout)
    scores["http_range1"] = (r.status_code == 206 and open(test_dir + '/../index.html', 'rb').read()[100:201] == r.content)
except:
    scores["http_range1"] = False
print(7)
print(scores)
# http range 100-
try:
    headers = { 'Range': 'bytes=100-' }
    r = requests.get('http://10.0.0.1/index.html', headers=headers, verify=False, timeout = 0.1)
    scores["http_range2"] = (r.status_code == 206 and open(test_dir + '/../index.html', 'rb').read()[100:] == r.content)
except:
    scores["http_range2"] = False

print(scores)
