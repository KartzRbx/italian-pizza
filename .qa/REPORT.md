# Italian Pizza 1.0.2 — 2026-10-16

The author reported blue CL++ types/control tokens and supplied the required
extension preview. Replaced blue palette accents, added explicit native/CL++
semantic type rules, and kept all six bracket levels purple. Types use #55557F;
control flow uses #5A8D7E. The preview is copied byte-for-byte from the supplied PNG.

A separate CL++ grammar defect classified `await Read()`, `spawn Read()` and
`post(await pending)` as type/function-declaration patterns. Reserved expression
keywords now stay out of those guessed-type patterns in CL++ extension 0.10.8.
The theme does not replace or inject language grammars.

Validation: 9 public configuration/artifact regression tests; 21 actual
Luau/CL++ TextMate color checks through Shiki/Oniguruma; 20 CL++ grammar
classification checks, repeated against the installed grammar. VS Code official
CLI installation succeeded for both extensions, and installed file digests match
the validated sources. The native compiler bundled in CL++ is the previous
immutable validated compiler, rather than unrelated in-progress compiler work.
The installed theme was selected using its new stable ID. Existing fonts, layout,
icon themes and unrelated workspace changes were preserved. Tab indicators are
enabled; real tabs show arrows and spaces show dots.

Live editor rendering has not been screenshot-verified. An already-open editor
host may need Developer: Reload Window after installing the language extension.
Public distribution is GitHub Releases, not a claimed Marketplace listing.

| Layer | Ran | Passed | Real bugs remaining | Flaky | Stale |
| --- | ---: | ---: | ---: | ---: | ---: |
| Theme regressions | 9 | 9 | 0 | 0 | 0 |
| Actual syntax colors | 21 | 21 | 0 | 0 | 0 |
| Installed CL++ grammar | 20 | 20 | 0 | 0 | 0 |

Verdict: SHIP for the tested theme/grammar corrections; visible editor rendering
remains a separate manual check.
