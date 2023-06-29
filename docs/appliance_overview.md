# Virtual Appliance overview

At Naralabs, we have elaborated a [Virtual appliance][virtual_appliance] 
containing a full application stack on top of trusted, robust and secure 
technologies. This virtual appliance contains `palau.lims`, your extension 
profile for [SENAITE LIMS][senaite_lims], that can be fully customized to make
the system to meet your present and future needs.

> **Warning**
> If you haven't received the Virtual appliance, together with the source code
> of your extension profile, please send an e-mail to info@naralabs.com with 
> the subject "Virtual appliance request".

Having a Virtual Appliance with all in place makes the deployment of
full-fledged instances of SENAITE easier, cause makes the system independent of
infrastructure and there is only the need to have a host with a virtualization
software ([hypervisor][hypervisor]) suitable for productive environments 
installed.

This virtual appliance is built on top of a [minimal installation of a Debian
 Operating System][senaite_os]. The SENAITE instance, as well as the rest of
tools shipped with the virtual appliance, have been deployed with 
[Red Hat Ansible][red_hat_ansible]. The Ansible recipe is included with this
extension profile, inside `ansible` folder.

> **Note**
> Instructions on how to create the virtual appliance or deploy the system
> from scratch by using the Ansible recipe are provided too. Check
> [Deployment of the application stack with Ansible][deployment_ansible] for
> detailed information.


Technical details
-----------------

The virtual appliance is shipped as an 
[Open Virtualization Format (OVF/OVA)][ovf], an open, secure, portable, 
efficient and extensible format for the packaging and distribution of software 
to be run in virtual machines. This guarantees it can be deployed in most (if 
not all) hypervisors.

The following are the settings of the virtual appliance:

* Debian 11 (bullseye) x64
* Hard disk: VM_HARD_DISK
* Processor: VM_PROCESSOR_CORES
* RAM: VM_RAM_SIZE
* Language: English
* Location: TIMEZONE
* Networks:
  * Adapter 1 (enp0s3): NAT (dynamic assigned over DHCP)
  * Adapter 2 (enp0s8): host-only (vboxnet0, static 192.168.33.10)
* Hostname: senaite-buster
* Username: senaite
* Automatic security updates: enabled
* HTTP/S Server: nginx (ports 80 and 443)
* HTTPS SSL: self-signed certificate
* TCP/HTTP Load Balancer: HAProxy (frontend port: 8080, status port: 9002)
* Process Control System: supervisor (port 9001)
* Monitoring: Munin (port 9003)
* Fireall: Ufw
* Open Ports: 22, 80, 443
* System's SENAITE User: senaite
* System's SENAITE Daemon User: senaite_daemon
* SENAITE Installation Root: /home/senaite/senaite
* Database: /home/senaite/data/senaite/*storage
* Backups: /home/senaite/data/senaite/*backups
* Zeo Server: 127.0.0.1:8100
* Zeo client 1: 127.0.0.1:8081
* Zeo client 2: 127.0.0.2:8082

SENAITE instance is installed at `/home/senaite/senaite` and database files
at `/home/senaite/data`. User `senaite_daemon` is the effective user that runs
the instance.

Network
-------

The appliance has two network interfaces enabled. The first one (`enp0s3`) is a
NAT, with dynamic assignment of IP over DHCP. The second is a host-only 
interface (`enp0s8`), with an static IP `192.168.33.10`.

Backups
-------

The system has been configured with two [cron][cron] jobs (run by 
`senaite_daemon`):

- `zeopack`: every day at 3:00 AM
- `backup`: every day at 7:00 PM

Backups are stored in `/home/senaite/data/backups`, but system is configured to
keep the last 5 backups of metadata (from filestorage) and last 5 days of 
blobs (from blobstorage). Hence, is strongly recommended to setup a 
[rsync][rsync] script in another machine to grab the backups  from the server
on a regular basis.


[senaite_lims]: https://www.senaite.com
[senaite_os]: senaite_os.md
[virtual_appliance]: https://en.wikipedia.org/wiki/Virtual_appliance
[hypervisor]: https://en.wikipedia.org/wiki/Hypervisor
[red_hat_ansible]: https://www.ansible.com/
[deployment_ansible]: ansible.md
[ovf]: https://en.wikipedia.org/wiki/Open_Virtualization_Format
[cron]: https://en.wikipedia.org/wiki/Cron
[rsync]: https://en.wikipedia.org/wiki/Rsync
