#!/usr/bin/python

import os
import pyssdeep
from getpass import getpass
from mysql.connector import connect, Error

ROOT_DIR = '/mnt/t'     # Where to begin the scan
fileCount = 0           # Count of number of files found
matches = 0
comparator = []
query = """
SELECT * FROM file
"""


if __name__ == "__main__":
   # Open a connection to MySQL
   try:
      with connect(host="localhost", user="root", db="comparator", password=getpass("Enter MySQL root user password:"),) as connection:

         # Get all the database records and put them in an indexed array of tuples
         cursor = connection.cursor()
         cursor.execute(query)

         # For each record, build an array of tuples for searching
         for row in cursor:
            comparator.append((row[1],row[2],row[3]))
            fileCount = fileCount + 1

   except Error as e:
       print(e)
   else:
       # Close cursor
       cursor.close()
       # Close database
       connection.close()

   for i in range(0,len(comparator)-1):
      (oPath, oFile, oHash) = comparator[i]
      for j in range(i+1,len(comparator)-1):
         (cPath, cFile, cHash) = comparator[j]

         qm=pyssdeep.fuzzy_compare(oHash, cHash)
         if(qm > 50):
            print("Processing: ", oPath, oFile)
            print("   Possible match: ", cPath, cFile, ", Score=", qm)
            matches = matches + 1
   print("Processed " + str(fileCount) + " records.\n\n")
   print("Found " + str(matches) + " possible matches.\n\n")
