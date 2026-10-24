import socket, ssl, http.client, time
from datetime import datetime
from share import list_sites

port = 443



for site in list_sites:
    tls_chip = None
    tls_sert = None
    tls_version = None
    tcp_corr = 0
    https_corr = 0
    ip_corr = 0
    tls_corr = 0
    https_code = 0

    errors =[]



    try:
        # пытаемся сделать сокет и обрабатываем ошибки
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)

            # часть про https
            conn = http.client.HTTPSConnection(site, port, timeout=10)

            try:
                conn.request('GET', '/')
                response = conn.getresponse()
                https_code = response.status

                if 200 <= response.status < 400:
                    https_corr += 1
            except OSError as e:
                errors.append(f'ошибка http  {e}')

            conn.close()

            # разрешаем домен
            try:
                ip = socket.gethostbyname(site)
            except socket.gaierror as e:
                errors.append(f'ошибка dns {site}: {e}')
            else:
                ip_corr += 1



            # проверка TCP
            if ip_corr == 1 :
                 sock_try = sock.connect_ex((ip, port))

                 # если прокнул tcp то делаем TSL
                 if sock_try == 0:
                   tcp_corr = 1

                   try :
                        context = ssl.create_default_context()


                        with context.wrap_socket(sock, server_hostname=site) as  tls_sock :
                             tls_version = tls_sock.version()
                             tls_chip = tls_sock.cipher()
                             tls_sert = tls_sock.getpeercert()



                   except ssl.SSLCertVerificationError as e :
                       errors.append(f'Ошибка проверки сертификата {site}: {e}')
                   except ssl.SSLError as e :
                             errors.append(f'Ошибка TLS {site}: {e}')
                   except OSError as e:
                          errors.append(f'Сетевая ошибка при TLS для {site}: {e}')
                   else:
                    tls_corr = 1
                 else :
                     errors.append(f'{site}: TCP-подключение не удалось, код {sock_try}')


    except OSError as e:
        errors.append(f'{site} сетевая ошибка {e}')



    with open('monitor.log','a',encoding='utf-8') as file :
                file.write(
                    f'для {site} : '
                    f'DNS {ip_corr}, TLS {tls_corr}, TCP {tcp_corr}, HTTPS {https_corr}, HTTP status = {https_code}\n'
                    f'согласованный набор шифров для {site}: {tls_chip} | согласованная версия TLS для {site} : {tls_version} | сведения о сертификате сервера для {site} : {tls_sert}\n'
                    f'ошибки : \n '
                    f'{errors}\n '

                )



