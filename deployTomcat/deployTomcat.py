#!/usr/bin/env python
# coding:utf-8
#批量部署tomcat

import ConfigParser
from fabric.api import *
from fabric.contrib.files import *

env.hosts = raw_input('ip:')
env.user = 'root'
env.password = raw_input('密码:')
tarball = "tomcat-7.0.93.tar.gz"
tomcatName = "tomcat-7.0.93"
localPath = "/data/"
tomcatPath = localPath + tarball
remotePath = "/data/"
config = "/conf/server.xml"
configPath="config.ini"
cf=ConfigParser.ConfigParser()
cf.read(configPath)
opts=cf.get(env.hosts,'app')

#上传Tomcat 并解压
def upload():
    put(tomcatPath, remotePath)
    with cd(remotePath):
        run("tar xzvf %s" % tarball)


#重命名改端口
def rename():
    with cd(remotePath):
        #suffix = prompt("输入应用名称")
        listSuffix = opts.split(',')

        shutdownPort = 8005
        httpPort = 8080
        redirectPort = 8443
        lastPort = 8009

        for suf in listSuffix:

            tomcatfile = tomcatName + "-" + suf
            tomcatConfig = tomcatfile + config
            run("cp -r %s %s" % (tomcatName, tomcatfile))

            cmd1 = '''sed -i 's/Server port="8005"/Server port="%s"/g' %s''' % (shutdownPort, tomcatConfig)
            cmd2 = '''sed -i 's/Connector port="8080"/Connector port="%s"/g' %s''' % (httpPort, tomcatConfig)
            cmd3 = '''sed -i 's/redirectPort="8443"/redirectPort="%s"/g' %s''' % (redirectPort, tomcatConfig)
            cmd4 = '''sed -i 's/Connector port="8009"/Connector port="%s"/g' %s''' % (lastPort, tomcatConfig)
            shutdownPort = shutdownPort - 1
            httpPort = httpPort + 1
            redirectPort = redirectPort + 1
            lastPort = lastPort + 1

            run(cmd1)
            run(cmd2)
            run(cmd3)
            run(cmd4)