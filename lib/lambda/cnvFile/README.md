# lambda function


build process の説明は，[../docs/LambdaDeploymentPackage.md](../docs/LambdaDeploymentPackage.md) を参照すること．


## File and Directory descriptions

| File or directory name      | Description Origin |
| --------------------------- | ------------------ |
| docker_sh/                  | docker 操作用の shell script を格納する directory |
| docker_sh/cp.sh             | container name で docker cp する shell script |
| docker_sh/rmc.sh            | container name で docker container を削除する shell script |
| docker_sh/rmi.sh            | container name で docker image を削除する shell script |
| docker_sh/sleep_until_docker_deamon_to_be_ready.sh | docker deameon が起動するまで待機する shell script |
| Dockerfile                  | Deployment package を build するための Dockerfile．Base image の環境を lambda runtime の環境に合わせてあり，実行環境と同じ環境で build できる． |
| README.md                   | 本ファイル． |
| build_deployment_package.sh | local 環境で deployment package を build する shell script． |
| build_dockerfile.sh         | Dockerfile の build に合わせて deployment package を build する shell script．Dockerfile は local の docker engine で build される． |
| build_dockerfile_by_DinD.sh | DinD で Dockerfile を build する shell script．Dockerfile は DinD container 内の Docker engine で build される． |
| build_dockerfile_by_DooD.sh | DooD で Dockerfile を build する shell script．Dockerfile は host OS の Docker engine で build される． |
| clean.sh                    | 生成物と一時ファイル，docker container，docker image を削除する shell script．git 管理外の file が全て削除される． |
| index.py                    | lambda 関数のエントリーポイント． |
| poetry.lock                 | lambda 関数に使う Python の deployment package を管理する lock file．Poetry が管理する file． |
| poetry.toml                 | lambda 関数に使う Python の deployment package を管理する file．Poetry が管理する file． |
| pyproject.toml              | lambda 関数に使う Python の deployment package を管理する file．Poetry が管理する file． |

