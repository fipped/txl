from django.db import models
from user.models import User
# Create your models here.


class AddressBook(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(u'姓名', max_length=30, null=False)
    phone = models.CharField(u'手机号码', max_length=20, null=False)
    add_time = models.DateTimeField(u'添加时间', auto_now_add=True)
    address = models.CharField(u'地址', max_length=80, null=True)
    email = models.EmailField(u' 邮箱', null=True)
    qq = models.CharField(max_length=11, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name