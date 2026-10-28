import socket, ssl, http.client, time
from datetime import datetime
from share import list_sites

port = 443

tcp_t = 0
dns_t = 0
https_t = 0
tls_t = 0

while True :
    for site in list_sites:
        tls_chip = None
        tls_sert = None
        tls_version = None
        tcp_corr = 0
        https_corr = 0
        ip_corr = 0
        tls_corr = 0
        https_code = 0
        dns_time = 0
        tcp_time = 0
        tls_time = 0
        https_time = 0

        errors =[]

        sall_time = time.perf_counter()
        try:
            # пытаемся сделать сокет и обрабатываем ошибки
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)


                # часть про https
                conn = http.client.HTTPSConnection(site, port, timeout=10)

                try:
                    start = time.perf_counter()
                    conn.request('GET', '/')
                    response = conn.getresponse()
                    https_code = response.status
                    https_time = (time.perf_counter() - start) * 1000

                    if 200 <= response.status < 400:
                        https_corr += 1
                        https_t += 1
                except OSError as e:
                    errors.append(f'ошибка http  {e}')
                    https_time = (time.perf_counter() - start) * 1000

                conn.close()

                # разрешаем домен
                try:

                    start = time.perf_counter()
                    ip = socket.gethostbyname(site)
                    dns_time = (time.perf_counter() - start) * 1000

                except socket.gaierror as e:
                    errors.append(f'ошибка dns {site}: {e}')
                    dns_time = (time.perf_counter() - start) * 1000
                else:
                    ip_corr += 1
                    dns_t += 1



                # проверка TCP
                if ip_corr == 1 :

                     start = time.perf_counter()
                     sock_try = sock.connect_ex((ip, port))
                     tcp_time = (time.perf_counter() - start) * 1000

                     # если прокнул tcp то делаем TSL
                     if sock_try == 0:
                       tcp_corr = 1
                       tcp_t += 1

                       try :

                            context = ssl.create_default_context()
                            start = time.perf_counter()


                            with context.wrap_socket(sock, server_hostname=site) as  tls_sock :
                                 tls_time = (time.perf_counter() - start) * 1000
                                 tls_version = tls_sock.version()
                                 tls_chip = tls_sock.cipher()
                                 tls_sert = tls_sock.getpeercert()



                       except ssl.SSLCertVerificationError as e :
                           errors.append(f'Ошибка проверки сертификата {site}: {e}')
                           tls_time = (time.perf_counter() - start) * 1000
                       except ssl.SSLError as e :
                                 errors.append(f'Ошибка TLS {site}: {e}')
                                 tls_time = (time.perf_counter() - start) * 1000
                       except OSError as e:
                              errors.append(f'Сетевая ошибка при TLS для {site}: {e}')
                              tls_time = (time.perf_counter() - start) * 1000
                       else:
                        tls_corr = 1
                        tls_t += 1
                     else :
                         errors.append(f'{site}: TCP-подключение не удалось, код {sock_try}')



        except OSError as e:
            errors.append(f'{site} сетевая ошибка {e}')



        all_time = (time.perf_counter() - sall_time) * 1000

        with open('monitor.log','a',encoding='utf-8') as file :
                    file.write(
                        f'для {site} : '
                        f'DNS {ip_corr}, TLS {tls_corr}, TCP {tcp_corr}, HTTPS {https_corr}, HTTP status = {https_code}\n'
                        f'согласованный набор шифров для {site}: {tls_chip} | согласованная версия TLS для {site} : {tls_version} | сведения о сертификате сервера для {site} : {tls_sert}\n'
                        f'общее время : {all_time:.2f} ms \n'
                        f'время на dns для {site} : {dns_time:.2f} ms \n'
                        f'время на tcp для {site} : {tcp_time:.2f} ms \n'
                        f'время на tls для {site} : {tls_time:.2f} ms \n'
                        f'время на https для {site} : {https_time:.2f} ms \n'
                        f'ошибки : \n '
                        f'{errors}\n '

                    )


    with open('monitor.log','a',encoding='utf-8') as file :
                    file.write(
                        f'проверенно всего {len(list_sites)} : \n'
                        f'ответили по dns {dns_t}\n'
                        f'ответили по tcp {tcp_t}\n'
                        f'ответили по tls {tls_t}\n'
                        f'ответили по https {https_t}\n'
                    )
    time.sleep(30)
