import os
import argparse
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


def shorten_link(link, headers):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = {
        'long_url': link
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    short_link = response.json()['id']
    return short_link


def get_count_clicks(short_link, headers):
    parsed_url = urlparse(short_link)
    parsed_bitlink = '{}{}'.format(parsed_url.netloc, parsed_url.path)
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(parsed_bitlink)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser(description='Сокращает ссылки и считает кол-во переходов по ней')
    parser.add_argument('link', help='ссылка для сокращения или подсчёта переходов по ней (в зависимости от типа ссылки)')
    args = parser.parse_args()

    token = os.getenv('BITLY_TOKEN')
    link = args.link
    headers = {'Authorization': 'Bearer {}'.format(token)}

    try:
        try:
            clicks_count = get_count_clicks(link, headers)
            print(clicks_count)
        except requests.exceptions.HTTPError:
            short_link = shorten_link(link, headers)
            print(short_link)
    except requests.exceptions.HTTPError:
        print('что-то пошло не так, проверьте введённую вами ссылку')
