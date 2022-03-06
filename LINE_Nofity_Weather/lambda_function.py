import requests
import time
from bs4 import BeautifulSoup


def parse_html(url):

    html = requests.get(url)
    print(html)

    return BeautifulSoup(html.text, "html.parser")


def send_message(token, list):

    headers = {
        # 各自発行したトークンを記述
        "Authorization": "Bearer "
        + token
    }

    icon_image = list[0]

    text = "\n" + "最低気温:" + list[1] + "度\n" + "最高気温:" + list[2] + "度\n" + "降水確率:" + list[3]
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
    current_weather = soup.find("section", class_="today-weather")

    # 天気画像
    icon_image_url = current_weather.find("img")["src"]
    # 最低気温
    min_temperature = current_weather.find("dd", class_="low-temp temp").find("span", class_="value").text
    # 最高気温
    max_temperature = current_weather.find("dd", class_="high-temp temp").find("span", class_="value").text
    # 降水確率
    rain_probs = current_weather.find("tr", class_="rain-probability").find_all("td")

    rain_prob = rain_probs[2].text

    return [icon_image_url, min_temperature, max_temperature, rain_prob]


def lambda_handler(event, context):
    # tenki.jpの天気予報ページ。(文京区)
    url = "https://tenki.jp/forecast/3/16/4410/13105/"
    token = "YOUR_TOKEN"
    send_message(token, crawl(url))
