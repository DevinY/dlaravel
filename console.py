#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from scripts import docker
arguments_list = sys.argv[1:]
number_of_arguments = len(arguments_list)

#參數
if(number_of_arguments > 0):
   parameter = arguments_list[0]
else:
  docker.execute(["exec","-u","dlaravel","php","bash"])

if(number_of_arguments == 1):
    if(parameter=="help"):
        docker.help()

    if(parameter=="node"):
        docker.node()

    if(parameter=="ps"):
        docker.ps()

    if(parameter=="up"):
        docker.up()

    if(parameter=="down"):
        docker.down()

    if(parameter=="pull"):
        docker.pull()

    if(parameter=="restart"):
        docker.restart()

    if(parameter=="info"):
        docker.info()

    if(parameter=="random"):
        docker.random()

    if(parameter=="normal"):
        docker.normal()

    if(parameter=="custom"):
        docker.normal()

    if(parameter=="mysql"):
        docker.mysql()

    if(parameter=="version"):
        docker.version()

    if(parameter=="alias"):
        docker.alias()

    if(parameter=="ext"):
        docker.ext()

    if(parameter=="reload"):
        docker.reload()

    if(parameter=="public"):
        docker.public()

    if(parameter=="secure"):
        docker.secure()

    if(parameter=="clear"):
        docker.clear()

    if(parameter=="logs"):
        docker.logs()

    if(parameter=="link"):
        docker.link()

    if(parameter=="chowner"):
        docker.chowner()

    if(parameter=="test"):
        docker.check_link()

if(number_of_arguments > 1):
    if(parameter=="exec"):
        docker.execute(arguments_list)

    if(parameter=="logs"):
        docker.logs(arguments_list[1:])
