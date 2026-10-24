import socket, ssl, http.client, time
from datetime import datetime


ip_loss = 0
ip_corr = 0



try:
    ip = socket.gethostbyname('goovbcxvbcvbcvbgle.com')

except socket.gaierror as e:
      ip_loss += 1
      print(e)
else :
     ip_corr += 1

print(f'ip_corr = {ip_corr}')
print(f'ip_lost = {ip_loss}')