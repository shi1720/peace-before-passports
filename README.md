# Peace Before Passports

**Documentary Grace and American Protection in the Maghreb, 1795–1816**  
Shivam Gupta · Research materials · 16 October 2026

This repository accompanies a historical study prepared for SHAFR 2027. It compares documentary transitions in United States treaties with Algiers, Tripoli, and Tunis, using Morocco in 1786 as a comparator, and reads Richard O'Brien's report on the brig *Mary* in October 1798.

## Findings and contribution

The study distinguishes the initial distribution of passports, the Tunis conge/testa requirement, temporary documentation for purchased prizes, and convoy declarations. Immediate passport issuance coexisted with transaction-specific temporary papers. The *Mary* dispatch connects documentary acceptability to consular intervention, the physical performance of paper, and a proposed period of overlapping validity. Different textual witnesses retain different eligibility and evidence conditions even when they agree on a numerical duration.

The contribution is a historical comparison and source-linked research apparatus. It is not the discovery of Mediterranean passports, a new cryptographic protocol, an estimate of seizure rates, or a claim of patentable software.

## Reproduce

Python 3.9 or later; analysis and tests require only the standard library:

```sh
python3 src/analyze.py
python3 -m unittest discover -s tests -v
```

Generate figures and the manuscript:

```sh
python3 -m pip install -r requirements.txt
python3 src/figures.py
python3 src/build_pdf.py
```

The PDF builder uses local Times New Roman/Arial fonts when available and standard PDF fonts otherwise. It writes the manuscript PDF to the parent directory. The archived manuscript is also in `docs/`.

## Files

- `data/clauses.json`: 30 selected article-witness units; interpretive annotations retained alongside passages.
- `data/source_manifest.json`: ten witness URLs, original downloaded HTML hashes, and hashes of the selected source transcripts.
- `data/dispatch_manifest.json`: provenance of the five-page public-domain dispatch extract.
- `sources/`: selected treaty passages and printed pages 258–262 of the 1798 dispatch.
- `results/`: descriptive comparison and corpus totals.
- `figures/`: generated illustrations in raster and vector formats where applicable.
- `docs/`: manuscript, literature and application notes.

There are seven treaty instruments including the Moroccan comparator, ten textual witnesses, and thirty selected article-witness units. These are not thirty independent historical events. Twenty-two units are from the edition's main texts; eight are from later translations. The Tunis instrument is the 1797 treaty as altered in 1799; the selected articles were not altered.

`duration: null` means that no numerical maximum is stated in the selected passage. It does not mean an unlimited entitlement. The value zero is used only for an immediate-issuance instruction. Pursuit delays are explicitly recorded in hours. `mechanism` and `reading` are editorial interpretations, not machine classifications. The later witnesses must not be silently merged with the main texts.

## Verification and limits

Eleven test methods check checksums, passage presence, identifiers, stated duration phrases, units, key differences between witnesses, and the comparison's treatment of null values. They establish reproducibility and internal consistency; they do not prove the interpretation or establish historical enforcement frequency. The *Mary* narrative is a single official's report, not a court transcript. Original Arabic and Ottoman Turkish manuscripts have not been newly translated here.

The manuscript states which secondary works were consulted through accessible abstracts or previews. The literature review supports a bounded contribution, not an assertion that no prior author has ever discussed a similar issue. See `docs/literature_review.txt`.

## Sources and rights

The treaty passages derive from Hunter Miller, ed., *Treaties and Other International Acts of the United States of America*, vol. 2 (GPO, 1931), via Yale's Avalon Project. The dispatch derives from Dudley W. Knox, ed., *Naval Documents Related to the United States Wars with the Barbary Powers*, vol. 1 (GPO, 1939), via the American Naval Records Society collection at ibiblio. Source links and attribution are retained. No copyrighted secondary-book PDFs are redistributed.

Code: MIT license. Manuscript and original annotations: © 2026 Shivam Gupta; all rights reserved. Government source material retains its original status. The PDF and source register are offered for scholarly inspection and citation; conference acceptance is not implied.
