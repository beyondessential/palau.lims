# Setup a minimal Debian server

## Introduction

For best performance, the installation of a minimal Debian server is
recommended. [Debian][debian] is a lightweight and thoroughly  tested Linux
distribution, well-known for its stability, reliability and security, mostly
because of [Debian release life cycle][debian_releases] and
[Debian Long Term Support (LTS)][debian_lts].

This documentation assumes the Operating System of choice is
[Debian 11 (bullseye)][debian_11], that was initially
[released on August 2021][debian_11_press_release] and is
[officially supported by Debian Project until June 2026][debian_lts].

> **Warning**
> Commands from this recipe have to be run in the server, so the command
> prompt is omitted by default. ``me@local:~$`` will be used otherwise, to
> indicate the command has to be run from the user's local machine.

## Installation

The easiest way to install debian is to download the latest
[net installer iso][debian_net installer] and then burn it into a USB stick and
use it as the boot device of the target machine/host/VM. If you are using a
_debian-like_ system, follow the instructions on
[how to write a CD/DVD/BD image to a USB flash drive][faq_write_usb].
Otherwise, pick any of the available tools out there for different Operating
Systems that allow burning ISO files into USB sticks.

Reboot the target system on which you want to install Debian and go to
its BIOS settings and change boot medium from Hard disk to bootable media
(like USB / DVD) if not set as the first bootable media.

Once rebooted, the system will boot into the "Installation Menu" of Debian:

![Choose-Graphical-Install-Debian11][debian_install_menu]

Select "Graphical Install" from the options, and the installation will begin.

**It is strongly recommended not to install any of the Graphical Desktop
environments of choice**. The rendering of graphical interface consumes RAM and
CPU; in a production environment this usually means a waste of space and
resources. Since access to this server will always be done through a
[Secure Shell (SSH)][ssh] connection, the installation of a graphical user
interface is not necessary.

### Installation settings

Be sure to set the correct settings within the installation process in the
following screens:

- **_Setup users and passwords_**: Leave `root` user without password. System's
  initial user account will be `senaite`.

- **_Partition disks_**: Select "_Guided – use entire disk and setup LVM_" and
  "_All files in one partition_". Installer will create a single LVM based
  partition automatically for whole disk.

- **_Software selection_**: **Leave all options unchecked except "_SSH server_"
  and "_standard system utilities_"**. We want a "minimal" debian server.

Please refer to the [Debian Installation Guide][debian_install_guide] for
detailed information about all installation options available.

## Update your Debian Installation

Login to the system as superuser (usually `root`) and make sure that your
``/etc/apt/sources.list`` contains the ``bullseye/updates`` repository (this
makes sure you always get the newest security updates), and that the
``contrib`` and ``non-free`` repositories are enabled as some required
packages are not in the main repository.

```shell
# nano /etc/apt/sources.list
```
```ini
deb http://deb.debian.org/debian/ bullseye main
deb-src http://deb.debian.org/debian/ bullseye main

deb http://security.debian.org/debian-security bullseye-security main
deb-src http://security.debian.org/debian-security bullseye-security main

deb http://deb.debian.org/debian/ bullseye-updates main
deb-src http://deb.debian.org/debian/ bullseye-updates main
```

Update the ``apt`` package database and install latest updates, if any:

```shell
# apt update
# apt upgrade
```

## Creation of senaite user

If either the system does not come with a ``senaite`` user with ``sudo``
privileges or you've created another user while installing the operating
system, login as the initial user or ``root`` and create a ``senaite`` user
with the following command:

```shell
# adduser --home /home/senaite --shell /bin/bash senaite
```

Check ``sudo`` command is installed or install it otherwise:

```shell
# apt update
# apt install sudo
```

> **Note**
> More information: [sudo command][sudo_command], [sudo manpage][sudo_manpage],
[adduser manpage][adduser_manpage]

## Add senaite user to sudoers

Login to the system as superuser (usually `root`) and add `senaite` user to the
group of `sudoers`:

```shell
# visudo -f /etc/sudoers.d/senaite
```
```ini
# User rules for SENAITE
senaite ALL=(ALL) NOPASSWD:ALL
```

