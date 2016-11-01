#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template,session,url_for, g, redirect, Response
from jinja2 import Template

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

def getresult(names,cursor):
  rows=[]
  for result in cursor:
    for cell in result:
      rows.append(cell)
    names.append(rows)  # can also be accessed using result[0]
    rows=[]
  cursor.close()
  #context = dict(data = names)
  return names

def generatesql(gselect,gfrom,gwhere):
  gsql="SELECT "
  for i,tlist in enumerate(gselect):
    if i!=len(gselect)-1:
      gsql=gsql+tlist+","
    else:
      gsql=gsql+tlist
  gsql+=" FROM "
  for i,tlist in enumerate(gfrom):
    if i!=len(gfrom)-1:
      gsql=gsql+tlist+","
    else:
      gsql=gsql+tlist
  gsql+=" WHERE "
  ct=0
  for i,tlist in enumerate(gwhere):
    if i!=0 and tlist and ct!=0:
      gsql=gsql+" AND "+ tlist
      ct+=1
    elif tlist and i==0:
      gsql=gsql+tlist
      ct+=1
    elif tlist:
      gsql=gsql+tlist
      ct+=1
  return gsql
glbticket=[]
glbtransaction=[]
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#
DATABASEURI = "postgresql://rl2849:7410@w4111vm.eastus.cloudapp.azure.com/w4111"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#engine.execute("""select * from test;""");

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/',methods=["GET"])
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  
  # DEBUG: this is debugging code to see what request looks like
  print request.args

  #
  # example of a database query
  #
  global glbticket
  glbticket=[]


  #cursor = g.conn.execute("SELECT * FROM %s;" % name)
  # cursor = g.conn.execute("SELECT * FROM airline;")
  # names = []
  # rows=[]
  # for result in cursor:
  #   for cell in result:
  #     rows.append(cell)
  #   names.append(rows)  # can also be accessed using result[0]
  #   rows=[]
  # cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  

  
  # context = dict(data = names)
  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/search',methods=['POST'])
def search():

  name = request.form['Tname']
  cursor=g.conn.execute("SELECT * FROM %s;" % name)
  names=[]
  datas=getresult(names,cursor)
  context = dict(data = datas)
  return render_template("result.html",**context)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['Tname']
  #g.conn.execute("INSERT INTO test(name) VALUES ('happy');")
  g.conn.execute("INSERT INTO test(name) VALUES ('%s');" % name)
  cursor=g.conn.execute("SELECT * FROM test;")
  names = []
  datas = getresult(names,cursor)
  context = dict(data = datas)
  return render_template("result.html",**context)

#airline booking system funcs


#customer funcs
@app.route('/ticket', methods=['POST'])
def ticket():
  global glbticket
  account=request.form['account']
  #print account
  pfrom = request.form['from']
  pto = request.form['to']
  pwhen = request.form['when']
  target = ["flight_no",'depart','arrive',"date","depart_time","arrive_time","ticket_quantity","company"]
  rlist=["flight_info"]
  if not pfrom and not pto and not pwhen:
    qualification=[]
  else:
    qualification=["depart='%s'"%pfrom if pfrom else None, "arrive='%s'" %pto if pto else None, "date='%s'"% pwhen if pwhen else None]
  sql=generatesql(target,rlist,qualification)
  #print sql
  cursor=g.conn.execute(sql)
  #cursor = g.conn.execute("SELECT flight_no,depart,arrive,date,depart_time,arrive_time,ticket_quantity,company FROM flight_info where depart='%s' and arrive='%s' and date='%s';" % (pfrom,pto,pwhen))
  names=[]
  
  names.append(target)
  tickets = getresult(names,cursor)
  glbticket=tickets
  #print tickets
  context = dict(data = tickets,acct=account)
  #print session
  #print session['tickets']
  if account:
    session['account']=account
    return redirect('/usr')
    
    #return redirect('/usr')
    #return redirect(url_for('.usr',account=account))
  else:
    return render_template("result.html",**context)



