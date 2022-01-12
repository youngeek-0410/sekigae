# Sekigae
席替えサービス

## Setup Procedure
初回は以下の手順を全て行う。  
次回以降は、基本的に"Server Startup"のみを行う。(ただし、依存関係やDBに変更があった場合は、適宜"Container Setup"の対応する手順を行う)
### Initialize
1. clone this repository
1. `cd sekigae`
1. `npm install`
1. pythonの仮想環境を作成
    1. `python -m venv venv`
    1. `source venv/bin/activate`
    1. `pip install -r requirements.txt`
1. 環境変数ファイルを追加 (tmplを参考に作成し、足りない情報はslackで確認)
    - add fastapi/fastapi.env

### Container Setup
1. コンテナ ボリューム ネットワーク作成・起動  
  ```sh
  docker-compose up -d
  ```
2. 依存パッケージのインストール
  ```sh
  docker-compose run fastapi poetry install
  ```
3. DB migrate
  ```sh
  docker-compose run fastapi poetry run alembic upgrade head
  ```

### Server Startup
```sh
docker-compose run -p 8000:8000 fastapi ./scripts/server
```
