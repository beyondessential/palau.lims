# Frequently Asked Questions (FAQs)

## How to get the password for admin user

You can get the password for `admin` user with the following command:

```bash
$ cd /home/senaite/senaite
$ cat live.cfg | grep user=
```

You should get an output similar to:

```
senaite@senaite:~/senaite$ cat live.cfg | grep user=
user=admin:<admin_password>
```

where `<admin_password>` is the password for `admin` user.


## How to manually reset the password of a given user

Login with `admin` user ([FAQ: How to get the password for admin user](#how-to-get-the-password-for-admin-user)),
go to "Site Setup > Zope Management Interface > acl_users > source_users", look
for the username and press the `Password` link next to it. Type the new 
password and Save.

## How to deploy/run bin/buildout

Stop all instances:

```bash
$ sudo supervisorctl stop all
```

Run bin/buildout

```bash
$ cd ~/senaite
$ bin/buildout -c live.cfg
```

Restart/restore the senaite app stack:

```bash
$ sudo service supervisor reload
$ sudo service haproxy restart
$ sudo service nginx restart
```

## How to check which clients are running

You can check which clients are running either by using supervisor's web 
interface or by using the following command:

```bash
$ sudo supervisorctl status
```

## How to check the log of a client

Clients logs are located at `/home/senaite/data/senaite/client*`. For instance,
to follow the log of `client1` at real-time, you can do the following:

```bash
$ cd ~/data/senaite
$ tail -f client1/event.log
```

**Tip**: you can use [multiple terminals](#how-to-enable-multiple-terminals) to
have multiple tabs in terminal. For instance, imagine you want to keep track of
logs from multiple zeo clients at same time you want to have a terminal 
available to do other tasks.

## How to enable multiple terminals

Allows you to have multiple terminals available in a single SSH session:

```bash
$ byobu
```

You can create more tabs with F2 and you can navigate across them with F3 (left)
and F4 (right).

## How to get the full traceback of an error log entry

Sometimes, when an error happens, users without administration privileges cannot
see the full stack trace of the error. Rather, a message like follows is 
displayed:

```
We're sorry, but there seems to be an error ...

The error has been logged as entry number 1574751866.520.0788186283412
```

To get the full traceback of this error, you need to login with `admin` user 
([FAQ: How to get the password for admin user](#how-to-get-the-password-for-admin-user))
and go to "Site Setup > Zope Management Interface" and then press the link
`error_log`. A view with the list of the most recent error logs will be
displayed. This list displays the error logs registered from the current client
you are connected to, so you might need to change the port of the url to see the
log you are looking for.

Click to the description of the error log from the list to get the full
traceback. For instance, for the error entry with the number above 
`1574751866.520.0788186283412`, you would get:

```
Time 	2019/11/26 09:04:26.523564 GMT+2
User Name (User Id) 	John Doe (john doe)
Request URL 	https://127.0.0.1/worksheets/worksheet_add
Exception Type 	KeyError
Exception Value 'The ID WS19-3788 is already taken in the path /senaite/worksheets'

Traceback (innermost last):

    Module ZPublisher.Publish, line 138, in publish
    Module ZPublisher.mapply, line 77, in mapply
    Module ZPublisher.Publish, line 48, in call_object
    Module Products.Archetypes.BaseObject, line 636, in processForm
    Module bika.lims.content.worksheet, line 145, in _renameAfterCreation
    Module bika.lims.idserver, line 556, in renameAfterCreation

KeyError: 'The ID WS19-3788 is already taken in the path /senaite/worksheets'
```
