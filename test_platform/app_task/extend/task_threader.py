import os
import json
import threading
from test_platform.common import Response
from app_case.models import TestCase
from app_task.models import Task
from app_task.models import TestResult
from .logout import info
from time import sleep
from xml.dom.minidom import parse
EXTEND_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_DATA = os.path.join(EXTEND_DIR,"task_data.json")
TASK_RUN = os.path.join(EXTEND_DIR,"task_run.py")
TASK_RESULT = os.path.join(EXTEND_DIR,"task_result.xml")




class TaskThreader():

    def __init__(self,task_id):
        self.task_id = task_id


    def run_cases(self):



        if self.task_id == "":
            return Response(code=10101, message="用例ID不能为空")

        task = Task.objects.get(id=self.task_id)

        if task.tests == "":
            return Response(code=10101, message="用例ID不能为空")
        cases = task.tests[1:-1].split(",")
        info(f"开始执行任务，任务状态status=1,为执行中")
        task.status = 1
        task.save()

        case_data = {}
        for caseId in cases:
            case = TestCase.objects.get(id=caseId)
            info(f"用例ID：{case.id}")
            case_data[case.name] = {
                "url":case.url,
                "method":case.method,
                "header":case.header,
                "paramter_type":case.paramter_type,
                "paramter_body":case.paramter_body,
                "assert_type":case.assert_type,
                "assert_text":case.assert_text
            }
        info(f"需执行的用例：{case_data}")
        case_str = json.dumps(case_data)

        #写成Json ddt驱动文件并保存
        with open(TASK_DATA,mode='w') as f:
            f.write(case_str)

        #运行用例
        os.system("python "+TASK_RUN)

        # 防止多线程执行，影响统计结果保存
        sleep(2)

        #保存结果
        self.save_result()

        #修改任务执行状态
        task = Task.objects.get(id=self.task_id)
        task.status = 2
        task.save()
        info(f"跑批执行任务完成，任务状态status=2,为执行完成")



    def save_result(self):
        #读取统计XML文件
        f = open(TASK_RESULT,"r",encoding="utf-8")
        result = f.read()
        f.close()

        #读取xml数据
        # 打开xml文档
        dom = parse(TASK_RESULT)

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

        if result=="":
            return Response(code=10101, message="获取的统计结果内容为空")

        if name=="" or failures=="" or errors == "" or skipped == "" or tests == "" or time == "":
            return Response(code=10102,message="获取统计结果数据有误")


        try:
            TestResult.objects.create(
                task_id=self.task_id,
                name=name,
                errors=errors,
                failures=failures,
                skipped=skipped,
                tests=tests,
                run_time=time,
                result=result,
            )
        except Exception as e:
            info(f"保存统计结果Errors:{e}")

    def run_task(self):
        info("开始创建线程跑批任务...")
        sleep(2)
        t1 = threading.Thread(target=self.run_cases)
        t1.start()
        t1.join()

    def run(self):
        t = threading.Thread(target=self.run_task)
        t.start()


