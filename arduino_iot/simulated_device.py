import asyncio
import serial
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# 社内LANでは繋がらない
# Anacondaの仮想環境 "digitaltwin" 下で実行する
# Arduino IDE を開いたままだとエラーになる。

# プライマリ接続文字列
CONNECTION_STRING = "HostName=DigitalTwin.azure-devices.net;DeviceId=arduino;SharedAccessKey=7CPJovUeUz2Hob3ffCKp45osswphlbTd4750L3AEHO0="

print("--------------------------------------Arduino Open Port--------------------------------------")

# serial.Serial(シリアルポート, ボーレート)
ser = serial.Serial('COM3', 9600, timeout=0.1) 
not_used = ser.readline()


async def run_telemetry_sample(client):
    # This sample will send temperature telemetry every second
    print("IoT Hub device sending periodic messages")
    print("")

    await client.connect()

    while True:
        val_arduino = ser.readline()
        val_decoded = val_arduino.decode('utf-8')
        message = Message(val_decoded)
        print("Sending message: {}".format(message))
        await client.send_message(message)
        print("Message successfully sent")
        await asyncio.sleep(1)

        # print("--------------------------------------Arduino Close Port--------------------------------------")
        # ser.close()


def main():

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run_telemetry_sample(client))
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        print("Shutting down IoTHubClient")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == '__main__':
    main()