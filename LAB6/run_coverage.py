"""Run an isolated coverage suite and save its real terminal transcript/report."""

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
MINIMUM = 90.0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["code", "branch"])
    mode = parser.parse_args().mode
    REPORTS.mkdir(exist_ok=True)
    transcript = []

    def emit(message=""):
        print(message, flush=True)
        transcript.append(message)

    def run(*arguments):
        emit("LAB6> python " + shlex.join(arguments))
        result = subprocess.run(
            [sys.executable, *arguments],
            cwd=ROOT,
            env={**os.environ, "PY_COLORS": "0", "COLUMNS": "110"},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        emit(result.stdout.rstrip())
        if result.returncode:
            raise RuntimeError(f"Command failed with exit code {result.returncode}")

    data = f".coverage.{mode}"
    report = f"reports/{mode}_coverage.json"
    exit_code = 0
    try:
        emit("LAB 6 - " + ("BRANCH COVERAGE" if mode == "branch" else "CODE (STATEMENT) COVERAGE"))
        emit(f"Python {sys.version.split()[0]}")
        emit()
        branch_options = ["--branch"] if mode == "branch" else []
        run(
            "-m", "coverage", "run", f"--data-file={data}",
            *branch_options, "--source=laundry_service", "-m", "pytest",
            f"test_{mode}_coverage.py", "-q",
        )
        run(
            "-m", "coverage", "report", f"--data-file={data}",
            "--show-missing", "--fail-under=90",
        )
        run(
            "-m", "coverage", "json", f"--data-file={data}",
            "--pretty-print", "-o", report,
        )
        totals = json.loads((ROOT / report).read_text(encoding="utf-8"))["totals"]
        covered = totals["covered_lines"]
        total = totals["num_statements"]
        percent = 100.0 * covered / total
        emit()
        emit(f"Statement coverage: {percent:.2f}% ({covered}/{total} statements)")
        if percent < MINIMUM:
            raise RuntimeError(f"Coverage is below the required {MINIMUM:.0f}%")
        if mode == "branch":
            covered_branches = totals["covered_branches"]
            total_branches = totals["num_branches"]
            branch_percent = 100.0 * covered_branches / total_branches
            emit(
                f"Branch coverage: {branch_percent:.2f}% "
                f"({covered_branches}/{total_branches} branch outcomes)"
            )
            if branch_percent < MINIMUM:
                raise RuntimeError(f"Branch coverage is below {MINIMUM:.0f}%")
        emit(f"PASS - minimum required: {MINIMUM:.0f}%")
    except RuntimeError as error:
        emit(f"FAIL - {error}")
        exit_code = 1
    finally:
        (REPORTS / f"{mode}_coverage_terminal.txt").write_text(
            "\n".join(transcript) + "\n", encoding="utf-8"
        )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
