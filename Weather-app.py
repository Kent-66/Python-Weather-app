import tkinter as tk
import requests

root = tk.Tk()
root.title("天気予報アプリ")
root.geometry("400x300")

#「都市名」と表示する
label = tk.Label(root, text = "都市名を入力して下さい")
label.pack()

#都市名を入力する場所
entry = tk.Entry(root)
entry.pack()

#天気が表示される
result_label = tk.Label(root, text = "ここに天気が表示されます")
result_label.pack()

def get_weather():
    city = entry.get()

    #都市名から経度・緯度を調べる
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name" : city,
        "count" : 10,
        "language" : "ja",
        "format" : "json",
        "countryCode" : "JP"
    }

    geo_response = requests.get(geo_url, params = geo_params)
    
    geo_data = geo_response.json()
    print(geo_data)

    #日本語で見つからなかったら英語でも検索
    if not geo_data.get("results"):
        geo_params["language"] = "en"

        geo_response = requests.get(geo_url, params = geo_params)

        geo_data = geo_response.json()

    if "results" not in geo_data or not geo_data["results"]:
        result_label.config(text = "地名が見つかりません")
        return

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    #天気データを取得するURL
    weather_url = "https://api.open-meteo.com/v1/forecast"

    #取得した緯度・経度を使う
    weather_params = {
        "latitude" : latitude,
        "longitude" : longitude,
        "current" : "temperature_2m,weather_code"
    }

    #天気APIに問い合わせる
    weather_response = requests.get(weather_url, params = weather_params)

    #返ってきたデータを取り出す
    weather_data = weather_response.json()

    #気温だけ取り出す
    temperature = weather_data["current"]["temperature_2m"]

    weather_code = weather_data["current"]["weather_code"]

    if weather_code == 0:
        weather = "快晴"
    elif weather_code in [1, 2]:
        weather = "晴れ"
    elif weather_code == 3:
        weather = "曇り"
    elif weather_code in [45, 48]:
        weather = "霧"
    elif weather_code in [51, 53, 55, 56, 57]:
        weather = "霧雨"
    elif weather_code in [61, 63, 65, 66, 67, 80, 81, 82]:
        weather = "雨"
    elif weather_code in [71, 73, 75, 77, 85, 86]:
        weather = "雪"
    elif weather_code in [95, 96, 99]:
        weather = "雷雨"
    else:
        weather = "不明"

    result_label.config(text = f"天気：{weather}\n気温：{temperature}℃")

#ボタンを作る
button = tk.Button(root, text = "天気を見る", command = get_weather)
button.pack()

root.mainloop()
