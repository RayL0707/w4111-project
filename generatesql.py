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
account = '001'
target = ["account","fname","lname","balance","tot_credit","card_level"]
rlist=["customer_get"]
qualification=["account='%s'"%account]
sql=generatesql(target,rlist,qualification)
print sql