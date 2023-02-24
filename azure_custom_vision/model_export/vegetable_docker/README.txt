# Custom Vision Dockerfile
Exported from customvision.ai.

## Build

```bash
docker build -t <your image name> .
```

### Build ARM container on x64 machine

Export "ARM" Dockerfile from customvision.ai. Then build it using docker buildx command.
```bash
docker buildx build --platform linux/arm/v7 -t <your image name> --load .
```

## Run the container locally
```bash
docker run -p 127.0.0.1:80:80 -d <your image name>
```

## Image resizing
By default, we run manual image resizing to maintain parity with CVS webservice prediction results.
If parity is not required, you can enable faster image resizing by uncommenting the lines installing OpenCV in the Dockerfile.

Then use your favorite tool to connect to the end points.

POST http://127.0.0.1/image with multipart/form-data using the imageData key
e.g
    curl -X POST http://127.0.0.1/image -F imageData=@some_file_name.jpg

POST http://127.0.0.1/image with application/octet-stream
e.g.
    curl -X POST http://127.0.0.1/image -H "Content-Type: application/octet-stream" --data-binary @some_file_name.jpg

POST http://127.0.0.1/url with a json body of { "url": "<test url here>" }
e.g.
    curl -X POST http://127.0.0.1/url -d '{ "url": "<test url here>" }'

For information on how to use these files to create and deploy through AzureML check out the readme.txt in the azureml directory.


---------和訳-------------------------------------------------------------------------------------------------------------


# Custom Vision Dockerfile
customvision.ai からエクスポートされました。

＃＃ 建てる

```バッシュ
docker build -t <イメージ名> .
```

### x64 マシンで ARM コンテナーをビルドする

customvision.ai から「ARM」Dockerfile をエクスポートします。 次に、docker buildx コマンドを使用してビルドします。
```バッシュ
docker buildx build --platform linux/arm/v7 -t <イメージ名> --load .
```

## コンテナをローカルで実行する
```バッシュ
docker run -p 127.0.0.1:80:80 -d <イメージ名>
```

## 画像のサイズ変更
デフォルトでは、手動の画像サイズ変更を実行して、CVS Web サービスの予測結果との同等性を維持します。
パリティが不要な場合は、Dockerfile で OpenCV をインストールする行のコメントを解除することで、イメージのサイズ変更を高速化できます。

次に、お気に入りのツールを使用してエンド ポイントに接続します。

imageData キーを使用して multipart/form-data で http://127.0.0.1/image を POST します
例えば
     curl -X POST http://127.0.0.1/image -F imageData=@some_file_name.jpg

POST http://127.0.0.1/image with application/octet-stream
例えば
     curl -X POST http://127.0.0.1/image -H "Content-Type: application/octet-stream" --data-binary @some_file_name.jpg

POST http://127.0.0.1/url { "url": "<test url here>" } の JSON 本体を使用
例えば
     curl -X POST http://127.0.0.1/url -d '{ "url": "<ここで URL をテスト>" }'

これらのファイルを使用して AzureML を介して作成およびデプロイする方法については、azureml ディレクトリの readme.txt を確認してください。