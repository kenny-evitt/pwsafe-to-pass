#!/usr/bin/env python
# vim:fileencoding=utf-8

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()


import csv
from subprocess import call
import os



# The following function was copied (but renamed) from [this answer](http://stackoverflow.com/a/35857/173497) to the following Stack Overflow question:
#
# - [shell - How to escape os.system() calls in Python? - Stack Overflow](http://stackoverflow.com/questions/35817/how-to-escape-os-system-calls-in-python)

def bashquote(s):
    return "'" + s.replace("'", "'\\''") + "'"



with open(args.file, 'r') as file:

    next(file) # Skip header row
    reader = csv.reader(file, delimiter='\t')


    for row in reader:

        ( group_title, username, passwd, url, created, passwd_modified, entry_modified, passwd_policy, passwd_policy_name, history, email, symbols, notes ) = row

        group_title = group_title.replace('.', '/')
        group_title = group_title.replace('»', '.')

        notes = notes.replace('»', '\n')


        entry = "{}\n".format(passwd)

        if username:           entry = "{}{}{}\n".format(entry, "Username: ", username)
        if url:                entry = "{}{}{}\n".format(entry, "URL: ", url)
        if email:              entry = "{}{}{}\n".format(entry, "Email: ", email)
        if symbols:            entry = "{}{}{}\n".format(entry, "Symbols: ", symbols)
        if created:            entry = "{}{}{}\n".format(entry, "Created time (pwSafe): ", created)
        if passwd_modified:    entry = "{}{}{}\n".format(entry, "Password last modified time (pwSafe): ", passwd_modified)
        if entry_modified:     entry = "{}{}{}\n".format(entry, "Entry last modified time (pwSafe): ", entry_modified)

        #if passwd_policy:      entry = "{}{}{}\n".format(entry, "Password policy (pwSafe): ", passwd_policy)
        #if passwd_policy_name: entry = "{}{}{}\n".format(entry, "Password policy name (pwSafe): ", passwd_policy_name)

        #if history:            entry = "{}{}{}\n".format(entry, "History: ", history)

        if notes:              entry = "{}{}{}\n".format(entry, "Notes:\n\n", notes)


        print "Adding entry for {}:".format(group_title)

        bash_command = "echo -e {} | pass insert --multiline --force {}".format( bashquote(entry), bashquote(group_title) )
        # The `stdout` argument effectively hides it from being printed when the script is run
        return_code = call(bash_command, executable='/bin/bash', stdout=open(os.devnull, 'wb'), shell=True)


        if return_code == 0:
            print "Added!"
        else:
            print "Failed to add!"
