# coding: utf-8

#Arduino IDE を開いたままだとエラーになる。

import serial

print("--------------------------------------Open Port--------------------------------------")

# serial.Serial(シリアルポート, ボーレート)
ser = serial.Serial('COM3', 9600, timeout=0.1) 
not_used = ser.readline()

while True:
    val_arduino = ser.readline()
    val_decoded = val_arduino.decode('utf-8')
    print(val_decoded)

    # JSONに変形
    # POST通信


    # print("--------------------------------------Close Port--------------------------------------")
    # ser.close()

print("--------------------------------------Close Port--------------------------------------")
ser.close()
