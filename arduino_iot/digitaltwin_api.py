import serial
import json
import datetime
import requests
import time


# 社内LANでは繋がらない
# Anacondaの仮想環境 "digitaltwin" 下で実行する
# Arduino IDE を開いたままだとエラーになる。

url_token = "https://digitaltwinapp.azurewebsites.net/api/Token"

url_post = "https://digitaltwinapp.azurewebsites.net/api/Thsensor"

token_body = {
    "username": "kawai",
    "password": "Tsuruminato2023"
}

token_header = {"content-type": "application/json"}

print("--------------------------------------Open Port--------------------------------------")
print()

# serial.Serial(シリアルポート, ボーレート)
ser = serial.Serial('COM3', 9600, timeout=0.1) 
not_used = ser.readline()

def main():

    while True:
        val_arduino = ser.readline()
        val_decoded = val_arduino.decode('utf-8')
        
        if val_decoded != "":
            
            list = val_decoded.split("-")

            now = datetime.datetime.now()
            now_format = "{0:%Y-%m-%dT%H:%M:%S.0000000}".format(now)

            data = [{
                "deviceid":1,
                "tempreture": float(list[0]),
                "humidity": float(list[1]),
                "date": now_format
            }]

            print("###Request Now...")
            print()
            print(data)
            print()
            token_response = requests.post(url_token, headers=token_header, json = token_body)
            token_text = token_response.json()
            token = token_text["token"]

            headers = {
                "content-type": "application/json",
                "Authorization": "Bearer " + token,
            }


            response = requests.post(url_post, headers=headers, json = data)


            if(response.status_code == 200):
                print("###Success!")
                print()
                print("--------Wait 10 seconds-------")
                print()
                time.sleep(10)
                continue
            else:
                print("###Failed...")
                print()
                print("--------------------------------------Close Port--------------------------------------")
                print()
                break
        else:
            continue

if __name__ == '__main__':
    main()