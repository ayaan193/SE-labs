# Lab 6 - Laundry Service Coverage

Individual submission for code (statement) coverage and branch coverage.
The supplied `laundry_service.py` is copied unchanged from
[SETAPESU26/L6_L7_41_laundry_service](https://github.com/SETAPESU26/L6_L7_41_laundry_service/tree/main/Lab%206).

## Code coverage

`test_code_coverage.py` checks invalid inputs, included weight, membership,
standard/express rates, large-order surcharges, order acceptance and drop-off outcomes.
It contains **20 collected tests** and achieves **100% statement coverage
(37/37 executable statements)** of `laundry_service.py`.

## Reproduce on Windows PowerShell

Run from this `LAB6` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_coverage.py code
```

The runner invokes pytest through Coverage.py, requires at least 90%, and saves the
JSON report and exact command/output transcript. Only `laundry_service.py` is the
coverage target; test and helper files are not counted as application statements.
Coverage data is kept separately in `.coverage.code`.

## Evidence

- [Code coverage terminal screenshot](screenshots/code_coverage.png)
- [Raw terminal transcript](reports/code_coverage_terminal.txt)
- [Machine-readable coverage report](reports/code_coverage.json)

The screenshot captures a local xterm.js terminal streaming a real invocation of
`run_coverage.py`. Its output is produced by the commands, not retyped or generated
as an illustration. The raw transcript and JSON report provide the underlying evidence.
