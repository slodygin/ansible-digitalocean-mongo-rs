#!/usr/bin/python
import pymongo
import time
import urllib 
con = pymongo.MongoClient('mongodb://testUser:passw0rd@mongo-test1:27017,mongo-test2:27017/?replicaSet=rp0')
time.sleep(2)
print con.nodes


coll = con.admin.collection_name
docs = [{"_id" : 1, "num" : 5}]
for doc in docs:
    coll.save(doc)


mydb = con["admin"]
mycol = mydb["collection_name"]

myquery = { "_id": 1 }
newvalues = { "$set": { "num": 4 } }
mycol.update_one(myquery, newvalues)

for x in mycol.find():
  print(x)

i=0
while(1):
  i=i+1
  time.sleep(1)
  try:
    for x in mycol.find():
      found=x
    print 'current value is %s, will write new value %s and sleep 1 second ...' %(found,i)
    myquery = { "_id": 1 }
    newvalues = { "$set": { "num": i } }
    mycol.update_one(myquery, newvalues)
    time.sleep(1)
  except Exception as e:
    print 'Exception: '+ str(e)

