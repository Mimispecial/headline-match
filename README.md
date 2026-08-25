# Headline Match

Runs pairwise validator comparisons of independently submitted headlines against a frozen article and fact boundary, then leaves selection to the editor.

## Why it is an Intelligent Contract

Compare a named pair and return LEFT, RIGHT, or TIE with a closed reason code: FAITHFUL, CLEARER, or BOTH_OVERREACH. GenLayer validators independently replay that semantic judgment before it becomes shared state. One-candidate-per-address enforcement, optional candidate revision, pair uniqueness, win counting, editor authorization, and final selection are deterministic.

## Reusable deployment model

Deploy once per article or editorial headline round. Reuse the source in a fresh deployment for a different article and candidate set.

A completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

The deployer is the editor. Each address may submit one candidate headline; only the editor locks candidates, requests comparisons, and selects a candidate with a recorded pairwise win.

State path: `COLLECTING_HEADLINES → PAIRWISE_COMPARISON → COMPLETE`

## Evidence boundary

The stored article title and body, supported-facts boundary, each candidate headline, and its declared promise. The contract does not browse or retrieve the article from elsewhere.

## Core invariants

- Candidates freeze before any pairwise comparison.
- An author address can create only one candidate and cannot overwrite another author.
- The same oriented or reversed pair cannot be compared twice.
- AI cannot publish or select; the editor can select only a candidate with a recorded win.

## Public interface

Write methods: `compare_headlines, lock_headlines, revise_headline, select_headline, submit_headline`

View methods: `get_comparison, get_headline, get_policy, get_state`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/headline_match.py
genvm-lint typecheck contracts/headline_match.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and uses three disposable Mimi-only accounts protected outside the workspace. It asserts finalized successful execution and reads committed state with `LATEST_FINAL`.

## Final StudioNet proof

- Contract: https://explorer-studio.genlayer.com/address/0xFB3708e4c3d241d7d9F034e7263552e44D9DD3CA
- Studio import: https://studio.genlayer.com/?import-contract=0xFB3708e4c3d241d7d9F034e7263552e44D9DD3CA
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0x20703d4748999c14dddb62df7a7f652d3172ab9ee548a9daf0f49495116eb386
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x22e75d0c1e730804b44de5064bbfa5f4c6b6f87513f119279c749865f7a6700e
- Observed committed state: `{"preferred":"LEFT","reason_code":"FAITHFUL"}`
- Audited source SHA-256: `c692c86855903470a67df19a455cb3351b825c6d4923188fdc0f8f2e5c5d3253`

## Limitations

- The frozen article and fact boundary are supplied by the deployer and are not independently verified.
- Pairwise comparison does not measure future clicks or audience reaction.
- The reason code is bounded editorial assistance, not a truth certification.

## Repository map

- `contracts/headline_match.py` — Intelligent Contract source
- `tests/direct` — hardened leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — reviewer material

License: MIT.
