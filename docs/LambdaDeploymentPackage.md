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

**<u>build.sh</u>**
```bash
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
Build に利用する Lambda のランタイムには，Lambda の実行不要な機能は一切 install されていないため，docker に入り対話的に install を試行錯誤することはできない．このため，Dockerfile の build に合わせて Deployment package も build する．

以下に作成した Dockerfile を示す．
最後の `./build_deployment_package.sh` を実行すると，`deployment-package.zip` が docker container 内に作成される．

**<u>Dockerfile</u>**
```Dockerfile
FROM amazon/aws-lambda-python:3.8.2021.11.08.18

COPY ./* /home/

RUN pip install poetry
RUN yum install -y zip

RUN cd /home; ./build_deployment_package.sh
```

### build 用の shell script 作成
Dockerfile の build を利用して生成した `deployment-package.zip` は，docker container 内に作成される．このため，`docker cp` コマンドを利用して，`deployment-package.zip` を docker container 内から取り出す．

ここでは，docker build 用の shell script に付属する形で，生成物をコピーする．

[**<u>./build_dockerfile.sh</u>**](./build_dockerfile.sh)
```bash
#!/bin/bash
CONTAINER_NAME=gen-deployment-package
GEN_TARGET=deployment-package.zip

docker build -t $CONTAINER_NAME ./
sh ./docker_cp.sh $CONTAINER_NAME ./home/$GEN_TARGET .
sh ./docker_rmi.sh $CONTAINER_NAME
```

[**<u>./docker_sh/cp.sh</u>**](./docker_sh/cp.sh)  
※ docker cp を実行するには，docker container が起動している必要がある．
```bash
#!/bin/bash

# Usage:
#   CONTAINER_NAME=xxx
#   ./docker_cp.sh $CONTAINER_NAME ./[copy from the container dir] ./[copy to the host dir]

CONTAINER_NAME=$1
docker run -d $CONTAINER_NAME:latest
CONTAINER_ID=$(docker ps | grep $CONTAINER_NAME | awk '{print $1}')
docker cp $CONTAINER_ID:$2 $3
docker rm -f $CONTAINER_ID
```

### DinD の検証
Build 環境を Pipeline に組み込むには，pipeline を実行する Docker container 上で更に build 用の docker container を起動する必要がある．こうした構成は，DinD (Docker in Docker) (あるいは DooD: Docker outside of Docker) と呼び，Docker container とのファイルのやり取りや，pipeline 側の Docker container に docker engine を用意する必要がある．

Docker container とのファイルのやり取りには，前述の通り `$ docker cp` コマンドを用いた．

ここでは，docker engine を持つ Docker container を用意し，DinD の動作を local 環境で検証する．

#### build 用 docker image の選定
Docker Hub が DinD 用の docker image を公開しているので，これ [`docker:stable-dind`](https://hub.docker.com/layers/docker/library/docker/stable-dind/images/sha256-a6b0193cbf4d3c304f3bf6c6c253d88c25a22c6ffe6847fd57a6269e4324745f?context=explore) を利用する．

#### DinD の動作テスト
DinD の動作をテストするには，DinD 用の docker image に `--privileged` オプションで権限を与え，`-d` オプションでバックグラウンド実行したあと，[`exec` オプションでログインする必要](http://shomi3023.com/2018/09/01/docker-in-docker/)がある．(直接 sh で入ると上手く動作しない) ．

例えば次のようにする．
```bash
$ docker run --privileged --name dind -d docker:19.03.0-dind
$ docker exec -it dind sh
```

DinD の起動プロセスをシェルスクリプトに落とし込む場合には注意が必要で，docker deamon の起動を待機してから `exec` でログインする必要がある．なお，`$ docker info` の結果をもってログインすると，docker deamon が完全に起動していない場合があるため，空の Dockerfile を作成して `$ docker build` を試すとよい．詳細は [./docker_sh/sleep_until_docker_deamon_to_be_ready.sh](./docker_sh/sleep_until_docker_deamon_to_be_ready.sh) を参照すること．

DinD docker container の起動前に build 処理が走り，エラーが発生することは，実際の CI でも起こるため注意すること．(参考: [GitLab CIでdocker imageをビルドする時、docker daemonが起動してくるまで待つ](https://qiita.com/jesus_isao/items/b141b45bf26293894559))

#### DooD の動作テスト
DooD の動作をテストするには，`-v` オプションを付けて[container 側から host の docker.sock (/var/run/docker.sock) をマウントする](https://blog.nijohando.jp/post/docker-in-docker-docker-outside-of-docker/)必要がある．すると，host 型の docker engine を用いて container が実行される．

例えば，次のようにする．
```
$ docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock docker sh
```

#### DinD と DooD の比較
DinD と DooD を比較すると，DooD の方が遥かに簡素に実装できるため，DooD で済むのであれば DooD を使うことが望ましい．

なお，DinD と DooD の比較は[Dockerコンテナ内からDockerを使うことについて](https://esakat.github.io/esakat-blog/posts/docker-in-docker/))にまとまっており，次のように説明されている．
> CI用途に関してはDooDを使うのが好ましいと思います. DinDの開発者自身がブログでDinDのCI利用について述べています https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/
> 
> ざっと要点
> 
> - そもそものDinDの用途はDockerの開発プロセス高速化のためだった
> - DinDは次の問題がある
>   - SELinuxとかをホストとコンテナで別設定にしていると、クラッシュする可能性がある
>   - ホストとコンテナで別々のファイルシステムを使っているとクラッシュする可能性がある
>   - /var/lib/dockerはdockerデーモンの専用領域みたいなものだから、別デーモン作って触らせると何が起きても知らないよ
> - CIをやりたないならDooDでいいんじゃない？
>   - ホストとDockerデーモンを共有することで、ビルドごとにイメージのキャッシュが消えたりがなくなると思うよ
>   - 上の問題点も解決すると思うよ
> 
> 参考: [Dockerコンテナ内からDockerを使うことについて](https://esakat.github.io/esakat-blog/posts/docker-in-docker/))

