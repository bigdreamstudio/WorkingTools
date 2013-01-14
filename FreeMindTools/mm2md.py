#!/usr/bin/env python
# encoding: utf-8

from xml.etree import ElementTree
import os
import conf4BlogListInGithub


class MMTransform():
    """freemind's file(.mm) transform tools"""

    def mm2md(self, mmFileContent):
        md = []
        mmtree = ElementTree.XML(mmFileContent)
        for node in mmtree.find('node').findall('node'):
            self._mm2SimpleMd(node, md)
        linesep = os.linesep
        return linesep.join(md)

    def mm2textile(self, mmFileContent):
        textile = []
        mmtree = ElementTree.XML(mmFileContent)
        for node in mmtree.find('node').findall('node'):
            self._mm2SimpleTextile(node, textile)
        linesep = os.linesep
        return linesep.join(textile)

    def _mm2SimpleMd(self, node, md, num=1):
        if node.get('TEXT'):
            branchcontent = []
            i = 0
            j = 0
            linesep = ''
            if num < 3:
                linesep = os.linesep
                if node.getchildren():
                    branchcontent.append(linesep)
                    branchcontent.append('#')
                    while i < num:
                        branchcontent.append('#')
                        i = i+1
                    branchcontent.append(' ')
            else:
                if node.getchildren():
                    while j < num-3:
                        branchcontent.append(' ')
                        j = j+1
                    branchcontent.append('- ')
            self._dumpstr(node,md,branchcontent,linesep)
            self._recursionMm2SimpleMd(node,md,num)


    def _dumpstr(self, node, md, branchcontent, linesep=''):
        branchcontent.append(node.attrib['TEXT'])
        branchcontent.append(linesep)
        md.append(''.join(branchcontent))

    def _recursionMm2SimpleTextile(self,node,md,num):
        for childbranch in node.getchildren():
            self._mm2SimpleTextile(childbranch, md, num + 1)

    def _recursionMm2SimpleMd(self,node,md,num):
        for childbranch in node.getchildren():
            self._mm2SimpleMd(childbranch, md, num + 1)

    def _mm2SimpleTextile(self, node, md, num=1):
        if node.get('TEXT'):
            branchcontent = []
            i = 0
            linesep = ''
            if num < 3:
                linesep = os.linesep
                if node.getchildren():
                    branchcontent.append(os.linesep)
                    branchcontent.append('h')
                    branchcontent.append(str(num))
                    branchcontent.append('. ')
            else:
                if node.getchildren():
                    while i < num-2:
                        branchcontent.append('*')
                        i = i+1
                    branchcontent.append(' ')
            self._dumpstr(node,md,branchcontent,linesep)
            self._recursionMm2SimpleTextile(node,md,num)


class MakeBlogInGithub():
    """make blog by markdown file in github.com"""
    def _getconf(self,mdFilename):
        mdfile = 'default'
        if  conf4BlogListInGithub.bloglist.has_key(mdFilename):
            mdfile = mdFilename
        return conf4BlogListInGithub.bloglist[mdfile]

    def md2blog(self, md, mdFilename):
        config = self._getconf(mdFilename)
        prefix = []
        prefix.append('---')
        prefix.append('layout : '+config['layout'])
        prefix.append('category : ' + config['category'])
        prefix.append('tags : [' + ', '.join(config['tags'].split(',')) + ']')
        prefix.append('title : ' + config['title'])
        prefix.append('---')
        prefix.append('[阅读思维导图]('+config['mmLink']+')')
        prefix.append(md)
        return os.linesep.join(prefix)

def main():
    mmdir = u'D:\Python26\FreeMindTools-master'
    # mddir = '/home/rain/download'
    mddir = u'C:\Documents and Settings\Administrator\桌面'
    mblog = MakeBlogInGithub()
    mmFilename = u'大量阅读的重要性.mm'
    textileFilename = 'textile.txt'
    mdFilename = mblog._getconf(mmFilename)['mdfname']

    mm = file(os.path.join(mmdir,mmFilename),'rb')
    md = file(os.path.join(mddir,mdFilename),'wb')
    textile = file(os.path.join(mddir,textileFilename),'wb')
    
    transform = MMTransform()
    md.write(mblog.md2blog(transform.mm2md(mm.read()).encode('utf8'), mmFilename))
    # textile.write(transform.mm2textile(mm.read()).encode('utf8'))
    mm.close()
    md.close()
    textile.close()

    

if __name__ == "__main__":
    main()