#admin funcs
# def transaction():
#   pfrom = request.form['from']
#   pto = request.form['to']
#   pwhen = request.form['when']
#   target = ["flight_no",'depart','arrive',"date","depart_time","arrive_time","ticket_quantity","company"]
#   rlist=["flight_info"]
#   if not pfrom and not pto and not pwhen:
#     qualification=[]
#   else:
#     qualification=["depart='%s'"%pfrom if pfrom else None, "arrive='%s'" %pto if pto else None, "date='%s'"% pwhen if pwhen else None]
#   sql=generatesql(target,rlist,qualification)
#   print sql
#   cursor=g.conn.execute(sql)
#   #cursor = g.conn.execute("SELECT flight_no,depart,arrive,date,depart_time,arrive_time,ticket_quantity,company FROM flight_info where depart='%s' and arrive='%s' and date='%s';" % (pfrom,pto,pwhen))
#   names=[]
  
#   names.append(target)
#   context = getresult(names,cursor)
#   return render_template("result.html",**context)

#
##
#user website
@app.route('/usr', methods=['POST','GET'])
def usr():
  global glbticket
  global glbtransaction
  if request.form:
    account=request.form['account']
    session['account']=account
  else:
    
    
    #print tickets
    account=session['account']
    #tickets=session['tickets']
    #print session
  #print type(account)
  target = ["account","fname","lname","balance","tot_credit","card_level"]
  rlist=["customer_get"]
  qualification=["account='%s'"%account]
  sql=generatesql(target,rlist,qualification)
  cursor=g.conn.execute(sql)
  names=[]
  names.append(target)
  info = getresult(names,cursor)

  uname = g.conn.execute("SELECT fname,lname FROM customer_get where account='%s';" % account)
  fullname=[]
  for ns in uname:
    for cell in ns:
      fullname.append(cell)
  uname.close()
  #print fullname
  #context['usrname']=fullname
  context = dict(accountinfo = info,usrname=fullname,acct=account)
  if glbticket:
    print glbticket
    context['data']=glbticket
    glbticket=[]
  if glbtransaction:
    context['data']=glbtransaction
    glbtransaction=[]
  return render_template("login.html",**context)


@app.route('/transaction', methods=['POST'])
def transaction():
  global glbtransaction
  fdate = request.form['tdatefrom']
  tdate=request.form['tdateto']
  #print session['account']
  account=session['account']
  print account
  target = ["T.trans_no","C.account","T.trans_time","F.flight_no","T.ticket_quantity","T.class","T.amount"]
  target1 = ["trans_no","account","trans_time","flight","quantity","class","amount($)"]
  rlist=["customer_get C","flight_info F","make_transaction_apply T"]
  qualification=["C.account='%s'"%account,"C.account=T.account","F.flight_code=T.flight_code"]
  checkdate=["T.trans_time>='%s 00:00:00'"%fdate if fdate else None,"T.trans_time<='%s 23:59:59'"%tdate if tdate else None]
  qualification.extend(checkdate)
  print qualification
  sql=generatesql(target,rlist,qualification)
  print sql
  cursor=g.conn.execute(sql)
  names=[]
  names.append(target1)
  data = getresult(names,cursor)
  glbtransaction=data
  return redirect('/usr')
  # uname = g.conn.execute("SELECT fname,lname FROM customer_get where account='%s';" % account)
  # fullname=[]
  # for ns in uname:
  #   for cell in ns:
  #     fullname.append(cell)
  # uname.close()
  # print fullname
  #print context
  #context = dict(data = info,usrname=fullname)
  #print context
  #usrname=dict(usrname = fullname)
  #return render_template("login.html",**context)











#user website
#
#
#
#
#
#





#airline booking system funcs


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


app.secret_key='asfsdfasdfasfasdf'
if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
