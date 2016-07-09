#!/usr/bin/env python


## Config
"""
{
	"auth": {
		"alliance": "Confederation of xXPIZZAXx",
		"allianceshort": "PIZZA",
		"domain": "xxpizzaxx.com"
	},
	"pingbot": {
		"username": "",
		"passwd": "",
		"domain": "xxpizzaxx.com"
	},

	"keytools": {
		"executorkeyid": "",
		"executorkeyvcode": "",
		"alliancelimit": 4.9
	},

	"groups": {
		"closedgroups": [
			"admin",
			"ping",
			"capital",
			"timerboard"
		],
		"opengroups": [
			"social",
			"dota"
		],
		"publicgroups": [
			"dota"
		]
	},
	"ts3": {
		"user": "serveradmin",
		"password": "",
		"server": "localhost",
		"port": 10011,
		"servergroups":	{
			"full": "7",
			"ally": "14",
			"none": "8"
		}
	},

	"ldap": {
		"server": "ldap://localhost/",
		"admin": "cn=admin,dc=yoursite,dc=com",
		"password": "",

		"basedn": "dc=yoursite,dc=com",
		"memberdn": "ou=People,dc=yoursite,dc=com",
		"groupdn": "ou=Groups,dc=yoursite,dc=com"
	},

	"skillindexer": {
		"server": "localhost",
		"user": "",
		"password": "",
		"database": ""
	},
	"mumble": {
		"server": "mumble.yoursite.com"
	},
	"reddit": {
		"comment": "REMOVE ENTIRE SECTION IF YOU'RE NOT USING REDDIT VERIFICATION",
		"clientname":	"",
		"clientid": 	"",
		"clientsecret":	"",
		"redirect_base": "http://host:port",
		"statekey":	""
	},
	"apikeys": [
		"REMOVEME"
		],
	"jabber": {
		"admins": [
			"lucia_denniard"
			]

	}
}
"""
## Wizard

import locale, dialog
from dialog import Dialog
import sys

config = {}

locale.setlocale(locale.LC_ALL, '')

d = Dialog(dialog="dialog")
d.set_background_title("pizza-auth configuration wizard")

d.msgbox("Welcome to the configuration interface for pizza-auth.")

config["auth"] = {}

code, tag = d.menu("Are you running this for a corp or alliance?",
		choices = [("1.", "Corporation"),
			   ("2.", "Alliance")])
if code != d.OK:
	sys.exit()

if tag == "1.":
	mode = "corp"
	config["auth"]["corp"] = d.inputbox("What is your corporation's name?")
	config["auth"]["allianceshort"] = d.inputbox("What is your corporation's ticker?")

elif tag == "2.":
	mode = "alliance"
	config["auth"]["alliance"] = d.inputbox("What is your alliance's name?")
	config["auth"]["allianceshort"] = d.inputbox("What is your corporation's ticker?")


