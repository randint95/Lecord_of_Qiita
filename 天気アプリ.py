# -*- coding: utf-8 -*-
"""
web api の練習
"""

import requests

print("----------------------------------------------------------------")
print("今日から明後日までの関西圏のざっくりとした天気を調べるPythonプログラムです。")
print("大阪、京都、奈良、兵庫、和歌山、滋賀の県庁所在地の天気が分かります。")
print("使い方")
print("入力例のように場所と時間を入力すれば天気が分かります。")
print("プログラムを終了させたい場合はendを入力してください。")
print("----------------------------------------------------------------")
print("")

Memory = 1
while Memory >= 1:
    print("Start→→→→→→")
    url = "https://weather.tsukumijima.net/api/forecast?city=" #URL(エンドポイント)
    Memory = 1
    
    ##############場所入力###############
    print("入力例：大阪")
    city = input("２府４県から調べたい場所はどこですか?：")
    
    if city == "大阪":
        url += "270000"
    elif city == "京都":
        url +="260010"
    elif city == "奈良":
        url +="290010"
    elif city == "兵庫":
        url +="280010"
    elif city == "和歌山":
        url +="300010"
    elif city == "滋賀":
        url +="250010"
    elif city != "end":
        print("入力エラー、期待された入力ではありません。")
        print("もう一度入力してください。")
        Memory = 2
    else:
        Memory = 0
    #####################################
    
    
    
    ####################時間入力##########
    if Memory == 1:
        print("入力例：今日")
        date = input("今日～明後日までのいつを調べたいですか?：")
        if date == "end":
            Memory = 0
        elif date == "今日":
            num = 0
        elif date == "明日":
            num = 1
        elif date == "明後日":
            num = 2
        else:
            print("入力エラー、期待された入力ではありません。")
            print("もう一度入力してください。")
            Memory = 2
    else:
        pass
    #####################################
    
    if Memory == 1:
        tenki_data = requests.get(url).json()
        print("")
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
        print(tenki_data["forecasts"][num]["dateLabel"]+"の"+tenki_data["title"])
        print("日付"+tenki_data["forecasts"][num]["date"])
        print("天気"+tenki_data["forecasts"][num]["telop"])
        print("詳細"+tenki_data["forecasts"][num]["detail"]["weather"])
        print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")
    
    print("End←←←←←←")
    print("")
    
    if Memory == 0:
        print("プログラムを終了します。")
    
    
    
    
    