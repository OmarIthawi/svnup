svnup
=====

FTP upload based on SVN changes. It's a tool I use to have the luxury of SCM on
old-fashioned ftp-enabled web hosts.

Setup
-----
This is meant to be used on Ubuntu 12.04 but mostly it's portable even to 
windows.

You'll need curl and subversion, of course: 

```
$ sudo apt-get install curl subversion
```

Usage
-----
Change the variable `sites` in `svnup.py` to contain your ftp connection 
information.

Then run the script by:  

```
$ python svnup.py site-name "Commit message"
```

TODO
----
 - Place configs in a separate file.
 - Handle svn conflicts and status other than `M` and `A` properly.