## Synchronize the System Clock

It is a good idea to synchronize the system clock with an [NTP (network time
protocol)][ntp] server over the Internet. Run the following to ensure the
system is alywas in sync.

```shell
# apt -y install ntp
```

## Secure SSH access

The remote access to this server will be done through a
[Secure Shell (SSH)][ssh] connection, that provides a
[secure channel][secure_channel] over an unsecured network. While logged in as
`root` user, install [`openssh-server`][openssh-server] in your system, if
not yet installed, as follows:

```shell
# apt install openssh-server
```

Once installed, `sshd` (`OpenSSH Daemon`), that listens for connections from
clients, will start automatically. `sshd` process will also start at boot.

In order to properly secure the system, it is recommended to ensure your SSH
server is configured according to best practices. SSH configuration involves
modifying the `sshd_config` file, that can be found at `/etc/ssh/sshd_config`.

```shell
# nano /etc/ssh/sshd_config
```

The recommended configuration is as follows:

- **`Port 3022`**: Port 22 is a well known SSH port and therefore a target for
  attacks. Port numbers below 1024 might have been officially reserved for some
  other protocol. Port number above 1024 is recommended.

- **`PermitRootLogin without-password`**: Allows the login as root, but only to
  users with an authorized key. Alternatively, use `PermiRootLogin no` to
  disable remote login with root permanently.

- **`PasswordAuthentication no`**: This makes it impossible  to access the
  system without an authorized public key. User  won't be prompted for
  password and server will deny access automatically.

- **`StrictModes yes`**: Specifies whether sshd should check file modes and
  ownership of	the user's files and home directory before accepting login.
  This is normally desirable because novices sometimes accidentally leave
  their directory or files world-writable.

- **`PubkeyAuthentication yes`**: This setting disables password-based logins,
  so only public key based logins are allowed.

- **`AllowAgentForwarding no`**: If enabled, this setting allows the user that
  connects remotely to the server to use it's own local SSH keys (e.g. for
  downloading from a repository) instead of relying on the keys sitting on the
  server. Thus if multiple users will have access to the server, it is a good
  practice to not permit agent forwarding.

- **`X11Forwarding no`**: The security risk of using X11 forwarding is that the
  client's X11 display server may be	exposed	to attack when the SSH client
  requests forwarding.

- **`PermitEmptyPasswords no`**: Explicitly disallow remote login from accounts
  with empty passwords.

Use the `-t` option to check the validity of the configuration file. If there
is an error, it will show on screen. Otherwise, it will not display any
message:

```shell
# sshd -t
```    

Add **your public key** to the server's authorized keys. If you don't yet have
your pair of private/public SSH keys, **create one in your local machine** as
follows:

```shell
$ ssh-keygen -t rsa -b 4096
```

> **Note**
> More information: [ssh-keygen at Wikipedia][ssh_keygen_wikipedia]

Install your SSH key on the server as an authorized key by typing the following
command in your **local machine**:

```shell
me@local:~$ ssh-copy-id -i ~/.ssh/id_rsa.pub senaite@host
```

where:
- `host`: the IP of the server we are setting up

> **Note**
> `id_rsa.pub` is the file name linux uses by default when creating your
> key pair. Change the file name if required. `host` is the host name or IP
> of the server we are configuring. More information:
> [`ssh-copy-id` manpage][ssh-copy-id]

You now will be able to access to your server without password. Type the
following command in your **local machine**:

```shell
me@local:~$ ssh senaite@host
Linux Debian-bullseye-64-minimal 5.10.0-23-amd64 #1 SMP Debian 5.10.179-1 (2023-05-12) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jun 10 22:35:16 2023 from 197.155.238.158
senaite@Debian-bullseye-64-minimal:~$
```

Go back to the terminal session in the server and restart the `sshd` process:

```shell
# service sshd restart
``` 

You will be able now to access to establish an SSH connection to the server
with `senaite` user, but using port `3022` instead:

