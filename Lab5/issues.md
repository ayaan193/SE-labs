# Lab 5: Static Code Analysis — Issues and Fixes

**Program:** `library_catalog_system.py`  
**Original Pylint score:** **5.32/10**  
**Original Bandit findings:** **5** (2 High, 1 Medium, 2 Low)  
**Original Flake8 findings:** **6**

The line numbers below refer to the **original supplied program**, before any fixes. Security findings are ordered by the severities reported in Bandit; additional findings are from Pylint, Flake8, and manual inspection.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak MD5 hashing (`B324`) | Security — **High** (Bandit) | 47 | MD5 is collision-prone and unsuitable for security-related hashing. | Replace `hashlib.md5` with `hashlib.sha256` for the patron identifier digest. This is **not** a password-storage algorithm. |
| Shell execution (`B605`) | Security — **High** (Bandit) | 58 | `os.system()` passes a message containing a filename to the shell. A user-controlled filename can lead to command injection. | Remove shell execution; use `print()` for the completion message. |
| Use of `eval()` (`B307`) | Security — **Medium** (Bandit) | 40–43 | Fine calculation executes a Python expression, potentially running attacker-controlled code. | Replace expression evaluation with numeric `days_overdue * daily_rate` and validate nonnegative inputs. |
| Predictable PIN (`B311`) | Security — **Low** (Bandit) | 50–51 | `random.randint()` is not suitable for generating security-sensitive PINs. | Use `secrets.randbelow(9000) + 1000` to produce four-digit PINs. Avoid logging the result. |
| Bare exception / ignored error (`B110`, `E722`, `W0702`) | Reliability / Security — **Low** (Bandit) | 23–27 | `except: pass` silently ignores any exception raised during a return. | Check the book and outstanding loan count explicitly; return `False` for invalid returns. |
| Hardcoded librarian credential | Security — Manual review | 62, 70 | A credential-like access token is stored directly in source and printed during execution. | Remove the embedded credential and the line that prints it. Real credentials should be kept out of source code. |
| Return without matching loan | Logic error — Manual review | 23–25, 64 | `return_book("B02")` increases stock although B02 was never issued. | Track outstanding loans, reject unmatched returns, and demonstrate a valid B01 return. |
| Mutable default list (`W0102`) | Bug / Pylint | 15 | `active_issues=[]` is shared among calls to the function. | Set the default to `None` and update only a list explicitly provided by the caller. |
| Non-standard function name (`C0103`) | Style / Pylint | 15 | `issueBook` uses camelCase rather than Python's conventional snake_case. | Rename it to `issue_book` and update calls. |
| Missing function docstrings (`C0116`) | Maintainability / Pylint | 15, 23, 30, 40, 46, 50, 54, 61 | Functions have no description of their purpose. | Add concise docstrings to all functions. |
| Old-style string formatting (`C0209`) | Style / Pylint | 19 | Uses `%` formatting where an f-string is clearer. | Use an f-string for the audit-log entry. |
| Comparison with `None` (`E711`, `C0121`) | Style / Flake8 and Pylint | 32 | `== None` violates common Python style conventions. | Simplify availability to a boolean result from a safe catalog lookup. |
| Unused variables (`F841`, `W0612`) | Quality / Flake8 and Pylint | 31, 41 | `late_fee` and `days` are assigned unnecessarily. | Remove unused variables; the fine computation now directly uses its inputs. |
| Misleading CSV import (`F401`, `W0611`) | Quality / Flake8 and Pylint | 6, 54–57 | `csv` is imported but the old export merely writes `str(catalog)` to a text file. | Use `csv.writer()` for a real UTF-8 catalog export. |
| File not context-managed (`W1514`, `R1732`) | Reliability / Pylint | 55–57 | File opening omits an encoding and relies on a manual `close()`. | Use `with open(..., encoding="utf-8", newline="")` for safe cleanup and proper CSV output. |
| Missing final newline (`C0304`, `W292`) | Style / Pylint and Flake8 | 73 | The source lacks a newline at the end of the file. | Add a final newline. |
| Overcomplicated availability condition (`R1703`, `R1705`) | Quality / Pylint | 34–37 | Returns `True` or `False` through redundant `if`/`else` branches. | Return the boolean comparison directly. |

## Verified Results (28 October 2026)

After fixing the issues, I ran the corrected Python program and repeated all three analysis tools on Windows with Python 3.12.10. The program successfully handled an invalid return, a valid return, availability checks, fine calculation, patron identifier hashing, temporary PIN generation, audit logging, and CSV export.

| Check | Before fixes | After fixes | Result |
|---|---|---|---|
| Pylint | **5.32/10** | **10.00/10** | Pass: exceeds 9.5/10 target |
| Bandit | **5** issues (2 High, 1 Medium, 2 Low) | **0** issues | Pass: no reported security findings |
| Flake8 | **6** violations | **0** violations (no output) | Pass: no reported style violations |

The **Pylint score improved by 4.68 points**. Bandit reported `No issues identified`, and Flake8 produced no output. These results are from the final checks run against `library_catalog_system.py`, not from the earlier saved `*_report.txt` files, which still represent the baseline.

Verification commands:

```cmd
python library_catalog_system.py
pylint library_catalog_system.py
bandit -r library_catalog_system.py
flake8 library_catalog_system.py
```

The cleaned program fixes more than the required four issues without losing its core library catalog functionality. Static analysis does not prove the absence of every defect, so the invalid-return behavior was also checked by running the program.
