import os
import shutil

class report_jacoco:

  def create(self, report_directory):
    JENKINS_PATH = "/var/lib/jenkins"
    JACOCO_PATH = JENKINS_PATH + "/workspace/Build/target/site/jacoco"
    JACOCO_XML_FILE = JACOCO_PATH + "/jacoco.csv"

    if os.path.exists(JACOCO_PATH):
      # Copy Jacoco file into report directory
      jacoco_file_name = "/jacoco.csv"
      jacoco_file = report_directory + jacoco_file_name

      open(jacoco_file, 'a')
      os.chmod(jacoco_file, 0o777)
      shutil.copyfile(JACOCO_XML_FILE, jacoco_file)

      # Return file as string
      with open(jacoco_file, "r") as file:
        jacoco = file.read()
      return jacoco

    else:
      return "-no jacoco report craeted due to error during build-"
