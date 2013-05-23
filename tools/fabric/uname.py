#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from fabric.api import run

def uname():
    run('uname -a')
