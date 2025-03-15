# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON:  4:59 PM
# LAST MODIFIED ON:
# AIM:
def create_error_response(code: int, message: str):
    return {'code': code, 'message': message}


UNKNOWN_ERROR = create_error_response(1, 'Unknown error')
SERVICE_TEMPORARILY_UNAVAILABLE = create_error_response(2, 'Service temporarily unavailable')
UNSUPPORTED_METHOD = create_error_response(3, 'Unsupported  method')
NO_PERMISSION_TO_ACCESS_DATA = create_error_response(4, 'No permission to access data')
INVALID_PARAMETER = create_error_response(5, 'Invalid parameter')
INVALID_PRIVILEGE = create_error_response(6, 'Operation required admin privilege')
INVALID_USER = create_error_response(7, 'Invalid user')
INVALID_PASSWORD = create_error_response(8, 'Invalid password')
USER_EXISTS = create_error_response(9, 'User already exists')
INVALID_BOOK = create_error_response(10, 'Invalid book')
INVALID_TOKEN = create_error_response(11, 'Invalid token')
DB_ERROR = create_error_response(12, 'DB error')
INVALID_CHAPTER = create_error_response(13, 'Invalid chapter')
INVALID_CHAPTER_CONTENT = create_error_response(14, 'Invalid chapter content')
INVALID_TERMINOLOGY = create_error_response(15, 'Invalid terminology')
TERMINOLOGY_EXISTS = create_error_response(16, 'Terminology already exists')
INVALID_TASK = create_error_response(17, 'Invalid task')
INVALID_TERMINOLOGY_COLLECTION = create_error_response(18, 'Invalid terminology')
INVALID_BOOK_FILE_VERSION = create_error_response(19, 'Invalid book file version')
INVALID_BOOK_FORMAT = create_error_response(20, 'Invalid book format')
INVALID_CHAPTER_FORMAT = create_error_response(21, 'Invalid chapter format')
INVALID_CHAPTER_CONTENT_FORMAT = create_error_response(22, 'Invalid chapter content format')
HTTP_SERVICE_REQUEST_FAILED = create_error_response(23, 'HTTP service request failed')
USER_NOT_EXISTS = create_error_response(24, 'User does not exists')
USER_BANNED = create_error_response(25, 'User is banned')
CONTENT_TAG_EXISTS = create_error_response(26, 'Content tag already exists')
INVALID_TIME_RANGE = create_error_response(27, 'The range of date should less than 31')
FAILED_TO_CALL_AI_SERVICE = create_error_response(28, 'Failed to call AI service')
BOOK_NAME_EXISTS = create_error_response(29, 'Book name already exists')
CHAPTER_NAME_EXISTS = create_error_response(30, 'Chapter name already exists')
TERMINOLOGY_NAME_EXISTS = create_error_response(31, 'Terminology name already exists')
INVALID_COLLECTION_FILE_FORMAT = create_error_response(32, 'Invalid collection format, please make sure the file is "utf8" and "gbk" encoding')
INVALID_DATA_TASK = create_error_response(33, 'Invalid data task format')
INVALID_TEMPLATE = create_error_response(34, "Invalid template")
DATA_TASK_EXISTS = create_error_response(35, 'Data task already exists')
STATISTICS_ALREADY_EXISTS = create_error_response(36, 'Statistic already exists')
INVALID_WEEKLY_DATE = create_error_response(37, 'Invalid weekly start or end, start should be Monday, end should be Sunday')
NO_TASK_IS_CREATED = create_error_response(38, 'No task is created')
INVALID_TASK_TYPE = create_error_response(39, 'Invalid task type')
INVALID_CHAPTER_WORD_COUNT = create_error_response(40, 'The word count of chapter is to long')
INVALID_TAG = create_error_response(41, 'Invalid tag')
EMPTY_CHAPTER_CONTENT = create_error_response(41, 'Empty chapter content')
TRANSLATE_ERROR = create_error_response(42, 'Translate error')
INVALID_LANGUAGE_PAIR = create_error_response(43, 'Invalid language pair')



