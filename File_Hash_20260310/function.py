import os
import hashlib
import input_validation as validate

#計算hash值
def calculate_hash(file_path,algorithm):
    hash_func=hashlib.new(algorithm)
    with open(file_path,"rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()

#存取hash值至txt檔
def save_hash(file_path,hash_value,hash_file,base_dir):
    relative_path=os.path.relpath(file_path,base_dir).replace(os.sep, "/")
    print(f"✅ Saved hash for: '{relative_path}'")
    with open(hash_file,"a") as f:
        f.write(f"{relative_path},{hash_value}\n")

#對比hash值
def verify_hash(file_path,hash_file,algorithm,base_dir,summary):
    validate.file(hash_file)
    
    current_hash=calculate_hash(file_path,algorithm)
    relative_path=os.path.relpath(file_path, base_dir).replace(os.sep, "/")
    with open(hash_file,"r") as f:
        for line in f:
            stored_file,stored_hash=line.strip().split(",")
            stored_file=stored_file.replace("\\", "/")
            if(stored_file==relative_path):
                if(stored_hash==current_hash):
                    print(f"✅ Integrity check passed: '{relative_path}'")
                    summary["passed"]+=1
                    return summary
                else:
                    print(f"⚠️ Integrity check failed: '{relative_path}'")
                    summary["fail"]+=1
                    return summary
                
    print(f"❌ No record found for: {relative_path}")
    summary["norecord"]+=1
    return summary
