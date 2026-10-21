import socket,time, errno, requests
from datetime import datetime
from share import sites, get_error_message, check_http_status, check_status


#бесконченый цикл
while True:

    fail_connect = 0
    success_connect = 0

# повторяется кол во раз сколько адресов
    for i in sites :

        # пытается подключиться пытается полдучить айпи
        try :
            host = i[0]
            ip = socket.gethostbyname(host)
            port = i[1]

            # делает сокет
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock :
                sock.settimeout(5)

                # засекает время получает статус конекта 0=все хорошо не 0 ошибка
                start = time.perf_counter()
                res_port = sock.connect_ex((ip, port))
                end = time.perf_counter()
                elapsed = (end - start) * 1000


            print("ip", ip)
            print('host', host)
            print('port', port)
            print(f'time connect {elapsed:.2f} мс ')

            # если все хорошо то статус success
            if res_port == 0:
                reason = "OK"
                status = "success"
                success_connect += 1

            # если нет то fail и передаем результат по порту
            else:
                reason = get_error_message(res_port)
                print(reason)
                status = "fail"
                fail_connect += 1

            # записываем в файл
            with open('monitor.log','a',encoding='utf-8') as file :
                file.write(
                    f'{datetime.now()} | host={host} | ip={ip} | '
                    f'port={port} | status={status} | time={elapsed:.2f} ms '
                    f'причина= {reason} | http_code={check_http_status(host)}\n'
                )
                print('результат сохранен')


        # вылавливаем ошибки сокета
        except socket.error as msg:
            print(f'ошибка {msg}')
            fail_connect += 1

            # записываем в файл
            with open('monitor.log','a',encoding='utf-8') as file :
                file.write(
                    f'{datetime.now()} | host={host} | '
                    f'status=ERROR | reason={msg}\n'
                )


    print(f'доступно, {success_connect}\n'
          f'недоступно, {fail_connect}\n')
    time.sleep(30)
