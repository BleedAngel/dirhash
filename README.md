# File Hash Save & Verify Tool

一個用於保存和驗證文件哈希值的命令行工具，幫助檢查文件完整性。

## 功能
- **保存模式 (s)**: 計算目錄中所有文件的哈希值並保存到 TXT 文件。
- **驗證模式 (v)**: 比對現有哈希文件來檢查文件是否被修改。
- **保存與驗證模式 (sv)**: 同時執行保存和驗證。
- 支援多種哈希算法（默認 SHA256）。
- 支援寫入或追加模式。

## 安裝
1. 確保安裝 Python 3.12 ~ 3.14。
2. 安裝依賴：
   ```
   pip install rich
   ```
3. 下載專案文件。

## 用法
運行主程式 `__main__.py`：

### 保存哈希值
```
python '__main__.py' -m s -a sha256 -fm w -s '/path/to/directory' -f '/path/to/hash_file.txt'
```

### 驗證哈希值
```
python '__main__.py' -m v -a sha256 -f '/path/to/hash_file.txt' -v '/path/to/verify_directory'
```

### 保存與驗證
```
python '__main__.py' -m sv -a sha256 -fm w -s '/path/to/directory' -f '/path/to/hash_file.txt' -v '/path/to/verify_directory'
```

### 參數說明
- `-m, --mode`: 模式 (s/v/sv)
- `-a, --algorithm`: 哈希算法 (默認 sha256)
- `-fm, --file-mode`: 文件模式 (w=寫入, a=追加，默認 w)
- `-s, --save-dir`: 保存哈希的目錄路徑
- `-f, --hash-file`: 哈希文件路徑
- `-v, --verify-file`: 驗證的目錄路徑

## 輸出示例
- 保存成功:
```
 ✅ Hash file saved successfully!*5
    Hash_file path: '/path/to/hash_file.txt'
```
- 驗證摘要:
  ```
  ✅ Integrity check Summary:
  ✅ passed*3 | ⚠️ failed*1 | ❌ No record found*1
  ```

## 注意事項
- 哈希文件格式: `相對路徑,哈希值`
- 支援所有 hashlib 可用算法。
- 使用 Rich 庫美化輸出。

## 授權
此專案為開源，歡迎貢獻。
