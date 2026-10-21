import socket,time, errno
from datetime import datetime


sites = [
    ("google.com", 443),
    ("github.com", 443),
    ("python.org", 443),
    ("this-domain-should-not-exist.invalid", 443),
        ]

def get_error_message(code):
    errors = {
        errno.ECONNREFUSED: "Соединение отклонено",
        errno.ETIMEDOUT: "Время ожидания истекло",
        errno.ENETUNREACH: "Сеть недоступна",
        errno.EHOSTUNREACH: "Хост недоступен",
    }

    return errors.get(code, f"Неизвестная ошибка: {code}")

while True:

    fail_connect = 0
    success_connect = 0


    for i in sites :

        try :
            host = i[0]
            ip = socket.gethostbyname(host)
            port = i[1]


            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock :
                sock.settimeout(5)


                start = time.perf_counter()
                res_port = sock.connect_ex((ip, port))
                end = time.perf_counter()
                elapsed = (end - start) * 1000


            print("ip", ip)
            print('host', host)
            print('port', port)
            print(f'time connect {elapsed:.2f} мс ')

            if res_port == 0:
                status = "success"
                success_connect += 1
            else:
                print(get_error_message(res_port))
                status = "fail"


            with open('monitor.log','a',encoding='utf-8') as file :
                file.write(
                    f'{datetime.now()} | host={host} | ip={ip} | '
                    f'port={port} | status={status} | time={elapsed:.2f} ms\n'
                )
                print('результат сохранен')


        except socket.error as msg:
            print(f'ошибка {msg}')
            fail_connect += 1


            with open('monitor.log','a',encoding='utf-8') as file :
                file.write(
                    f'{datetime.now()} | host={host} | error={msg} | '
                    f'status=ERROR | reason=DNS/Socket error: {msg}\n'
                )
    print(f'доступно, {success_connect}\n'
          f'недоступно, {fail_connect}\n')
    time.sleep(30)
