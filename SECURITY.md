# Security

## Scope

This repository contains one bounded Intelligent Contract, direct tests, a five-validator GLSim test, and an opt-in StudioNet smoke test. It has no frontend, backend, database, token, payout, proxy upgrade, or repository secret.

## Trust model

Untrusted evidence is delimited as data, model outputs use closed schemas, and validator replay must agree before semantic state is stored.

The deployer is the editor. Each address may submit one candidate headline; only the editor locks candidates, requests comparisons, and selects a candidate with a recorded pairwise win.

## Implemented controls

- Concrete immutable GenVM runner hash; no floating runner dependency.
- Address normalization, explicit role separation, collection caps, one-time actions, and lifecycle locks.
- Bounded text plus strict `[EXPECTED]` and `[LLM_ERROR]` failure classes.
- Sorted, delimited evidence packets and independent validator replay.
- Storage is copied before nondeterministic callbacks; static audit requires zero callback reads from `self`.
- No cross-contract calls, fund custody, transfer, automated purchase, external deletion, or webhook.
- `.env`, caches, artifacts, wallet files, and local secrets are ignored. Live wallets are encrypted outside the workspace.

## Contract-specific safety properties

- Candidates freeze before any pairwise comparison.
- An author address can create only one candidate and cannot overwrite another author.
- The same oriented or reversed pair cannot be compared twice.
- AI cannot publish or select; the editor can select only a candidate with a recorded win.

## Residual risks

- The frozen article and fact boundary are supplied by the deployer and are not independently verified.
- Pairwise comparison does not measure future clicks or audience reaction.
- The reason code is bounded editorial assistance, not a truth certification.

Do not use this contract to make legal, medical, financial, employment, admission, credit, or physical-safety decisions beyond the explicit low-risk policy in its source. A new use case requires a fresh deployment and independent domain review.

## Reporting

Report vulnerabilities privately to the repository owner with the contract name, affected method, reproduction, expected invariant, and impact. Never include private keys, wallet passwords, or personal data.
