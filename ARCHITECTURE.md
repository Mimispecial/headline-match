# Architecture

## Deployment boundary

Deploy once per article or editorial headline round. Reuse the source in a fresh deployment for a different article and candidate set.

Constructor data establishes the deployment subject and fixed role boundary. Later writes add only the bounded records permitted by the lifecycle; a completed instance cannot be reopened.

## Participants

The deployer is the editor. Each address may submit one candidate headline; only the editor locks candidates, requests comparisons, and selects a candidate with a recorded pairwise win.

Addresses are normalized before authorization comparisons. Role checks and lifecycle gates execute before semantic assessment.

## State machine

`COLLECTING_HEADLINES → PAIRWISE_COMPARISON → COMPLETE`

The phase-like field is the primary lifecycle lock. Each write advances that path, performs a documented bounded loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

The stored article title and body, supported-facts boundary, each candidate headline, and its declared promise. The contract does not browse or retrieve the article from elsewhere.

Before consensus, the contract normalizes bounded text, copies required storage into plain local values, serializes a sorted JSON packet, and places it between explicit START/END delimiters. Nondeterministic callbacks do not read contract storage.

## Consensus boundary

Compare a named pair and return LEFT, RIGHT, or TIE with a closed reason code: FAITHFUL, CLEARER, or BOTH_OVERREACH.

The leader callback validates exact JSON shape, field types, closed labels, masks or codes, and length bounds. A validator reruns the same semantic operation and rejects disagreement before state is committed.

## Deterministic boundary

One-candidate-per-address enforcement, optional candidate revision, pair uniqueness, win counting, editor authorization, and final selection are deterministic.

Important invariants:

- Candidates freeze before any pairwise comparison.
- An author address can create only one candidate and cannot overwrite another author.
- The same oriented or reversed pair cannot be compared twice.
- AI cannot publish or select; the editor can select only a candidate with a recorded win.

No method sends value, pays rewards, escrows assets, deletes external data, calls another contract, or invokes a webhook.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and cannot be stored.
- Validator disagreement cannot commit the semantic result.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.
