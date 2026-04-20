import sys
import hashlib
import os

#檢查檔案、資料夾路徑、演算法、檔案模式
def directory(path):
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a valid directory")
        sys.exit(1)
    return True
def file(path):
    if not os.path.isfile(path):
        print(f"Error: '{path}' is not a valid file")
        sys.exit(1)
    return True
def algorithm(algorithm):
    if algorithm not in hashlib.algorithms_available:
        print(f"Error: '{algorithm}' is not supported.")
        sys.exit(1)
    return True
def response(response,options):
    if response not in options:
        print(f"Error: '{response}' is not supported.")
        sys.exit(1)
    return True