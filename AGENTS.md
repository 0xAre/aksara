# AKSARA Shared Agent Instructions

## Project Identity

- Project name: AKSARA.
- AKSARA is the backronym for "Authenticated Key-based Secure Autonomous Relay Architecture"; its documented development direction is commercial.
- AKSARA is a serverless, encrypted, two-party P2P terminal chat application.
- Main stack: Rust 2021, Tokio, ratatui/crossterm, LAN discovery with mDNS/TCP, and Tor onion services.
- The repository is a single crate and single binary with `src/main.rs` as its entry point; primary modules are `identity`, `crypto`, `transport`, `contacts`, `session`, and `tui`.
- Cryptographic implementation recorded by the completed audits includes Noise IK, Ed25519, X25519, Argon2id, ChaCha20-Poly1305, BLAKE2s, and supporting components.
- AKSARA is not `CARAKA-APP` and is not the separate `Caraka` project. Never merge their facts or documents.
- Current documented implementation status is v0.2.1. The existing project record reports 46 passing tests and clean Clippy under CI; do not present these as newly verified unless they are rerun.
- License: proprietary, all rights reserved.

## Academic Context

- The deliverable is the final assignment for the Implementasi Kriptografi course.
- It is group work by three members, not an individual thesis or skripsi.
- Member names are CONFIRMED as of 2026-07-27, sourced from `docs/mini-ta/00-template/PROPOSAL CARAKA (2).docx` (same course, same group): Andika Aryansyach Fauzan (2322101878), Mahendra Nur Hidayat (2322101937), Rafi Putra Fadlurrahman (2322101963). Study program: Rekayasa Sistem Kriptografi. Institution: Politeknik Siber dan Sandi Negara. Year: 2026. The placeholders `Anggota 1/2/3` are retired; only the mapping of each name to a specific module assignment remains `NEEDS_CONFIRMATION`.
- Focus on factual cryptographic implementation and justification. Keep the scope proportional to a course assignment while maintaining academic substance and accuracy.

## Mandatory Startup Sequence

For mini-TA work, read in order:

1. `docs/mini-ta/PROJECT_MEMORY.md`
2. `docs/mini-ta/01-claude-preparation/PROGRESS.md`
3. The latest `SESSION_N_HANDOFF.md`
4. The deliverable for the active stage

Do not repeat a stage marked `DONE` unless a specific, documented contradiction requires it.

## Source-of-Truth Hierarchy

1. Actual source code
2. `Cargo.toml` and versions verified from `Cargo.lock`
3. Tests and build output
4. Verified audit evidence
5. Project documentation
6. Old proposals as historical context only
7. External references for theory, never as proof of local implementation

## Anti-Hallucination Rules

- Do not invent features, algorithms, parameters, test results, benchmarks, references, DOIs, authors, years, or venues.
- Documentation alone does not prove `IMPLEMENTED`.
- Every implementation claim needs a source path and symbol.
- Every theoretical claim needs a source.
- Every result claim needs experimental data.
- Use `NEEDS_CONFIRMATION` when evidence is unavailable.
- Distinguish `IMPLEMENTED`, `PARTIAL`, `PLANNED`, `DOCUMENTED_ONLY`, `NOT_FOUND`, `INCONSISTENT`, and `NEEDS_EXPERIMENT`.

## Filesystem Rules

- Write all mini-TA output only under `docs/mini-ta/`.
- Do not create root files or directories except `AGENTS.md` or an official file explicitly requested by the user.
- Never use sentences, claims, evidence, response text, model data, or JSON content as a file or directory name.
- Paths must be short, static, and deterministic. Validate every output path before writing.
- Before ending, run `git status --short --untracked-files=all`.
- Clean up or quarantine abnormal root artifacts before ending the session.

## Source-Code Protection

For documentation work:

- Do not modify `src/`, `Cargo.toml`, `Cargo.lock`, tests, or production configuration.
- Do not run a repository-wide formatter.
- Do not run `git clean`, `git reset`, `git checkout`, or destructive deletion.
- Source changes require an explicit user request.

## Progress and Handoff

After completing a stage, update `docs/mini-ta/01-claude-preparation/PROGRESS.md`.

When a session approaches its limit:

1. Stop starting new work.
2. Save all findings.
3. Update `PROGRESS.md`.
4. Create or update `SESSION_N_HANDOFF.md`.
5. Record the next action.
6. Stop.

An agent's internal memory must never be the only location for important facts. Store all cross-agent facts in the repository.
