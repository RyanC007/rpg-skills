# Social Engine Sunday/Monday Workflow
**Date Added:** 2026-03-25
**Applies To:** Trinity, Scarlett

## Core Directive
The Social Engine pipeline operates on a strict two-step schedule with NO automated polling and NO approval emails. Scarlett generates the content on Sunday and drops it in Drive. Trinity picks it up on Monday morning ONLY when explicitly asked by Ryan.

## Details
1. **Sunday 18:00 UTC (Scarlett):** Scarlett runs `pipeline_runner.py --client ryan` via a scheduled task. This generates 7 days of content and uploads it to the Drive `content-drafts` folder. It does NOT send an email.
2. **Monday Morning (Trinity):** Trinity waits for Ryan to say "run the pipeline", "push to Blotato", or "pick up Golden Moments".
3. **Trinity's Execution:** When asked, Trinity runs `golden_moments_handoff.py --client ryan` to convert the Drive files, then runs `cloud_daily_run.py --client ryan --force-post --day 1` (and subsequent days) to push directly to Blotato.
4. **Polling is permanently disabled:** The `cloud_daily_run.py` polling sentinel is set to disabled. Do not re-enable it.
