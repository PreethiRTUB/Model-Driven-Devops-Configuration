#!/usr/local/bin/python
# Create jenkins jobs from XML files

import shutil
import os
import sys
import subprocess


if len(sys.argv) != 3 :
  print "This script saves the XML configuration files of Jenkins."
  print "!!!It can only be executed from within the VM!!!"
  print "Usage: python saveConfiguration USERNAME PASSWORD"
  print "If configuration is not changed in \"../main.yml\", then following values are valid:"
  print "Username = admin"
  print "Password = admin"
  sys.exit()

JENKINS_PORT = "8080"
FILES_DIRECTORY = "../files/jenkins_config_files"
JENKINS_SECRETS_DIRECTORY = FILES_DIRECTORY + "/secrets"
JENKINS_CREDENTIALS_XML = FILES_DIRECTORY + "/credentials.xml"
JENKINS_HOME = "/var/lib/jenkins"

# SAVING JENKINS CREDENTIALS
# Delete old creadential files
print ("Delete old credential files if they exist:")
if os.path.exists(JENKINS_SECRETS_DIRECTORY) :
  shutil.rmtree(JENKINS_SECRETS_DIRECTORY)
  print (" - deleted \"" + JENKINS_SECRETS_DIRECTORY + "\"")
if os.path.exists(JENKINS_CREDENTIALS_XML) :
  os.remove(JENKINS_CREDENTIALS_XML)
  print (" - deleted \"" + JENKINS_CREDENTIALS_XML + "\"")

# Copy new credential files
print ("Copy new credential files:")
shutil.copytree(JENKINS_HOME + "/secrets", JENKINS_SECRETS_DIRECTORY)
print (" - copied \"" + JENKINS_HOME + "/secrets" + "\"")
shutil.copy(JENKINS_HOME + "/credentials.xml", JENKINS_CREDENTIALS_XML)
print (" - copied \"" + JENKINS_HOME + "/credentials.xml" + "\"")

# SAVING JENKINS JOBS
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
JOB_DIRECTORY = FILES_DIRECTORY + "/jobs/"

print "Delete old job configuration files:"
for x in os.listdir(JOB_DIRECTORY):
  if ".xml" in x:
    os.remove(JOB_DIRECTORY + x)
    print " - removed job \"" + x + "\""

print "Try to save Jenkins jobs to XML files using Jenkins CLI:"
jenkinsCliQuery = "java -jar jenkins-cli.jar -s http://localhost:" + JENKINS_PORT + "/ -auth " + USERNAME + ":" + PASSWORD
jobsString = subprocess.check_output(jenkinsCliQuery + " list-jobs", shell=True)
jobs = jobsString.splitlines()
if len(jobs) == 0:
  print "Found no jobs on Jenkins server. Exit."
else:
  print "Found " + str(len(jobs)) + " job(s). Trying to save them:"
  for x in jobs:
    filename = x.replace(" ", "_") + ".xml"
    query = jenkinsCliQuery + " get-job '" + x + "' > " + JOB_DIRECTORY + filename
    exitCode = os.system(query)
    if exitCode == 0:
      print " - saved job \"" + x + "\" as XMl file."
    else:
      print "Failed with exitCode=" + str(exitCode)
