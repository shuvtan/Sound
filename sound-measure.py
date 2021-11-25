import requests

ip = '192.168.212.35' # Usually 192.168.212.X. Find X in oscilloscope settings

if (ip == ''):
    print('Setup ip-address of Tekronix oscilloscope')
    quit()

url = 'http://' + ip + '/image.png'
r = requests.get(url, allow_redirects=True)

with open('tektronix.png', 'wb').write(r.content) as file:
    file.write(r.content)