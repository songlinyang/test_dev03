# coding:utf-8
# 组装1：unittest测试框架+ddt
import os
import unittest
import requests
import json
import xmlrunner
from pathlib import Path
result_path = Path.cwd().joinpath("extend/task_result.xml")

class RunTaskTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):

        # payload str ==> dict
        url = "http://httpbin.org/post"
        data = {"key":"value"}

        r = requests.post(url, data=data)
        rsp = r.json()
        print(rsp)

if __name__ == '__main__':
    print(result_path)
    with open('./extend/task_result.xml','wb') as output:

        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),failfast=False,
            buffer=False,catchbreak=False
        )
