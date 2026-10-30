# Production workflow

## 1. Establish a brief

Record topic, audience, central question, one takeaway, mode, output language, total duration, sample duration if applicable, dimensions, fps, audio choice, and available references. Record these in the project's brief or `brief.md` so later revisions retain them. Use the skill defaults for routine missing choices; ask only when the answer materially changes the deliverable.

For an extension, inspect the actual sources, timeline, fonts, palette, assets, and approved opening. Preserve useful work. If only a rendered video exists, distinguish reusing that clip from recreating its source. Do not promise pixel-identical recreation without the project.

Done: the deliverable and what the viewer should learn are explicit.

## 2. Verify the explanation

Use current primary sources for changing technical claims, exact quotations, scientific findings, dates, limits, and product capabilities. Prefer the user's supplied sources and official documentation. If browsing is unavailable, mark unverified claims rather than inventing citations. Avoid unsupported numerical comparisons; mark invented values as illustrative.

Keep a compact fact ledger in `sources.md`: claim, direct URL or supplied document location, access date, applicable configuration/version, and visual consequence. Distinguish facts, simplifications, and illustrative data. For example, a retry arrow needs a named triggering condition, and a managed service boundary must not imply that it writes the customer's application logic.

Define the scenario narrowly enough to remain correct: chosen protocol, deployment model, success/failure behavior, consistency or retry semantics when relevant. Include one useful limitation. For nontechnical subjects, apply the same discipline to evidence, causal claims, chronology, and uncertainty. Never convert a correlation into a causal animation without support.

Done: each consequential claim has evidence or a visible uncertainty label; the example can be followed without contradictory data.

## 3. Plan time and visual meaning

Write a storyboard with: start/end, learning objective, visible entities and their state, action, exact captions, audio cue, and relevant fact-ledger entries. Scenes must cover the requested duration without accidental gaps or overlaps. Explicit intentional transitions may overlap visually.

Use one continuing example. Introduce the question, show the normal mechanism, expose a failure or boundary, and return to the takeaway. A two-minute video usually needs 6–8 meaningful beats; three minutes allows a deeper example and a failure case. These counts are guidance, not requirements.

Extend by adding explanation, not stretching footage: show previously hidden steps, contrast two conditions, trace a failure and recovery, or add a worked example. Keep the accepted opening when it still fits. Do not pad with long holds, repeated captions, or slower playback.

Use a shared timeline, such as `timeline.json`, for scenes, captions, audio events, and review timestamps. Define time units and fps. For a duration D and frame rate F, render N = round(D × F) frames at t = n/F, n = 0…N−1. The final timeline boundary is D; it is not an extra frame. Name the output duration tolerance in the brief (default ±1 second).

Write language-specific captions at natural reading speed; English and Chinese cannot be translated by fixed word-for-character lengths. As a first layout pass, use at most two short caption lines and keep them inside a 5% safe margin; then inspect at the actual output size. A few words may take 2 seconds; dense explanation needs longer or fewer words. Treat these as starting points, not proof of readability.

Done: the full timeline adds up; every motion communicates an identifiable state change, relation, or cause.

## 4. Choose one rendering path

Use the existing engine if it fits. Otherwise pick one:

- React project: Remotion and its frame-based animation tools.
- HTML/SVG/Canvas project: HyperFrames or HTML + Playwright + ffmpeg with a deterministic `seek(t)` entry point.

Read the installed engine's current docs before invoking commands; do not invent an interchangeable CLI across these tools. Use a project-local environment and lockfile when adding dependencies. Reuse authorized local fonts/assets; record their source and license. The skill itself requires no cloud account or API key.

For HTML rendering, `seek(t)` must derive the complete frame from t, including captions, paths, particles, and transitions. Avoid wall-clock timers, live network data, unseeded randomness, or animation state that depends on the previously rendered frame. Wait for fonts and assets before capture. Frame-based engines should meet the same determinism requirement using their native API.

Use stable object identities and consistent colors. Distinguish data flow from control/configuration edges; label conceptual groups that are not physical machines. Do not animate requests through a DNS lookup or an authorization policy as though they were data-processing servers.

Done: one representative frame renders, repeated seeks to the same t match, and the reproduction command is recorded.

## 5. Preview, inspect, and render

Implement the requested preview or an internal short draft, then inspect it. Internal drafts do not create a new approval gate. If the user asked to approve the preview, stop with a reviewable preview and wait; otherwise fix issues and continue.

Sample scene starts, midpoints, scene ends, and transition boundaries (including one frame before/after where useful). Include timestamps on the contact sheet. Check clipping, missing glyphs, contrast, overlaps, captions, arrow direction, and factual meaning. Contact sheets are sampled evidence, not full playback verification.

Check temporal behavior with video playback or an available equivalent: reading time, pacing, continuity, audio synchronization, and clipping/clicks. Use generated or appropriately licensed music; do not inherit a particular song or its 17-second cue from an example. Add narration only when requested, and align the final timing to the actual voice track.

Render the final artifact for the selected mode. Inspect media metadata with ffprobe or an equivalent tool: duration, dimensions, fps, video/audio streams, codec compatibility, and file readability. Prefer broadly playable MP4 (H.264/yuv420p and AAC when an audio track exists) when supported. Record the actual parameters, not just the requested settings.

Done: the artifact exists, metadata meets the brief, and visual/temporal checks are documented. If full playback, listening, or rendering cannot be performed, explicitly mark that check unverified.

## 6. Deliver a reproducible project

Adapt names to the existing project; a new project can use:

```text
brief.md                 # mode, language, assumptions, output contract
storyboard.md            # timing, actions, exact captions
sources.md               # factual claims and asset provenance
timeline.json            # single timing source used by renderer/review
src/                     # editable scenes and required local assets
output/preview.mp4       # preview mode
output/final.mp4         # full/extend mode
output/contact-sheet.png
qa.md                    # actual checks, limitations, fixes
README.md                # dependencies, exact render/preview commands
```

For prompt-only mode, put the relevant contract inside the prompt instead of producing these rendering artifacts. Include primary source links and instruct the receiving agent to recheck changing facts.

Report what was created, where it is, how to reproduce it, and remaining limitations. Separate “planned”, “rendered”, “frame-inspected”, and “played/listened to”. A video is complete only when the requested output and verification appropriate to the available tools have actually been delivered.
