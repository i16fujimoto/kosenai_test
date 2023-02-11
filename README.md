# kosenai_back
高専メジャーのバックエンド

# Usage

## dockerの起動

### コンテナのビルド方法
- 初めてサービスを立ち上げる時に利用（imageがない時も同様）
- requirements.txtを更新した際は再度ビルドする必要がある
```bash
 $ make build
```
### コンテナの作成，起動
- 基本的にはupを利用する
- docker-composeにサービスを追加，requirements.txtを更新した時は再ビルドする必要がある
```bash
 $ make up // コンテナの作成、起動
```
### コマンド機能
| コマンド |image構築|コンテナ構築|コンテナ起動|
| :---: | :---: | :---: | :---: |
| build | ○ | × | × |
| up | △ | ○ | ○ |

※ 具体的なコマンド内容についてはMakefileを参照

## MinIOの利用方法
- [MinIO](https://min.io)
- MinIO: ローカル環境におけるAWS S3環境

### MinIOコンソールにアクセス
コンテナ起動後，[http://localhost:9090]にアクセスするとMinIOのコンソールが起動
- ログイン時のIDとパスワードは`.env`で指定
![スクリーンショット 2022-10-14 17 11 12](https://user-images.githubusercontent.com/29566903/195796672-66d43868-ea27-475a-9fed-eb310a1f5cb6.png)
![スクリーンショット 2022-10-14 17 11 29](https://user-images.githubusercontent.com/29566903/195796771-650a891d-e1a0-4f2f-85e1-44daf0f473ed.png)

### pythonからS3にアクセスするサンプルコード

```python
import boto3
import os
from dotenv import load_dotenv

BUCKET_NAME = 'static'

# 環境変数を設定
load_dotenv()

if __name__ == '__main__':
    
    # 初期化 & S3に接続
    s3 = boto3.resource(
        service_name='s3', 
        endpoint_url='http://minio:9000',
        aws_access_key_id=os.environ['MINIO_ACCESS_KEY'],
        aws_secret_access_key=os.environ['MINIO_SECRET_KEY'],
        region_name=''
    )
    # バケット情報を取得
    bucket = s3.Bucket(BUCKET_NAME)
    # バケットの内容を出力
    for obj in bucket.objects.all():
        print(obj.key)
```

## Djongoの利用方法
下記のリファレンスを参照
### [Djongoリファレンス](https://www.djongomapper.com/integrating-django-with-mongodb/)

# Develop Rules

1. issueを確認する or issueを作成する
2. ブランチを作成する（`[タグ]/#[issue番号]-[実装内容]`）

| タグ | 詳細 |
| --- | --- |
| feat | UI・機能実装 |
| bugfix | バグ修正 |
| setup | セットアップ |
| release | リリース |
