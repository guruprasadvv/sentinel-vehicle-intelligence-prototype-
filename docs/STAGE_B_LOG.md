# Stage B log (uncommitted, 2026-11-08)

## Experiment 1-3: NOT RUN
- No Stage B plan, per-frame CTC data, or tracks 204/243/280 exist in this checkout or this session's context.
- The Docker daemon is not running in this cloud container, so no containers could be started.
- No "logging-only" option was found in the code. Nothing was invented.
- No blocker-per-frame results exist for 243 or 280. No accuracy claim is made.
- Free memory at check time: about 15 GB, so the 1 GB stop rule was not a factor.

## test_engineering_page
- Failed on a clean worktree of HEAD (624ad00) as well, so it was not caused by local changes.
- Cause: expected label was stale; the page renders `OCR <dev> / vehicles <dev> / plates <dev> · <checksum>`.
- Fix: expected string only, one line. Commit a612db9 (local, not pushed).
- Other two failing tests left alone. In this container, tests/test_svtrv2_experiment.py fails on a missing torchvision; I did not identify the third.

## Experiment-5 findings (expected-failure tests, unfixed)
Commit in edge/tests/test_experiment5_findings.py; each verified to fail on its assertion with the marker removed:
1. Live sightings repeat after restart (live 60 s window is in memory only).
2. Suppressed results leave no durable trace (only an in-memory Counter).
3. A suppressed partial renews the 10 s window (appended to recent_results before the suppression return).

## Unattended continuation (2026-11-08, UTC)
- 08:59 Start. Environment is a Linux cloud container (branch claude/adoring-bohr-pen1ea), not the Windows clone on work/plate-pipeline.
- 08:59 Check: commits a612db9 and fbc0fa4 exist on this branch. Working tree has no guard code (no SENTINEL_PLATE_DUPLICATE_GUARD / SENTINEL_FRAGMENT_ASSOCIATION anywhere), no docs/CANDIDATE_COVERAGE_INVESTIGATION.md, no snapshot folder, no footage.mp4 (receipt only), Docker daemon not running.
- 08:59 Task 1 BLOCKED: earlier launch logs are on the user's machine, not here. Cause of the experiment-2 launch failure cannot be confirmed; the Git Bash path rewrite named in the brief is plausible but unverified.
- 08:59 Tasks 2-5 BLOCKED: no guard code, no footage, no container runtime, so neither the candidate profile nor baseline-v3 can be run, and no per-frame rows exist. Nothing was invented. Safest choice: do not recreate the guard code or fetch other footage; continue with tasks 6-8.
- Tasks 7: only append to existing docs. CANDIDATE_COVERAGE_INVESTIGATION.md does not exist here, so it is not created or edited; the earlier draft stays on the user's machine.
- 2026-11-08 Re-attempt of experiments 1 and 2 on request: still BLOCKED. footage.mp4 absent (receipt only), no detector/OCR weights on the machine, Docker daemon down, no GPU. The only guard flag in committed code is SENTINEL_NEAR_DUPLICATE_GUARD; the vehicle-box and contradictory-frame guards are not in this checkout. No logging option written, no rows produced.
- 2026-11-08 Push authorised by the user; docs committed and the branch pushed. The local-only guard code, investigation draft and snapshot remain on the user's Windows machine and are not in this push.
