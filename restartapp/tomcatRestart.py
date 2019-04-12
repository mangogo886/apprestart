#!/usr/bin/env python
#coding:utf-8

from fabric.api import *
from fabric.contrib.files import *   #导入文件判断模块
env.user='ubuntu'
hostsPath='/data/ops/restart/info_hosts'
appPath='/data/ops/restart/info_app'

host=file(hostsPath).readlines()
ip_list=[]
for ip in host:
    ip=ip.strip()
    ip_list.append(ip)

env.hosts=ip_list
env.password='qtqky@2018'



@parallel(pool_size=5)
def start():
    path=file(appPath,'r').readlines()
    for dir in path:
        dir = dir.strip()    #strip()去掉空行
        app_path='/data/%s'%dir
        if exists(app_path):         #判断远程目录或文件是否存在
            run('set -m;%s/bin/startup.sh'%app_path)
@parallel(pool_size=5)
def stop():
    path=file(appPath,'r').readlines()
    for dir in path:
        dir = dir.strip()
        app_path='/data/%s'%dir
        if exists(app_path):
            run('set -m;%s/bin/stop.sh'%app_path)

'''
rd01='172.16.1.22'            #设置特例主机
app19='172.16.1.42'
app18='172.16.1.41'
app17='172.16.1.40'
app21='172.16.1.44'
app02='172.16.1.25'


@hosts(rd01)       #使用装饰器hosts，对特例主机进行个别操作
def rd():
    run('set -m;/data/zookeeper-3.4.6/bin/zkServer.sh start')
    run('set -m;/data/tomcat-7.0.69-exhibitor-war-1.0/bin/startup.sh')
    with cd('/usr/local/bin'):
        sudo('set -m;nohup ./redis-server &')


@hosts(app19)
def oa():
    with cd("/data/qky-oa-backservice"):
        run("set -m;start.sh")

@hosts(app18)
def resource():
    with cd("/data/qky-resource-service/bin"):
        run("set -m;./start.sh")


@hosts(app17)
def kong():
    sudo("set -m;kong restart") 


@hosts(app21)
def mq():
    with cd("/data/rocketmq/bin"):
        run("set -m;nohup ./mqnamesrv &")
        run("set -m;nohup ./mqbroker -n 172.16.1.44:9876 &")

@hosts(app02)
def mqtt():
    with cd("/data/mqttServer/bin")
        run("set -m;nohup ./moquette.sh &") 

'''