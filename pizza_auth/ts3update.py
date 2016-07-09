#!/usr/bin/python
import ts3tools, announce
from ldaptools import LDAPTools
from keytools import KeyTools
from ts3tools import ts3manager
import json
import logging
import time
from logging import handlers

# Load configuration
with open("config.json") as fh:
	config=json.loads(fh.read())
assert(config)

# Set up all classes
ldaptools = LDAPTools(config)
keytools = KeyTools(config)
ts3manager = ts3manager(config)


def main():
	# Internal
	internal_group = str(config["ts3"]["servergroups"]["full"])
	users = ldaptools.getusers("accountStatus=Internal")
	if len(users)>0:
		ts3manager.update_access_permissions(users, internal_group)
	# Ally
	ally_group = str(config["ts3"]["servergroups"]["ally"])
	users = ldaptools.getusers("accountStatus=Ally")
	if len(users)>0:
		ts3manager.update_access_permissions(users, ally_group)
	# Internal Groups
	users = ldaptools.getusers("accountStatus=Internal")
	if len(users)>0:
		ts3manager.update_groups(users)


if __name__ == "__main__":
	main()
