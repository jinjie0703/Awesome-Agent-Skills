#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
git_diff_inspect.py - Git 变更与敏感信息静态扫描仪
读取当前本地 Git 仓库的未提交修改（staged / unstaged）或分支差量，
自动扫描高危 Secret 泄露、调试残留（console.log / print）并生成结构化差量简报。

用法:
  python git_diff_inspect.py              # 扫描当前未暂存和已暂存的所有修改
  python git_diff_inspect.py --staged     # 仅扫描已暂存 (git diff --cached) 的修改
  python git_diff_inspect.py --branch main# 扫描当前分支与 main 分支的差量
  python git_diff_inspect.py --output report.json # 导出 JSON 报告
"""

import sys
import re
import json
import shutil
import argparse
import subprocess
from pathlib import Path

# 确保 Windows 终端 UTF-8 编码正常输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# 高危敏感信息扫描正则模式库
SECRET_PATTERNS = [
    ("OpenAI / LLM API Key", re.compile(r'(?:sk-[a-zA-Z0-9]{20,T3BlbkFJ[a-zA-Z0-9]{20,}|sk-proj-[a-zA-Z0-9_-]{40,})')),
    ("AWS Access Key", re.compile(r'\b(AKIA[0-9A-Z]{16})\b')),
    ("Generic Private Key", re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),
    ("GitHub Personal Access Token", re.compile(r'\b(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}\b')),
    ("Slack Token / Webhook", re.compile(r'xox[baprs]-[0-9a-zA-Z]{10,48}|https://hooks\.slack\.com/services/T[0-9A-Z]{8}/B[0-9A-Z]{8}/[0-9a-zA-Z]{24}')),
    ("Hardcoded Password / Secret", re.compile(r'''(?i)(?:password|passwd|pwd|secret|api_key|apikey|auth_token)\s*[:=]\s*['"][^'"\s]{6,}['"]''')),
    ("Database Connection URI with Creds", re.compile(r'(?:postgres|mysql|mongodb|redis)://[^:\s]+:[^@\s]+@[^/\s]+')),
    ("Internal IPv4 Address", re.compile(r'\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b')),
]

# 调试残留扫描正则
DEBUG_PATTERNS = [
    ("Console Debug Residual", re.compile(r'\bconsole\.(?:log|debug|trace|dir)\s*\(')),
    ("Python Print Residual", re.compile(r'\bprint\s*\([^)]*?(?:test|debug|here|temp|xxx|111)[^)]*?\)', re.IGNORECASE)),
    ("Debugger / Breakpoint Statement", re.compile(r'\b(?:debugger;|breakpoint\(\)|import\s+pdb|pdb\.set_trace\(\))')),
    ("TODO / FIXME Tag", re.compile(r'\b(?:TODO|FIXME|XXX|HACK)\b[:\s]?(.*)', re.IGNORECASE)),
]


def backup_file(file_path: Path) -> str:
    """在修改前自动创建 .bak 备份副本"""
    if not file_path.exists():
        return ""
    bak_path = file_path.with_suffix(f".bak{file_path.suffix}")
    shutil.copy2(str(file_path), str(bak_path))
    return str(bak_path)


def run_git_cmd(cmd_list: list) -> str:
    """执行 git 命令并返回标准输出"""
    try:
        res = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            return ""
        return res.stdout
    except Exception:
        return ""


def get_git_diff(staged_only: bool = False, target_branch: str = None) -> str:
    """获取 git diff 文本"""
    if target_branch:
        return run_git_cmd(["git", "diff", f"{target_branch}...HEAD"])
    elif staged_only:
        return run_git_cmd(["git", "diff", "--cached"])
    else:
        # 同时包含已暂存和未暂存的修改
        unstaged = run_git_cmd(["git", "diff"])
        staged = run_git_cmd(["git", "diff", "--cached"])
        if unstaged and staged:
            return unstaged + "\n" + staged
        return unstaged or staged


def parse_diff(raw_diff: str) -> dict:
    """解析 git diff 文本并执行敏感信息与代码异味扫描"""
    files_changed = []
    current_file = None
    current_lines = []
    
    total_insertions = 0
    total_deletions = 0
    security_alerts = []
    debug_residuals = []

    for line in raw_diff.splitlines():
        if line.startswith("diff --git "):
            if current_file:
                files_changed.append({"file": current_file, "lines_count": len(current_lines)})
            # 提取文件名
            match = re.search(r'b/(.*)$', line)
            current_file = match.group(1) if match else "unknown"
            current_lines = []
        elif line.startswith("+++ ") or line.startswith("--- "):
            continue
        elif line.startswith("+"):
            total_insertions += 1
            added_text = line[1:]
            current_lines.append(added_text)

            # 扫描新增行是否包含敏感信息
            for name, pattern in SECRET_PATTERNS:
                if pattern.search(added_text):
                    # 脱敏显示
                    match_obj = pattern.search(added_text)
                    matched_str = match_obj.group(0)
                    masked = matched_str[:4] + "****" + matched_str[-4:] if len(matched_str) > 8 else "****"
                    security_alerts.append({
                        "file": current_file,
                        "type": name,
                        "snippet": added_text.strip()[:100],
                        "masked_match": masked
                    })

            # 扫描调试残留
            for name, pattern in DEBUG_PATTERNS:
                if pattern.search(added_text):
                    debug_residuals.append({
                        "file": current_file,
                        "type": name,
                        "snippet": added_text.strip()[:100]
                    })
        elif line.startswith("-"):
            total_deletions += 1

    if current_file:
        files_changed.append({"file": current_file, "lines_count": len(current_lines)})

    # 获取当前分支与状态
    branch_name = run_git_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip() or "unknown"
    status_summary = run_git_cmd(["git", "status", "--short"]).strip()

    return {
        "branch": branch_name,
        "total_files_changed": len(files_changed),
        "total_insertions": total_insertions,
        "total_deletions": total_deletions,
        "files": files_changed,
        "security_alerts": security_alerts,
        "debug_residuals": debug_residuals,
        "status_summary": status_summary.splitlines() if status_summary else []
    }


def generate_markdown_summary(data: dict) -> str:
    """生成易读的 Markdown 审查前置简报"""
    lines = []
    lines.append(f"# 🔍 Git 变更与安全审查简报")
    lines.append(f"- **当前分支**: `{data['branch']}`")
    lines.append(f"- **影响文件数**: {data['total_files_changed']}")
    lines.append(f"- **代码变动**: `+{data['total_insertions']}` 行 / `-{data['total_deletions']}` 行\n")

    if data["security_alerts"]:
        lines.append(f"## 🚨 高危安全隐患拦截 ({len(data['security_alerts'])} 处)")
        lines.append(f"> ⚠️ **检测到敏感凭据泄露风险，请在 Commit 提交前务必清理！**\n")
        for item in data["security_alerts"]:
            lines.append(f"- **文件**: `{item['file']}` | **类型**: `{item['type']}`")
            lines.append(f"  - 片段: `{item['snippet']}` (脱敏值: `{item['masked_match']}`)")
        lines.append("")
    else:
        lines.append(f"## 🛡️ 安全合规检测: ✅ 无高危 Secret 泄露风险\n")

    if data["debug_residuals"]:
        lines.append(f"## 🧹 调试代码与残留提醒 ({len(data['debug_residuals'])} 处)")
        for item in data["debug_residuals"][:15]:
            lines.append(f"- `{item['file']}` -> [{item['type']}]: `{item['snippet']}`")
        lines.append("")

    if data["files"]:
        lines.append(f"## 📂 变更文件列表")
        for f in data["files"]:
            lines.append(f"- `{f['file']}`")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Git 变更与敏感信息静态扫描仪")
    parser.add_argument("--staged", action="store_true", help="仅扫描已暂存 (git diff --cached) 的变更")
    parser.add_argument("--branch", help="比对当前分支与指定目标分支的差量 (如 --branch main)")
    parser.add_argument("--output", "-o", help="输出 JSON 格式审查报告到指定文件")
    parser.add_argument("--markdown", action="store_true", help="输出 Markdown 易读简报")
    args = parser.parse_args()

    raw_diff = get_git_diff(staged_only=args.staged, target_branch=args.branch)
    
    if not raw_diff.strip():
        # 如果没有 diff，检查是否是初始状态或无修改
        status = run_git_cmd(["git", "status", "--short"])
        if not status.strip():
            print("ℹ️ 当前 Git 工作区非常干净，没有检测到任何新增或修改的代码。")
            sys.exit(0)
        else:
            print("ℹ️ 检测到存在未跟踪的文件（Untracked Files），但暂无已修改的 diff。请先 git add 后重新扫描。")
            sys.exit(0)

    report = parse_diff(raw_diff)

    if args.output:
        out_path = Path(args.output)
        bak_msg = ""
        if out_path.exists():
            bak = backup_file(out_path)
            if bak:
                bak_msg = f"（原报告已备份至: {bak}）"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"JSON 报告已成功保存至: {out_path}{bak_msg}")

    if args.markdown:
        print(generate_markdown_summary(report))
    elif not args.output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
