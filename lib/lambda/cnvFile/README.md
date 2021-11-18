# Lambda deproyment package の構成手順

ここでは，.zip file archives として Lambda function を構成する手順を説明する．

- 参考: 
  - [Deploy Python Lambda functions with .zip file archives](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
  - [.zip ファイルアーカイブで Python Lambda 関数をデプロイする](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-package.html)

## Deployment package の管理
ここでは deployment package を package manager で管理する．
Package manager には Poetry を用いる．

### Poetry の install と仮想環境の構築
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
   既存の `pyproject.toml` から lockfile を生成する場合は，`$ poetry install` により，ライブラリを install し，`pyproject.toml` から `poetry.lock` を生成する．

## .zip file archive の生成

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





