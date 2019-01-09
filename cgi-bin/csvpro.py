import csv
import boto3
import mysql.connector
import cgi
import os
import cgitb; cgitb.enable()



class CsvManage(object):

  def __init__(self):
    print("Content-type:text/html\r\n\r\n")
    print("")
    self.form = cgi.FieldStorage()
    self.mydb = mysql.connector.connect(
      host="csvparserdb.cyfe0sx7z6fu.us-east-1.rds.amazonaws.com",
      user="csvparserdbuser",
      passwd="CsvParser2019",
      database="csvparser")
    self.mycursor = self.mydb.cursor()
    self.sql = "INSERT INTO csv_data (sku,p_name, price) VALUES (%s, %s,%s)"
    

  def getS3List(self):
    pass
    print("")
    print(','.join(os.listdir()))
  
  def deleteObj(self,filename):
    print(type(filename))
    os.remove(filename)
  
  def fileUpload(self):
    fileitem = self.form['file']
    if fileitem.filename:
      fn = os.path.basename(fileitem.filename)
      open(fn, 'wb').write(fileitem.file.read())

      message = 'The file "' + fn + '" was uploaded successfully'
      csv_file = open(fn).readlines()
      f = csv.reader(csv_file)
      csv_data = []
      for row in f:
        if not row:continue
        csv_data.append((row[0],row[1],row[2]))
        
      self.mycursor.executemany(self.sql, csv_data)
      self.mydb.commit()
    else:
      message = 'No file was uploaded'
    print(message)


c = CsvManage()

if "getdata" in c.form.getlist("action"):
  c.getS3List()
elif 'file' in c.form.keys():
  c.fileUpload()
elif c.form.getlist("selectBox"):
  c.deleteObj(c.form.getlist("selectBox")[0])
#print("<html><h1>Test</h1></html>")


