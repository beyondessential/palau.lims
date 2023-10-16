# Setup a development environment


SENAITE is an Add-on for the [Plone Content Management Framework][PLONE] and the
installation instructions depend therefore mostly on the successful
[installation of Plone][PLONE-installation].

## Operating system

We recommend installing SENAITE on [Ubuntu][UBUNTU] or [Debian][DEBIAN] Linux.
Installation on MacOS works as well, but needs additional packages installed
via [Homebrew][HOMEBREW].

In this secion we will mostly use **Ubuntu 18.04 LTS** as reference system.

The installation on other Linux distributions, MacOS or Windows is not covered here.


## A note about Versions

The current codebase of SENAITE is at the moment only compatible with the latest
version 5 of Plone.

**☝️Note:**
**This version of Plone works only with [Python][PYTHON] 2.x.**


## Python

Most UNIX based operating system (Linux/Mac OSX) ship already with a Python
interpreter installed. However, it is not recommended to use the system
interpreter to setup and install SENAITE on the local system.

Besides the required super-user permissions for installing additional Python
libraries is that it might get upgraded by the system and get incompatible.

Therefore, it is better to setup a virtual Python environment with one of the
following tools:

  - Virtualenv: <https://pypi.org/project/virtualenv>
  - Miniconda: <https://conda.io/miniconda.html>

In this manual we will use **Miniconda**.


## Create a new User

Create a new user `senaite` in your system with the following command:

```shell
$ sudo adduser --home /home/senaite --shell /bin/bash senaite
```

And make sure you became this user within the following sections:

```shell
$ sudo su - senaite
$ whoami
senaite
```


## Miniconda

Download and install the `Python 2.7` version for your operating system:

```shell
$ wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
$ bash /home/senaite/Miniconda2-latest-Linux-x86_64.sh
$ source /home/senaite/.bashrc
```

*You can accept the default settings of the miniconda installer*

Create a new Python environment with the name `senaite`:

```shell
$ conda create --name senaite python=2.7
```

Activate the Python environment:

```shell
$ conda activate senaite
```

The command `which python` can be used to check if the right Python interpreter
is active in the current session:

```shell
$ which python
/home/senaite/miniconda2/envs/senaite/bin/python
```

```shell
$ python
Python 2.7.17 |Anaconda, Inc.| (default, Oct 21 2019, 19:04:46)
[GCC 7.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```


## Install System dependencies

Install the required dependencies for SENAITE:

```shell
$ sudo apt install build-essential
$ sudo apt install python2.7 python2.7-dev
$ sudo apt install libxml2 libxml2-dev libxslt1.1 libxslt1-dev
$ sudo apt install libffi-dev libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0
$ sudo apt install zlib1g zlib1g-dev
```


## Download the Plone unified installer

The [Plone Unified Installer][PLONE-unified-installer] installs Plone and its
dependencies from source on most Unix-like platforms.

```shell
$ wget --no-check-certificate https://launchpad.net/plone/5.2/5.2.14/+download/Plone-5.2.14-UnifiedInstaller-1.0.tgz
$ tar xzf Plone-5.2.14-UnifiedInstaller-1.0.tgz
$ cd Plone-5.2.14-UnifiedInstaller
```

## Install Plone

Next step is to install Plone with the provided `install.sh` shell script:

```shell
$ ./install.sh standalone --target=/home/senaite --instance=senaitelims --password=admin
```

**☝️Note:**
We install SENAITE in the directory `/home/senaite/senaitelims` and we have set
the admin password to `admin`

## Install SENAITE

To install SENAITE we need to modify the generated `buildout.cfg` config file.
[Buildout][BUILDOUT] is an automation tool written in and extended with Python:

```shell
$ cd /home/senaite/senaitelims
$ vim buildout.cfg
```

**☝️Note:**
You can use `nano` or any other text editor you feel comfortable with

Add `extensions` section before the `eggs` section of the file:

```config
[buildout]
...

extensions =
    mr.developer

always-checkout = true

eggs =
    ...
...
```


Add `palau.lims`, `plone.reload` and `Products.PrintingMailHost` to the `eggs` 
section of the file:

```config
[buildout]
...
eggs =
    ...
    palau.lims
    plone.reload
    Products.PrintingMailHost

zcml =
...
```

Add a `develop` and `sources` sections after `eggs` section:

