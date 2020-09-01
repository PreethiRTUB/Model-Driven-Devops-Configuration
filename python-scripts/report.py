from report_jira import report_jira
from report_jacoco import report_jacoco
import shutil
import os
import time
import datetime

class report:

  timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

  def create_report_dir(self):
    REPORT_BASE_DIR = "/home/vagrant/report"
    report_directory = REPORT_BASE_DIR + "/report-" + report.timestamp
    os.mkdir(report_directory)
    os.chmod(report_directory, 0o777)
    print "created " + report_directory
    return report_directory

  def create_build_report(self):
    date = str(report.timestamp.split("_")[0])
    time = str(report.timestamp.split("_")[1])

    build = "jenkins-job-name,date,time\n"
    build += "Build," + date + "," + time + "\n"
    return build

  def combine_reports(self, report_directory, main, jira, jacoco):
    # Create combined report from multiple strings
    new_report = "REPORT\n"
    new_report += main + "\n\n"
    new_report += "JIRA_ISSUES\n"
    new_report += jira + "\n\n"
    new_report += "JACOCO\n"
    new_report += jacoco + "\n\n"

    # Save combined report as CSV
    with open(report_directory + "/report.csv", "w") as file:
      file.write(new_report)
    os.chmod(report_directory + "/report.csv", 0o777)

  def create(self):
    report_creator = report()
    report_dir = report_creator.create_report_dir()

    # Crate report parts
    build = report_creator.create_build_report()
    jira = report_jira().create(report_dir)
    jacoco = report_jacoco().create(report_dir)

    # Create combined report
    report_creator.combine_reports(report_dir, build, jira, jacoco)
    return "Created new report \"" + report_dir + "/report.csv\""
