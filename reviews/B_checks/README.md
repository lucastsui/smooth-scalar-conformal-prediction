**Reviewer B check artifacts**

These artifacts were produced in a separate AI technical review of frozen manuscript v1. They do not constitute external expert validation.

- `checks.py`: independent reference calculations and stress checks; writes `check_results.json`.
- `check_results.json` and `checks.log`: structured and textual results of the executed checks.
- `reproduced/`: original confirmatory script rerun with the same configuration and seeds; all 28 raw NPZ arrays match the original results exactly.
- `reproduction.log`: output from that complete rerun.
- `linear_boundary_probe.json`: recorded failure when the linear experiment is given an infinite-threshold setting outside its frozen configuration.
- `independent_test_audit_recomputed.json`: independently recomputed means and Monte Carlo uncertainty from the saved calibration-level test counts.
- `page-01.png` through `page-10.png`: frozen PDF pages rendered with Poppler and inspected.

The supplied six tests were run separately with `.venv/bin/python -m pytest -q -p no:cacheprovider src/test_core.py`; the captured tool result was `6 passed in 0.41s`. No original source file or evidence file was edited.

Re-run the reviewer script from the project root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python reviews/B_checks/checks.py
```

For a new confirmatory reproduction, select a fresh output directory; the supplied runner intentionally refuses to overwrite a completed run.
