# Lab 6 - Laundry Service Coverage

Individual submission for code (statement) coverage and branch coverage.
The supplied `laundry_service.py` is copied unchanged from
[SETAPESU26/L6_L7_41_laundry_service](https://github.com/SETAPESU26/L6_L7_41_laundry_service/tree/main/Lab%206).

## Code coverage

`test_code_coverage.py` checks invalid inputs, included weight, membership,
standard/express rates, large-order surcharges, order acceptance and drop-off outcomes.
It contains **20 collected tests** and achieves **100% statement coverage
(37/37 executable statements)** of `laundry_service.py`.

## Branch coverage

`test_branch_coverage.py` is an independent suite with **71 collected tests**.
It achieves **100% branch coverage (26/26 branch outcomes)** and **100% statement
coverage (37/37 statements)**. It covers both sides of every measured decision,
including membership/bedding combinations, validation failures, the exact
ten-extra-kilogram surcharge boundary, item/weight limits and all four drop-off
cutoff combinations at the accepted/late/rejected boundaries.

| Suite | Tests passed | Statements | Branch outcomes |
| --- | ---: | ---: | ---: |
| Code coverage | 20 | 37/37 = **100%** | Not measured in this run |
| Branch coverage | 71 | 37/37 = **100%** | 26/26 = **100%** |

The tests preserve the supplied behavior. In particular, delicate orders are
accepted by item count alone, bedding gets no membership weight bonus, and an
order with exactly ten extra kilograms does not receive the large-order surcharge.
Assertions check returned charges, acceptance decisions, statuses and exception
messages; they do not merely call the functions to inflate coverage.

## Reproduce on Windows PowerShell

Run from this `LAB6` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_coverage.py code
.\.venv\Scripts\python.exe run_coverage.py branch
```

The runner invokes pytest through Coverage.py, requires at least 90%, and saves the
JSON report and exact command/output transcript. Only `laundry_service.py` is the
coverage target; test and helper files are not counted as application statements.
Coverage data is kept separately in `.coverage.code` and `.coverage.branch`, so
the suites do not borrow execution evidence from each other.

The branch run uses `coverage run --branch`. Coverage.py's ordinary `Cover` column
combines statements and branches; the runner also computes the **branch-only**
percentage from the JSON `covered_branches` and `num_branches` values and requires
that percentage independently to meet 90%.

Run both test files together without replacing the separate reports:

```powershell
.\.venv\Scripts\python.exe -m pytest test_code_coverage.py test_branch_coverage.py -q
```

## Evidence

- [PDF report: full test listings, terminal screenshots and coverage results](reports/LAB6_Coverage_Report.pdf)
- [Code coverage terminal screenshot](screenshots/code_coverage.png)
- [Raw terminal transcript](reports/code_coverage_terminal.txt)
- [Machine-readable coverage report](reports/code_coverage.json)
- [Branch coverage terminal screenshot](screenshots/branch_coverage.png)
- [Branch terminal transcript](reports/branch_coverage_terminal.txt)
- [Machine-readable branch report](reports/branch_coverage.json)
- [Code report screenshot from the latest run](reports/code_coverage_screenshot.png)
- [Branch report screenshot from the latest run](reports/branch_coverage_screenshot.png)

The screenshots are direct Windows terminal captures of the code and branch
coverage runs using `run_coverage.py`. Each shows the final coverage percentages.
The matching raw transcripts and JSON reports provide the underlying evidence.

## Separate commits

The code coverage test file, its report and screenshot are added in one commit.
The branch coverage test file, its report and screenshot are added in a second
commit. All submission files are contained in `LAB6`; the virtual environment,
coverage databases and temporary screenshot tooling are ignored.

References: [Coverage.py branch measurement](https://coverage.readthedocs.io/en/7.17.0/branch.html)
and [JSON reporting](https://coverage.readthedocs.io/en/7.17.0/commands/cmd_json.html).
