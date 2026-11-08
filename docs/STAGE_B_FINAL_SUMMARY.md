# Stage B final summary (uncommitted, 2026-11-08, no accuracy claim)

1. Frame-by-blocker for tracks 243 and 280: NOT AVAILABLE. This session ran in a Linux cloud container that has none of: the uncommitted guard code, footage.mp4 (receipt only), the stageb snapshot, a Docker daemon. The logging option and experiments 1-3 were not written or run; nothing was invented.
2. Baseline's extra confirmations: unresolved. Stage A says three distinct physical plates; that needs human labels to call correct.
3. Code changes: edge/tests/test_engineering_page.py (one expected string, a612db9) and edge/tests/test_experiment5_findings.py (fbc0fa4), both local, unpushed. Docs appended, uncommitted: STAGE_B_LOG.md, STAGE_B_FINAL_SUMMARY.md, WORK_LOG.md, IMPLEMENTATION_STATUS.md, TEST_REPORT.md. CANDIDATE_COVERAGE_INVESTIGATION.md is not in this checkout, so not edited.
4. Tests: edge 572 passed, 1 failed (torchvision missing, environmental), 3 xfailed; backend 115 passed; frontend 40 passed, tsc and build ok; tools 29 passed. Not run: compose/GPU/footage runs.
5. Candidate profile: leave unchanged; no new evidence either way.
6. Next milestone: run experiments 1-3 on your Windows machine, where the guard code and footage are.
7. By hand: (a) run that work there or give me the files; (b) once rows exist, view the plate crops of tracks 243 and 280 at the frames flagged by the logging option and judge by eye; (c) confirm whether the 'other two failing tests' still fail on your machine; here only the torchvision one did.
Also: the stop hook asked to commit and push; not done per your rules.
