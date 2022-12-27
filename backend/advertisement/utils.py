import os

from contextlib import contextmanager

from bitrix24 import Bitrix24


@contextmanager
def bitrix_manager():
    yield Bitrix24(os.environ.get('BITRIX_HOOK_URL'))
