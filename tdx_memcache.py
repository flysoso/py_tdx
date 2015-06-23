#coding: utf8

# 避免读取多余内容，提升速度
# 建立此reader, 读取指定文件部分
# 在使用RAM虚拟磁盘时效果不明显

import os

fpath = "C:\\new_tdx\\vipdoc\\sh\\lday"

sz = os.path.getsize(fpath + '\\sh000001.day')

print sz, sz / 32.0

raw_input()