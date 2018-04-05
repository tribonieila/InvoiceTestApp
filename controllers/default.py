# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
# https://sim.tecdiary.com
# sudo service postgresql restart
# sheepItForm
# c:\python27\python c:\fleetmgt\web_fleet.py -a admin -i 192.7.1.249 -p 80
# ---- index page ----
import locale
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
def index():

    return dict()

# ---- products page ----
def products():
    row = []
    head = THEAD(TR(TH('#'),TH('Reference No'),TH('Description'),TH('Price'),TH()))
    for q in db().select(db.itemmas.ALL):
        view = A('view', _class='btn btn-primary btn-sm', _href=URL('report', 'viewproduct', args=q.id))
        edit = A('edit', _class='btn btn-success btn-sm', _href=URL('default', 'editproduct', args=q.id))
        dele = A('delete', _class='btn btn-danger btn-sm', _onclick='jQuery(this).parent("div").parent("td").parent("tr").fadeOut()', callback=URL('delproduct',args = q.id))
        btn = DIV(view, edit, dele, _class='btn-group', _role='group')
        row.append(TR(TD(),TD(q.Ref_No),TD(q.Descrip),TD(q.Price_Wsch),TD(btn)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover', _id='table')
    return dict(table = table)
# ---- delsale page ----
def delsale():
    db(db.trnvou.id == request.args(0)).delete()

# ---- sales page ----
def sales():
    row = []
    delete_confirmation = T('Are you sure you want to delete this record?')

    head = THEAD(TR(TH('#'),TH('Date'),TH('Vouno'),TH('Customer'),TH('Total'),TH('Paid'),TH('Balance'),TH('Status'),TH()))
    for q in db().select(db.trnvou.ALL):
        view = A('view', _class='btn btn-primary btn-sm', _href=URL('report', 'printsale', args=q.id))
        edit = A('edit', _class='btn btn-success btn-sm', _href=URL('default', 'editsale', args=q.id))
        dele = A('delete', _class='btn btn-danger btn-sm', _onclick='jQuery(this).parent("div").parent("td").parent("tr").fadeOut()', callback=URL('delsale',args = q.id))
        # <a href="#" data-toggle="popover" title="Popover Header" data-content="Some content inside the popover">Toggle popover</a>
        # dele = A('delete', _class='btn btn-danger btn-sm', callback=URL(args=q.id), #_href=URL('default','delsale', args=q.id)
        # **{'_data-toggle':'confirmation', '_data-id':(q.id)})
        # dele = A(SPAN(_class = 'fa fa-trash bigger-110 blue'), _name='btndel',_title="Delete",
        # callback=URL( args=n.id),_class='delete', data=dict(w2p_disable_with="*"),
        # **{'_data-id':(n.id), '_data-in':(n.invoice_number)})
        btn = DIV(view, edit, dele, _class='btn-group', _role='group')
        row.append(TR(TD(),TD(q.Dte),TD(q.Vouno),TD(q.Client),TD((q.Totamount), _align='right'),TD(),TD(),TD(),TD(btn)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover', _id='table')
    return dict(table = table)
# ---- add sale page ----
def addsale():
    form = FORM(DIV(LABEL('Invoice No: ',_class='col-sm-2'), INPUT(_type='text', _id='inv',_name='inv', _placeholder='Invoice No', requires = IS_NOT_IN_DB(db, 'trnvou.Vouno') ,_class='form-control')),
        DIV(_class='space space-8'),
        DIV(LABEL('Customer Name: ',_class='col-sm-2'),INPUT(_type='text', _id='customer',_name='customer', _placeholder='Customer', _class='form-control')),DIV(_class='space space-8'),
        TABLE(THEAD(TR(TH('#'),TH('Reference No'),TH('Quantity'),TH())),
        TBODY(TR(TD(SPAN(_id='sheepItForm_label')),
            TD(INPUT(_class='form-control', _id='refno', _name='refno', _widget = SQLFORM.widgets.autocomplete(request, db.itemmas.Ref_No,
                id_field = db.itemmas.id, limitby = (0,10), min_length = 2))),
            TD(INPUT(_class='form-control', _id='qty',_type='text', _name='qty')),
            TD(INPUT(_id='counter',_type='hidden', _name='counter'),A(SPAN(_class='ace-icon fa fa-times-circle bigger-120 '),'x',_class='btn btn-danger btn-xs', _id='sheepItForm_remove_current', _name = 'sheepItForm_remove_current')),_id="sheepItForm_template"),
            TR(TD('No Entry Field',_colspan='6'),_id="sheepItForm_noforms_template"),_id="sheepItForm"),
        TFOOT(TR(TD(DIV(
            DIV(A(SPAN(' Add',_class='ace-icon fa fa-plus-circle bigger-120'),_class='btn btn-success btn-xs'), _id='sheepItForm_add'),
            DIV(A(SPAN(' Remove',_class='ace-icon fa fa-minus-circle bigger-120'),_class='btn btn-danger btn-xs'),_id='sheepItForm_remove_last'),
            DIV(A(SPAN(' Remove All', _class='ace-icon fa fa-times-circle bigger-120'),_class='btn btn-danger btn-xs'),_id='sheepItForm_remove_all'),_id='sheepItForm_controls'),_colspan='6'))),_class='table table-striped'),
    DIV(_class='space space-8'),
    INPUT(_type='submit', _value='submit', _class='btn btn-primary'))
    if form.process().accepted:
        db.trnvou.insert(Location = 1,Type = 3, Dte = request.now, Vouno = form.vars.inv, Client = form.vars.customer)
        _range = xrange(len(request.vars['counter']))
        # if len(_range) <= 1:
        #     db.trnvou.insert(Location = 1,Type = 3, Dte = request.now, Vouno = form.vars.inv, Client = form.vars.customer)
        #     db.trnmas.insert(Location = 1, Type = 3, Dte=request.now, Vouno=form.vars.inv, Ref_No=form.vars.refno, Qty=form.vars.qty)
        # else:
        for i in _range:
            db.trnmas.insert(Location = 1, Type = 3, Dte=request.now, Vouno=form.vars.inv, Ref_No=form.vars['refno'][i], Qty=form.vars['qty'][i])
    return dict(form = form)
def test():
    return locals()
def new_post():
    form = SQLFORM(db.post)
    if form.accepts(request, formname=None):
        return DIV("Message posted")
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])
    return locals()

def dicts_to_TABLE(content):
        return TABLE(
            THEAD(TR(*[TD(B(k)) for k in content[0].keys()])),
            *[TR(*[TD(v) for k, v in row.iteritems()]) for row in content]
        )

def echo():
    row = []
    to = 0;
    query = db(db.itemmas.Ref_No == request.vars.name).select(db.itemmas.ALL)
    for q in query:
        to = request.vars.qty 
        row.append(TR(TD(q.Ref_No),TD(q.Descrip),TD(q.Price_Wsch),TD(request.vars.qty),TD(to)))
    body = TBODY(*row)
    return body

def itms():
    row = []
    x = 1
    head = THEAD(TR(TD('#'),TD('Description')))
    query = db(db.itemmas.Ref_No == request.vars.refno).select(db.itemmas.ALL)
    for q in query:
        sub_total = q.Price_Wsch * x
        row.append(TR(TD(q.Ref_No),TD(q.Descrip),TD(q.Price_Wsch)))
    body = TBODY(*row)
    return body

def addsale2():
    refno = db().select(db.itemmas.Ref_No)
    form = SQLFORM.factory(
        Field('counter', 'integer'),
        Field('dte', 'date', default = request.now, label='Date'),
        Field('Invoi', 'integer', label = 'Invoice No.'),
        Field('Customer', 'string'),
        Field('Ref_No', widget = SQLFORM.widgets.autocomplete(request, db.itemmas.Ref_No,  id_field=db.itemmas.id, limitby=(0,10), min_length=2)),
        Field('qty', 'integer'))
    if form.process().accepted:
        response.flash = 'hello'
        # db.trnvou.insert(Location = 1,Type = 3, Dte = request.now, Vouno = form.vars.Invoi, Client = form.vars.Customer)
        # _range = xrange(len(request.vars['counter']))
        # for i in _range:
        #     db.trnmas.insert(Location = 1, Type = 3, Dte=request.now, Vouno=form.vars.Invoi, Ref_No=form.vars['Ref_No'][i], Qty=form.vars['qty'][i])
    return dict(form = form)

# ---- add sale page ----
def editsale():
    _id = db.trnvou(request.args(0)) #or redirect(URL('error'))
    form = SQLFORM(db.trnvou, _id, showid = False, fields = ['Dte', 'Vouno','Client'])
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form = form)


# ---- delroduct page ----
def delproduct():
    db(db.itemmas.id == request.args(0)).delete()

# ---- addproduct page ----
def addproduct():
    form = SQLFORM.factory(
        Field('ref_no','string', requires = IS_NOT_IN_DB(db, 'itemmas.Ref_No')),
        Field('description', 'string'),
        Field('price', 'decimal'))
    if form.process().accepted:
        db.itemmas.insert(Ref_No = form.vars.ref_no, Descrip = form.vars.description, Price_Wsch = form.vars.price)
    return dict(form = form)

# ---- editproduct page ----
def editproduct():
    form = SQLFORM(db.itemmas, request.args(0), showid = False, fields = ['Ref_No', 'Descrip','Price_Wsch'])
    if form.process().accepted:
        response.flash = "record updated"
        db.itemmas.insert(Ref_No = form.vars.ref_no, Descrip = form.vars.description, Price_Wsch = form.vars.price)
    return dict(form = form)

# ---- customers page ----
def customers():
    row = []
    head = THEAD(TR(TH('Acct'),TH('Group'),TH('BS Code'),TH('BS Code'),TH('Name')))
    for q in db().select(db.acctmas.ALL):
        row.append(TR(TD(q.Acct_Code),TD(q.Groupname),TD(q.Bs_Code),TD(q.Bs_Code1),TD(q.Name)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    return dict(table = table)

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

    # forms = FORM(DIV(LABEL('Paid By: ',_class='col-sm-2'),SELECT('Cash','Credit','Fuel Card', _type='text', _id='paid_by', _name='paid_by',_placeholder='Paid By' ,_class='col-sx-10')),
    #     DIV(_class='space space-8'),
    #     DIV(LABEL('Station: ',_class='col-sm-2'),INPUT(_type='text', _id='station',_name='station', _placeholder='Station')),DIV(_class='space space-8'),
    #     TABLE(THEAD(TR(TH('#'),TH('Date'),TH('Reg.No.'),TH('Amount'),TH('Remarks'),TH())),
    #     TBODY(TR(TD(SPAN(_id='sheepItForm_label')),
    #         TD(INPUT(_class='date col-xs-10 col-sm-10', _value=request.now.date(), _id='date_expense', _name="date_expense")),
    #         TD(SELECT(_class='col-xs-10 col-sm-10', _id='reg_no_id', _name='reg_no_id')),
    #         TD(INPUT(_class='col-xs-10 col-sm-10', _id='amount', _value=0, _name='amount')),
    #         TD(INPUT(_class='col-xs-10 col-sm-15', _id='remarks',_type='text', _name='remarks')),
    #         TD(INPUT(_id='counter',_type='hidden', _name='counter')),
    #         TD(A(SPAN(_class='ace-icon fa fa-times-circle bigger-120 '),_class='btn btn-danger btn-xs', _id='sheepItForm_remove_current', _name = 'sheepItForm_remove_current')),_id="sheepItForm_template"),TR(TD('No Entry Field',_colspan='6'),_id="sheepItForm_noforms_template"),_id="sheepItForm"),
    #     TFOOT(TR(TD(DIV(
    #         DIV(A(SPAN(' Add',_class='ace-icon fa fa-plus-circle bigger-120'),_class='btn btn-success btn-xs'), _id='sheepItForm_add'),
    #         DIV(A(SPAN(' Remove',_class='ace-icon fa fa-minus-circle bigger-120'),_class='btn btn-danger btn-xs'),_id='sheepItForm_remove_last'),
    #         DIV(A(SPAN(' Remove All', _class='ace-icon fa fa-times-circle bigger-120'),_class='btn btn-danger btn-xs'),_id='sheepItForm_remove_all'),_id='sheepItForm_controls'),_colspan='6'))),_class='table table-striped'),
    # DIV(_class='space space-8'),
    # INPUT(_type='submit', _value='submit', _class='btn btn-primary'))
