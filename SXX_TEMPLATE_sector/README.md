# SXX_TEMPLATE_sector — template (v0.3.1)

This is a **minimal** sector template folder.

Purpose:
- Provide a stable slot for sector splits (`S01_<sector>`, `S02_<sector>`, ...).
- Keep sector-specific inputs/params/adapters/notes **separate** from the baseline core (`00_core`) and the multisector harness (`01_tests_multisector`).

Recommended subfolders:
- `inputs/`  : sector fixtures / raw sources (optional)
- `adapters/`: sector parsing / mapping notes or code (optional)
- `outputs/` : sector reports (optional; may be git-ignored)
- `notes/`   : sector constraints, assumptions, deltas vs baseline

No code is required here.
