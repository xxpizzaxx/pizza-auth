#!/usr/bin/python
import ts3tools, announce
from ldaptools import LDAPTools
from keytools import KeyTools
import json
import logging
import time
from logging import handlers
from ldap import MOD_ADD, MOD_DELETE, MOD_REPLACE

# Load configuration
with open("config.json") as fh:
	config=json.loads(fh.read())
assert(config)

# Set up all classes
ldaptools = LDAPTools(config)


if __name__ == "__main__":
	logger = logging.getLogger("buildgroups")
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler("./logs/buildgroups_%d.log" % time.time())
	formatter = logging.Formatter('%(asctime)s - %(message)s')
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	allgroups = config["groups"]["opengroups"] + config["groups"]["closedgroups"]
	for group in allgroups:
			members = ldaptools.getusers("authGroup=%s" % group)
			if not members:
						continue
			attrs = {}
			attrs["cn"] = str(group)
			attrs["description"] = str(("Autogenerated %s group") % group)
			attrs["member"] = map(lambda x: str(("uid=%s,%s") % (x.uid[0], config["ldap"]["memberdn"])), members)
 			try:
 		 				ldaptools.deletegroup(group)
 			except:
 		 				pass
 			finally:
 		 				ldaptools.addgroup(attrs)