#!/usr/bin/python
from sys import argv
from os import path
import os
from subprocess import Popen, PIPE, call
from multiprocessing.pool import ThreadPool

sites = {
    "SITENAME": {
        "localdir": "/var/www/PROJECT",
        "remotedir": "/",
        "host": "SERVER",
        "username": "USERNAME",
        "password": "PASSWORD",
    }
}

settings = {
    "concurrentConnections": 7
}


def svnup(site, commitmessage):
    svn = Popen(['svn', 'status'], cwd=site['localdir'], stdout=PIPE, stderr=PIPE)
    
    
    files = []
    for line in svn.stdout.readlines():
        lineprefix = 'A  +    '
        
        if line.startswith('M') or line.startswith('A'):
            line = line[len(lineprefix):]
            line = line.rstrip('\r').rstrip('\n')
            files.append(line)
        elif (line.startswith('?') 
              or line.startswith('C') 
              or line.startswith('!')):
            call(['svn', 'status'], cwd=site['localdir'])
            exit(1)

    if len(files):
        print 'Uploading: ', '\n'.join(files)
    else:
        print 'Nothing to Update'
        call(['svn', 'status'], cwd=site['localdir'])
        exit(0)
    
    stdout, stderr = svn.communicate()
    
    if stderr:
        print stderr
        exit(1)
    
    def upload(filename):
        remotefilename = path.join(site['remotedir'], filename)
        remoteaddress = 'ftp://%s%s' % (site['host'], remotefilename)
        
        if not path.isdir(filename):
            print 'Uploading: \n', filename
            exitcode = call(['curl',
                  '--progress-bar',
                  '-T', filename, 
                  '--ftp-create-dirs',
                  '--user', '%s:%s' % (site['username'], site['password']),
                  remoteaddress],
                  cwd = site['localdir'])
            
            print ''
            if exitcode:
                print 'Error in uploading "%s"' % filename
                print 'Destenation is "%s"' % remoteaddress
                exit(1)
    
    pool = ThreadPool(settings['concurrentConnections'])
    pool.map(upload, files)
    
    
    for filename in files:
        upload(filename)

    
    call(['svn', 'commit', '-m', commitmessage], cwd=site['localdir'])

    
try:
    svnup(sites[argv[1]], argv[2])
except IndexError:
    print '$ %s sitename commit-message' % path.basename(__file__)
    print 'Sites are: ', sites.keys()





