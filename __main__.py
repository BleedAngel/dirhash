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

    #執行模式(-m/--mode)
    parser.add_argument(
        "-m","--mode",
        choices=["s","v","sv"],
        required=True,
        help="Execute_Mode: s=Save, v=Verify, sv=Save & Verify",
        dest="m"
    )

    #雜湊算法(-a/--algorithm)
    parser.add_argument(
        "-a","--algorithm",
        choices=hashlib.algorithms_available,
        default="sha256",
        help="Algorithm (Default=sha256)",
        dest="a"
    )

    #文件模式(-fm/--file-mode)
    parser.add_argument(
        "-fm","--file-mode",
        choices=["w","a"],
        default="w",
        help="File_Mode: w=Write, a=Append (Default=w)",
        dest="fm"
    )

    #需存取hash值的目錄(-s/--save-dir)
    parser.add_argument(
        "-s","--save-dir",
        help="Save_Dir Path",
        dest="s"
    )

    #存取hash值的txt檔路徑(-f/--hash-file)
    parser.add_argument(
        "-f","--hash-file",
        help="Hash_File Path",
        dest="f"
    )

    #需對比hash值的目錄(-v/--verify-file)
    parser.add_argument(
        "-v","--verify-file",
        help="Verify_dir Path",
        dest="v"
    )

    #錯誤日誌輸出路徑(-el/--error-log)
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

        # 逐一生成並存取hash值
        # 預先計算總檔案大小以建立進度條（以總檔案樹的10%為單位）
        total_size = 0
        for _root, _dirs, files in os.walk(args.s):
            for file in files:
                file_path = os.path.join(_root, file)
                total_size += os.path.getsize(file_path)
        if total_size == 0:
            total_size = 1

        processed_size = 0
        for root,dirs,files in os.walk(args.s):
            for filename in files:
                file_path=os.path.join(root,filename)
                hash_value=fn.calculate_hash(file_path,args.a)
                rel, err = fn.save_hash(file_path, hash_value, hash_file, args.s)
                if rel:
                    summary["save"]+=1
                else:
                    print(f"Failed to save hash for: {file_path} -> {err}")

                # 更新進度條（10 個單位，每單位代表總檔案大小的10%）
                processed_size += os.path.getsize(file_path)
                units = int((processed_size * 10) / total_size)
                if units > 10:
                    units = 10
                # 使用白色方塊表示已完成的單位，未完成用空格占位，並保持單行輸出
                bar = "".join([" ██" for _ in range(units)]) + "".join([" " for _ in range(10 - units+1)])
                percent = (processed_size / total_size) * 100
                console.print(f"Scanning (save): [{bar}] {percent:5.1f}%", end='\r')
        # 掃描完成後換行以結束行內顯示
        console.print("")

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

        # 逐一對比hash值
        # 預先計算總檔案大小以建立進度條（以總檔案樹的10%為單位）
        total_size = 0
        for _root, _dirs, files in os.walk(args.v):
            for file in files:
                file_path = os.path.join(_root, file)
                total_size += os.path.getsize(file_path)
        if total_size == 0:
            total_size = 1

        processed_size = 0
        for root,dirs,files in os.walk(args.v):
            for filename in files:
                file_path=os.path.join(root,filename)
                summary,error_msg=fn.verify_hash(file_path,hash_dict,args.a,args.v,summary)
                if error_msg:
                    error_list.append(error_msg)

                # 更新進度條（10 個單位，每單位代表總檔案大小的10%）
                processed_size += os.path.getsize(file_path)
                units = int((processed_size * 10) / total_size)
                if units > 10:
                    units = 10
                bar = "".join([" ██" for _ in range(units)]) + "".join([" " for _ in range(10 - units+1)])
                percent = (processed_size / total_size) * 100
                console.print(f"Scanning (verify): [{bar}] {percent:5.1f}%", end='\r')
        # 掃描完成後換行以結束行內顯示
        console.print("")

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
