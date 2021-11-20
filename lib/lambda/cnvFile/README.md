# Lambda deproyment package の構成手順

ここでは，.zip file archives として Lambda function を構成する手順を説明する．

- 参考: 
  - [Deploy Python Lambda functions with .zip file archives](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
  - [.zip ファイルアーカイブで Python Lambda 関数をデプロイする](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-package.html)

## Deployment package の管理
ここでは deployment package を package manager で管理する．
Package manager には Poetry を用いる．

### Poetry の install
```
$ PATH=$PATH:$HOME/.poetry/bin
```
1. install
   コマンド
   ```
   $ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3
   ```
2. path の追加
   path を追加する．~/.bash_profile に以下を追記する．(何故か ~/.bash_profile が無い場合は，~/.bashrc に追記する)．
   ```
   PATH=$PATH:$HOME/.poetry/bin
   ```
3. path のロード
   追記した path をシステムに読み込むには，PC を再起動するか，以下のコマンドを実行する．
   ```
   source ~/.bash_profile
   ```

### Poetry による仮想環境の構築
poetry の使い方は，[基本的な使い方 @ Poetry documentation](https://cocoatomo.github.io/poetry-ja/basic-usage/) を参照する．

1. 初期化 (`poetry.toml` が生成される)
   ```
   $ poetry init
   ```
2. package の install 先 (`.venv`) の作成
   ```
   $ poetry config --list  # 環境の確認
   $ poetry config virtualenvs.in-project true --local  # ローカルに `.venv` を作成するように変更 (`pyproject.toml`が生成される)
   ```
   - 設定が上手く反映されないことが多いため，`$ poetry config --list` で都度確認すること．
   - また，仮想環境ができた後に `$ poetry install` しても `.venv` はローカルに作成されないため注意する．この場合 `$ poetry env list` で環境名を調べ，`$ poetry env remove [環境名]` で仮想削除し，もう一度作り直す必要がある．
   - 参考: 
     - [poetryでパッケージ・仮想環境を管理](https://rinoguchi.net/2020/06/poetry.html)
     - [Poetryのインストールと仮想環境作成先の変更](https://medium.com/music-and-technology/poetry%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%A8%E4%BB%AE%E6%83%B3%E7%92%B0%E5%A2%83%E4%BD%9C%E6%88%90%E5%85%88%E3%81%AE%E5%A4%89%E6%9B%B4-96e1bab83725)
3. ライブラリの追加  
   `pyproject.toml` にライブラを追加する．
   ```
   $ poetry add [ライブラリ名]
   ```
4. Script の実行  
   仮想環境で Script の動作を確認するには，以下のコマンドを実行する．
   ```
   $ poetry run python your_script.py
   ```
5. lockfile の生成  
   既存の `pyproject.toml` から lockfile を生成する場合は，以下のコマンドにより，ライブラリを install し，`pyproject.toml` から `poetry.lock` を生成する．
   ```
   $ poetry install
   ```

## .zip file archive の生成

### .zip archive を作成する環境
docker で Lambda の実行環境に揃えるとよい．

### .toml file を pip の requirements.txt 形式へ変換する
[AWS のドキュメント](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-package.html) では，pip の requirements.txt の形式で .zip file archive 化している．ここでは大事を取って同じプロセスで zip file archive を生成すべく，`pyproject.toml` を `requirements.txt` に変換する．

```
$ poetry export -f requirements.txt --output requirements.txt
```

### requirements.txt から package を展開する
```
$ pip install -r requirements.txt --target ./package
```

### 展開した package を .zip file archive 化する
```
$ cd package
$ zip -r ../deployment-package.zip .
$ cd ..
```

### .zip file の root に index.py を追加する
```
$ zip -g deployment-package.zip index.py
```

## build process の shell script 化
build process を自動化するために，ここまでの処理を下記のような shell script にする．

- **<u>build.sh</u>**
  ```sh
  #!/bin/bash
  poetry install
  poetry export -f requirements.txt --output requirements.txt
  
  pip install -r requirements.txt --target ./package
  
  cd package
  zip -r ../deployment-package.zip .
  cd ..
  
  zip -g deployment-package.zip index.py
  ```

## build 環境と実行環境の統一
build 環境が実行環境と異なると，Lambd 関数が正常に機能しない場合がある．
ここでは，Lambda の実行環境と同じ docker image で deployment package を build する．

### build 用の docker image 選定
[Lambda の実行環境のランタイム](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html)にはいくつかが種類り，ここでは Amazon Linux 2 ベースの Python 3.8 のランタイムを用いる．なお，Python 2.7 などの古いランタイムは[サポート期限](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/runtime-support-policy.html)が迫っているので，使用しないほうがよい．

Amazon Linux 2 に Python 3.8 のランタイムを追加した Docker image は，[コンテナイメージで Python Lambda 関数をデプロイ](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html)できるように，AWS が base image を用意している．今回は，この Docker image で Deployment package を build する．

Docker image は，[`Docker Hub リポジトリ (amazon/aws-lambda-python)`](https://hub.docker.com/r/amazon/aws-lambda-python) や `Amazon ECR リポジトリ (gallery.ecr.aws/lambda/nodejs)` から提供されており，今回は，Docker Hub リポジトリを用いる．厳密に version を固定するため dockerhub の [Tages](https://hub.docker.com/r/amazon/aws-lambda-python/tags) から，厳密に build 日時の明記された image のタグを指定するとよい．

### build 用の Dockerfile 作成
ここでは，pipeline で必要となる Docker container の中で Docker container を build する構成の検証を簡素化するため，Docker container の中で Dockerfile を build する構成とする．

Build 環境を Pipeline に組み込むには，pipeline を実行する Docker container 上で更に build 用の docker container を起動する必要がある．こうした構成は，DinD (Docker in Docker) (あるいは DooD: Docker outside of Docker) と呼び，Docker container とのファイルのやり取りや，pipeline 側の Docker container に docker engine を用意する必要があるなど，構成が複雑となる．








