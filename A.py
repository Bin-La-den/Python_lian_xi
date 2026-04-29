import sys
import platform
import os
import time
import cpuinfo
import getpass

#with open('output_Fedora.txt', 'w', encoding='utf-8') as f:
with open('output_Windows.txt', 'w', encoding='utf-8') as f:
    f.write("当前 Python 路径: " + sys.executable + "\n")
    f.write("操作系统信息: " + platform.platform() + "\n")
    f.write("当前工作目录的绝对路径: " + os.path.abspath(os.getcwd()) + "\n")
    f.write("系统信息: " + os.name + " " + platform.system() + " " + platform.release() + " " + platform.version() + "\n")
    f.write("架构信息: " + str(platform.architecture()) + "\n")
    f.write("机器类型: " + platform.machine() + "\n")
    f.write("计算机主机名: " + platform.node() + "\n")
    f.write("处理器信息: " + platform.processor() + "\n")
    f.write("Python 构建信息: " + str(platform.python_build()) + "\n")
    f.write("系统名称: " + str(platform.uname()) + "\n")
    f.write("当前时间: " + time.asctime() + "\n")
    f.write("文件系统编码格式：" + sys.getfilesystemencoding() + "\n")
    f.write("用户主目录：" + os.path.expanduser("~") + "\n")
    f.write("当前用户: " + getpass.getuser() + "\n")
    f.write("CPU 信息: " + cpuinfo.get_cpu_info()['brand_raw'] + "\n")
    f.write("架构信息: " + cpuinfo.get_cpu_info()['arch'] + "\n")