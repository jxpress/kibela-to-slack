from typing import Any, Callable, List
import re

from .types import Config, Item

comment_pattern = re.compile('<!--.*?-->', re.DOTALL)


def filter_folder(item: Item, config: Config):
    if config.folder:
        return item.folder and config.folder in item.folder
    return True


def filter_title(item: Item, config: Config):
    if config.title:
        return item.title and config.title in item.title
    return True


def filter_edit_coment(item: Item, config: Config):
    if config.edit_comment:
        return item.edit_comment
    return True


def filter_draft(item: Item, config: Config):
    if config.skip_draft and item.title:
        return ('WIP' not in item.title
                and 'Draft' not in item.title
                and '下書き' not in item.title)
    return True


def convert_pretext(payload: dict, item: Item, config: Config):
    template = config.pretext
    if template:
        payload['attachments'][0]['pretext'] = template.format(**item.dict())


def convert_channel(payload: dict, item: Item, config: Config):
    if config.channel:
        payload['channel'] = config.channel


def convert_trim_comment(payload: dict, item: Item, config: Config):
    print(payload['attachments'][0]['text'])
    if not config.preserve_comments and payload['attachments'][0]['text']:
        payload['attachments'][0]['text'] = comment_pattern.sub(
            '', payload['attachments'][0]['text'])


Filter = Callable[[Item, Config], Any]
filters: List[Filter] = [filter_folder, filter_title, filter_edit_coment, filter_draft]

Converter = Callable[[dict, Item, Config], Any]
converters: List[Converter] = [convert_pretext, convert_channel, convert_trim_comment]
