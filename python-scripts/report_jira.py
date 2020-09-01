from jira import JIRA
import re
import sys
import os

class report_jira:

  def create(self, report_directory):

    # Print CSV headline
    csv = "key, summary, assignee, priority, status, created, updated\n"

    # Connect to Jira
    options = {'server': 'https://mydevops2018.atlassian.net'}
    jira = JIRA(options, auth=('s.ortmanns@gmx.de', 'bast88ardos'))

    # Get Jira issues
    JIRA_PROJECT_KEY = "MYW"
    projects = jira.projects()
    issues = jira.search_issues('project=' + JIRA_PROJECT_KEY)

    for issue in issues :

      # Filter issues with status DONE
      status = str(issue.fields.status)
      if not status == "Done":

        name = str(issue.key).replace("\n", " ")
        summary = str(issue.fields.summary).replace("\n", " ")
        assignee = str(issue.fields.assignee).replace("\n", " ")
        priority = str(issue.fields.priority).replace("\n", " ")
        created = str(issue.fields.created).replace("\n", " ")
        updated = str(issue.fields.updated).replace("\n", " ")

        # Print CSV line
        csv += name + "," + summary + "," + assignee + "," + priority + "," + status + "," + created + "," + updated + "\n"

    # Create CSV file
    with open(report_directory + "/jira.csv", "w") as file:
      file.write(csv)
    os.chmod(report_directory + "/jira.csv", 0o777)

    return csv
