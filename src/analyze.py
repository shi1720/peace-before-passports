"""Reproduce descriptive tables; no statistical or causal inference is performed."""
import csv, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def load():
    return json.loads((ROOT/'data/clauses.json').read_text())

def verify_sources():
    for item in json.loads((ROOT/'data/source_manifest.json').read_text()):
        actual = hashlib.sha256((ROOT/item['selected_file']).read_bytes()).hexdigest()
        if actual != item['selected_sha256']:
            raise ValueError('Source checksum mismatch: '+item['id'])
    dispatch=json.loads((ROOT/'data/dispatch_manifest.json').read_text())
    actual=hashlib.sha256((ROOT/'sources/obrien_1798_p258-262.pdf').read_bytes()).hexdigest()
    if actual != dispatch['extract_sha256']:
        raise ValueError('Dispatch extract checksum mismatch')

def summarize(rows):
    main = [r for r in rows if r['witness_type']=='edition_main_text']
    summary = []
    for witness in ('1795t','1796t','1797t','1805t','1815t','1816t'):
        selected = [r for r in main if r['witness']==witness]
        transition = next(r for r in selected if r['mechanism'] in ('initial_transition','conge_transition','immediate_issuance'))
        prize = next(r for r in selected if r['mechanism']=='purchased_prize')
        summary.append(dict(witness=witness,transition_type=transition['mechanism'],transition_months=transition['duration'],purchase_months=prize['duration'],transition_article=transition['article'],purchase_article=prize['article']))
    return summary

def main():
    verify_sources(); rows=load(); result=ROOT/'results';result.mkdir(exist_ok=True)
    summary=summarize(rows)
    with (result/'treaty_comparison.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    audit=dict(article_witness_units=len(rows),distinct_treaty_instruments=len({r['year'] for r in rows}),text_witnesses=len({r['witness'] for r in rows}),main_text_units=sum(r['witness_type']=='edition_main_text' for r in rows),later_translation_units=sum(r['witness_type']=='later_translation' for r in rows),purchase_terms_months=[r['purchase_months'] for r in summary],note='Null means no numerical limit stated in this selected clause, not perpetual validity. Translations and treaty renewals are not independent observations.')
    (result/'summary.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps(audit,indent=2))

if __name__=='__main__':main()