```shell
me@local:~$ ssh -p3022 senaite@host
Linux Debian-bullseye-64-minimal 5.10.0-23-amd64 #1 SMP Debian 5.10.179-1 (2023-05-12) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jun 10 22:35:16 2023 from 197.155.238.158
senaite@Debian-bullseye-64-minimal:~$
```

> **Warning**
> Note that remote access with `root` is no longer permitted depending on the
> value set for `PermitRootLogn` setting (see sshd configuration above).

## Modify server's hostname

During the installation of the minimal server you are asked to set a hostname.
You may have either skipped that step, or you've realized the hostname you've
set won't work. For instance, with the SSH sessions we've done in the previous
section, we can see the hostname is `Debian-bullseye-64-minimal`. This
hostname does not resemble to what the server will be used for. You can change
the hostname to e.g. `senaite-qsystem`, `senaite-psystem`, etc. as follows:

```shell
$ sudo hostnamectl set-hostname senaite-qsystem
$ hostname
senaite-qsystem
``` 

Open the file `/etc/hosts` and replace the old hostname by the new one:

```shell
$ sudo nano /etc/hosts
```

There is no need to reboot the server. If you open a new SSH connection, the
command prompt displays the new hostname:

```shell
me@local:~$ ssh -p3022 senaite@host
Linux senaite-qsystem 5.10.0-23-amd64 #1 SMP Debian 5.10.179-1 (2023-05-12) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jun 10 22:35:16 2023 from 197.155.238.158
senaite@senaite-qsystem:~$
```

## Setup ufw (Uncomplicated Firewall)

[ufw (Uncomplicated Firewall)][ufw] is a program for managing a netfilter
firewall designed to be easy to use. For this server we only want the
following ports to be open:

- 80: Default port for http connections
- 443: Default port for Https connections
- 3022: The SSH port we configured earlier for SSH connections

Install ufw with the following command:

```shell
$ sudo apt install ufw
```

Set the open ports as follows:

```shell
$ sudo ufw allow 80
$ sudo ufw allow 443
$ sudo ufw allow 3022
``` 

And enable the firewall afterwards:

```shell
$ sudo ufw enable
$ sudo ufw status numbered
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 3022                       ALLOW IN    Anywhere
[ 2] 80                         ALLOW IN    Anywhere
[ 3] 443                        ALLOW IN    Anywhere
[ 4] 3022 (v6)                  ALLOW IN    Anywhere (v6)
[ 5] 80 (v6)                    ALLOW IN    Anywhere (v6)
[ 6] 443 (v6)                   ALLOW IN    Anywhere (v6)
```

## Add custom ssh motd login message

By-default most Linux/Unix machine has an `/etc/motd` file that contains
text message that will be printed when anyone login on the machine. You can
optionally modify this message by editing `/etc/motd` file as follows:

```shell
$ sudo nano /etc/motd
```
```
************************************************************************
WARNING: Unauthorized access to this system is forbidden and will be
prosecuted by law. By accessing this system, you agree that your actions
may be monitored if unauthorized usage is suspected.
************************************************************************
```

## Setup logrotate for mail

System processes (e.g. cron) will keep sending emails to the local mail
account. Unless you setup a mail server [Postfix][postfix] and forward the
emails to an external email account, the system's mail files will keep growing.
To prevent disk space shortage, it is recommended to enable
[`logrotate`][logrotate] to rotate the files from `/var/mail`. Edit the
configuration file `/etc/logrotate.d/mail` as follows:

```ini
/var/mail/* {
    # Rotate if the size is >=10MB:
    size 10M

    # Keep 5 rotated logs
    rotate 5

    # Do not rotate if empty
    notifempty

    # Compresses rotated logs
    compress
}
```

## Add authorized RSA keys

To allow users to SSH into this server or into SENAITE instances from within
the same network through this server, you need to add their public RSA keys
to the authorized keys file:

