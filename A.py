import sys
import platform
import os
import time

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("当前 Python 路径: " + sys.executable + "\n")
    f.write("操作系统信息: " + platform.platform() + "\n")
    f.write(os.path.abspath(os.getcwd()) + "\n")
    f.write(os.name + " " + platform.system() + " " + platform.release() + " " + platform.version() + "\n")
    f.write(str(platform.architecture()) + "\n")
    f.write(platform.machine() + "\n")
    f.write(platform.node() + "\n")
    f.write(platform.processor() + "\n")
    f.write(str(platform.python_build()) + "\n")
    f.write(str(platform.uname()) + "\n")
    f.write(time.asctime() + "\n")
    f.write("文件系统编码格式：" + sys.getfilesystemencoding() + "\n")
    f.write("用户主目录：" + os.environ['HOMEPATH'] + "\n")
    f.write("当前用户：" + os.environ['USERNAME'] + "\n")