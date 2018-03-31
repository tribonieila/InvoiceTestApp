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

# ---- sales page ----
def sales():
    row = []
    head = THEAD(TR(TD('Date'),TD('Vouno'),TD('Customer'),TD('Total'),TD('Paid'),TD('Balance'),TD('Status'),TD('Actions')))
    for q in db().select(db.trnvou.ALL):
        #A('Fuel', _href=URL('default', 'Fuel', args=n.vehicle.id))
        view = BUTTON('view', _type='button', _class='btn btn-primary btn-sm')
        edit = A('edit', _class='btn btn-success btn-sm', _href=URL('default', 'editsale', args=q.id))
        #edit = BUTTON('edit', _type='button', _class='btn btn-success btn-sm', _href="URL("editsale", args=q.trnvou.id))
        dele = BUTTON('delete', _type='button', _class='btn btn-danger btn-sm')
        btn = DIV(view, edit, dele, _class='btn-group', _role='group')

        row.append(TR(TD(q.Dte),TD(q.Vouno),TD(q.Client),TD(locale.format('%.2f',q.Totamount, grouping = True), _align='right'),TD(),TD(),TD(),TD(btn)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    return dict(table = table)

# ---- add sale page ----
def addsale():
    refno = db().select(db.itemmas.Ref_No)
    form = SQLFORM.factory(
        Field('counter', 'integer'),
        Field('dte', 'date', default = request.now, label='Date'),
        Field('Invoi', 'integer', label = 'Invoice No.'),
        Field('Customer', 'string'),
        Field('Ref_No', widget = SQLFORM.widgets.autocomplete(request, db.itemmas.Ref_No,  id_field=db.itemmas.id, limitby=(0,10), min_length=2)),
        Field('qty', 'integer'))
    if form.accepts(request):
        # _range = xrange(len(request.vars['counter']))
        ref = db(db.itemmas.Ref_No == form.vars.Ref_No).select(db.itemmas.Descrip).first()
        print ref
        # if len(_range) <= 1:
        #     print "1 range"
        # else:
        #     for v in _range:
        #         print form.bars['RefNo'][v]
    return dict(form = form, refno = refno)

# ---- add sale page ----
def editsale():
    _id = db.trnvou(request.args(0)) #or redirect(URL('error'))
    form = SQLFORM(db.trnvou, _id, showid = False)
    return dict(form = form)

# ---- products page ----
def products():
    row = []
    head = THEAD(TR(TH('Ref_No'),TH('Ref_No2'),TH('Ref_No3'),TH('Description'),TH('Brand Line'),TH()))
    for q in db().select(db.itemmas.ALL):
        row.append(TR(TD(q.Ref_No),TD(q.Ref_No2),TD(q.Ref_No3),TD(q.Descrip),TD(q.Brand_Line),TD('view, edit, delete')))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table table-striped table-bordered table-hover')
    return dict(table = table)

# ---- products page ----
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
