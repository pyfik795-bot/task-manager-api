import socket, ssl, http.client, time
from datetime import datetime




port = 443

correct_conn = 0
lost_conn = 0
https_corr = 0
https_lost = 0

list_sites = [
     "google.com",
    "youtube.com",
    "github.com",
    "microsoft.com",
    "cloudflare.com",
    "wikipedia.org",
    "python.org",
    "kernel.org",
    "mozilla.org",
    "debian.org",
    "ubuntu.com",
    "archlinux.org",
    "stackoverflow.com",
    "reddit.com",
    "example.com",
    "gnu.org",
    "iana.org",
    "eff.org",

]

for site in list_sites:
    try:
        # пытаемся сделать сокет и обрабатываем ошибки
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            ip = socket.gethostbyname(site)

            # проверка TCP
            sock_try = sock.connect_ex((ip, port))

            # если прокнул сокет то делаем TSL
            try :

                context = ssl.create_default_context()

                tls_sock = context.wrap_socket(sock, server_hostname=site)
                tls_version = tls_sock.version()
                tls_chip = tls_sock.cipher()
                tls_sert = tls_sock.getpeercert()
                tls_binarn_sert = tls_sock.getpeercert(binary_form=True)


            except ssl.SSLCertVerificationError as e :
                print(f'Ошибка проверки сертификата {e}')
            except ssl.SSLError as e :
                print(f'Ошибка TLS {e}')
            except OSError as e :
                print(f'Сетевая или системная ошибка {e}')


            if sock_try == 0:
                correct_conn += 1
            else :
                lost_conn += 1

    except OSError as e:
        print(e)

    # часть про https
    conn = http.client.HTTPSConnection(site, port, timeout= 10)

    try:
        conn.request('GET', '/')
        response = conn.getresponse()

        if response.status == 200:
            https_corr += 1
        else :
            https_lost += 1

    except OSError as e:
        print(f'ошибка https {e}')

    conn.close()

    with open('monitor.log','a',encoding='utf-8') as file :
                file.write(
                    f'{datetime.now()} | согласованный набор шифров для {site}: {tls_chip}\n'
                    f'{datetime.now()} | сведения о сертификате сервера для {site} : {tls_sert}\n'
                    f'{datetime.now()} | согласованная версия TLS для {site} : {tls_version}'

                    f'успешных по tcp : {correct_conn}, по https : {https_corr}\n'
                    f'неуспешных по tcp : {lost_conn}, по https : {https_lost}\n'
                    f'проверенно сайтов : {len(list_sites)}'




                )



print(f'успешных по tcp : {correct_conn}, по https : {https_corr}\n'
      f'неуспешных по tcp : {lost_conn}, по https : {https_lost}\n'
      f'проверенно сайтов : {len(list_sites)}')

print( f'согласованный набор шифров для {site}: {tls_chip}\n'
       f'сведения о сертификате сервера для {site} : {tls_sert}\n'
       f'согласованная версия TLS для {site} : {tls_version}')