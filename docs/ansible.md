# Deployment of the application stack with Ansible

[Ansible][Ansible] is a radically simple IT automation engine that, amongst
many other IT needs, automates application deployment. This document covers how
to deploy SENAITE and `palau.lims` on a server by using Ansible playbook.

The Ansible playbook provided with this software has been used for the
deployment of the [Virtual Appliance][appliance_overview] you should have 
received along with this document. This Ansible playbook has been tested 
successfully on a [Minimal Debian server][senaite_os].

## Requirements

A `senaite` user, and member of `sudoers` group, must be in place in the
destination server. Also, SSH access to the server with this `senaite` user is
required.

## Prepare the local environment

First, clone the source code of `palau.lims` into your local machine using 
[git][git] and go to the `ansible` directory from inside:

```shell
$ sudo apt install git
$ git clone https://github.com/beyondessential/palau.lims.git
$ cd palau.lims/ansible
```

There are some configuration files that you might need to change in order to
make the ansible playbook work properly with your server. Open the file
`hosts.cfg` and apply the proper modifications regarding to the SSH connection.

```shell
$ cat hosts.cfg
```
```ini
[senaite_host]
senaite ansible_ssh_host=<your_server_ip> ansible_ssh_user=senaite ansible_ssh_port=<ssh_port>
```

If you want to change the hostname (`senaite_host` in this example), remember
to edit the file `playbook.cfg` accordingly. The file `configure.yml` allows to
change some values that will be used while deploying the application stack.
Also, note the file `credentials.yml` contains the users and passwords that
will be used by default for accessing to some building parts of the application
stack (such as munin, haproxy, supervisor).

Note that the real IP of the host to where SENAITE will be installed is defined
in the file `hosts.cfg`. You might need to change the default host IP used by
default in this recipe: `192.168.33.10`.

The file `credentials.yml` has been encrypted with a vault file. If you don't
have received this file, please e-mail us to info@naralabs.com with the subject
"Ansible vault request: palau.lims".

Install ansible and python in your operating system:

```shell
$ sudo apt install ansible python
```

Without leaving the `ansible` directory from `palau.lims`, check that
everything is in place, and you are able to reach the server with Ansible:

```shell
$ ansible senaite_host -i hosts.cfg -m setup
```

If ansible is able to connect with the target host and everything is correct, a
long json should be displayed in the terminal after running the previous
command. The output might look similar to:

```
[WARNING]: Invalid characters were found in group names but not replaced, use -vvvv to see details
[WARNING]: Platform linux on host senaite is using the discovered Python interpreter at
/usr/bin/python, but future installation of another Python interpreter could change this. See
https://docs.ansible.com/ansible/2.9/reference_appendices/interpreter_discovery.html for more
information.
senaite | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "10.0.2.15", 
            "192.168.33.10"
        ], 
        "ansible_all_ipv6_addresses": [
            "fe80::a00:27ff:fe1e:9eab", 
            "fe80::a00:27ff:fe01:b85b"
        ], 
        "ansible_apparmor": {
            "status": "enabled"
        }, 
        "ansible_architecture": "x86_64", 
        "ansible_bios_date": "12/01/2006", 
        "ansible_bios_version": "VirtualBox", 
        "ansible_cmdline": {
            "BOOT_IMAGE": "/boot/vmlinuz-4.19.0-14-amd64", 
            "quiet": true, 
            "ro": true, 
            "root": "UUID=786467f3-284a-4a31-9e68-0a62bf4d8eb7"
        },
        ...
    "changed": false
}
```

If you get an error, then check the configuration from `hosts.cfg` and try
again.

## Install Ansible requirements

Without leaving the `ansible` directory, install the Ansible dependencies for
SENAITE. With the following command the system will automatically download
other ansible recipes and templates the current playbook depends on.

```shell
$ ansible-galaxy install -f -r senaite.ansible-playbook/requirements.yml
```

## Run the Ansible playbook

Before running the Ansible playbook, please be sure you've copied the
`vault.txt` file provided by other means in the `ansible` directory. Note this
file is not provided by default in the repository for security reasons.

To run the Ansible playbook, type the following command without leaving the
`ansible` directory from inside `palau.lims` source code:

```shell
$ ansible-playbook -vv -i hosts.cfg playbook.yml --vault-password-file vault.txt
```

The system will automatically install everything in the server. It also
generates an SSH key that will use for the automatic download of the latest
source code of `palau.lims`. The following message will appear:

```
TASK [Wait for user to copy SSH public key] ******************************************************************************************
task path: /home/johndoe/palau.lims/ansible/custom_pre.yml:35
[Wait for user to copy SSH public key]
Please, add the SSH public key above to the GitHub account ...:
```

If you don't have admin rights for `palau.lims` repository, please e-mail the
output to info@naralabs.com and Naralabs will add this public SSH key to the
source code repository and notify back to you. Press enter to resume the
process as soon as you receive our confirmation that the deployment key has
been added to the repository.

## Create a new SENAITE site

After Ansible playbook is run and succeed, there is still one action that must
be done manually: the creation of the SENAITE site on top of the Plone
framework.

Login to the host through SSH and grab the Zope admin user credentials:

```shell
$ cat senaite/live.cfg | grep "user="
```

Create a new SENAITE site by using lynx:

```sh
$ lynx http://localhost:8081
```

