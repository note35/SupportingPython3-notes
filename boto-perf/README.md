# DDB CRUD Performance Test for boto2 and boto3

This package uses [Boto2 DDB v1 API](http://boto.cloudhackers.com/en/latest/dynamodb_tut.html), [Boto2 DDB v2 API without batch](http://boto.cloudhackers.com/en/latest/dynamodb2_tut.html), and [boto3 DDB API with batch](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html).

## Steps

**1. Setup**

```bash
# Intallation
# put access_key, secret_key, and region into config.py
(env) $ pip install tox
(env) $ tox

# Syntax Check
(env) $ tox -epep8

# Run once py37-boto2 and py37-boto3 to create the table
(env) $ python perf-test/test_boto2_ddb.py
(env) $ python perf-test/test_boto2_ddbv2.py
(env) $ python perf-test/test_boto3_ddb.py
```

**2. Perf**

```bash
# Perf Test
(env) $ tox -e py27-boto2
(env) $ tox -e py37-boto2
(env) $ tox -e py27-boto2v2
(env) $ tox -e py37-boto2v2
(env) $ tox -e py27-boto3
(env) $ tox -e py37-boto3
(env) $ tox -e py27-boto3_with_batch_writers
(env) $ tox -e py37-boto3_with_batch_writers
```

**3. Teardown**

```
# Remove the table manually
```

## Result Analysis

* You can find the detail in file: example.benchmark

- The benchmark is simple, doing following actions:
  1. put 5 items
  2. get 5 items
  3. update 5 items
  4. delete 5 items

- boto comparison
  - Python2
      - boto3 is 35% faster than boto2 v1
      - boto3 is 25% faster than boto2 v2
      - boto2 v2 is 15% faster than boto2 v1 
  - Python3
      - boto3 is 67% faster than boto2 v1
      - boto3 is 50% faster than boto2 v2
      - boto2 v2 is 12% faster than boto2 v1 
- Python comparison
  - In both boto2 v1 and boto2 v2
    - python37 is twice slower than python27.
  - In both boto3 and boto3 batch
    - python37 is slightly slower than python27. (0~5%)
  - In boto3 batch mode
    - both python27 and python37 get speed improvement. (30~35%)
        - put/delete have 80% speed improvement
- Conclusion
  - boto3 > boto2 v2 > boto2 v1
