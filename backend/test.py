import requests

url = 'http://127.0.0.1:5000/login/charleszqwang@gmail.com/Iambored123/False'
r = requests.get(url)
out = r.json()
print(out)
code = input('code: ')
url = 'http://127.0.0.1:5000/verify/charleszqwang@gmail.com/Iambored123/False'
r = requests.get('/'.join([url,out['device_token'], out['result'], code, out['challenge_id']]))

print(r.url)
print(r.json())