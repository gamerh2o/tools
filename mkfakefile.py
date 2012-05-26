#!/usr/bin/python
'''创建应急文件

@see: https://twitter.com/cxiaoji/status/174700088998899713
  RT @cxiaoji: 代表拖延重症患者介绍一下：一个随机二进制文件生成器是居家必备。你熟练地生成一个大小合理的文件，加上真实文件头，视情境重命名为 zip 或 pdf，在限期前两分钟上传。客户、助教或老师会反馈「文件打不开重发」，但这是几天以后的事情了。你知道，他们都有拖延症。

脚本原作者：@shellexy     链接：https://bitbucket.org/shellexy/my-bin-script/raw/tip/mkfakefile.py

转换为适合 python3 的版本，一些小改动
'''

VERSION = '0.0.1'

USAGE = '''
Usage: mkfakefile.py [arguments] FILENAME

Arguments:
    -h          display this help and exit
    -v          output version information and exit
    -f          fileformat, it will be zip or pdf, default is zip
    -s          filesize, optional suffixes k or m, default is 142k

Examples:
    mkfakefile.py  homework.zip
    mkfakefile.py  homework.pdf
    mkfakefile.py  -s 2m  homework.zip
    mkfakefile.py  -s 2m  -f pdf homework.pdf
'''

format = 'zip'
size = '140k'

import sys
import os
import getopt
import random
import subprocess

DD = 'dd if=/dev/urandom of={0} oflag=append conv=notrunc bs=512 count={0}'.split()

HEADS = {
    'zip' : 'PK\x03\x04\n\x00\x00\x00\x00\x00&y]@\xde\xbd\xac\x82\x00\x04\x00\x00\x00\x04\x00\x00\n\x00\x1c\x00',
    'pdf' : '%PDF-1.4\n%\xe1\xe9\xeb',
}

def gentail(size = 1024):
    return ''.join([ chr(random.randrange(256)) for i in range( random.randrange(size)) ])

def dd(file_name, kbytes):
    count = int(kbytes) * 2
    DD[2] = DD[2].format(file_name)
    DD[6] = DD[6].format(count)
    return subprocess.check_call(DD)

def size2kbytes(size):
    size = size.lower()
    if size.endswith('k'):
        return str(int(size[:-1]))
    elif size.endswith('m'):
        return str(int(size[:-1]) * 1024)
    else:
        try:
            return str(int(size))
        except:
            return 0
        pass
    pass

def mkfakefile(file_name, format = format, size = size):
    kbytes = size2kbytes(size)
    if not kbytes:
        return 1
    head = HEADS.get(format)
    if not head:
        return 1
    try:
        os.makedirs(os.path.dirname(file_name))
        pass
    except:
        pass
    open(file_name, 'wb').write(bytes(head, encoding='utf-8'))
    dd(file_name, kbytes)
    open(file_name, 'ab').write(bytes(gentail(), encoding='utf-8'))
    pass

def main():
    global format, size
    opts, args = getopt.getopt(sys.argv[1:], 'hvf:s:')
    if args:
        file_name = args[0]
        pass
    else:
        print(USAGE)
        return 1
    if file_name.lower().endswith('.zip'):
        format = 'zip'
        pass
    elif file_name.lower().endswith('.pdf'):
        format = 'pdf'
        pass
    for o, v in opts:
        if o == '-v':
            print(VERSION)
            return 1
        elif o == '-h':
            print(USAGE)
            return 1
        elif o == '-f':
            format = v
            pass
        elif o == '-s':
            size = v
            pass
        pass
    if mkfakefile(file_name, format, size):
        print(USAGE)
        return 1
    return 0
    

if __name__=="__main__":
    main()


