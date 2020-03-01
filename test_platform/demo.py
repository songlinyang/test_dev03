# # coding:utf-8
# import unittest
#
# class Test(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         global Token
#         Token = "Token@123"
#
#     @classmethod
#     def tearDownClass(self):
#         pass
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def test_Token(self):
#         # global Token
#         Token = "123"
#
#         print(Token)
#     def test_Token2(self):
#         print(Token)
#
#
# if __name__ == '__main__':
#     unittest.main()
#
from test_platform.logout import info
from xml.dom.minidom import parse
#读取xml数据
# 打开xml文档
dom = parse("./task_result.xml")

# 得到文档元素对象
root = dom.documentElement

# 获取(一组)标签
testsuite = root.getElementsByTagName('testsuite')
name = testsuite[0].getAttribute("name")
failures = testsuite[0].getAttribute("failures")
errors = testsuite[0].getAttribute("errors")
skipped = testsuite[0].getAttribute("skipped")
tests = testsuite[0].getAttribute("tests")
time = testsuite[0].getAttribute("time")

info(f"name:{name}")
info(f"failures:{failures}")
info(f"errors:{errors}")
info(f"skipped:{skipped}")
info(f"tests:{tests}")
info(f"time:{time}")

if errors == "":
    info(f"errors:{errors}，为空")