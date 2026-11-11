# Lab 7 - Laundry Service Fuzz Testing

The Lab 6 application is in ../LAB6/laundry_service.py. The instructor has a
separate Lab 7 starter for the same laundry-service topic:
https://github.com/SETAPESU26/L6_L7_41_laundry_service/tree/main/Lab%207

Its functions are parse_order, weight_average and payable_charge. The original
Lab 6 coverage functions are different. processor_original.py preserves the
instructor's Lab 7 laundry_service.py unchanged. processor.py uses the filename
requested in the submission notice. test_processor.py completes and extends
the three no-crash tests in the instructor's starter.

## Validation choices

The Lab 7 student handout requires all three functions to withstand unexpected
input without crashing. The following validation policies are implementation
choices used by this solution:

- Invalid inputs return None; the interactive program prints "Invalid input".
- Garments are regular, delicate or bedding, ignoring case and outer whitespace.
- Weights, charges and discounts must be finite nonnegative numbers.
- CSV weights may be fractional. The result is a true arithmetic mean.
- Payable charge retains the starter's 18% tax and lower bound of zero.
- Non-finite computed results are rejected.

Tests include arbitrary text, None and other types, valid generated inputs,
explicit invalid examples, and a regression for the original floor-division bug.
The original starter raises exceptions for None/empty strings, parses non-finite
and negative numbers, and truncates fractional averages.

## Run and capture evidence (PowerShell)

Verified locally on 11 November 2026 with Python 3.12.10: the original-module
run produced 3 failed tests (20 deselected); the corrected-module run produced
23 passed tests. Actual output is saved in evidence/. Dependencies are pinned
to a pure-Python Hypothesis release compatible with this Windows environment.

Run all commands from this LAB7 directory. Do not activate the environment;
using its Python directly avoids PowerShell activation policy issues.

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    New-Item -ItemType Directory -Force screenshots,evidence

1. Run the original app:

    .\.venv\Scripts\python.exe processor_original.py

Enter regular:6, then 3,4, then 300|40. Screenshot the prompts and outputs,
including the incorrect average of 3. Save as screenshots/01_original.png.

2. Run the same fuzz tests against the preserved original:

    $env:PROCESSOR_MODULE = "processor_original"
    .\.venv\Scripts\python.exe -m pytest test_processor.py -k no_crash -v --tb=short -p no:cacheprovider 2>&1 | Tee-Object evidence/02_original_failures.txt

Capture each function's "Falsifying example" and exception, plus the summary.
Expect all three selected tests to fail; the exact examples vary.
Use several screenshots if needed: 02a_parse_failure.png,
02b_average_failure.png, 02c_charge_failure.png.

3. Switch to the fixed module:

    Remove-Item Env:PROCESSOR_MODULE
    .\.venv\Scripts\python.exe processor.py

Enter regular:6, then 3,4, then 300|40. Capture the corrected average 3.5
and the other results as screenshots/03_corrected.png.
Optionally run again with regular:-1, 3,,4 and 300|nan to show safe rejection.

4. Run the full final suite:

    .\.venv\Scripts\python.exe -m pytest test_processor.py -v --hypothesis-show-statistics -p no:cacheprovider 2>&1 | Tee-Object evidence/04_final_tests.txt

Capture the passing test names and final summary as screenshots/04_final_pass.png.
The number in the pytest summary counts test cases; each @given test separately
runs many generated examples. Capture the statistics if desired.

## Consolidated PDF and Git submission

Make ONE PDF containing:
- Your name/SRN, lab title and repository URL.
- The original, fuzz-failure, corrected and final-pass screenshots with captions.
- A short bug/fix explanation and the validation choices above.
- Complete processor.py and test_processor.py source listings.

Suggested filename: reports/LAB7_Fuzz_Testing_Report.pdf.
Use actual terminal screenshots (Win+Shift+S). Transcripts are supporting evidence.

From the SE-labs repository root, after checking your screenshots and PDF:

    git status --short
    git add LAB7
    git commit -m "Complete Lab 7 laundry service fuzz testing"
    git push

Verify that the complete LAB7 folder is visible on GitHub, then submit the one
PDF via the Google Form in the assignment. Do not include the virtual environment.

## Completed submission artifacts

- [Consolidated PDF: screenshots and both complete source listings](reports/LAB7_Fuzz_Testing_Report.pdf)
- [Original application execution](screenshots/01_original_application.png)
- [Original fuzz failures](screenshots/02_original_fuzz_failures.png)
- [Original failure summary](screenshots/03_original_failure_summary.png)
- [Corrected application execution](screenshots/04_corrected_application.png)
- [Initial passing tests](screenshots/05_initial_passing_tests.png)
- [Initial passing summary](screenshots/06_initial_passing_summary.png)
- [Safe invalid-input handling](screenshots/07_invalid_input_handling.png)
- [parse_order counterexamples](screenshots/08_parse_order_counterexamples.png)
- [weight_average counterexamples](screenshots/09_weight_average_counterexamples.png)
- [payable_charge counterexamples](screenshots/10_payable_charge_counterexamples.png)
- [Final clean result: 23 passed](screenshots/11_final_23_tests_passed.png)

The screenshot files are unchanged copies of the student's terminal captures.
Earlier captures show pytest cache permission warnings; the final run disables
the optional cache provider and passes all 23 tests without those warnings.
