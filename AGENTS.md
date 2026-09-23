# Project instructions: Information Rain

## Start every task

- Read `START-HERE.md`, `docs/project/brief.md`, and the current stage gates.
- Restate the requested outcome and its acceptance criteria before changing behavior.
- Preserve the approved first-release boundary; propose scope changes explicitly.
- Explain decisions and results to the project owner in plain language.

## Engineering agreements

- Keep changes small, independently testable, and visible in Git.
- Run the project's verification command after relevant changes.
- Add or update tests when behavior changes or a defect is fixed.
- Do not add a dependency without explaining its purpose and maintenance cost.
- Never commit real secrets, tokens, customer data, production exports, or local credentials.
- Record architecture-significant or difficult-to-reverse decisions in `docs/project/decisions/`.
- External actions such as repository changes, cloud provisioning, secret setting, deployment, or production access require an explicit user request.

## Product experiments

- Before experiment work, read `docs/project/experiment-scaffold.md`, the current round's `PLAN.md`, any previous round `RESULT.md`, and the relevant product's current design. Do not revive a rejected candidate from an older document.
- Work in this order for each candidate: proactive external research, first-principles derivation and stress testing, iterative discussion and a polished `DESIGN.md`, operable product mechanism Demo, mechanism trial, then three content experiences and their trials. Content topics must not determine a product mechanism retroactively.
- In round 01, keep the medium textual, the experience mobile-first, and the visual design language shared across products. Different mechanisms may require different layouts and movement behavior.
- For every product, search external market, adjacent-product, and technical sources yourself. Keep source evaluation and conflicting evidence in `RESEARCH.md`; derive and stress-test mechanisms in `WORKING.md`. Make and explain your own product choice; do not offer deliberately weakened concepts merely as experimental controls.
- Each product `DESIGN.md` must contain at least 10,000 Chinese characters of substantive body text; market-demand observation and technical understanding together must contain at least 3,000. The final document should read like a technical blog, not a raw notebook or questionnaire. Character count does not excuse weak evidence or repetition.
- Discuss the market judgment, product derivation, technical constraints, and design choice with the owner across drafts. Record corrections and revise the actual design before treating it as ready.
- Check those counts with `node scripts/check-experiment-design.mjs <product DESIGN.md>` before moving to a mechanism Demo; review substance by hand as well.
- Preserve information rain's open definition: multiple reachable information trajectories from the current position. Explain the mechanism chosen for the specific product so it can be experienced and built, without imposing fixed direction semantics, adjacency logic, backtracking, or an exhaustive movement protocol in advance.
- Each product needs three structurally distinct content experiences, created after its mechanism Demo. Each must support at least ten minutes of effective reading and interaction without forced waiting or recycled filler; record a timed walkthrough.
- Label prewritten content, rules, and model generation accurately. Preserve raw trial records and owner quotes; the owner's actual experience is the final product judgment. Use that experience and your analysis to direct the next iteration.
- The former R01-B single-successor idea is excluded by the project owner. Its replacement must be chosen through product discussion; do not implement the former idea as a control.

## Stage changes

When real users, production data, payments, scheduled writes, new vendors, or business-critical use are introduced, reassess `.project-start/manifest.json` before proceeding.
