from enum import Enum


class ErrorObject(dict, Enum):
    # Common
    BAD_REQUEST = {'code': 1001, 'msg': 'BAD_REQUEST'}
    # Article app
    ARTICLE_NOT_FOUND = {'code': 2001, 'message': 'ARTICLE_NOT_FOUND'}
