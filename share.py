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
    except requests.exceptions.ConnectionError as f:
        return f'ошибка {f}'
    except requests.exceptions.RequestException as f:
        return f'ошибка {f}'



def check_status(result):
    if result == "success":
        return 'сайт доступен'
    elif result == "fail":
        return 'проверить порт и сетевое соединение'
    else:
        return 'ошибка проверить dns или адрес'

list_sites = [
        # Поисковики
    "www.google.com",
    "www.bing.com",
    "duckduckgo.com",
    "yandex.ru",

    # Видеохостинги и соцсети
    "www.youtube.com",
    "www.twitch.tv",
    "www.reddit.com",
    "www.facebook.com",
    "www.instagram.com",
    "www.tiktok.com",
    "x.com",

    # Разработка и Git
    "github.com",
    "gitlab.com",
    "stackoverflow.com",
    "pypi.org",
    "www.python.org",

    # Облачные сервисы
    "www.cloudflare.com",
    "one.one.one.one",
    "www.microsoft.com",
    "www.apple.com",
    "aws.amazon.com",

    # Мессенджеры и коммуникации
    "telegram.org",
    "discord.com",
    "web.whatsapp.com",

    # Игры
    "store.steampowered.com",
    "www.minecraft.net",

    # Новости и информация
    "www.bbc.com",
    "www.wikipedia.org",
    "www.cnn.com",

    # Дополнительный тест
    "www.mozilla.org"
]
