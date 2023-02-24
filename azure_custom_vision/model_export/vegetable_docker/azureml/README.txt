How to build and deploy an AzureML Image using this package
===========================================================

First you need a few files from the docker app. 

Assuming you are in the azureml subdirectory run the following:

copy ..\app\requirements.txt
copy ..\app\predict.py
copy ..\app\model.pb
copy ..\app\labels.txt

These 4 files along with the score.py file will make up the assets needed to create an AzureML image.

Using the Azure ML Command Line Interface you can create and deploy a service using the following steps.

If you haven't previously setup a Model Management account, please follow the instructions at https://docs.microsoft.com/en-us/azure/machine-learning/preview/deployment-setup-configuration

1. Create a manifest to describe the image creation.

az ml manifest create --manifest-name <your manifest name> -m model.pb -d labels.txt -d predict.py -r python -p requirements.txt -f score.py

When this runs you'll see the following output:

model.pb
Successfully registered model
Id: <model id>
More information: 'az ml model show -m <model id>'
Creating new driver at C:\Users\<user name>\AppData\Local\Temp\tmp3i9c498m.py
labels.txt
predict.py
score.py
Successfully created manifest
Id: <manifest id>
More information: 'az ml manifest show -i <manifest id>


2. Create an image from the manifest

az ml image create --manifest-id <manifest id> -n <name of your image>

When this runs you'll see the following output:

Creating image...................Done.
Image ID: <image id>
More details: 'az ml image show -i <image id>'
Usage information: 'az ml image usage -i <image id>'

3. Create a realtime service to serve your model

az ml service create realtime -n <name of service> --image-id <image id>

This will now create and deploy a service. When successful it will log some usage information that will show you how
to connect to and test the service.

For more information please see:
 https://docs.microsoft.com/en-us/azure/machine-learning/preview/model-management-service-deploy
 https://docs.microsoft.com/en-us/azure/machine-learning/preview/model-management-custom-container
 https://docs.microsoft.com/en-us/azure/machine-learning/preview/deploy-to-iot-edge-device


 このパッケージを使用して AzureML イメージをビルドおよびデプロイする方法
================================================== =========


----和訳--------------------------------------------------------------------------------------------------------------------------


まず、docker アプリからいくつかのファイルが必要です。

azureml サブディレクトリにいると仮定して、次を実行します。

コピー ..\app\requirements.txt
コピー ..\app\predict.py
コピー ..\app\model.pb
コピー ..\app\labels.txt

これらの 4 つのファイルと score.py ファイルは、AzureML イメージの作成に必要なアセットを構成します。

Azure ML コマンド ライン インターフェイスを使用すると、次の手順でサービスを作成してデプロイできます。

以前にモデル管理アカウントをセットアップしていない場合は、https://docs.microsoft.com/en-us/azure/machine-learning/preview/deployment-setup-configuration の指示に従ってください

1. イメージの作成を説明するマニフェストを作成します。

az ml manifest create --manifest-name <マニフェスト名> -m model.pb -d labels.txt -d predict.py -r python -p requirements.txt -f score.py

これを実行すると、次の出力が表示されます。

モデル.pb
モデルが正常に登録されました
Id: <モデル ID>
詳細: 「az ml モデル ショー -m <モデル ID>」
C:\Users\<ユーザー名>\AppData\Local\Temp\tmp3i9c498m.py に新しいドライバーを作成する
ラベル.txt
予測.py
スコア.py
マニフェストが正常に作成されました
Id: <マニフェスト ID>
詳細: 'az ml manifest show -i <manifest id>


2. マニフェストからイメージを作成する

az ml image create --manifest-id <マニフェスト ID> -n <イメージの名前>

これを実行すると、次の出力が表示されます。

画像の作成.................................完了。
イメージ ID: <イメージ ID>
詳細: 「az ml image show -i <image id>」
使用法に関する情報: 'az ml image usage -i <image id>'

3. モデルを提供するリアルタイム サービスを作成する

az ml service create realtime -n <サービス名> --image-id <イメージ ID>

これで、サービスが作成されてデプロイされます。 成功すると、使用方法に関する情報が記録されます。
サービスに接続してテストします。

詳細については、次を参照してください。
  https://docs.microsoft.com/en-us/azure/machine-learning/preview/model-management-service-deploy
  https://docs.microsoft.com/en-us/azure/machine-learning/preview/model-management-custom-container
  https://docs.microsoft.com/en-us/azure/machine-learning/preview/deploy-to-iot-edge-device