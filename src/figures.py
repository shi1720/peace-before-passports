"""Generate figures directly from the comparison and a cited public-domain scan."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
C='#234c65';ACC='#ae623b';GRAY='#59636b'

def windows():
 from analyze import load,summarize
 rows=summarize(load());labels=['Algiers\n1795','Tripoli\n1796','Tunis\n1797/99','Tripoli\n1805','Algiers\n1815','Algiers\n1816']
 fig,axs=plt.subplots(2,1,figsize=(8.1,5.5),gridspec_kw={'height_ratios':[1,1.6]})
 ax=axs[0];ax.set_xlim(-.6,5.6);ax.set_ylim(0,1);ax.axis('off');ax.text(-.55,.95,'A  General documentary instruction',weight='bold',color=C)
 for i,r in enumerate(rows):
  text='18 months\ninitial supply' if r['transition_type']=='initial_transition' else '18 months\nconge/testa' if r['transition_type']=='conge_transition' else 'Immediate\nissuance'
  ax.text(i,.43,text,ha='center',va='center',bbox=dict(boxstyle='round,pad=.55',facecolor='#eef2f4',edgecolor='none'),fontsize=9,color=C)
 ax=axs[1];ax.set_xlim(-.6,5.6);ax.set_title('B  Temporary documentation for purchased prizes',loc='left',weight='bold',color=C,pad=15)
 for i,r in enumerate(rows):
  if r['purchase_months'] is None:
   ax.text(i,12,'Numerical limit\nnot stated',ha='center',va='center',fontsize=8,color=GRAY)
  else:
   ax.bar(i,r['purchase_months'],width=.5,color=ACC);ax.text(i,r['purchase_months']+.5,str(r['purchase_months']),ha='center',fontsize=10)
 ax.set_ylabel('Months stated');ax.set_xticks(range(6),labels);ax.set_ylim(0,28);ax.set_yticks([0,6,12,18,24]);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 fig.tight_layout(h_pad=1.2)
 for ext in ['png','pdf','svg']:fig.savefig(ROOT/f'figures/figure1_windows.{ext}',dpi=240,bbox_inches='tight')
 plt.close(fig)

def mary():
 fig,ax=plt.subplots(figsize=(8.1,2.7));ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
 items=[('5 OCT','Arrival in Algiers','Register and sea letter;\nMediterranean pass absent.'),('6 OCT','Contested hearing','O’Brien advances substitute\npapers; Dey reserves decision.'),('8 OCT','Reported release','Dey treats vessel as prize,\nthen releases as a favor.'),('12 OCT','Dispatch and proposal','O’Brien reports defects and\nproposes overlapping passes.')]
 for i,(date,title,body) in enumerate(items):
  x=.01+i*.25
  ax.add_patch(FancyBboxPatch((x,.25),.225,.49,boxstyle='round,pad=.008',facecolor='#f0f3f5',edgecolor='#b4c2cc'))
  ax.text(x+.1125,.66,date,ha='center',weight='bold',color=ACC,fontsize=11)
  ax.text(x+.1125,.55,title,ha='center',weight='bold',fontsize=9,color=C)
  ax.text(x+.1125,.41,body,ha='center',va='center',fontsize=8,linespacing=1.8)
  if i<3:ax.annotate('',xy=(x+.249,.50),xytext=(x+.228,.50),arrowprops=dict(arrowstyle='->',color=C))
 ax.text(.5,.91,'The Mary episode, October 1798',ha='center',fontsize=14,color=C,weight='bold')
 ax.text(.5,.08,'Sequence reconstructed from one dispatch; boxes are equally spaced, not a time scale.',ha='center',fontsize=9,color=GRAY)
 fig.tight_layout()
 for ext in ['png','pdf','svg']:fig.savefig(ROOT/f'figures/figure2_mary.{ext}',dpi=240,bbox_inches='tight')
 plt.close(fig)

def material():
 import pymupdf
 src=pymupdf.open(ROOT/'sources/obrien_1798_p258-262.pdf');page=src[2]
 # Crop retains the paragraph about size, dampness and exact fit, plus the enclosed-specimen description.
 starts=page.search_for('I have examined fully');ends=page.search_for('As the french')
 top=197.3
 bottom=493.0
 clip=pymupdf.Rect(70,top,369,bottom)
 pix=page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=clip);pix.save(ROOT/'figures/figure3_material.png')
 print('Facsimile crop:',clip)

if __name__=='__main__':
 (ROOT/'figures').mkdir(exist_ok=True);windows();mary();material()
