#!/usr/local/bin/python
# Load jenkins jobs from XML files

import os
import sys
import urllib2
import time
import jenkins

if len(sys.argv) != 4 :
  print "Missing paramter!"
  print "Usage: python loadConfiguration USERNAME PASSWORD JENKINS_PORT"
  sys.exit(2)

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
JENKINS_PORT = sys.argv[3]
JOB_DIRECTORY = "../files/jenkins_config_files/jobs/"

jenkinsUrl = "http://localhost:" + JENKINS_PORT + "/"

# Wait for Jenkins to restart
server = jenkins.Jenkins(jenkinsUrl, timeout=10)
if server.wait_for_normal_op(60):

    # Get XLM config files and load them into Jenkins
    jobs = os.listdir(JOB_DIRECTORY)

    if len(jobs) == 0:
      print "Found no jobs in \"" + JOB_DIRECTORY + "\". Exit script with error code. Change if having no jobs defined is no error."
      sys.exit(3)

    # Try to delete jobs in Jenkins to enable job configuration during provision
    print "Try to delete jobs, where a XML exist, so that old job configuration can be overwritten:"
    print "(The expression \"ERROR: No such job\" can be ignored, if the jobs do not exist at the moment in jenkins)."
    for x in jobs:
      jenkinsCliQuery = "java -jar jenkins-cli.jar -s " + jenkinsUrl +  " -auth " + USERNAME + ":" + PASSWORD + " delete-job "
      if ".xml" in x:
        jenkinsCliQuery += x.replace(".xml", "")
        exitCode = os.system(jenkinsCliQuery)
        if exitCode == 0:
          print " - deleted job \"" + x.replace(".xml", "") + "\""

    # Load jobs into Jenkins
    print "Load jobs from XML into Jenkins"
    for x in jobs:
      jenkinsCliQuery = "java -jar jenkins-cli.jar -s " + jenkinsUrl +  " -auth " + USERNAME + ":" + PASSWORD + " create-job "
      if ".xml" in x:
        jenkinsCliQuery += x.replace(".xml", "")
        jenkinsCliQuery += " < " + JOB_DIRECTORY + x
        exitCode = os.system(jenkinsCliQuery)
        if exitCode == 0:
          print " - load job \"" + x.replace(".xml", "") + "\""
        else:
          print "Failed loading configurations with exitCode=" + str(exitCode)
          sys.exit(4)

else:
    print("Jenkins failed to be ready in sufficient time")
    sys.exit(5)
