import os
import hashlib
import argparse
import input_validation as validate
import function as fn
from rich.console import Console
console = Console()


def main():

    #CLI參數
    parser=argparse.ArgumentParser(description="Hash Save & Verify Tool")

    #執行模式
    parser.add_argument(
        "-m","--mode",
        choices=["s","v","sv"],
        required=True,
        help="Execute_Mode: s=Save, v=Verify, sv=Save & Verify",
        dest="m"
    )

    #雜湊算法
    parser.add_argument(
        "-a","--algorithm",
        choices=hashlib.algorithms_available,
        default="sha256",
        help="Algorithm (Default=sha256)",
        dest="a"
    )

    #文件模式
    parser.add_argument(
        "-fm","--file-mode",
        choices=["w","a"],
        default="w",
        help="File_Mode: w=Write, a=Append (Default=w)",
        dest="fm"
    )

    #需存取hash值的目錄
    parser.add_argument(
        "-s","--save-dir",
        help="Save_Dir Path",
        dest="s"
    )

    #存取hash值的txt檔路徑
    parser.add_argument(
        "-f","--hash-file",
        help="Hash_File Path",
        dest="f"
    )

    #需對比hash值的目錄
    parser.add_argument(
        "-v","--verify-file",
        help="Verify_dir Path",
        dest="v"
    )

    #錯誤日誌輸出路徑
    parser.add_argument(
        "-el","--error-log",
        help="Error log file path (optional)",
        dest="el"
    )

    args=parser.parse_args()

    #統計次數
    summary={
        "save":0,
        "passed":0,
        "fail":0,
        "norecord":0,
        "invalid":0
    }

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
                rel, err = fn.save_hash(file_path, hash_value, hash_file, args.s)
                if rel:
                    summary["save"]+=1
                else:
                    print(f"Failed to save hash for: {file_path} -> {err}")

        console.print("Hash file saved: \n"
                f"  path: [bold blue]'{hash_file}'[/] \n"
                f"  files hashed* {summary['save']}"
        )

    #要求對比hash值
    if("v" in args.m):
        validate.directory(args.v)

        #讀取已有的hash值存取txt檔
        if("s" not in args.m):
            hash_file=args.f
            validate.file(hash_file)

        # 載入hash文件
        hash_dict,invalid_lines=fn.load_hash_file(hash_file)
        summary["invalid"]+=len(invalid_lines)

        error_list=invalid_lines[:]

        #逐一對比hash值
        for root,dirs,files in os.walk(args.v):
            for filename in files:
                file_path=os.path.join(root,filename)
                summary,error_msg=fn.verify_hash(file_path,hash_dict,args.a,args.v,summary)
                if error_msg:
                    error_list.append(error_msg)

        # 輸出錯誤日誌
        if args.el:
            error_log_path = validate.resolve_error_log_path(args.el, args.v)
            with open(error_log_path, "w", encoding="utf-8") as f:
                f.write("Error Log\n"
                    "==========\n"
                    f"{fn.render_summary(summary)}\n\n")
                if error_list:
                    f.write("Issues:\n")
                    for error in error_list:
                        f.write(f"- {error}\n")
                else:
                    f.write("No issues detected.\n")
            console.print(f"Error log saved: [bold blue]'{error_log_path}'[/]")

        print(fn.render_summary(summary))
        if error_list and not args.el:
            print("Issues detected. Use --error-log <path> to save details.")
        elif not error_list:
            print("No issues detected.")

if(__name__=="__main__"):
    main()
