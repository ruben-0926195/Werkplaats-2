# import requests
#
# url = "http://127.0.0.1:5000/login"
#
# passwords = ["123456", "password", "admin", "admin123", "admin"]
#
# for password in passwords:
#     r = requests.post(url, data={"username": "admin", "password": password})
#     if "Wachtwoord komt niet overeen" in r.text:
#         print(f"{password} gefaald")
#         break
#     else:
#         print(f"{password} gelukt!!")
#         continue

import requests

url = "http://127.0.0.1:5000/login"
passwords = ["123456", "password", "admin", "admin123", "admin"]

for password in passwords:
    r = requests.post(url, data={"username": "admin", "password": password})
    print("status:", r.status_code)
    if r.status_code == 429:
        print("Blocked by rate limiter (429 Too Many Requests)")
        break
    elif "Wachtwoord komt niet overeen" in r.text:
        print(f"{password} gefaald")
    else:
        print(f"{password} gelukt!!")
        break
