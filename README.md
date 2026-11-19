# Lab 6 – Code and Branch Coverage Analysis

**Name:** S Kushal Raju  
**SRN:** PES2UG24AM139  
**Assignment:** L6_L7_54 – Museum Admission

## Files

| File | Description |
|---|---|
| `museum_admission.py` | Module under test (given): `ticket_price`, `group_discount`, `gallery_entry` |
| `test_museum_admission.py` | Starter test file (given, 2 tests) |
| `CodeCoverageTest_museum_admission.py` | Test cases written for code (line) coverage |
| `BranchCoverageTest_museum_admission.py` | Test cases written for branch coverage |
| `screenshots/` | Terminal output of the coverage runs |

## How to run

```bash
pip install coverage pytest

# Code (line) coverage
coverage run -m pytest CodeCoverageTest_museum_admission.py
coverage report -m

# Branch coverage
coverage run --branch -m pytest BranchCoverageTest_museum_admission.py
coverage report -m
```

## Starting point (given tests only)

| Metric | `museum_admission.py` |
|---|---|
| Line coverage | 47% (19 of 36 statements missed) |
| Branch coverage | 42% (10 partial branches) |

## Code coverage – 100%

The 17 tests in `CodeCoverageTest_museum_admission.py` execute every statement once: both `raise` lines in each function, the free entry for under-5s, the Monday and weekend price changes, both guided-tour fees, every discount tier and all three gallery results.

![Code coverage](screenshots/code_coverage_report.png)
