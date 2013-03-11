#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from xml.etree import ElementTree
import os
import sys
import yaml
from mm2md import MMTransform

def main(argv):
    confile = file('app.yaml','rb')
    config = yaml.load(confile)
    dirconf = 'file_dir'
    mddir = config[dirconf]['md']
    mmdir = config[dirconf]['mm']

    textileFilename = 'wiki.txt'
    mmFilename = '研发团队3-6月份团队目标.mm'
    mm = file(os.path.join(mmdir,mmFilename),'rb')
    textile = file(os.path.join(mddir,textileFilename),'wb')
    transform = MMTransform()
    textile.write(transform.mm2textile(mm.read()).encode('utf8'))
    textile.close()

if __name__ == "__main__":
    main(sys.argv)
    # main([])