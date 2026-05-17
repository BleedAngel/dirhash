import sys
import hashlib
import os
from rich.console import Console
console = Console()

#檢查檔案、資料夾路徑、演算法、檔案模式
def directory(path):
    if not os.path.isdir(path):
        console.print(f"[bold red]Error: '{path}' is not a valid directory")
        sys.exit(1)
    return True
def file(path):
    if not os.path.isfile(path):
        console.print(f"[bold red]Error: '{path}' is not a valid file")
        sys.exit(1)
    return True
def algorithm(algorithm):
    if algorithm not in hashlib.algorithms_available:
        console.print(f"[bold red]Error: '{algorithm}' is not supported.")
        sys.exit(1)
    return True
def response(response,options):
    if response not in options:
        console.print(f"[bold red]Error: '{response}' is not supported.")
        sys.exit(1)
    return True

#解決錯誤的error_log_file路徑
def resolve_error_log_path(output_path, verify_dir):
    if os.path.isdir(output_path):
        verify_name = os.path.basename(os.path.normpath(verify_dir))
        return os.path.join(output_path, f"error_log_file({verify_name}).txt")
    return output_path