```config
[buildout]
...
eggs =
    ...
    palau.lims
    plone.reload
    Products.PrintingMailHost

develop =
    src/palau.lims
    src/senaite.core
    src/senaite.core.listing
    src/senaite.core.spotlight
    src/senaite.core.supermodel
    src/senaite.impress
    src/senaite.jsonapi
    src/senaite.lims

[sources]
palau.lims = git git@github.com:beyondessential/palau.lims.git branch=master
senaite.core = git git@github.com:senaite/senaite.core.git branch=2.x
senaite.core.listing = git git@github.com:senaite/senaite.core.listing.git branch=2.x
senaite.core.spotlight = git git@github.com:senaite/senaite.core.spotlight.git branch=2.x
senaite.core.supermodel = git git@github.com:senaite/senaite.core.supermodel.git branch=2.x
senaite.impress = git git@github.com:senaite/senaite.impress.git branch=2.x
senaite.jsonapi = git git@github.com:senaite/senaite.jsonapi.git branch=2.x
senaite.lims = git git@github.com:senaite/senaite.lims.git branch=2.x

zcml =
...
```

Modify the `versions` section of the file as follows:

```shell
[versions]
zc.buildout =
setuptools =
#Pillow = 5.1.0
#cssselect2 = 0.2.2
#soupsieve = 1.9.5

#buildout.sanitycheck = 1.0.2
#collective.recipe.backup = 4.0
#plone.recipe.unifiedinstaller = 4.3.2
```

**☝️Note:**
The version unpinning of `zc.buildout` and `setuptools` is important!


### Upgrade pip, setuptools and zc.buildout

We need to ensure that `pip`, `setuptools`, and `zc.buildout` are available in a
compatible version:

Create a `requirements.txt` file:

```shell
$ cd /home/senaite/senaitelims
$ cat << EOF > requirements.txt
setuptools==39.2.0
zc.buildout==2.13.2
pip==19.3.1
EOF
```

Install the requirements with the `pip` command of the local Python environment:

```shell
$ which pip
/home/senaite/miniconda2/envs/senaite/bin/pip

$ pip install -r requirements.txt
```

**☝️Note:**
A wrong version of `setuptools` can lead to the infamous 
[Error while buildout: There is a version conflict. We already have: UNKNOWN 0.0.0](https://github.com/senaite/senaite.lims/issues/106)

Re-run the `buildout` script:

```shell
$ which buildout
/home/senaite/miniconda2/envs/senaite/bin/buildout
$ PYTHONHTTPSVERIFY=0 buildout
```

## Further links

- https://github.com/senaite/senaite.lims#readme
- http://www.buildout.org/en/latest/
- https://setuptools.readthedocs.io/en/latest
- https://docs.conda.io/en/latest/miniconda.html


## Starting SENAITE

After the `buildout` command of the previous step returned without errors, you
can start SENAITE from the terminal.

To start SENAITE in foreground (debug) mode, use this command:

```shell
$ bin/instance fg
```

To stop the server, you can press `CTRL+C` on your keyboard.

**Note**
You can also start SENAITE in the background (production) mode with the command
`bin/instance start` and stop it again with `bin/instance stop`.


This will print several logs to the terminal and notifies when the server is ready with the line:

```log
2019-09-14 09:59:44 INFO Zope Ready to handle requests
```

Open a browser (Safari/Chrome/FireFox ...) and navigate to http://localhost:8080
and log in with `admin:admin` to proceed to the next page.

You can continue with the default settings and press the *Install SENAITE LIMS* button.
After a few moments, SENAITE should be installed and the dashboard view appears.
Go to "Site Setup > Add ons", select `PALAU LIMS` and press install.


[PLONE]: https://plone.org  "The Ultimate Enterprise CMS"
[PLONE-installation]: https://docs.plone.org/4/en/manage/installing/installation.html#how-to-install-plone  "How to install Plone 4"
[PYTHON]: https://www.python.org   "Python Programming Language"
[DEBIAN]: https://www.debian.org/distrib/netinst  "Debian Linux"
[UBUNTU]: https://ubuntu.com/download/server   "Ubuntu Linux"
[HOMEBREW]: https://brew.sh "The missing package manager for macOS (or Linux)"
[PLONE-unified-installer]: https://github.com/plone/Installers-UnifiedInstaller  "Plone Unified Installer"
[BUILDOUT]: http://www.buildout.org/en/latest/  "Buildout, an automation tool written in and extended with Python"
