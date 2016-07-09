#!/usr/bin/python
import announce
from ldaptools import LDAPTools
from keytools import KeyTools
import json
import logging
import time
from logging import handlers
from ldap import MOD_ADD, MOD_DELETE, MOD_REPLACE, TYPE_OR_VALUE_EXISTS

# Load configuration
with open("config.json") as fh:
	config=json.loads(fh.read())
assert(config)

# Set up all classes
ldaptools = LDAPTools(config)
keytools = KeyTools(config)

if "ts3" in config:
	from ts3tools import ts3manager
	ts3manager = ts3manager(config)

safecharacters = ["twistedbot", "pingbot"]

def update_characters(characters=None):
	logger = logging.getLogger("updateusers")
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler("./logs/updateusers_%d.log" % time.time())
	formatter = logging.Formatter('%(asctime)s - %(message)s')
	fh.setFormatter(formatter)
	logger.addHandler(fh)

	ldap_characters = []
	if characters is not None:
		for character in characters:
			ldap_characters.append(ldaptools.getuser(character))
	else:
		ldap_characters = ldaptools.getusers("objectclass=xxPilot")

	for character in ldap_characters:
		try:
			characters = keytools.getcharacters(character.keyID, character.vCode)
			characters = json.dumps(characters, default=lambda x:x.__dict__)
			characters = json.loads(characters)
			results = {}
			for char in characters:
				r = {}
				for col, row in zip(char["_cols"], char["_row"]):
					r[col] = row
				r["result"] = char["result"]
				if "allianceID" in char:
					r["allianceID"] = char["allianceID"]
					r["allianceName"] = char["allianceName"]
				else:
					r["allianceID"] = ""
					r["allianceName"] = ""
				results[r["name"]] = r
			assert(character.characterName[0] in results)
			newcharacter = results[character.characterName[0]]
			if character.accountStatus[0] != newcharacter["result"]:
				logger.info( "%s status update \t %s -> %s" % ( character.get_id(), character.accountStatus[0], newcharacter["result"]) )
				ldaptools.modattr(character.get_id(), MOD_REPLACE, "accountStatus", newcharacter["result"])

			create = False
			if not hasattr(character, "alliance"):
				create = True
				character.alliance = [""]
			if character.alliance[0] != newcharacter["allianceName"]:
				logger.info( "%s alliance update \t %s -> %s" % ( character.get_id(), character.alliance[0], newcharacter["allianceName"]) )
				if create:
					try:
						ldaptools.modattr(character.get_id(), MOD_ADD, "alliance", newcharacter["allianceName"])

					except TYPE_OR_VALUE_EXISTS:
						# Sneaky devil
						# alliances can change
						ldaptools.modattr(character.get_id(), MOD_REPLACE, "alliance", newcharacter["allianceName"])
				else:
					ldaptools.modattr(character.get_id(), MOD_REPLACE, "alliance", newcharacter["allianceName"])
			if character.corporation[0] != newcharacter["corporationName"]:
				logger.info( "%s corp update \t %s -> %s" % ( character.get_id(), character.corporation[0], newcharacter["corporationName"]) )
				ldaptools.modattr(character.get_id(), MOD_REPLACE, "corporation", newcharacter["corporationName"])

		except RuntimeError:
			if ("Expired" not in character.accountStatus) and (character.get_id() not in safecharacters):
				logger.warn( "%s status update \t %s -> %s" % ( character.get_id(), character.accountStatus[0], "Expired") )
				ldaptools.modattr(character.get_id(), MOD_REPLACE, "accountStatus", "Expired")
		except AssertionError:
			logger.error("%s is not on this account" % character.characterName[0])


if __name__ == "__main__":
	update_characters()
