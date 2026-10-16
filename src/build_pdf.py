"""Build the manuscript and the two venue-specific submission packets."""
from pathlib import Path
import re,json
from xml.sax.saxutils import escape
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image,Table,TableStyle,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import paper_content as p
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT.parent
FONTS=Path('/System/Library/Fonts/Supplemental')
for name,file in [('Serif','Times New Roman.ttf'),('SerifB','Times New Roman Bold.ttf'),('SerifI','Times New Roman Italic.ttf'),('SerifBI','Times New Roman Bold Italic.ttf'),('Sans','Arial.ttf'),('SansB','Arial Bold.ttf')]:
 if (FONTS/file).exists():pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))
 else:
  fallback={'Serif':'Times-Roman','SerifB':'Times-Bold','SerifI':'Times-Italic','SerifBI':'Times-BoldItalic','Sans':'Helvetica','SansB':'Helvetica-Bold'}
  pdfmetrics.registerFont(pdfmetrics.Font(name,fallback[name],'WinAnsiEncoding'))
pdfmetrics.registerFontFamily('Serif',normal='Serif',bold='SerifB',italic='SerifI',boldItalic='SerifBI')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansB',italic='Sans',boldItalic='SansB')
INK=colors.HexColor('#18252e');BLUE=colors.HexColor('#234c65');MUTED=colors.HexColor('#53616b')
W=612;H=792;M=57;CW=W-2*M
styles={
'body':ParagraphStyle('body',fontName='Serif',fontSize=11.3,leading=15.2,spaceAfter=8.5,alignment=TA_JUSTIFY,allowWidows=0,allowOrphans=0,textColor=INK),
'h':ParagraphStyle('h',fontName='SerifB',fontSize=13.4,leading=17.2,spaceBefore=14,spaceAfter=8,keepWithNext=True,textColor=INK),
'abs':ParagraphStyle('abs',fontName='Serif',fontSize=10.5,leading=13.8,spaceAfter=10,alignment=TA_JUSTIFY,textColor=INK),
'caption':ParagraphStyle('caption',fontName='Sans',fontSize=8.2,leading=11.2,spaceAfter=10,textColor=MUTED),
'cell':ParagraphStyle('cell',fontName='Serif',fontSize=9,leading=11.5,textColor=INK),
'headcell':ParagraphStyle('headcell',fontName='SansB',fontSize=8.3,leading=10.5,textColor=colors.white),
'note':ParagraphStyle('note',fontName='Serif',fontSize=9.2,leading=12,spaceAfter=7,textColor=INK),
'cv':ParagraphStyle('cv',fontName='Serif',fontSize=10.6,leading=14.2,spaceAfter=9,textColor=INK),
'packet':ParagraphStyle('packet',fontName='Serif',fontSize=11.5,leading=16,spaceAfter=12,textColor=INK),
'packet_h':ParagraphStyle('packet_h',fontName='SansB',fontSize=11.5,leading=16,spaceBefore=14,spaceAfter=7,keepWithNext=True,textColor=BLUE),
}
def P(text,style='body'):return Paragraph(text,styles[style])
def header_footer(label):
 def f(c,d):
  c.saveState();c.setStrokeColor(colors.HexColor('#c6cdd2'));c.setLineWidth(.4);c.line(M,H-38,W-M,H-38)
  c.setFont('Sans',7.5);c.setFillColor(MUTED);c.drawString(M,H-29,label);c.drawRightString(W-M,30,str(d.page));c.restoreState()
 return f

def doc(path,story,label):
 d=SimpleDocTemplate(str(path),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=53,bottomMargin=48,title=p.TITLE+': '+p.SUBTITLE,author='Shivam Gupta',subject='Early American foreign relations; SHAFR 2027')
 d.build(story,onFirstPage=header_footer(label),onLaterPages=header_footer(label))

def title(story,kind):
 story.append(P(kind.upper(),'caption'));story.append(Spacer(1,12))
 story.append(Paragraph(p.TITLE,ParagraphStyle('title',fontName='SerifB',fontSize=27,leading=31,textColor=INK,spaceAfter=7)))
 story.append(Paragraph(p.SUBTITLE,ParagraphStyle('sub',fontName='Serif',fontSize=16,leading=20,textColor=INK,spaceAfter=18)))
 story.append(P('Shivam Gupta<br/>Independent Researcher, Delhi, India<br/>shivam1720406@gmail.com','cv'))

def table(data,widths,caption):
 cells=[[P(str(x),'headcell' if i==0 else 'cell') for x in row] for i,row in enumerate(data)]
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f0f3f5'),colors.white]),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#bbc6ce'))]))
 return [t,Spacer(1,6),P(caption,'caption')]