```shell
$ nano ~/.ssh/authorized_keys
```
````
# Jordi Puiggené (Naralabs)
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDIbHWNfaomvkwZCZXCeEXrgyyVFdFuimb5gzn+qHTglu6yF2Cp84YvLDAdU0hwJbK3DDzDrGOVJS5BJoUmY1r5mi6HSndSNPDK7JRMBg0ycyhDexzwwznvtGlVW7xNwbWQrRIDDgyXBzjYQhgbCH5zPIAZBIXl+HAmi7QOEvc1BHdMiiESf5ECDdEx0SHcnbgzDpTI/DMPmjao1diWX5tqHUf3s3Bb7NQ1wnE1p6k+OuqfQDiE39h5G0ITX1+F5qGppwIF+mvn+xKrueX8fkFyG1DLwNlAFcXHFqDfW+6xTQnT6puV5M+/ksFIOou9u9zFZJU3vaLWQRGvWpd6PMATaDLixNk9SYwkdYVmz+Dv2co1HrxSkhMc32668ZngX8RAbpe5Ek9Y0EOVHKMT4NtCP0XfW7ergK+uC7DMx26dWGeB4pD/YLGu0FraRSwtsl1Zf31HMv1kpFr23fPG4Y69Wop7pQfLs6rErpIbOHbK/hRI6MSuyT+ZM3njof5oSLVJZg5IH0gasgrrM7/CW9XITM0X0zvRaTleO2ZCLmRDsGmVXCeCL83g/eIzvBSDDCbyun3tRWwEyBXkcIAEZgM5/PepfRjGgSWC9qeuVJjMtKcPASTs2D7+APp+b+5SWA97DrjJxvo3NNjzx/J0LO5L49mESA/v02naMb05jbVU8w== jp@naralabs.com (buster)
```

## Configure static IP

First, identify the ethernet interface on which we will configure static IP
address:

```shell
$ ip -c link show
```

Note down the Debian Linux interface name (eg. `ens192`) and type the
following ip command to see the current IP address assigned to that network
interface:

```shell
$ ip -c addr show ens192
```

The `/etc/network/interfaces` file contains network interface configuration
information for Debian Linux. Hence, edit the file, and properly configure the
interface you identified above. The section for the configuration of the
interface with an static IP should look similar to:

```shell
$sudo nano /etc/network/interfaces
```
```ini
# The primary network interface
auto ens192
iface ens192 inet static
address 192.168.1.100
netmask 255.255.255.0
gateway 192.168.1.1
dns-domain sweet.home
dns-nameservers 8.8.8.8 192.168.1.1
```

Reboot for the changes to take effect:

```shell
$ sudo reboot -h now
```

[debian]: https://www.debian.org/
[debian_releases]: https://www.debian.org/releases/
[debian_lts]: https://wiki.debian.org/LTS
[debian_11]: https://www.debian.org/releases/bullseye/
[debian_11_press_release]: https://www.debian.org/News/2021/20210814
[debian_net installer]: https://www.debian.org/releases/bullseye/debian-installer/
[faq_write_usb]: https://www.debian.org/CD/faq/index.en.html#write-usb
[debian_install_guide]: https://www.debian.org/releases/stable/installmanual
[debian_install_menu]: https://user-images.githubusercontent.com/832627/242884081-afb46732-0fdf-473a-be06-29c0b1f2c046.png
[sudo_command]: https://wiki.debian.org/sudo
[sudo_manpage]: https://manpages.debian.org/bullseye/sudo-ldap/sudo.8.en.html
[adduser_manpage]: https://manpages.debian.org/bullseye/adduser/adduser.8.en.html
[ntp]: https://en.wikipedia.org/wiki/Network_Time_Protocol
[ssh]: https://en.wikipedia.org/wiki/Ssh_(Secure_Shell)
[ssh_keygen_wikipedia]: https://en.wikipedia.org/wiki/Ssh-keygen
[ufw]: https://en.wikipedia.org/wiki/Uncomplicated_Firewall
[secure_channel]: https://en.wikipedia.org/wiki/Secure_channel
[openssh-server]: https://packages.debian.org/bullseye/openssh-server
[ssh-copy-id]: https://manpages.debian.org/bullseye/openssh-client/ssh-copy-id.1.en.html
[postfix]: https://en.wikipedia.org/wiki/Postfix_(software)
[logrotate]: https://linux.die.net/man/8/logrotate
