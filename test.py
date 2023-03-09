import time
import hashlib
import requests
z = f'{round(time.time())}oeh2VDE78zNKAiFNXrKz6VU3'
hash_object = hashlib.sha1(z.encode())
print(z)
hash = hash_object.hexdigest()[5:16]
print(hash)
params = {'time': round(time.time()), 'hash': hash}
r = requests.get("https://nebo.live/api/v2/cities/krs", params=params, headers={'X-Auth-Nebo': 'z1hpY1bkCTaiMhMik7cEAJqq'})
print(r.json())
print(round(time.time()))

for i in r.json():
    print(i['name'])