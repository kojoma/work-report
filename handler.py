# -*- coding: utf-8 -*-

import json
import logging
import os
import time
import boto3

from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DYNAMODB_TABLE_NAME = os.environ['dynamoDBTableName']
dynamodb = boto3.resource('dynamodb')
dynamodb_table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def record_work_time(event, context):
    logger.info(json.dumps(event))

    if 'project_name' in event.keys():
        project_name = event['project_name']
    else:
        raise Exception("project_name is required parameter!")

    if 'start_datetime' in event.keys():
        start_timestamp = __datetime_to_timestamp(event['start_datetime'])
    else:
        start_timestamp = datetime.today().timestamp()

    if 'end_datetime' in event.keys():
        end_timestamp = __datetime_to_timestamp(event['end_datetime'])
    else:
        end_timestamp = datetime.today().timestamp()

    __save_work_time(project_name, start_timestamp, end_timestamp)

def __datetime_to_timestamp(dt_str: str) -> float:
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
    except:
        raise Exception("start_datetime and end_datetime is '%Y-%m-%d %H:%M' format parameter!")

    return dt.timestamp()

def __save_work_time(project_name: str, start_timestamp: float, end_timestamp: float) -> None:
    dynamodb_table.put_item(
        Item={
            'project_name': project_name,
            'start_time': str(start_timestamp),
            'end_time': str(end_timestamp),
        }
    )
