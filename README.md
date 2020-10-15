# Kibela Slack Integraion Webhook

ナレッジシェアの SaaS「[Kibela](https://kibe.la/)」の Slack 連携を強化するための OSS です。

次のような機能があります。

- フォルダごとの Slack チャンネルの打ち分け
- Slack に投稿する文章のテンプレート化
- 編集コメントつきな記事編集のみの通知

## 設定

### Kibela への登録

Kibela の Outgoing Webhook で「Slack」の Webhook を追加してください。

URL には、次のような URL を指定します。URLのドメイン部は *.kibe.la ではなく、この OSS をデプロイした際の ドメインです。

`https://your-deployment-url/webhook`

URL パラメータを通じて、カスタマイズできます。 `https://your-deployment-url/` から URL を生成することもできます。

### 環境変数

次の環境変数の指定が必要です。

|環境変数|意味|例|
|:---|:---|:---|
|SLACK_WEBHOOK_URL|**必須**。Slack の Incoming Webhook の URL|https://hooks.slack.com/services/ABCDEF...|
|KIBELA_BASE_URL|**コメントのフォルダごと打ち分けに場合必須**。Kibela の URL|https://XXX.kibe.la|
|KIBELA_API_TOKEN|**コメントのフォルダごと打ち分けに場合必須**。Kibela の API の個人用アクセストークン([取得用URL](https://my.kibe.la/settings/access_tokens))|secret/AB/CDEF....|

### オプション

Kibela の Outgoing Webhooks に登録する際、次のオプションを利用することができます。全てのオプションは任意です。

**パラメータの値は、URLエンコードしてください**。(例： hoge/ぴよ → hoge%2F%E3%81%B4%E3%82%88)

|パラメータ|意味|例|
|:---|:---|:---|
|channel|Slack のチャンネル名|general|
|folder|フォルダの指定(部分一致)。必ず URL エンコードをしてください|hoge/ぴよ|
|pretext|pretext(Slack 投下時の文字列)のテンプレートです。Python の `str.format` に有効な文字列です|{author_name}が記事を作成しました|
|edit-comment|編集コメントがある場合のみ通知します|1|

## デプロイ

FastAPI を使っているので、通常の Python のデプロイに従ってください([参考](https://fastapi.tiangolo.com/deployment/))。

また、[Serverless Framework](https://www.serverless.com/) もサポートしています。

```
npm install
npm run deploy
```

## 開発

[Poetry](https://python-poetry.org/) を使った依存ライブラリのインストールが必要です(pip install で個別にインストールしても問題ありません)。

```
poetry install
```

環境変数を設定した上で、次のコマンドで立ち上げることができます。

```
poetry run uvicorn src.app:app --reload    
```
