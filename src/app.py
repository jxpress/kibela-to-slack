import json
from typing import Any, Optional
import re
from pathlib import Path

import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse


from .types import Config, Item
from .filters import filters, converters
from .config import KIBELA_API_TOKEN, KIBELA_BASE_URL, SLACK_WEBHOOK_URL


app = FastAPI()

re_comment = re.compile(f'{KIBELA_BASE_URL}[^#|]+')


def payload_to_item(payload: dict) -> Item:
    attachment = payload['attachments'][0]
    field_list = attachment.get('fields') or []
    fields = {f['title']: f['value'] for f in field_list}
    item = Item(
        text=attachment['text'],
        title=attachment.get('title'),
        folder=fields.get('フォルダ'),
        group=fields.get('グループ'),
        edit_comment=fields.get('編集コメント'),
        author_name=attachment['author_name'],
    )
    if KIBELA_API_TOKEN and KIBELA_BASE_URL and not item.title and not fields:
        # Assume that "item" is a comment, not wiki
        if match := re_comment.search(attachment.get('pretext', '')):
            path = match.group()
            res = requests.post(f'{KIBELA_BASE_URL}/api/v1', json={
                "query": '''
                query($path: String!) {
                    noteFromPath(path: $path) {
                        title
                        folderName
                    }
                }
                ''',
                "variables": {
                    "path": path
                }
            }, headers={
                "Authorization": f"Bearer {KIBELA_API_TOKEN}"
            })
            if res.ok and res.json().get('data'):
                note = res.json()['data']['noteFromPath']
                item.title = note['title']
                item.folder = note['folderName']
    return item


@app.get('/', response_class=HTMLResponse)
def index():
    path = Path(__file__).parent / 'index.html'
    with open(path) as f:
        return f.read()


@app.post("/webhook")
def post_webhook(pretext: Optional[str] = None, edit_comment: Optional[Any] = None,
                 folder: Optional[str] = None, channel: Optional[str] = None,
                 preserve_comments: Optional[Any] = None,
                 payload: str = Form(...)):
    config = Config(
        pretext=pretext,
        edit_comment=edit_comment,
        folder=folder,
        channel=channel,
        preserve_comments=preserve_comments
    )
    payload_dic = json.loads(payload)
    item = payload_to_item(payload_dic)

    send = True
    for should_send in filters:
        if send:
            send = should_send(item, config)

    if send:
        for convert in converters:
            convert(payload_dic, item, config)
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload_dic))

    return {
        "status": "ok"
    }
