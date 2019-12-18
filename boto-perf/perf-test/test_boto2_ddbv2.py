import cProfile
import random

import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table

from config import REGION, ACCESS_KEY, SECRET_KEY


class PerfTester:
    TABLE_NAME = 'perf_test_for_boto2_v2'
    NUMS = 5
    PRE_GEN_KV_PAIR = []

    def __init__(self, remove_table=False):
        self.pre_generate_kv()
        self.setup()
        self.perf_test()
        if remove_table:
            self.teardown()

    def perf_test(self):
        self.put_items()
        self.get_items()
        self.update_items()
        self.delete_items()

    def pre_generate_kv(self):
        for _ in range(self.NUMS):
            self.PRE_GEN_KV_PAIR.append(
                [str(random.randint(0, 10000)), str(random.randint(0, 10000))]
            )

    def mexec(self, func):
        func()

    def put_items(self):
        def _exec():
            for pair in self.PRE_GEN_KV_PAIR:
                self.table.put_item(
                    data={
                        'username': pair[0],
                        'last_name': pair[1],
                        'age': random.randint(0, 100),
                        'account_type': 'standard_user'
                    }
                )
        self.mexec(_exec)

    def get_items(self):
        def _exec():
            for target in self.PRE_GEN_KV_PAIR:
                self.table.get_item(
                    username=target[0],
                    last_name=target[1]
                )
        self.mexec(_exec)

    def update_items(self):
        def _exec():
            for target in self.PRE_GEN_KV_PAIR:
                item = self.table.get_item(
                    username=target[0],
                    last_name=target[1]
                )
                item['age'] = random.randint(0, 100)
                item.save()
        self.mexec(_exec)

    def delete_items(self):
        def _exec():
            for target in self.PRE_GEN_KV_PAIR:
                self.table.delete_item(
                    username=target[0],
                    last_name=target[1]
                )
        self.mexec(_exec)

    def setup(self):
        try:
            # try create table anyway
            self.table = Table.create(
                self.TABLE_NAME,
                schema=[
                    HashKey('username'),
                    RangeKey('last_name'),
                ],
                throughput={
                    'read': 5,
                    'write': 5,
                },
                connection=boto.dynamodb2.connect_to_region(
                    REGION,
                    aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY
                )
            )
        except Exception:
            self.table = Table(self.TABLE_NAME)

    def teardown(self):
        self.table.delete()


cProfile.run('PerfTester()')
