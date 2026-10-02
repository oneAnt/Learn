from django.db import models

# Create your models here.
class Task(models.Model):
    """
    任务
    """
    # 定义变量
    id = models.AutoField(primary_key=True) # id
    title = models.CharField(max_length=100) # 标题
    status = models.BooleanField(default=False) # 状态 默认未完成
    created_at = models.DateTimeField(auto_now_add=True) # 创建时间

    class Meta:
        # 表名
        db_table = "task"
        # 按照创建时间倒序排序
        ordering = ["-created_at"]