def manuscript():
 story=[];title(story,'Research paper | 16 October 2026');story.append(P('<b>Abstract</b>','abs'));story.append(P(p.ABSTRACT,'abs'))
 story.append(P('<b>Keywords:</b> early American republic; Maghreb; maritime protection; Mediterranean passports; consular history; public history','caption'))
 story.append(P('<b>Research materials:</b> <link href="https://github.com/shi1720/peace-before-passports" color="#234c65">github.com/shi1720/peace-before-passports</link>','caption'))
 for kind,text in p.BLOCKS:
  if kind in ('p','h'):story.append(P(text,'body' if kind=='p' else 'h'))
  elif kind=='table':
   if text=='treaties':
    data=[['Instrument / main witness','Articles in register','Additional witness','Purpose in comparison'],['Morocco, 1786','4, 5, 11','None','Convoy, inspection, pursuit comparator'],['Algiers, 1795','4, 8, 12, 19','Kramers rendering of Turkish, same articles','Transition, purchase, personal proof'],['Tripoli, 1796','4, 5, 8','Snouck Hurgronje rendering of Arabic, arts. 4-5','Initial supply and purchased prizes'],['Tunis, 1797/1799','4, 5, 7','None','Conge/testa, convoy, local purchase papers'],['Tripoli, 1805','6, 7, 10','None','Immediate supply and two-year purchase term'],['Algiers, 1815','7, 8, 11','None','Immediate supply and six-month purchase term'],['Algiers, 1816','7, 8, 11','Kramers rendering of Turkish summary, arts. 7-8','Renewal and documentary divergence']]
    story.extend(table(data,[107,67,150,174],'<b>Table 1.</b> Source coverage. Thirty selected article-witness units, ten witnesses, seven instruments. Later translations are not counted as new treaties. Selection is mechanism-based, not a census of treaty provisions.'))
   else:
    data=[['Dimension','English original, art. 8','Kramers rendering of Turkish summary, art. 8'],['Vessel category','Purchased prize condemned by a contracting party or another nation','Ship bought by Americans from other persons'],['Accepted evidence','Certificates of condemnation AND bill of sale','Consular statement OR bill of sale'],['Voyage condition in clause','No explicit homeward condition','Encounter on the way home'],['Numerical allowance','Six months','Six months'],['Witness status','English original in Miller’s account','Accompanying Turkish translation or summary, rendered later into English']]
    story.extend(table(data,[103,196,199],'<b>Table 2.</b> Agreement on a number does not establish agreement on a protected object. Capitalized AND/OR highlight differences in the published English wording, not a formal legal judgment about the instruments’ authority. Source: Algiers 1816, art. 8, main text and Kramers witness (note 20).'))
  elif kind=='fig':
   if text=='windows':
    file='figure1_windows.png';width=CW;caption='<b>Figure 1.</b> Different transitions in the six principal treaty instruments. Panel A separates initial supply, the Tunis conge/testa provision, and immediate issuance. Panel B shows only numerical terms for purchased-prize documentation; a blank column with a text label denotes an unstated numerical limit. Terms are not enforcement outcomes. Sources: register, articles in Table 1.'
   elif text=='mary':
    file='figure2_mary.png';width=CW;caption='<b>Figure 2.</b> Reported sequence in the Mary dispute. Arrival at Algiers is not identified as the date of capture at sea. The subsequent timetable for replacing passes is O’Brien’s proposal, not demonstrated policy implementation. Source: dispatch of 12 October 1798, 258-262 (note 1).'
   else:
    file='figure3_material.png';width=345;caption='<b>Figure 3.</b> O’Brien’s discussion of passport dimensions, dampness, matching edges, and the enclosed specimens. Cropped reproduction of printed page 260, Knox, ed., Naval Documents, vol. 1 (1939). U.S. government publication. The reported one-tenth-inch discrepancy is not a new measurement. Source: note 15.'
   from PIL import Image as PILImage
   im=PILImage.open(ROOT/'figures'/file);height=width*im.height/im.width
   story.append(KeepTogether([Spacer(1,6),Image(str(ROOT/'figures'/file),width=width,height=height),Spacer(1,7),P(caption,'caption')]))
 story.append(PageBreak());story.append(P('Notes','h'))
 for i,n in enumerate(p.NOTES,1):story.append(P(f'<b>{i}.</b> '+n,'note'))
 story.append(P('Selected bibliography','h'))
 for b in p.BIBLIOGRAPHY:story.append(P(b,'note'))
 doc(OUT/'Peace_Before_Passports_Shivam_Gupta.pdf',story,'GUPTA  |  PEACE BEFORE PASSPORTS')
 (ROOT/'docs/manuscript.txt').write_text(p.TITLE+'\n'+p.SUBTITLE+'\nShivam Gupta\n\nAbstract\n'+p.ABSTRACT+'\n\n'+'\n\n'.join(re.sub('<[^>]+>','',v) if k in ('p','h') else '['+k+': '+v+']' for k,v in p.BLOCKS)+'\n\nNotes\n'+'\n\n'.join(f'{i}. '+re.sub('<[^>]+>','',n) for i,n in enumerate(p.NOTES,1)))

if __name__=='__main__':manuscript()
