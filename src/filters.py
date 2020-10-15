from .types import Config, Item
from typing import Any, Callable, List


def filter_folder(item: Item, config: Config):
    if config.folder:
        return item.folder and config.folder in item.folder
    return True


def filter_edit_coment(item: Item, config: Config):
    if config.edit_comment:
        return item.edit_comment
    return True


def convert_pretext(payload: dict, item: Item, config: Config):
    template = config.pretext
    if template:
        payload['attachments'][0]['pretext'] = template.format(**item.dict())


def convert_channel(payload: dict, item: Item, config: Config):
    if config.channel:
        payload['channel'] = config.channel


Filter = Callable[[Item, Config], Any]
filters: List[Filter] = [filter_folder, filter_edit_coment]

Converter = Callable[[dict, Item, Config], Any]
converters: List[Converter] = [convert_pretext, convert_channel]
