[![progress-banner](https://backend.codecrafters.io/progress/shell/757761f3-9740-45f2-9ec0-5462935972f5)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

# 🐚 Build Your Own Shell — Completed

A fully functional POSIX-compliant shell built in Python as part of the [CodeCrafters "Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).

---

## ✅ Completed Stages

| Stage | Feature | Status |
|---|---|---|
| 1 | REPL (Read-Eval-Print Loop) | ✅ |
| 2 | `exit` builtin | ✅ |
| 3 | `echo` builtin | ✅ |
| 4 | `type` builtin — builtins | ✅ |
| 5 | `type` builtin — executables | ✅ |
| 6 | Run external programs via `PATH` | ✅ |
| 7 | `pwd` builtin | ✅ |
| 8 | `cd` builtin (absolute & relative paths) | ✅ |
| 9 | Single & double quote parsing | ✅ |
| 10 | Output redirection (`>`, `1>`, `>>`, `1>>`) | ✅ |
| 11 | Stderr redirection (`2>`, `2>>`) | ✅ |
| 12 | Tab completion — commands | ✅ |
| 13 | Tab completion — files & directories | ✅ |
| 14 | `history` builtin (`-r`, `-w`, `-a`, `HISTFILE`) | ✅ |
| 15 | Pipelines (`\|`) | ✅ |

---

## 🚀 Features

- **REPL loop** — persistent prompt that reads, evaluates, and prints results
- **Built-in commands** — `echo`, `exit`, `pwd`, `cd`, `type`, `history`
- **External command execution** — resolves executables from `PATH` and runs them via `subprocess`
- **Quote handling** — correctly parses single-quoted and double-quoted strings using `shlex`
- **I/O redirection** — supports `>`, `1>`, `>>`, `1>>`, `2>`, `2>>` for stdout and stderr
- **Pipelines** — chains multiple commands together with `|`, handling both builtins and external processes
- **Tab completion** — completes command names and file/directory paths; rings the bell on ambiguity and lists all matches on a double-tab
- **History** — tracks command history in-session and persists to/from a file via `HISTFILE`, with `-r`, `-w`, `-a` flags and `history N` support


