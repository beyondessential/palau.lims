# Performance improvement tips

## Introduction

There are several factors that can have an impact to the overall performance of
SENAITE. We can categorize them within the following groups/levels:

- Hardware: number of CPUs, RAM, type of disks (SSD vs HHD), RAID, ...
- Server virtualization: vmware hypervisor, shared resources, ...
- Server baseline configuration: swappiness, partitions distribution, ...
- Zope DB data access strategy: write-intensive vs read-intensive
- SENAITE baseline configuration: clients, zodb-cache-size, zodb-socket, ...
- SENAITE application stack: proxy-cache (nginx), client backends (haproxy), ...
- SENAITE functional usage: users concurrency, types of concurrent tasks, ...
- Environmental: electricity cut-offs frequency, connectivity, ...

The improvement of the performance requires actions to take place for each of 
the abovementioned categories. Is also important that some actions might 
improve the performance at a given category, but might have a bad impact in 
another. Thus, is important to always keep all categories (or levels) in mind 
and find the solution that best fits with our needs. Monitoring the system for
long periods of time while keeping an eye on how the laboratory makes use of 
the system is the best strategy to get insights for performance improvement.

In this document, we will explore several mechanisms/actions that might be
useful for the performance improvement of the system.


## Server baseline configuration

### noatime for filestorage and blobstorage

Linux records information about when files were created and last modified as
well as when it was last accessed (attribute `atime`). There is a cost
associated with recording the last access time. The ext2 file system of Linux
has an attribute (`noatime`) that allows the super-user to mark individual 
files such that their last access time is not recorded. This may lead to 
significant performance improvements on often accessed frequently changing 
files such as the contents of filestorage and blobstorage folders.

```bash
$ cd /home/senaite/data/senaite
$ sudo chattr -R +A filestorage
$ sudo chattr -R +A blobstorage
```

### Swap space

