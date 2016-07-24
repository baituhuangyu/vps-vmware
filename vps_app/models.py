# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Usr(models.Model):
    user = models.OneToOneField(User, verbose_name='用户')
    user_name = models.CharField(max_length=30, verbose_name='用户名')
    email = models.CharField(max_length=30, verbose_name='邮箱')
    wei_chart = models.CharField(max_length=30, verbose_name='微信')
    qq = models.CharField(max_length=30, verbose_name='QQ')
    tel = models.CharField(max_length=30, verbose_name='固定电话')
    phone = models.CharField(max_length=30, verbose_name='手机')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #
    asset = models.FloatField(default=0, verbose_name='资产')


class Host(models.Model):
    host_name = models.CharField(max_length=30, verbose_name='host主机名')
    ip = models.CharField(max_length=30, verbose_name='host_ip')


class VmType(models.Model):
    """
    母本镜像
    """
    name = models.CharField(max_length=30, verbose_name='名字')
    vm_id = models.CharField(max_length=30, verbose_name='镜像ID')
    path_name = models.CharField(max_length=128, verbose_name='镜像路径')
    desc = models.CharField(max_length=128, verbose_name='镜像简介')
    os_name = models.CharField(max_length=128, verbose_name='操作系统')

    host_name = models.CharField(max_length=30, verbose_name='host主机名')
    ip = models.CharField(max_length=30, verbose_name='host_ip')


class Vm(models.Model):
    name = models.CharField(max_length=30, verbose_name='名字')
    vm_id = models.CharField(max_length=128, verbose_name='主机 ID')
    type_name = models.CharField(max_length=30, verbose_name='资源名称')
    os_name = models.CharField(max_length=30, verbose_name='系统模板')
    path_name = models.CharField(max_length=128, verbose_name='vps路径')

    net_type = models.CharField(max_length=30, verbose_name='网络类型')
    lan_ip = models.CharField(max_length=30, verbose_name='内网IP')
    # 外网IP为固定IP或者动态IP,固定IP写出IP值
    eth_ip = models.CharField(max_length=30, verbose_name='外网IP')
    gate_way = models.CharField(max_length=30, verbose_name='网关')
    network_mask = models.CharField(max_length=30, verbose_name='掩码')

    # 时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 充值后重新计算修改
    stop_at = models.DateTimeField(auto_now_add=True)

    # adsl
    adsl_pwd = models.CharField(max_length=30, verbose_name='adsl密码')
    adsl = models.CharField(max_length=30, verbose_name='adsl用户名')

    #
    login_name = models.CharField(max_length=30, verbose_name='登陆账户名')
    login_password = models.CharField(max_length=30, verbose_name='登陆账户密码')


