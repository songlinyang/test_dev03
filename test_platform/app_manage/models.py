from django.db import models

# Create your models here.
#django ORM
class Project(models.Model):
    """
    项目管理表
    """
    name = models.CharField('名称',max_length=100,null=False,blank=True)
    describe = models.TextField('描述',default='')
    status = models.BooleanField('状态',default=True,null=False)
    update_time = models.DateTimeField('更新时间',auto_now=True)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    """
    模块管理表
    """
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    name = models.CharField('名称',max_length=100,null=False,blank=True)
    describe = models.TextField('描述',default='')
    update_time = models.DateTimeField('更新时间',auto_now=True)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)


