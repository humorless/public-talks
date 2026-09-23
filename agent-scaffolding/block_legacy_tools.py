#!/usr/bin/env python3
"""PreToolUse:Bash hook — 擋下 legacy 工具 (grep/sed/find)，改用 rg/sd/fd/jq。

只檢查「指令位置」上的字，因此：
  - 引號內的字串、heredoc 內容不會誤判 (echo "find it"、rg 'sed')
  - git grep、--find-renames 不會誤判
  - egrep/fgrep、/usr/bin/grep、\\grep、xargs grep、$(grep ...)、bash -c '...' 會被抓到
"""
import sys
import json
import os
import re
import shutil

GREP = {"grep", "egrep", "fgrep", "ggrep"}
SED = {"sed", "gsed"}
FIND = {"find", "gfind"}

MSG = {
    "grep": "Please use `rg` (ripgrep) instead of `grep`. (rg -uu to include ignored files)",
    "sed": ('Please use `sd` instead of `sed`. Syntax: sd "find" "replace" file. '
            "For line ranges or deleting lines (sed -n '10,20p', sed '/x/d'), "
            "use the Read tool or `rg -n` to locate lines, then the Edit tool — not awk/perl."),
    "find": "Please use `fd` instead of `find`. Syntax: fd <pattern> <path>",
    "json": "Please use `jq` to parse/manipulate JSON instead of text tools.",
}
# 每條規則對應的新工具；新工具沒裝時不擋（放行 legacy 工具，由 Claude 回報缺少的工具）
REPLACEMENT = {"grep": "rg", "sed": "sd", "find": "fd", "json": "jq"}


def blocked(kind):
    return MSG[kind] if shutil.which(REPLACEMENT[kind]) else None

# 這些是「前綴」，後面接的才是真正的指令
WRAPPERS = {"sudo", "command", "builtin", "exec", "env", "nohup", "time", "nice",
            "xargs", "timeout", "!", "{", "then", "do", "else", "elif", "if",
            "while", "until"}
# 帶參數的 flag（要連同下一個 token 一起跳過）
FLAGS_WITH_ARG = {"-I", "-n", "-P", "-L", "-d", "-E", "-s", "-u"}
# fd -x / -X 後面接的是一個新指令
FD_EXEC = {"-x", "--exec", "-X", "--exec-batch"}


def strip_heredoc_bodies(cmd):
    """移除 heredoc 內文（保留 <<EOF 那一行）。"""
    lines = cmd.split("\n")
    out, delim = [], None
    for line in lines:
        if delim is not None:
            if line.strip() == delim:
                delim = None
            continue
        out.append(line)
        m = re.search(r"<<-?\s*(['\"]?)(\w+)\1", line)
        if m:
            delim = m.group(2)
    return "\n".join(out)


def strip_literals(s):
    """把引號內的字面文字換成 `_`，但保留雙引號中的 $(...) 與 `...`（那是會執行的程式碼）。"""
    out = []
    stack = [["N", 0]]  # N=一般, DQ=雙引號內, S=$( ) 內, B=反引號內
    i, n = 0, len(s)
    while i < n:
        mode = stack[-1]
        ch = s[i]
        if mode[0] == "DQ":
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                stack.pop()
                out.append(" _ ")
            elif s.startswith("$(", i):
                stack.append(["S", 0])
                out.append(" ; ")
                i += 2
                continue
            elif ch == "`":
                stack.append(["B", 0])
                out.append(" ; ")
            i += 1
            continue
        # N / S / B：一般程式碼
        if ch == "\\":
            if i + 1 < n:
                out.append(s[i + 1])
            i += 2
            continue
        if ch == "'":
            j = s.find("'", i + 1)
            i = n if j == -1 else j + 1
            out.append(" _ ")
            continue
        if ch == '"':
            stack.append(["DQ", 0])
            out.append(" ")
        elif mode[0] == "S" and ch == "(":
            mode[1] += 1
            out.append(ch)
        elif mode[0] == "S" and ch == ")":
            if mode[1] == 0:
                stack.pop()
                out.append(" ; ")
            else:
                mode[1] -= 1
                out.append(ch)
        elif mode[0] == "B" and ch == "`":
            stack.pop()
            out.append(" ; ")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def command_starts(tokens):
    """回傳每個「實際被執行的指令」在 tokens 中的 index。"""
    starts = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if re.match(r"^\w+=", t):  # FOO=bar 環境變數
            i += 1
            continue
        if t in WRAPPERS:
            i += 1
            while i < len(tokens) and tokens[i].startswith("-"):
                i += 2 if tokens[i] in FLAGS_WITH_ARG else 1
            if t == "timeout" and i < len(tokens) and re.match(r"^[\d.]+[smhd]?$", tokens[i]):
                i += 1
            continue
        starts.append(i)
        break
    # fd ... -x grep ...
    if starts and os.path.basename(tokens[starts[0]]) == "fd":
        for k, tok in enumerate(tokens):
            if tok in FD_EXEC and k + 1 < len(tokens):
                starts.append(k + 1)
    return starts


def check_segment(tokens):
    for idx in command_starts(tokens):
        name = os.path.basename(tokens[idx])
        args = tokens[idx + 1:]
        kind = None
        if name in GREP:
            kind = "grep"
        elif name in SED:
            kind = "sed"
        elif name in FIND:
            kind = "find"
        elif any(a.endswith(".json") for a in args):
            if name in {"sd", "awk", "gawk", "cut"}:
                kind = "json"
            elif name == "rg" and any(a in {"-o", "--only-matching", "-r", "--replace"}
                                      or re.match(r"^-\w*o", a) for a in args):
                kind = "json"
        msg = kind and blocked(kind)
        if msg:
            return msg
    return None


def check(command):
    # bash -c '...' / sh -c "..."：遞迴檢查內層字串
    for m in re.finditer(r"\b(?:ba|z)?sh\s+-c\s+(['\"])(.*?)(?<!\\)\1", command, re.S):
        msg = check(m.group(2))
        if msg:
            return msg
    code = strip_literals(strip_heredoc_bodies(command))
    for seg in re.split(r"\|\||&&|[|;&\n()`]", code):
        tokens = seg.split()
        if tokens:
            msg = check_segment(tokens)
            if msg:
                return msg
    return None


def main():
    # Claude Code 會透過 stdin 傳入包含 tool_input 的 JSON
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    msg = check(command)
    if msg:
        # Exit code 2 會直接擋下工具呼叫，並將 stderr 餵給 Claude 當作修正依據
        print(f"[Policy Violation] {msg} Your command was blocked: {command}", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
