---
marp: true
theme: default
paginate: true
style: |
  h1 {
    border-bottom: 2px solid #4a90d9;
    padding-bottom: 6px;
    color: #1a1a2e;
  }
  blockquote {
    border-left: 4px solid #4a90d9;
    padding-left: 16px;
    color: #444;
    background: none;
  }
  table {
    font-size: 22px;
  }
  section.lead h1 {
    border-bottom: none;
    font-size: 48px;
    color: #1a1a2e;
  }
---

<!-- _class: lead -->

# Harness Engineering

> 整理我應用 coding agent 的有效作法

---

# Table of Contents

- Human intention
- Error prevention
- Context && Automation


--- 

# Human 

1. spec-driven development => superpowers
2. decision log
3. 要求 agent 畫 Mermaid graph 來寫文件。

---

# Mermaid 

```
## Diagrams

Use Mermaid for workflows and decision trees.

Use `mmdc` (mermaid-cli) to check every Mermaid diagram you write or edit before
committing: `mmdc -q -i doc.md -o <scratchpad>/out.md` 
```

---

# Error prevention

1. Mono repo (消除了 repo 同步類的錯誤)
2. TDD with integration harness (消除了 testing stub != real instance 的錯誤)
3. htmx (消除 frontend/backend state 同步類錯誤) (**design decision**)
4. prefer FP language (**design decision**)

---

# Context && Automation

1. gh/glab CLI => 讓 agent 可以直接開 issue、加 comment
2. o11y CLI => logs/traces queryable by agent
3. Other CLI ... 

---

# 結論

總是有很多可以改進 harness 的作法，建議積極思考以下三個方向：

- 意圖溝通
- 防錯
- 自動化 