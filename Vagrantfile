Vagrant.configure(2) do |config|
 config.vm.box = "ubuntu/bionic64"
 config.vm.hostname = "ci-server"
 config.ssh.forward_x11 = true
 # Jenkins server
 config.vm.network "forwarded_port", guest: 8080, host: 7070
 # Tomcat server
 config.vm.network "forwarded_port", guest: 9090, host: 8090
 config.vm.provision :shell, path: "bootstrap.sh"
 config.vm.provision "ansible" do |ansible|
 	ansible.inventory_path = "hosts"
 	ansible.limit = "all"
  ansible.playbook = "playbook.yml"
  ansible.extra_vars = {
    jenkins_vm_port: 8080,
    tomcat_vm_port: 9090
  }

 end
end
