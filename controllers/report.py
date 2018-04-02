from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas
logo_path = request.folder + 'static/images/invoice.jpg'
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
I = Image(logo_path)
I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
I.drawWidth = 1.25*inch
I.hAlign='RIGHT'

tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.8*inch, leftMargin=30, rightMargin=30)#, showBoundary=1)
TestApp = Paragraph('''<font size=14><b>Invoice TestApp </b><font color="gray">|</font></font> <font size=9 color="gray"> A Cloud Invoice System</font>''',styles["BodyText"])


###########

def _title(title):
    title = 'Title'
    return str(title)

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Vehicle Summary Report'
    header = Table([['',I],[TestApp,''],['Invoice TestApp','']], colWidths=[None,90])
    header.setStyle(TableStyle([('SPAN',(1,0),(1,1)),('SPAN',(0,2),(1,2)),('ALIGN',(0,0),(0,0),'RIGHT'),('LINEBELOW',(0,1),(1, 1),0.25, colors.gray),('BOTTOMPADDING',(0,0),(0, 1),10),('TOPPADDING',(0,2),(1,2),6)]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .7 * inch)


    # Footer
    import time
    from datetime import date
    today = date.today()
    footer = Table([[today.strftime("%A %d. %B %Y")]], colWidths=[535])
    footer.setStyle(TableStyle([('TEXTCOLOR',(0,0),(0,0), colors.gray),('FONTSIZE',(0,0),(0,0),8),('ALIGN',(0,0),(0,0),'RIGHT'),('LINEABOVE',(0,0),(0,0),0.25, colors.gray)]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .7 * inch)

    # Release the canvas
    canvas.restoreState()

###########
            # db.trnvou.insert(Location = 1,Type = 3, Dte = request.now, Vouno = form.vars.inv, Client = form.vars.customer)
            # db.trnmas.insert(Location = 1, Type = 3, Dte=request.now, Vouno=form.vars.inv, Ref_No=form.vars.refno, Qty=form.vars.qty)
            # db.itemmas.Ref_No
            # db.itemmas.Descrip
            # db.itemmas.Price_Rtch
def printsale():
    ctr = 0
    grand_total = 0
    row = []
    for t in db(db.trnvou.id == request.args(0)).select(db.trnvou.ALL):
        data = [['Date: ', t.Dte],
        ['Invoice No.:', t.Vouno],
        ['Customer: ', t.Client]]
        tran = [['#','Reference No', 'Description','Price','Quantity','Total']]
        for y in db(db.trnmas.Vouno == t.Vouno).select(db.trnmas.ALL, db.itemmas.ALL, left=db.trnmas.on(db.trnmas.Ref_No == db.itemmas.Ref_No)):
            ctr += 1
            total = y.itemmas.Price_Rtch * y.trnmas.Qty
            grand_total += total
            tran.append([ctr,y.itemmas.Ref_No,y.itemmas.Descrip,y.itemmas.Price_Rtch,y.trnmas.Qty,total])
    tran.append(['','','','','GRAND TOTAL: ', grand_total])
    tran_table =Table(tran, colWidths=[25,70,200,75,75,75])
    tran_table.setStyle(TableStyle([('FONTSIZE',(0,0),(0,0),9)]))
    trn_table = Table(data,colWidths=[100,200],hAlign='LEFT')

    row.append(trn_table)
    row.append(tran_table)
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def viewproduct():
    ctr = 0
    row = []
    for t in db(db.itemmas.id == request.args(0)).select(db.itemmas.ALL):
        data = [['Reference No: ', t.Ref_No],
        ['Description:', t.Descrip],
        ['Price: ', t.Price_Wsch]]
    trn_table = Table(data,colWidths=[100,200],hAlign='LEFT')
    row.append(trn_table)
    doc.build(row, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data
