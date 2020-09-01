# DevOps environment
This program creates a virtual machine with a preconfigured DevOps environment. Please read carefully this README to prepare your system to run the project and understand its structure and function.

An image of the virtual machine should be possible to be host on any system that is able to run VirtualBox. The building of the virtual machine otherwise has multiple requirements besides VirtualBox listed under Prerequisites.

Please notice, that relative paths (e.g. `./Vagrantfile`) mentioned in this README are always considered relative to the root directory of the project on the host machine. Absolute paths (e.g. `/home/vagrant`) are always considered to be located on the virtual machine.

### Prerequisites
- Operating systems that are able to be used as a host machine are any of Red Hat, Debian, CentOS, OS X and BSDs. Windows can not be used, because Ansible as the central provisioning tool does not support it. The development and testing of the project was done with Ubuntu 16.04 LTS and Ubuntu 18.04 LTS.
- Install [VirtualBox](https://www.virtualbox.org/) to host the virtual machine
- Install [Vagrant](https://www.vagrantup.com/) to create and configure the virtual machine
- Install [Ansible](https://www.ansible.com/) to install software and manage the configuration of the virtual machine
- Internet connection to allow Ansible to download necessary software during the provision of the virtual machine and to enable a connection to Jira during the creation of the report.

### Create the virtual machine
The project can be cloned via git after all dependent software is installed on an operating system that is supported by Ansible. With a terminal go into any directory of the project and start the creation of the virtual machine with *vagrant up*. Thereupon Vagrant will create a virtual machine within virtual box and will trigger Ansible to configure the virtual machine. This process will take about 10 to 15 minutes, depending on the host machine and the internet connection, since a lot of software needs to be downloaded and installed. Sometimes the provisioning fails because necessary software could not be downloaded on time. In this case you can restart the provision with *vagrant provision*. The creation of the virtual machine and the provisioning of the virtual machine are two distinct processes. After the virtual machine is running in VirtualBox you can bring changes in the Ansible scripts with the *vagrant provision* command into affect. Only Ansible commands that were altered are triggered after a rerun of *vagrant provision*, which drastically reduce execution time. Some changes however will not be realized and it is necessary to delete the whole virtual machine with *vagrant destroy* and rebuild it with *vagrant up*.

You can verify the initialization of the virtual machine by enter it with the command *vagrant ssh*. The Jenkins server should now be running on port *7070* and the Tomcat server on port *8090*. The server are accessible from a browser with the URLs *http://localhost:7070* and *http://localhost:8090* respectively. The credentials can be found in `./main.yml`.

### Vagrant
##### Configuration
The file `./Vagrantfile` contains the configuration of vagrant. Among other things it defines what virtual machine is used, the port mapping, the host name of the virtual machine and the provisioning tool. The ports for the Jenkins and Tomcat server are passed here as extra variables to Ansible.

Another noticeable fact is, that vagrant will create a folder `/vagrant` on the virtual machine that contains the project directory. This folder is shared by both the host machine and the virtual machine. That means, if you add the file `./example.txt` on the host, this file is also accessible from the virtual machine  `/vagrant/example.txt`.

##### Important commands
- `vagrant up`: Command vagrant to create a virtual machine in VirtualBox and to run Ansible for the provision
- `vagrant provision`: Vagrant just runs Ansible for the provision. This command is only possible to execute, if the virtual machine is already running in VirtualBox.
- `vagrant destroy`: Destroy the whole virtual machine. Changes that are not saved with mechanisms mentioned later in this document will be irreversible deleted.
- `vagrant ssh`: Access the virtual machine
- `vagrant status`: Get the status of the virtual machine vagrant is running

### Ansible
As the provisioner Ansible is responsible for all software on the virtual machine and almost all configuration of this software. After the setup of the virtual machine in VirtualBox, Vagrant will execute `./playbook.yml`. This playbook will load the most important configuration variables from `./main.yml`, such as the Jenkins and Tomcat credentials, the git username and git email address and the home path of Jenkins. After that multiple Jenkins roles and other tasks are executed.

##### Roles
Most of the software is installed via Ansible roles. The roles can be obtained from Github or from [Galaxy](https://galaxy.ansible.com/), an web page that is dedicated to them. You can find all roles that are used by the project in the directory `./roles`. The `./main.ylm` only contains a small fraction of variables to configure Ansible. Most roles have a directory *defaults* and a file *main.yml* which has various variables that can be used to configure and adjust the installed software (e.g. for Jenkins `./roles/geerlingguy.jenkins/defaults/main.yml`).

Following software is installed via Ansible roles:

- Git
- Java
- Maven
- Jenkins
- Pip
- Jira
- Tomcat
- LibreOffice

### Configure Jenkins
Jenkins is the central Continuous Integration and Continuous Deployment tool. It uses so called jobs to define how to build, test and deploy projects. Webhooks can be used to trigger jobs and terminal commands can be used from within the jobs to execute any kind of script on the host machine. There exist various plugins that will extend the functionality of Jenkins. You can find them and their ID in the Jenkins user interface under *http://localhost:7070/pluginManager/available*. If you want to permanently add a plugin to the DevOps environment you need to add its ID to the variable *jenkins_plugins* in `./main.yml`.

Jenkins save all of its configurations in XML files in its home directory `/var/lib/jenkins` on the virtual machine. We need to save these files manually with a script to keep altered configuration details even after the virtual machine is destroyed. Be aware, that only some of the configurations will be saved at the moment! This includes deleting, creating or altering the Jenkins jobs and the authentication keys managed by Jenkins. Some authentication keys of plugins like *JiraTestResultReporter* are stored in separate XML files. The configuration files will be saved in `./files/jenkins_config_files/`. Please take into consideration that executing the script will lead to the deletion of any old configuration files.

**How to configure and save configurations:**
1 Configure Jenkins by using its user interface at *http://localhost:7070/*
2 Enter the virtual machine by executing *vagrant ssh* from within the project directory
3 Change to the directory on the virtual machine to */vagrant/python-scripts*
4 Execute `python saveConfiguration.py admin admin`, where '*admin*' and '*admin*' are the Jenkins username and password.

### Git repository
##### Load repository
Ansible executes a Git clone command during the provision phase. This command will try to clone the repository mentioned in the variable *git_repo_remote_url* and installs it to the path on the virtual machine mentioned in the variable *git_repo_local_path*; Both variables are defined in `./main.yml`. At the moment only repositories can be cloned that do not need verification, but with small changes a verification via username and password or SSH key should be realizable.

##### Change repository
The java project that is at the moment loaded into the virtual machine (https://github.com/PreethiRTUB/mywebapp.git) uses Maven for executing the tests and build the project. The Jenkins jobs *Build* and *Deployment* are specialized to exactly run this project (exspecially the execution of the test, since this is realized with Maven profiles).

Using a non Maven Java project will break test- and build-phase in the preconfigured Jenkins jobs and using a non Java project will also break coverage code analysis done by Jacoco. You need to adjust the Jenkins jobs, tools and scripts if you want to change the project. For testing purposes you can use the current project, because you can trigger the whole DevOps cycle without permissions by doing commits.

Following instructions are not tested:
If you want to replace the current project with another one that uses Maven, this should be realizable by either adjusting the Maven build goals in the Jenkins jobs or ensure that the Maven build goals in the Jenkins jobs can run in the new project without error. After that updating *git_repo_local_path* make it possible to run another project.

##### Git hook
Under the current configuration Ansible will copy the Git hook file `./files/post-commit` into the *hooks* directory of the loaded Git project. This file is executed after each commit of the project and will notify Jenkins about the changes.

### Jira
1. Create Jira admin account
2. In github, generate OAuth for the account and get the Cliend Id and Client Password.
3. In Jira, generate a DVCS account and link JIRA with github.
4. This automatically pulls all the repositories from the github to JIRA.
5. Select the repository that is required for this automation and it gets integrated with JIRA
6. Make sure the SMART COMMIT tab is checked so that when you make changes in github it automatically reflects in JIRA.
7. Now create a ticket in JIRA by giving the summary or purpose of the ticket and assign the ticket to a developer.
8. As soon as the developer makes changes in the project and commits the code with the ticket ID in the commit message, the JIRA ticket with that ticket ID is updated automatically.
9. Through this we can track the status as well as the part of the code that has been modified in the commit.

### Report
The DevOps report is created by multiple python scripts. The script `/vagrant/python-scripts/postBuildScript.py` will be executed each time the Jenkins *Build* job is triggered and will itself execute other scripts that will create the report. You can find the report on the virtual machine `/home/vagrant/report`.
