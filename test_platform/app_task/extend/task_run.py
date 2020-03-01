# coding:utf-8
# 组装1：unittest测试框架+ddt
import os
import unittest
import requests
import json
import xmlrunner
from ddt import ddt,file_data

EXTEND_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DATA = os.path.join(EXTEND_DIR,"task_data.json")
TASK_RUN = os.path.join(EXTEND_DIR,"task_run.py")
TASK_RESULT = os.path.join(EXTEND_DIR,"task_result.xml")

@ddt
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


    @file_data(TASK_DATA)
    def test_run(self,url,header,method,paramter_type,paramter_body,assert_type,assert_text):

        # payload str ==> dict
        #1A 数据
        paramter_body = json.loads(paramter_body)
        header = json.loads(header)
        if method == 1:
            #2A 执行
            r = requests.post(url=url,headers=header,params=paramter_body)
            print(f"请求方法为GET:{r.text}")

            #3A断言
            if assert_type == 1:
                self.assertIn(assert_text,r.text)

            if assert_type == 2:
                self.assertEqual(assert_text, r.text)

        if method == 2:

            if paramter_type == 1:
                r = requests.post(url=url,headers=header,data=paramter_body)
                print(f"请求方法为POST,参数类型为:form -->{r.text}")

                # 3A断言
                if assert_type == 1:
                    self.assertIn(assert_text, r.text)

                if assert_type == 2:
                    self.assertEqual(assert_text, r.text)

            if paramter_type == 2:
                r = requests.post(url=url,headers=header,json=paramter_body)
                print(f"请求方法为POST,参数类型为:json -->{r.text}")

                # 3A断言
                if assert_type == 1:
                    self.assertIn(assert_text, r.text)

                if assert_type == 2:
                    self.assertEqual(assert_text, r.text)

if __name__ == '__main__':

    with open(TASK_RESULT,'wb+') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
