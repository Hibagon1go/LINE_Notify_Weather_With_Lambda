import requests
from bs4 import BeautifulSoup


def parse_html(url):

    html = requests.get(url)
    return BeautifulSoup(html.text, "html.parser")


def send_message(list):

    headers = {
        # 各自発行したトークンを記述
        "Authorization": "Bearer {Your Token}"
    }

    icon_image = list[0]

    text = (
        "\n" + "最低気温:" + list[1] + "度\n" + "最高気温:" + list[2] + "度\n" + "降水確率:" + list[3]
    )
    files = {
        "message": (None, text),
        "imageFullsize": (None, icon_image),
        "imageThumbnail": (None, icon_image),
    }

    requests.post("https://notify-api.line.me/api/notify", headers=headers, files=files)


def crawl(url):
    # htmlをパース
    soup = parse_html(url)

    # 天気情報
    current_weather = soup.find("a", id="forecast-entry-13113")
    # 天気詳細情報
    current_weather_detail = current_weather.find("p", class_="temp-precip")

    # 天気画像
    icon_image_url = current_weather.find("img", class_="forecast-image")["src"]
    # 最低気温
    min_temperature = current_weather_detail.find("span", class_="min-temp").text
    # 最高気温
    max_temperature = current_weather_detail.find("span", class_="max-temp").text
    # 降水確率
    rain_prob = current_weather_detail.find("span", class_="prob-precip").text

    return [icon_image_url, min_temperature, max_temperature, rain_prob]


def lambda_handler(event, context):
    # tenki.jpの天気予報ページ。(渋谷区)
    url = "https://tenki.jp/forecast/3/16/"
    send_message(crawl(url))
