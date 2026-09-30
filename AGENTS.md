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
- Work in this order for each candidate: proactive research and derivation; a per-Demo product-and-creative brief; an independently readable content draft and editorial review; a minimal operable Demo that opens directly into content; separate product, content, and functional reviews; then owner trial and iteration. A long-form `DESIGN.md` is optional later. Neither content nor mechanism may be used to excuse failure of the other.
- The original round-01 candidate comparison remains mobile-first and primarily textual. The separately imported distribution Demo may retain its supplied cover illustrations; do not treat that exception as permission to rewrite its content. Across later validation, preserve the owner's adopted text → illustration → short-video progression and the tool/distribution product distinction (decision 0006). Different mechanisms may require different layouts and movement behavior.
- For every product, search external market, adjacent-product, and technical sources yourself. Keep source evaluation and conflicting evidence in `RESEARCH.md`; derive and stress-test mechanisms in `WORKING.md`. Make and explain your own product choice; do not offer deliberately weakened concepts merely as experimental controls.
- If a product later needs a comprehensive `DESIGN.md`, use the existing long-form standard and `node scripts/check-experiment-design.mjs <product DESIGN.md>`; do not generate length merely to unlock a Demo.
- Make and review Demo iterations autonomously using the recorded principles. Do not ask the owner to preselect a concept or approve a draft before an operable Demo exists. Before coding, write `DEMO-BRIEF.md` with a concrete product value proposition and creative context for this specific content, then write `CONTENT-DRAFT.md`; read the draft without UI or mechanism labels and revise it if it cannot hold attention on its own. Record corrections and revise the product when the owner does provide feedback.
- A user-facing Demo is content to experience, not a mechanism showcase or a website about the product. Default to opening directly in representative content, with the least interface needed to understand and act. Do not insert a marketing hero, product slogan, experiment directory, or explanatory rule prose into the reading flow unless it performs a specific user task that the brief justifies.
- Keep internal neutral fixtures and rule/state checks separate from the user-facing Demo. Review creative quality, product fit, and functional correctness separately; passing tests or visual checks never marks a Demo ready for owner trial when its content has no standalone value.
- Preserve information rain's open definition: multiple reachable information trajectories from the current position. Explain the mechanism chosen for the specific product so it can be experienced and built, without imposing fixed direction semantics, adjacency logic, backtracking, or an exhaustive movement protocol in advance.
- Formal content-experience trials, when undertaken, need three structurally distinct experiences created after a viable Demo and owner trial. Each must support at least ten minutes of effective reading and interaction without forced waiting or recycled filler; record a timed walkthrough. Internal mechanism fixtures are not product Demos or those formal experiences.
- Label prewritten content, rules, and model generation accurately. Preserve raw trial records and owner quotes; the owner's actual experience is the final product judgment. Use that experience and your analysis to direct the next iteration.
- The former R01-B single-successor idea is excluded by the project owner. Choose any replacement through research, product reasoning, and the revised Demo process; do not implement the former idea as a control.

## Stage changes

When real users, production data, payments, scheduled writes, new vendors, or business-critical use are introduced, reassess `.project-start/manifest.json` before proceeding.

## Product and document boundaries

- `products/distribution/` is the active reader product source. `products/tool-agent/` is reserved for a separate future tool product. Keep product code, build output, deployment settings, and runtime assets within the correct product boundary.
- Product definitions and roadmaps belong in `docs/products/<product>/`; long-term technical vision belongs in `docs/vision/`; business plans belong in `docs/business/`; sourced external research belongs under `docs/research/<topic>/`; cross-product workflow belongs in `docs/project/`.
- `experiments/` is for bounded experiments and historical samples. Do not place the active product source there.
- `START-HERE.md` is the single workspace entry index. Each documentation category maintains its own README index. Add a link to the relevant index whenever adding a durable document; update all references when moving a file.
- Do not copy a document into a second folder to make it easier to find. Link to its single authoritative location instead.
