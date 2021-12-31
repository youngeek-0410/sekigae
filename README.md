# Sekigae
席替えサービス

## Steps development at first time
1. clone this repository
1. `cd sekigae`
1. `npm install`
1. pythonの仮想環境を作成
    1. `python -m venv venv`
    1. `source venv/bin/activate`
    1. `pip install -r requirements.txt`
1. 環境変数ファイルを追加 (tmplを参考に作成し、足りない情報はslackで確認)
    - add fastapi/fastapi.env
    - add postgres/postgres.env
1. docker containerを起動
    1. `source env.sh`
    1. `build`
    1. `docker-compose run --entrypoint "poetry install" fastapi`
    1. `up`

## Steps development after first setup
1. `cd sekigae`
1. `source venv/bin/activate`
1. `source env.sh`
1. `up`