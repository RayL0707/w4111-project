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
  if not gwhere:
    return gsql
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
# gselect=['a','b','c','d']
# gfrom=['aa','bb']
# gwhere=['aaa','bbb']
target = ["flight_info as Flight",'depart','arrive',"date","depart_time","arrive_time","ticket_quantity","company"]
rlist=["flight_info"]


pfrom = None
pto = None
pwhen = None
if not pfrom and not pto and not pwhen:
	qualification=[]
else:
	qualification=["depart='%s'"%pfrom if pfrom else None, "arrive='%s'" %pto if pto else None, "date='%s'"% pwhen if pwhen else None]
#print qualification
sql=generatesql(target,rlist,qualification)
print sql
#gwhere=[pfrom,pto,pwhen]
#generatesql(target,rlist,qualification)

