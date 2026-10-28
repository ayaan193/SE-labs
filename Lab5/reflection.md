# Lab 5: Static Code Analysis — Reflection

*The supplied lab handout references four reflection questions but does not include their wording. The following four questions and responses reflect the lab objectives; the headings can be adjusted if the instructor provides the official questions.*

## 1. What is static code analysis, and what is the role of each tool?

Static code analysis examines source code without running it. Pylint checks code quality, naming conventions, missing docstrings, suspicious programming patterns, and maintainability. Bandit identifies security risks such as unsafe `eval()`, weak hashes, and shell execution. Flake8 checks Python style and common coding errors, such as unused imports, bare exceptions, and missing final newlines. The three tools complement each other instead of performing identical checks.

## 2. What were the most significant issues found, and how were they fixed?

The initial Bandit scan found five issues: two High, one Medium, and two Low. The most serious findings were the use of MD5, execution of a shell command, and use of `eval()` to calculate overdue fines. I replaced MD5 with SHA-256 for identifier hashing, replaced `os.system()` with a normal print statement, and calculated fines through numeric multiplication. I also replaced `random.randint()` with `secrets.randbelow()` for PIN generation, removed the bare exception handler, and removed the hardcoded librarian token. Pylint and Flake8 also identified a mutable default list, missing docstrings, inconsistent naming, unnecessary variables, and file-handling issues; these were corrected as part of the cleanup.

## 3. How did fixing the reported issues improve the program?

The changes made the program safer, easier to maintain, and more predictable. Fine calculation no longer runs arbitrary Python expressions, and exporting the catalog no longer invokes a shell. Temporary PINs now come from a cryptographically secure generator, and the program does not print authentication secrets. Using clear function names, docstrings, and context-managed file operations improves readability and reliability. The original program also accepted an invalid book return and increased the available stock; tracking outstanding loans prevents this inventory error. The export now produces a structured CSV file instead of a string representation of a dictionary.

## 4. What did you learn about the benefits and limitations of static analysis?

I learned that a program can run without an error and still contain security problems, style violations, and logical mistakes. Pylint, Bandit, and Flake8 make these problems easier to spot early, and rerunning them after a fix provides useful evidence of improvement. However, automated tools do not catch every behavioral bug: none of the reported findings directly identified the incorrect increase in book stock after returning an unissued book. Static analysis should therefore be combined with manual code review, meaningful test cases, and checking actual program output.

## Verification and Results

I ran the corrected program successfully and reran all three tools on 28 October 2026. **Pylint improved from 5.32/10 to 10.00/10** (+4.68 points). **Bandit went from five findings to zero** (initially two High, one Medium, and two Low), and **Flake8 went from six violations to zero** (the final command displayed no output). This meets the lab's target of a Pylint score above 9.5 and shows that the reported security and style issues were resolved.

A perfect static analysis result does not guarantee correct behavior in every scenario, so running the library program and examining its output remains an important part of validation.
