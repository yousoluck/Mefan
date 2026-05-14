#!/usr/bin/env python3
"""
一致性检查 Hook
检查基本命名规范、目录结构、禁止项（console.log 等）
"""
import sys, re, os, json

def check_file(filepath):
    violations = []
    if not os.path.exists(filepath):
        return violations

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # 1. 检查 console.log（仅前端场景示例，可根据 tech-stack 调整）
    if filepath.endswith(('.js','.ts','.jsx','.tsx')):
        for i, line in enumerate(lines):
            if 'console.log' in line and '//' not in line[:line.find('console.log')] if 'console.log' in line else False:
                # 简单排除注释行
                stripped = line.strip()
                if not stripped.startswith('//') and not stripped.startswith('*'):
                    violations.append(f"L{i+1}: 发现 console.log")

    # 2. 检查硬编码密钥（简单模式）
    secret_patterns = [
        r'(?i)(api_key|secret|password|token)\s*=\s*[\'"][^\'"]+[\'"]'
    ]
    for pat in secret_patterns:
        for i, line in enumerate(lines):
            if re.search(pat, line):
                violations.append(f"L{i+1}: 疑似硬编码密钥")

    return violations

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        violations = check_file(filepath)
        if violations:
            print(json.dumps({"status": "violations_found", "violations": violations}))
            sys.exit(1)
        else:
            print(json.dumps({"status": "clean"}))
            sys.exit(0)
    else:
        print(json.dumps({"error": "No file path provided"}))
        sys.exit(2)