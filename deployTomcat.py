#!/usr/bin/env python
# coding:utf-8
#批量部署tomcat

from fabric.api import *
from fabric.contrib.files import *

env.hosts = ['']
env.user = 'ubuntu'
env.password = ''
tarball = "tomcat-7.0.82-done.tar.gz"
tomcatName = "tomcat-7.0.82"
localPath = "/data/ops/test/"
tomcatPath = localPath + tarball
remotePath = "/data/ops/test/"
config = "/conf/server.xml"

#上传Tomcat 并解压
def upload():
    put(tomcatPath, remotePath)
    with cd(remotePath):
        run("tar xzvf %s" % tarball)


#重命名改端口
def rename():
    with cd(remotePath):
        suffix = prompt("输入名称")
        listSuffix = suffix.split(',')

        shutdownPort = 8005
        httpPort = 8080
        redirectPort = 8443
        lastPort = 8009

        for suf in listSuffix:
            shutdownPort = shutdownPort - 1
            httpPort = httpPort + 1
            redirectPort = redirectPort + 1
            lastPort = lastPort + 1

            tomcatfile = tomcatName + "-" + suf
            tomcatConfig = tomcatfile + config
            run("cp -r %s %s" % (tomcatName, tomcatfile))

            cmd1 = '''sed -i 's/Server port="8005"/Server port="%s"/g' %s''' % (shutdownPort, tomcatConfig)
            cmd2 = '''sed -i 's/Connector port="8080"/Server port="%s"/g' %s''' % (httpPort, tomcatConfig)
            cmd3 = '''sed -i 's/redirectPort="8443"/Server port="%s"/g' %s''' % (redirectPort, tomcatConfig)
            cmd4 = '''sed -i 's/Connector port="8009"/Server port="%s"/g' %s''' % (lastPort, tomcatConfig)

            run(cmd1)
            run(cmd2)
            run(cmd3)
            run(cmd4)