"""Evidence-integrity checks and independent checks of the published comparison."""
import hashlib,json,re,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from analyze import load,summarize,verify_sources
class EvidenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rows=load();cls.by={r['id']:r for r in cls.rows}
 def test_source_checksums(self):verify_sources()
 def test_identifiers_unique(self):self.assertEqual(len(self.rows),len(self.by))
 def test_quotes_present_in_archived_excerpts(self):
  manifest={r['id']:r for r in json.loads((ROOT/'data/source_manifest.json').read_text())}
  for r in self.rows:
   with self.subTest(unit=r['id']):self.assertIn(r['text'],(ROOT/manifest[r['witness']]['selected_file']).read_text())
 def test_durations_independently_read_from_text(self):
  anchors={'1795t-a4':('Eighteen Months',18),'1796t-a4':('eighteen months',18),'1796t-a5':('one year',12),'1797t-a4':('eighteen months',18),'1797t-a7':('one year',12),'1805t-a7':('two years',24),'1815t-a8':('six months',6),'1816t-a8':('six months',6),'1816e-a8':('six months',6)}
  for uid,(phrase,n) in anchors.items():
   with self.subTest(unit=uid):self.assertIn(phrase,self.by[uid]['text']);self.assertEqual(n,self.by[uid]['duration'])
 def test_unstated_not_zero(self):
  r=self.by['1795t-a8'];self.assertIsNone(r['duration']);self.assertIn('untill such time',r['text'])
 def test_tunis_not_blanket_waiver(self):
  r=self.by['1797t-a4'];self.assertEqual(r['mechanism'],'conge_transition');self.assertIn('respect shall be paid to the said passports',r['text']);self.assertIn('without requiring the conge',r['text'])
 def test_1816_witnesses_not_merged(self):
  eng=self.by['1816t-a8']['text'];tur=self.by['1816e-a8']['text']
  self.assertIn('Certificates of condemnation, and bill of sale',eng);self.assertIn('Consul or the bill of sale',tur);self.assertIn('on their way home',tur)
 def test_scope_owned_vessels(self):
  self.assertIn('Absolutely the Property of Citizens',self.by['1795t-a4']['text']);self.assertIn('crew not being under his rule',self.by['1795e-a4']['text'])
 def test_pursuit_delays_not_months(self):
  for r in self.rows:
   if r['mechanism']=='pursuit_delay':self.assertEqual(r['unit'],'hours');self.assertEqual(r['duration'],24);self.assertIn('twenty four hours',r['text'])
 def test_table_preserves_both_transitions(self):
  table=summarize(self.rows);self.assertEqual([r['purchase_months'] for r in table],[None,12,12,24,6,6]);self.assertEqual(table[2]['transition_type'],'conge_transition');self.assertEqual(table[3]['transition_months'],0);self.assertEqual(table[3]['purchase_months'],24)
 def test_translation_not_counted_as_new_treaty(self):
  self.assertEqual(len({r['year'] for r in self.rows}),7);self.assertEqual(len({r['witness'] for r in self.rows}),10)
if __name__=='__main__':unittest.main(verbosity=2)
