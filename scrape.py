import requests
import time

login_url = 'https://myclass.apps.binus.ac.id/Auth/Login'
data = {
    'Username': 'leonardus.yobeth',
    'Password': 'passwordKevin25'
}

s = requests.Session()
s.post(login_url, data)
schdl = s.get('https://myclass.apps.binus.ac.id/Home/GetViconSchedule')

print(schdl.json()[0]['MeetingUrl'])


# with requests.Session() as s:
#     response = requests.post(login_url, data)
#     print(response.text)
#     schdl = s.get(
#         'https://myclass.apps.binus.ac.id/Home/GetViconSchedule')
#     schdl.json()
