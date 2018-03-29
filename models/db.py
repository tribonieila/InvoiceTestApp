# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configure.get('heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       ', 'date'),','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
#
db = DAL('postgres://root:admin@localhost/TestApp')

db.define_table('itemmas',
    Field('Ref_No', 'string', length = 15),
    Field('Ref_No2', 'string', length = 15),
    Field('Ref_No3', 'string', length = 15),
    Field('Descrip', 'string', length = 35),
    Field('Brand_Line', 'string', length = 4),
    Field('Brand_Line2', 'string', length = 10),
    Field('Supp_Code', 'string', length = 8),
    Field('Group', 'string', length = 25),
    Field('Maingroup', 'string', length = 30),
    Field('Mr_Cost', 'decimal(10,2)'),
    Field('Ave_Cost', 'decimal(10,2)'),
    Field('Mr_Lndcost', 'decimal(10,2)', ),
    Field('Currency', 'string', length = 5),
    Field('Units', 'string', length = 10),
    Field('Units2', 'integer'),
    Field('Supp_Unit', 'integer'),
    Field('Stk_Loc', 'integer'),
    Field('Op_Avcost', 'decimal(10,2)'),
    Field('Mrk_Cost', 'decimal(10,2)'),
    Field('Batprom', 'decimal(10,2)'),
    Field('Promqty', 'decimal(10,2)'),
    Field('Tot_Damqty', 'decimal(10,2)'),
    Field('Last_Recdt', 'date'),
    Field('Last_Issdt', 'date'),
    Field('Qty_Order', 'decimal(10,2)'),
    Field('Expectdte', 'date'),
    Field('Price_Wsch', 'decimal(10,2)'),
    Field('Price_Rtch', 'decimal(10,2)'),
    Field('Price_Vnch', 'decimal(10,2)'),
    Field('Price_Unit', 'decimal(10,2)'),
    Field('Opstkloc', 'integer'),
    Field('Opendte', 'date'),
    Field('Purccode', 'string', length = 8),
    Field('Salecode', 'string', length = 8),
    Field('Ibcode', 'string', length = 8),
    Field('Batcst', 'decimal(10,2)'),
    Field('Batlndcst', 'decimal(10,2)'),
    Field('Batqty', 'integer'),
    Field('Batdte', 'date'),
    Field('Batord', 'string', length = 8),
    Field('Lat_Price', 'decimal(10,2)'),
    Field('Csocode', 'string', length = 8),
    Field('Lst_Invno', 'string', length = 15),
    Field('Lst_Grvno', 'string', length = 15),
    Field('Cnt_Orign', 'string', length = 30),
    Field('Discount', 'decimal(10,2)'),
    Field('Off_Price', 'decimal(10,2)'),
    Field('Bar_Code', 'string', length = 20),
    Field('Ib', 'integer'))

db.define_table('acctmas',
    Field('Acct_Code', 'string', length = 8),
    Field('Groupname', 'string', length = 20),
    Field('Bs_Code', 'string', length =	15),
    Field('Bs_Code1', 'string', length = 15),
    Field('Name','string', length =	45),
    Field('Addrs1',	'string', length = 35),
    Field('Addrs2', 'string', length = 35),
    Field('Addrs3',	'string', length = 35),
    Field('Addrs4', 'string', length = 35),
    Field('City_Town', 'string', length = 35),
    Field('Country', 'string', length =	35),
    Field('Email1', 'string', length = 35),
    Field('Email2',	'string', length = 35),
    Field('Web1', 'string', length = 35),
    Field('Zip_Code', 'string', length = 12),
    Field('Tel_No1', 'string', length = 16),
    Field('Tel_No2', 'string', length = 16),
    Field('Acts_Telno', 'string', length = 12),
    Field('Contact1', 'string',	length = 20),
    Field('Grade', 'string', length = 10),
    Field('Benefe', 'string', length = 45),
    Field('Bankers', 'string', length = 45),
    Field('Bad1', 'string',	length = 45),
    Field('City', 'string',	length = 45),
    Field('Sort_Code', 'string', length = 25),
    Field('Bnk_Code', 'string', length = 25),
    Field('Currency', 'string',	length = 20),
    Field('Contact2', 'string',	length = 20),
    Field('Acc_Nbr', 'string',	length = 45),
    Field('Crt_Bal1', 'integer'),
    Field('Opn_Bal1', 'decimal(10,2)'),
    Field('Opn_Dte', 'date'),
    Field('Last_Updte', 'date'),
    Field('Status', 'string', length = 10),
    Field('Crt_Limit', 'integer'),
    Field('Ac_Op_Dte', 'date'),
    Field('Agr_Dte', 'date'),
    Field('Sp_Name', 'string', length = 45),
    Field('Id_Date', 'date'),
    Field('Paymt_Trms', 'string', length = 45),
    Field('Trms_Dep1', 'integer'),
    Field('Cat_Dep1', 'string',	length = 6),
    Field('Agrement', 'boolean'),
    Field('Agr_Date', 'date'),
    Field('Sponsor', 'string', length = 30),
    Field('Sp_Idno', 'string', length = 20),
    Field('Id_Dte', 'date'),
    Field('Id_Expdt', 'date'),
    Field('Remarks', 'string', length = 35),
    Field('Collector', 'string', length = 35),
    Field('Budget',	'decimal(10,2)'),
    Field('Letterctr', 'integer'),
    Field('Lettersw', 'integer'),
    Field('Active',	'boolean'),
    Field('Group1',	'string', length = 15),
    Field('Tgrade',	'string', length = 1),
    Field('Acc_Name', 'string',	length = 25),
    Field('Gm_Name', 'string', length = 25),
    Field('Gm_Tel',	'string', length = 10),
    Field('Pur_Name', 'string',	length = 25),
    Field('Pur_Tel', 'string', length = 10),
    Field('Mvno', 'integer'),
    Field('Cr_L1', 'integer'),
    Field('Cr_Days', 'integer'),
    Field('Mflag', 'boolean'),
    Field('Trn_Type', 'integer'),
    Field('Group', 'string', length = 15))

