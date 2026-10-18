import socket,time


print('введите название домена с например google.com')
name_do = str(input())

try :
    host = name_do
    ip = socket.gethostbyname(host)
    port = 443


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock :
        sock.settimeout(5)


        start = time.perf_counter()
        res = sock.connect_ex((ip, port))
        end = time.perf_counter()
        elapsed = (end - start) * 1000


    print("ip", ip)
    print('host', host)
    print('port', port)
    print(f'time connect {elapsed:.2f} мс ')

    if res == 0:
        print('success')
    else:
        print('fail')


except socket.error as msg:
    print(f'ошибка {msg}')


