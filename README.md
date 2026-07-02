# dirhash

A command-line tool for saving and verifying file hash values to ensure file integrity.

## Features
- **Save Mode (s)**: Computes hashes for all files in a directory and stores them in a text file.
- **Verify Mode (v)**: Compares the current files against an existing hash file to detect modifications.
- **Save & Verify Mode (sv)**: Executes both operations in a single run.
- Supports multiple hash algorithms (default: sha256).

## Installation
1. Ensure Python 3.13.13 is installed.
2. Install the required dependency:
   ```bash
   pip install rich==15.0.0
   ```
3. Clone or download the project files.

## Usage
Run the main script, `__main__.py`:

### Save Hash Values
```bash
python '__main__.py' -m s -s 'save_directory_path' -f 'hash_file_path'
```

### Verify Hash Values
```bash
python '__main__.py' -m v -v 'verify_directory_path' -f 'hash_file_path'
```

### Save & Verify
```bash
python '__main__.py' -m sv -s 'save_directory_path' -v 'verify_directory_path' -f 'hash_file_path'
```

### Parameter Reference
- `-m, --mode`: Execution mode (`s`, `v`, or `sv`).
- `-a, --algorithm`: Hash algorithm (default: sha256).
- `-fm, --file-mode`: File mode (`w` for write, `a` for append, default: `w`).
- `-s, --save-dir`: Directory to scan and hash.
- `-v, --verify-file`: Directory to verify.
- `-f, --hash-file`: Path to the hash file.
- `-el, --error-log`: Optional path for the verification error log.

## Output Examples
- Save successful:
  ```text
Scanning (save): [ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ] 100.0%
Hash file saved:
  path: 'hash_file_path'
  files hashed* number_of_files
  ```
- Verification summary:
  ```text
Scanning (verify): [ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ] 100.0%
Error log saved: 'error_log_file'
Integrity check summary
  passed:        number_of_files
  failed:        0
  invalid lines: 0
  no record:     0
No issues detected.
  ```

## Notes
- Hash file format: `{"path": "relative_path", "hash": "hash_value"}`
- Supports all algorithms available in `hashlib`.
- Uses the Rich library for enhanced terminal output.

## License
This project is open source.

## Author Information
[YouTube](https://youtube.com/@BleedAngel_AMV)  
[TikTok](https://tiktok.com/@bleedangel_amv)  
[Instagram](https://instagram.com/bleedangel_amv)