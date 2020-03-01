from django.db import models

# Create your models here.

class Task(models.Model):
    name = models.CharField("名称",max_length=50,blank=True,null=False)
    desc = models.TextField("描述",null=False)
    status = models.IntegerField("状态",null=False)
    tests = models.TextField("测试用例集",null=False)
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)


class TestResult(models.Model):
    """
    测试结果表
    """
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    name = models.CharField("名称",max_length=100,blank=False,default="")
    errors = models.IntegerField("错误用例")
    failures = models.IntegerField("失败用例")
    skipped = models.IntegerField("跳过用例")
    tests = models.IntegerField("总用例数")
    run_time = models.FloatField("运行时长")
    result = models.TextField("详细", default="")
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        return self.name
