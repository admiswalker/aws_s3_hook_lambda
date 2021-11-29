# Lambda と S3 の接合について

ここでは，Lambda 関数と S3 との連携について説明します．


## アクセス権限の設定
例えば，以下のようにする．
```
s3_bucket.grantReadWrite(lambda_function)
```

## ファイルの受け渡し
Lambda と S3 の間でのファイルの受け渡しについては，
[チュートリアル: Amazon S3 トリガーを使用してサムネイル画像を作成する](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/with-s3-tutorial.html) を参照すること．