db.define_table('brandmas',
    Field('Supp_Code', 'string', length = 8),
    Field('Supp_Name', 'string', length = 35),
    Field('Brand_Code', 'string', length = 4),
    Field('Brand_Cod2', 'string', length = 10),
    Field('Brand_Line', 'string', length =	30),
    Field( 'Lines', 'string', length =	30),
    Field( 'Brandgroup', 'string', length =	30),
    Field( 'Group', 'string', length = 25),
    Field( 'Maingroup', 'string', length = 30),
    Field( 'Ib', 'integer'),
    Field( 'Tgt_Qtr1', 'integer'),
    Field( 'Tgt_Qtr2', 'integer'),
    Field( 'Tgt_Qtr3', 'integer'),
    Field( 'Tgt_Qtr4', 'integer'),
    Field( 'Trg_Tot', 'integer'),
    Field( 'Sup_Trg', 'integer'),
    Field( 'Rgroup', 'string', length =	25),
    Field( 'Tgroup', 'string', length =	25),
    Field( 'Rankgrp', 'string', length = 25),
    Field( 'Lineflag', 'boolean'),
    Field( 'Product', 'string', length = 45),
    Field( 'Grouplines', 'string', length =	60),
    Field( 'Br_Lines', 'string', length = 60),
    Field( 'Br_Class', 'string', length = 60),
    Field( 'Itsub_Type', 'string', length =	60))

db.define_table('trnmas',
    Field('Location', 'integer'),
    Field('Type', 'integer'),
    Field('Dte', 'date'),
    Field('Vouno', 'integer'),
    Field('Ref_No', 'string', length = 15),
    Field('Price_Cost', 'decimal(10,2)'),
    Field('Qty', 'integer'),
    Field('Units', 'integer'),
    Field('Catagory', 'string', length = 1),
    Field('Dflag', 'string', length = 1),
    Field('Av_Cost', 'decimal(10,2)'),
    Field('Ws_Cost', 'decimal(10,2)'),
    Field('Rt_Cost', 'decimal(10,2)'),
    Field('Sale_Cost', 'decimal(10,2)'),
    Field('Sup_Cus', 'string', length = 8),
    Field('Supp_Code', 'string', length = 8),
    Field('Brand_Code', 'string', length = 4),
    Field('Ref_No2', 'string', length = 15),
    Field('Entrydte', 'date'),
    Field('Saleman', 'string', length =	10))

db.define_table('trnvou',
    Field('Location', 'integer'),
    Field('Type', 'integer'),
    Field('Dte', 'date'),
    Field('Vouno', 'integer'),
    Field('Supp_Custm', 'string', length = 8),
    Field('Totamount', 'decimal(10,2)'),
    Field('Discount', 'integer'),
    Field('Disc_Added', 'decimal(10,2)'),
    Field('Other_Chrg', 'integer'),
    Field('Order_Ref', 'integer'),
    Field('Lc_No', 'integer'),
    Field('Invno', 'string', length = 10),
    Field('Exch_Rate', 'integer'),
    Field('Lnd_Rate', 'integer'),
    Field('Creditcode', 'integer'),
    Field('Sales_Man', 'string', length = 10),
    Field('Spare', 'string', length = 10),
    Field('Stvdestin', 'integer'),
    Field('Ordtype', 'integer'),
    Field('Order_Ref2', 'string', length = 8),
    Field('Entrydte', 'date'),
    Field('Client', 'string', length = 30),
    Field('Card', 'string', length = 35),
    Field('Order_Ref3', 'string', length = 8),
    Field('Address', 'string', length = 35),
    Field('Tel', 'string', length = 15))
