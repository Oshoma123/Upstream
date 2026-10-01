# UPSTREAM contribution protocol

Every contribution filed under this program follows these rules. They exist
because each submission spends a volunteer maintainer's time and is made under
a real person's name.

1. **Evidence first.** A contribution starts from a reproducible finding: a
   script, a record, a failing case. No finding, no contribution.
2. **Duplicate check.** Search the target's issues and PRs before filing, and
   record the search and its date in the contribution's `STATUS.json`.
3. **Check against current upstream.** Confirm the problem still exists on the
   branch maintainers merge into (e.g. MassBank-data `dev`, not `main`).
4. **Pass upstream's own checks locally.** Run whatever CI the project runs
   (MassBank Validator, R CMD check, pytest) before filing, and test the
   checker on a deliberately broken input to prove it is actually checking.
5. **Smallest useful change.** One concern per PR. No drive-by reformatting.
6. **Follow the project's process.** Target the right branch, follow
   CONTRIBUTING, and open an issue first where the project expects one.
7. **Disclose AI assistance.** One line in each PR. The author reviews the
   diff and the checks before filing, so the disclosure stays true.
8. **Credit only real work.** A `Co-authored-by` trailer on an upstream
   commit is added only for someone who worked on that specific change.
   Program-level credit lives in `AUTHORS.json`.
9. **No volume targets.** n is whatever maintainers merge. Rejected PRs stay
   in the ledger.
10. **Answer review.** Maintainer questions get answered promptly by someone
    who understands the change.
