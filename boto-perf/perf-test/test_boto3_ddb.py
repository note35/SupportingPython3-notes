import cProfile
import os
import random

import boto3

from config import REGION, ACCESS_KEY, SECRET_KEY


class PerfTester:
    TABLE_NAME = 'perf_test_for_boto3'
    NUMS = 5
    PRE_GEN_KV_PAIR = []

    def __init__(self, remove_table=False, with_batch_writers=False):
        self.pre_generate_kv()
        self.setup()
        self.perf_test(with_batch_writers)
        if remove_table:
            self.teardown()

    def perf_test(self, with_batch_writers):
        self.put_items(with_batch_writers)
        self.get_items()
        self.update_items()
        self.delete_items(with_batch_writers)

    def pre_generate_kv(self):
        for _ in range(self.NUMS):
            self.PRE_GEN_KV_PAIR.append(
                [str(random.randint(0, 10000)), str(random.randint(0, 10000))]
            )

    def mexec(self, func, with_batch_writers):
        if with_batch_writers:
            with self.table.batch_writer() as batch:  # noqa: F841
                func(batch)
        else:
            func()

    def put_items(self, with_batch_writers=False):
        def _exec(indicator=self.table):
            for pair in self.PRE_GEN_KV_PAIR:
                indicator.put_item(
                    Item={
                        'username': pair[0],
                        'last_name': pair[1],
                        'age': random.randint(0, 100),
                        'account_type': 'standard_user',
                    }
                )
        self.mexec(_exec, with_batch_writers)

    def get_items(self):
        for target in self.PRE_GEN_KV_PAIR:
            self.table.get_item(
                Key={
                    'username': target[0],
                    'last_name': target[1]
                }
            )

    def update_items(self):
        for target in self.PRE_GEN_KV_PAIR:
            self.table.update_item(
                Key={
                    'username': target[0],
                    'last_name': target[1]
                },
                UpdateExpression='SET age = :val1',
                ExpressionAttributeValues={
                    ':val1': random.randint(0, 100)
                }
            )

    def delete_items(self, with_batch_writers=False):
        def _exec(indicator=self.table):
            for target in self.PRE_GEN_KV_PAIR:
                indicator.delete_item(
                    Key={
                        'username': target[0],
                        'last_name': target[1]
                    }
                )
        self.mexec(_exec, with_batch_writers)

    def setup(self):
        session = boto3.Session(
            region_name=REGION,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        dynamodb = session.resource('dynamodb')
        try:
            # try create table anyway
            self.table = dynamodb.create_table(
                TableName=self.TABLE_NAME,
                KeySchema=[
                    {
                        'AttributeName': 'username',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'last_name',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'last_name',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            # Wait until the table exists.
            self.table.meta.client.get_waiter('table_exists').wait(
                TableName=self.TABLE_NAME
            )
        except Exception:  # botocore.errorfactory.ResourceInUseException:
            self.table = dynamodb.Table(self.TABLE_NAME)

    def teardown(self):
        self.table.delete()


with_batch_writers = True if os.environ.get('with_batch_writers') else False
cProfile.run('PerfTester(with_batch_writers=with_batch_writers)')
