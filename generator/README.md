## vvv988 lucky-number generator notes

`generate_site.py` and `content_lucky.py` came from the 2026-07-12 upload that produced the 441-page static package.

Current blocker: `generate_site.py` imports `materials_lucky.py`, but that file was not included in the upload. The checked-in production candidate is therefore based on the generated HTML package plus local SEO hardening, not a fully reproducible generator run.

Before using this generator for daily page expansion, either restore `materials_lucky.py` from the original author or replace the generator with a complete local implementation.
