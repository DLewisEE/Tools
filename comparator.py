#!/usr/bin/python

import os
import pyssdeep
from getpass import getpass
from mysql.connector import connect, Error

ROOT_DIR = '/mnt/t'     # Where to begin the scan
fileCount = 0           # Count of number of files found
query = """
INSERT INTO file 
(path, filename, fuzzy) 
VALUES 
(%s, %s, %s)
"""


if __name__ == "__main__":
   # Open a connection to MySQL
   try:
      with connect(
               host="localhost",
               user="root",
               db="comparator",
               password=getpass("Enter MySQL root user password:"),
            ) as connection:

         # Now time for a directory walk
         for subdir, dirs, files in os.walk(ROOT_DIR):
            for file in files:
               fileCount = fileCount + 1
               print("Processing "+str(fileCount)+" "+os.path.join(subdir,file))
               try:
                  sshash=pyssdeep.get_hash_file(os.path.join(subdir,file))
                  # Write out the file information to the DB
                  file=bytes(file,'utf-8').decode('utf-8','ignore')
                  with connection.cursor() as cursor:
                     cursor.execute(query, (subdir,file,sshash))
                     connection.commit()
               except pyssdeep.FuzzyHashError as err:
                  print(err)
               except IOError as err:
                  print(err)
   except Error as e:
       print(e)
   print("Processed " + str(fileCount) + " files.\n\n")
