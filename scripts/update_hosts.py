#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
arguments_list = sys.argv[1:]
number_of_arguments = len(arguments_list)
if(number_of_arguments > 0):
   parameter = arguments_list[0]
try:
  with open("/etc/hosts","a") as f:
       f.write("\n127.0.0.1 {}.test".format(parameter))
except:
  print("sudo need")
