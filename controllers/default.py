# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- sales page ----
def sales():
    response.flash = T('sales page')
    grid = SQLFORM.smartgrid(db.trnmas)
    return dict(grid = grid)

# ---- products page ----
def products():
    <div class="btn-group">
        <a class="tip btn btn-primary btn-xs" title="" href="#" data-original-title="Edit Product"><i class="fa fa-edit"></i></a>
        <a class="tip btn btn-danger btn-xs" title="" href="#" onclick="return confirm('You are going to remove this product. Press OK to proceed and Cancel to Go Back')" data-original-title="Delete Product"><i class="fa fa-trash-o"></i></a>
    </div>
    response.flash = T('products page')
    grid = SQLFORM.smartgrid(db.itemmas)
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
