#!/usr/bin/env python3
"""
Diff Size 检查 Hook
检查单次变更行数是否异常，超阈值(200行)警告，需人工确认
"""
import sys, json

def check_diff_size(filepath):
    """检查文件变更大小"""
    violations = []

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        line_count = len(lines)
    except Exception as e:
        return [{"error": str(e)}]

    # 阈值: 200行
    THRESHOLD = 200

    if line_count > THRESHOLD:
        violations.append(f"文件 {filepath} 超过 {THRESHOLD} 行限制，当前 {line_count} 行")
        return [{
            "status": "size_warning",
            "file": filepath,
            "lines": line_count,
            "threshold": THRESHOLD,
            "message": f"文件超过单次变更阈值 {THRESHOLD} 行，需人工确认"
        }]

    return [{
        "status": "clean",
        "file": filepath,
        "lines": line_count
    }]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        result = check_diff_size(filepath)
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    else:
        print(json.dumps([{"error": "No file path provided"}]))
        sys.exit(2)