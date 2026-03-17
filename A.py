import sys
import platform
import os

print("当前 Python 路径:", sys.executable)
print("操作系统信息:", platform.platform())
print(os.path.abspath(os.getcwd()))