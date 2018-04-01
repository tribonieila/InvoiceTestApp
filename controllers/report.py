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

tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.8*inch, leftMargin=30, rightMargin=30)#, showBoundary=1)


###########

def _title(title):
    title = 'Title'
    return str(title)

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header 'Vehicle Summary Report'
    header = Table([['',I],[darwish,''],['Fleet Summary Report','']], colWidths=[None,90])
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
                # db.trnmas.insert(Location = 1, Type = 3, Dte=request.now, Vouno=form.vars.inv, Ref_No=form.vars['refno'][i], Qty=form.vars['qty'][i])
                # db.itemmas.Ref_No
                # db.itemmas.Descrip
                # db.itemmas.Price_Wsch
def salereport():
    row = []
    ctr = 0
    for c in db(db.trnvou.id == request.args(0)).select(db.trnvou.ALL):
        data = [['Date: ', c.Dte, '02', '03', '04'],
            ['Invoice No.:', c.Vouno, '12', '13', '14'],
            ['Customer: ', c.Client, '22', 'Bottom\nRight', '']]
        t = Table(data,style=[('GRID',(0,0),(-1,-1),0.5,colors.grey),
            ('BACKGROUND',(0,0),(1,1),colors.palegreen),
            ('BACKGROUND',(-2,-2),(-1,-1), colors.pink)])

        tran = [['#','Reference No.','Description', 'Quantity', 'Price', 'Total']]
        for t in db(db.trnmas.Vouno == c.Vouno).select(db.trnmas.ALL, db.itemmas.ALL, left=db.trnmas.on(db.itemmas.Ref_No == db.trnmas.Ref_No)):
            ctr += 1
            tran.append([ctr, t.itemmas.Ref_No, t.itemmas.Descrip, t.tranmas.Qty, t.itemmas.Price_Wsch, 'total'])

    tran_tbl = Table(tran, colWidths=[25,25,25,25,25,25])
    fle

    row.append(t)
    doc.build(row)#, onFirstPage=_header_footer, onLaterPages=_header_footer)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data
