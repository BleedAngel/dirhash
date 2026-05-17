import os
import hashlib
from rich.console import Console
console = Console()

#計算hash值
def calculate_hash(file_path,algorithm):
    hash_func=hashlib.new(algorithm)
    with open(file_path,"rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()

#存取hash值至txt檔
def save_hash(file_path,hash_value,hash_file,base_dir):
    relative_path = os.path.relpath(file_path, base_dir).replace(os.sep, "/")
    try:
        with open(hash_file, "a", encoding="utf-8") as f:
            f.write(f"{relative_path},{hash_value}\n")
    except OSError as e:
        console.print(f"[red]Error writing to hash file: {e}[/]")
        return None, str(e)
    return relative_path, None

#對比hash值
def verify_hash(file_path, hash_dict, algorithm, base_dir, summary):
    
    current_hash=calculate_hash(file_path,algorithm)
    relative_path=os.path.relpath(file_path, base_dir).replace(os.sep, "/")
    
    if relative_path in hash_dict:
        stored_hash=hash_dict[relative_path]
        if(stored_hash==current_hash):
            summary["passed"]+=1
            return summary,None
        else:
            error_msg=f"Integrity check failed: '{relative_path}'"
            summary["fail"]+=1
            return summary,error_msg
    else:
        error_msg=f"No record found for: '{relative_path}'"
        summary["norecord"]+=1
        return summary,error_msg

#載入hash文件
def load_hash_file(hash_file):
    hash_dict={}
    invalid_lines=[]
    with open(hash_file,"r") as f:
        for line in f:
            try:
                stored_file,stored_hash=line.strip().split(",")
                stored_file=stored_file.replace("\\", "/")
                hash_dict[stored_file]=stored_hash
            except ValueError:
                error_msg=f"Invalid line in hash file: '{line.strip()}'"
                invalid_lines.append(error_msg)
                continue
    return hash_dict,invalid_lines

#輸出統計摘要
def render_summary(summary):
    return (
        "Integrity check summary\n"
        f"  passed:        {summary['passed']}\n"
        f"  failed:        {summary['fail']}\n"
        f"  invalid lines: {summary['invalid']}\n"
        f"  no record:     {summary['norecord']}"
    )
