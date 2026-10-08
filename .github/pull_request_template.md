<!-- See CONTRIBUTING.md. For a new video, please link the claim issue: Closes #... -->

**Result:** family NNN (title)
**Paper(s):** repo/preprints/...
**Lean status on the card:** formalized / not yet formalized (and which part, if partial)

**Preview:** drag the rendered MP4 here, plus a contact sheet or two.

**AI use:** none / which parts. I have personally reviewed the output.

### Checklist
- [ ] Every name, date, number and attribution comes from the paper or is standard fact. Uncertain claims are cut.
- [ ] The result is presented as a claim from a manuscript produced by an OpenAI model, not yet peer reviewed.
- [ ] The status card says "formalized" only if `repo/lean/docs/NNN.md` covers the main theorem; partial coverage is explained in the narration.
- [ ] No "first ever" or "open since" claims unless the paper makes them.
- [ ] The proof section explains the paper's actual mechanism.
- [ ] Contact sheets are clean: nothing overlaps, nothing is off-screen, no awkward line wraps.
- [ ] Runs about 3.5–5 minutes; `./render.sh videos/vNN_slug.py high` works on a fresh checkout.
- [ ] Only my own files changed (`videos/vNN_*.py`, `videos/data/*vNN*`); no rendered video, cache or `repo/` committed.
