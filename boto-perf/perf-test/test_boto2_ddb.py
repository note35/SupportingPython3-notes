import cProfile
import random

import boto.dynamodb

from config import REGION, ACCESS_KEY, SECRET_KEY


class PerfTester:
    TABLE_NAME = 'perf_test_for_boto2_v1'
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
                item = self.table.new_item(
                    hash_key=pair[0],
                    range_key=pair[1],
                    attrs={
                        'age': random.randint(0, 100),
                        'account_type': 'standard_user'
                    }
                )
                item.put()
        self.mexec(_exec)

    def get_items(self):
        def _exec():
            for target in self.PRE_GEN_KV_PAIR:
                self.table.get_item(
                    hash_key=target[0],
                    range_key=target[1]
                )
        self.mexec(_exec)

    def update_items(self):
        def _exec():
            for target in self.PRE_GEN_KV_PAIR:
                item = self.table.get_item(
                    hash_key=target[0],
                    range_key=target[1]
                )
                item['age'] = random.randint(0, 100)
                item.put()
        self.mexec(_exec)

    def delete_items(self):
        def _exec():
            for target in self.PRE_GEN_KV_PAIR:
                item = self.table.get_item(
                    hash_key=target[0],
                    range_key=target[1]
                )
                item.delete()
        self.mexec(_exec)

    def setup(self):
        conn = boto.dynamodb.connect_to_region(
            REGION,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )
        message_table_schema = conn.create_schema(
            hash_key_name='username',
            hash_key_proto_value=str,
            range_key_name='last_name',
            range_key_proto_value=str
        )
        try:
            # try create table anyway
            self.table = conn.create_table(
                name=self.TABLE_NAME,
                schema=message_table_schema,
                read_units=5,
                write_units=5
            )
        except Exception:
            self.table = conn.get_table(self.TABLE_NAME)

    def teardown(self):
        self.table.delete()


cProfile.run('PerfTester()')
