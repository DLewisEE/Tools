#!/usr/bin/python

import os
import re

ROOT_DIR = '/mnt/t'     # Where to begin the scan
fileCount = 0           # Count of number of files found

if __name__ == "__main__":
   # Now time for a directory walk
   for subdir, dirs, files in os.walk(ROOT_DIR):
      for file in files:
         orig = ""
         fileCount = fileCount + 1
         orig = file
         
         print("Changing " + orig + " to " + file)
         os.rename(os.path.join(subdir,orig),os.path.join(subdir,re.sub(r'[^\x00-\x7F]+', '', file)))
   print("Processed " + str(fileCount) + " files.\n\n")
