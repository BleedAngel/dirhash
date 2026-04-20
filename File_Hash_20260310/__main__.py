import os
import hashlib
import argparse
import input_validation as validate
import function as fn

def main():
    parser=argparse.ArgumentParser(description="Hash Save & Verify Tool")

    parser.add_argument(
        "-m","--mode",
        choices=["s","v","sv"],
        required=True,
        help="Execute_Mode: s=Save, v=Verify, sv=Save & Verify",
        dest="m"
    )

    parser.add_argument(
        "-a","--algorithm",
        choices=hashlib.algorithms_available,
        default="sha256",
        help="Algorithm (Default=sha256)",
        dest="a"
    )

    parser.add_argument(
        "-fm","--file-mode",
        choices=["w","a"],
        default="w",
        help="File_Mode: w=Write, a=Append (Default=w)",
        dest="fm"
    )

    parser.add_argument(
        "-s","--save-dir",
        help="Save_Dir Path",
        dest="s"
    )

    parser.add_argument(
        "-f","--hash-file",
        help="Hash_File Path",
        dest="f"
    )

    parser.add_argument(
        "-v","--verify-file",
        help="Verify_dir Path",
        dest="v"
    )

    args=parser.parse_args()

    #統計次數
    save_summary=0
    verify_summary=0

    #要求存取hash值
    if("s" in args.m):
        validate.directory(args.s)

        if(args.fm=="w"):
            hash_file=args.f

            if(validate.directory(hash_file)):
                save_dir_name=os.path.basename(args.s)
                hash_file=os.path.join(hash_file,f"hash_file({save_dir_name}).txt")
            
            else:
                validate.file(hash_file)
        
        if(args.fm=="a"):
            hash_file=args.f
            validate.file(hash_file)
        
        open(hash_file,args.fm).close()

        #逐一生成並存取hash值
        for root,dirs,files in os.walk(args.s):
            for filename in files:
                file_path=os.path.join(root,filename)
                hash_value=fn.calculate_hash(file_path,args.a)
                fn.save_hash(file_path,hash_value,hash_file)
                save_summary+=1

        print(f"✅ Hash file saved successfully!*{save_summary}")

    #要求對比hash值
    if("v" in args.m):
        verify_dir=args.v
        validate.directory(verify_dir)

        #讀取已有的hash值存取txt檔
        if("s" not in args.m):
            hash_file=args.f
            validate.file(hash_file)

        #逐一對比hash值
        for root,dirs,files in os.walk(verify_dir):
            for filename in files:
                file_path=os.path.join(root,filename)
                fn.verify_hash(file_path,hash_file,args.a)
                verify_summary+=1

        print(f"✅ File checked successfully!*{verify_summary}")

if(__name__=="__main__"):
    main()