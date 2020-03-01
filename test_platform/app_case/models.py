from django.db import models
from app_manage.models import Module

class TestCase(models.Model):
    """
    测试用例表
    """
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    name = models.CharField("用例名称",max_length=50,null=False) #最大长度50，不能为空null=False
    url = models.TextField("URL",null=False)
    #1.GET 2.POST 3.DELETE 4.PUT
    method = models.IntegerField("请求方法",null=False)
    header = models.TextField("请求头",null=False)
    #1.form-data 2.Json
    paramter_type = models.IntegerField("参数类型",null=False)
    paramter_body = models.TextField("请求体",null=False)
    result = models.TextField("响应结果",null=False)
    assert_type = models.IntegerField("断言类型",null=False)
    assert_text = models.TextField("断言内容",null=False)
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        return self.name