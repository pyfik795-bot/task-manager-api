import errno
import requests

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


def check_http_status(host):
    try:
        res_http = requests.get(url=f'https://{host}', timeout=5)
        return res_http.status_code

    except requests.exceptions.Timeout:
        return 'таймаут'
    except requests.exceptions.RequestException as f:
        return f'ошибка {f}'
    except requests.exceptions.ConnectionError as file:
        return f'ошибка {file}'



def check_status(result):
    if result == "success":
        return 'сайт доступен'
    elif result == "fail":
        return 'проверить порт и сетевое соединение'
    else:
        return 'ошибка проверить dns или адрес'