You can move through the links with the cursor. Choose "Create a new SENAITE
site" and press "Enter". Type then the username and password and submit.

A "Site Installation" form is displayed. Change the "Default timezone" by a
suitable value and leave the defaults on the rest of the settings ("Path
identifier", "Title", "Language"). Move with the cursor to "Create SENAITE
Site" and press "Enter".

Once the SENAITE site is created, you should be able to access to SENAITE from
outside the host: http://192.168.33.10

Remember to change the IP in accordance and accept the self-signed certificate.
You can log in with the same credentials you've used previously for the site
creation. Go to the add-ons installation page thereafter:
https://192.168.33.10/prefs_install_products_form

If not yet activated, press the button "Install" above "palau.lims" to install 
the SENAITE extension.

## Troubleshooting

This section provides answers and solutions to some common answers and
pitfalls.

### Resume the installation process

If the process was not able to finish properly (e.g. because lack of internet
connectivity), you can always re-run the Ansible playbook to resume the
installation:

```sh
$ ansible-playbook -vv -i hosts.cfg playbook.yml --vault-password-file vault.txt
```

### Error setting locale

I get this message in the terminal:

```
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
        LANGUAGE = "en_US:en",
        LC_ALL = (unset),
        LC_MESSAGES = "en_US.UTF-8",
        LANG = "en_US.UTF-8"
are supported and installed on your system.
```

See this link for a solution:
https://askubuntu.com/questions/162391/how-do-i-fix-my-locale-issue

Once resolved, rerun the Ansible playbook.

### Permission denied

Traceback:

```
zope.configuration.xmlconfig.ZopeXMLConfigurationError: File "/home/senaite/senaitelims/parts/client1/etc/site.zcml", line 16.2-16.23
    ZopeXMLConfigurationError: File "/home/senaite/buildout-cache/eggs/Products.CMFPlone-4.3.17-py2.7.egg/Products/CMFPlone/configure.zcml", line 98.4-102.10
    ZopeXMLConfigurationError: File "/home/senaite/senaitelims/src/senaite.core/bika/lims/configure.zcml", line 15.0-15.35
    ZopeXMLConfigurationError: File "/home/senaite/buildout-cache/eggs/Products.TextIndexNG3-3.4.14-py2.7.egg/Products/TextIndexNG3/configure.zcml", line 8.2-8.61
    IOError: [Errno 13] Permission denied: '/home/senaite/buildout-cache/eggs/zopyx.txng3.core-3.6.2-py2.7.egg/zopyx/txng3/core/configure.zcml'
```

Also see this issue: https://github.com/senaite/senaite.core/issues/861

Change the permissions on the `eggs` directory:

```shell
$ sudo chmod -R ug+rwX,o-rwx /home/senaite/buildout-cache/eggs
```
    

And rerun the Ansible playbook.

### Global Python interpreter is used

Add this to the end of `/home/senaite/.profile` to use the local python
interpreter from the buildout.

    if [ -d "$HOME/python2.7" ] ; then
        echo "Using local Python installation"
        PATH="$HOME/python2.7/bin:$PATH"
    fi

And rerun the Ansible playbook.

### Error: Wheels are not supported

Traceback:

```
handler in zc.buildout.easy_install.UNPACKERS
While:
  Installing.
  Loading extensions.
  Getting distribution for 'mr.developer==1.37'.
Error: Wheels are not supported
```

Setuptools `38.2.0` started supporting wheels which fails
in `zc.buildout < 2.10.0`. Please pin `zc.buildout` to version `2.10.0` in your
buildout.cfg

### Error: Couldn't find a distribution for 'plone.api'

Please add this index section to your `buildout.cfg`:

```ini
[buildout]
...
index = https://pypi.python.org/simple/
...
```

### Permission denied (pip and setuptools)

Traceback:

```
An internal error occurred due to a bug in either zc.buildout or in a
recipe being used:
Traceback (most recent call last):
  File "/home/senaite/python2.7/local/lib/python2.7/site-packages/zc/buildout/buildout.py", line 2174, in main
    getattr(buildout, command)(args)
  File "/home/senaite/python2.7/local/lib/python2.7/site-packages/zc/buildout/buildout.py", line 716, in install
    self._compute_part_signatures(install_parts)
  File "/home/senaite/python2.7/local/lib/python2.7/site-packages/zc/buildout/buildout.py", line 962, in _compute_part_signatures
    sig = _dists_sig(pkg_resources.working_set.resolve([req]))
  File "/home/senaite/python2.7/local/lib/python2.7/site-packages/zc/buildout/buildout.py", line 1880, in _dists_sig
    result.append(dist.project_name + '-' + _dir_hash(location))
  File "/home/senaite/python2.7/local/lib/python2.7/site-packages/zc/buildout/buildout.py", line 1864, in _dir_hash
    f = open(path, 'rb')
IOError: [Errno 13] Permission denied: '/home/senaite/python2.7/lib/python2.7/site-packages/pip-19.3.1.dist-info/INSTALLER'
```

Change the permissions of the pip package contents:

```shell
$ sudo chmod -R +r /home/senaite/python2.7/lib/python2.7/site-packages
```

And rerun the Ansible playbook.


[senaite_os]: senaite_os.md
[Ansible]: https://www.ansible.com
[git]: https://git-scm.com/
[appliance_overview]: appliance_overview.md
