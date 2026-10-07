# Release Checklist

## Pre-Release
- [x] Verify all 128 tests pass locally.
- [x] Check that `README.md` instructions are accurate.
- [x] Confirm no API keys or personal credentials exist in the codebase.
- [x] Review uncommitted changes and plan commits.
- [ ] Make a project License decision.
- [x] Draft `CHANGELOG.md` and `docs/release_notes_v1.0.0.md`.

## Release Operations (Awaiting User Approval)
- [ ] Commit Phase 6 features (Streamlit UI).
- [ ] Commit Phase 7 features (Benchmark Runner).
- [ ] Commit Phase 8 features (Documentation & Paper).
- [ ] Merge `main` to `main` (fast-forward, currently no branches).
- [ ] Create Git tag `v1.0.0`.
- [ ] Push commits and tag to remote.

## Post-Release
- [ ] Publish GitHub Release using `release_notes_v1.0.0.md`.
- [ ] Verify tarball/zip generation on GitHub.
