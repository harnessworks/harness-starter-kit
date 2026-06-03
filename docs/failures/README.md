# docs/failures

These records are this kit's own failure history. Each file documents a real
mistake or failed approach encountered during kit development, the fix applied,
and the automated check that prevents recurrence.

They are not examples to copy into a target repository. When adopting this kit,
your target repository gets `000-template.md` as the starting shape. Create your
own `docs/failures/*.md` records there as your project encounters failures worth
preserving.

`scripts/check_failure_memory.py` validates that every record in this folder
names a concrete detection or prevention check.