Swap space (SWP) is the portion of virtual memory that is on the hard disk, 
used when RAM is full. Since swap is a special file-backed region in the 
hard-disk for that scratch memory, the I/O access to swap is much slower than 
direct access to RAM. Thus, Swap is crtically important for when RAM is full, 
otherwise the system can become practically unable to execute any task, 
something commonly known as 
*[swap-death](https://en.wikipedia.org/wiki/Paging#Swap_death)*.

You can check the amount of Swap of your system by typing the following:

```bash
$ sudo swapon --show
```

After long periods of uptime, swap space will be used, regardless of how much
available RAM. The Linux Kernel will move memory pages which are hardly ever
used into swap space to ensure that even more cacheable space is made available
in-memory for more frequently used memory pages (a page is a piece of memory).
Swap usage becomes a performance problem when the Kernel is pressured to
continuously move memory pages in and out of memory and swap space.

Swap does not change the amount of RAM required for a healthy server for that
matter. **Swap is designed to be complimentary to performance on healthy
systems**.

To summarize:

- Even if there is still available RAM, the Linux Kernel will move memory pages
which are hardly ever used into swap space.

- It's better to swap out memory pages that have been inactive for a while,
keeping often-used data in cache and this should happen when the server is most
idle, which is the aim of the Kernel.

- Avoid setting your swap space too large if it will result in prolonging
performance issues, outages or your response time.

Although the swap is directly mapped to a logic partition, you can add more
swap by creating a file for this specific purpose. In this example, we will add
5 GB of Swap. First, create the file in which we will store the 5 Gb of swap
and set the correct permissions:

```bash
$ sudo fallocate -l 5G /swapfile
$ sudo chmod 600 /swapfile
```

Use the `mkswap` tool to set up a Linux swap area on the file:

```bash
$ sudo mkswap /swapfile
$ sudo swapon /swapfile
```

and make the change permanent in `/etc/fstab`:

```
/swapfile swap swap defaults 0 0
```

More info:
- [Linux Performance: Why You Should Almost Always Add Swap Space, Hyden James](https://haydenjames.io/linux-performance-almost-always-add-swap-space/)
- [Swap Management (kernel_dos)](https://www.kernel.org/doc/gorman/html/understand/understand014.html)
- [Page Frame Reclamation (kernel docs)](https://www.kernel.org/doc/gorman/html/understand/understand013.html)

### Swappiness

**Swappiness** is a Linux kernel property that defines how often the system 
will use the swap space. Swappiness can have a value between 0 and 100. A low 
value will make the kernel to try to avoid swapping whenever possible while a
higher value will make the kernel to use the swap space more aggressively.

System tries to reach the proportions of usage between RAM and Swap based on 
the Swappiness value:

- Swappiness 0: RAM 100% – SWAP 0%
- Swappiness 20: RAM 80% – SWAP 20%
- Swappiness 60: RAM 40% – SWAP 60%
- Swappiness 100: RAM 0% – SWAP 100%

For instance, a value of swappiness of 100 means that the system will try to
keep as much RAM free as possible and will try to write to disk all that is not
being used at a given time. Setting a swappiness value of 0 is not recommended,
cause there are performance benefits when swap is enabled, even when there is
more than enough RAM.

The default swappiness value in Linux systems is 60. While this value is OK for
desktop systems and/or for systems with <1 GB RAM, for production servers we
suggest to set this value to 10. We suggest to apply changes to this value
gradually while monitoring the system.

You can check the current swappiness value by typing the following command:

```bash
$ cat /proc/sys/vm/swappiness
```

To set the swappiness value to 10, type:

```bash
$ sudo sysctl vm.swappiness=10
```

To make this parameter persistent across reboots append the following line to
the `/etc/sysctl.conf` file:

```
vm.swappiness=10
```

More info:
- [Linux Performance: Why You Should Almost Always Add Swap Space, Hyden James](https://haydenjames.io/linux-performance-almost-always-add-swap-space/)


## SENAITE and Zope baseline

Zope is the application server that runs SENAITE. In combination with ZEO, user
experience mostly hinges on proper performance tuning of the Zope-ZEO combo.
Unfortunately, Zope/ZEO tuning is not an exact science. Optimal performance
might require several iterations.

### Socket as zeo-address

By default, clients communicate with through a TCP/IP connection, that is
defined in parameter `zeo-address`, that is declared in buildout's `zeoserver`
and `client_base` parts. Nevertheless, ZEO supports a full path to a socket
instead of an url. Let Zope clients communicate with ZEO over a socket, so at
least no overhead as through the TCP connection.

```buildoutcfg
[buildout]
zeo-socket = ${buildout:directory}/var/zeo.socket
...
[zeoserver]
zeo-address = ${buildout:zeo-socket}
...
[client_base]
zeo-address = ${buildout:zeo-socket}
...
```

### zodb-cache-size

`zodb-cache-size` refers to the number of objects a given ZEO client will keep
in RAM. So, when a thread from a ZEO client requests objects to ZEO server, the
latter queries against ZODB and returns back the data requested. ZEO client
then aggressively caches the returned objects in RAM. As soon as the number of
objects in memory reaches the limit defined by `zodb-cache-size`, ZEO client
automatically allocates space for newest objects by removing oldest ones from
cache. Thus, this setting allows to reduce the number of calls to ZEO server 
and therefore, disk reads from ZODB.

Please note that the cache-size setting actually specifies the number of
objects. This means that it might be difficult to gauge how much memory will
actually be consumed. This can only be determined after Zope has been running
by actually looking at ps/top output. For instance, a Sample object weights
more in RAM than a Method object, cause the former contain more attributes, 
etc.

Also, keep in mind that `zodb-cache-size` refers to the number of objects each
thread from a given ZEO client will store in cache. Basically, the number of
threads specifies how many requests one ZEO client can handle. By default, the
number of threads per ZEO client (`zserver-threads` directive) is set to 2.

All this means that with a `zodb-cache-size` value of 10000 and a
`zserver-threads` value of 2, the ZEO client will cache 2 x 10000 = 20000
objects in RAM at maximum.

We can consider two types of ZEO clients: specialized clients (e.g. for running
very specific tasks) or generalist clients (for running general and
heterogeneous tasks like querying, creating samples, etc.). The redirection of
requests to specialized or generalist ZEO clients is done by Haproxy. Having
ZEO clients for different purposes means that the value for `zodb-cache-size`
for each client might be different too.

In our experience, we've found that more or less, 100k cached objects = ~5G 
RAM.

- 3 generalist ZEO clients, 2 threads each = 3 * 5 * 2 = ~30 GB RAM
- 5 specialist ZEO clients, 2 threads each = 5 * 0.5 * 2 = ~5 GB RAM

The RAM consumption of other services have to be added here though (ZEOServer
~ 5 GB, nginx ~1 GB, kernel pages, etc.). With this configuration, we need at
least 45 GB of RAM, but we recommend 50 GB minimum to allocate additional RAM 
for other tasks like backups, reserved clients, zeopacks, etc.
