#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from scripts import docker
arguments_list = sys.argv[1:]
number_of_arguments = len(arguments_list)

#參數
if(number_of_arguments > 0):
   parameter = arguments_list[0]

if(number_of_arguments == 1):

    if(parameter=="--help"):
        print("usage: {} [<option>] [Project name]".format(sys.argv[0]))
        print("Example")
        print("{} [project name]: Create a new laravel proejct into sites folder.".format(sys.argv[0]))
        print("options:")
        help="""  --help : help
  --host [project name]: Adding [project name].test to /etc/hosts, But don't want to install laravel framework.
  --db [project name]: Create a database name and user name that is the same as project name."""
        print(help)
    else:
       project=parameter
       docker.dlaravel_new(project)
       docker.dlaravel_config(project)
       docker.create_db(project)

if(number_of_arguments == 2):

    if(re.search("^--\\w+", arguments_list[0], re.I | re.M)):
        option=arguments_list[0]
        project=arguments_list[1]
    else:
        option=arguments_list[1]
        project=arguments_list[0]

    if(option=="--db"):
        docker.create_db(project)

    if(option=="--host"):
        docker.create_host(project)
