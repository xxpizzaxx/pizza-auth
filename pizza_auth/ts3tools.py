import ts3
import eveapi
from ldap import MOD_ADD, MOD_DELETE, MOD_REPLACE, TYPE_OR_VALUE_EXISTS
from itertools import chain
import eveapi


# tickers
tickers = {}


def getticker(corp):
	if corp not in tickers:
		api = eveapi.EVEAPIConnection()
		r = api.eve.CharacterID(names=corp)
		i = r.characters[0].characterID
		r = api.corp.CorporationSheet(corporationID=i)
		tickers[corp] = r.ticker
	return tickers[corp]


class ts3manager():
	def __init__(self, config):
		self.config = config["ts3"]

	def modpermissions(self, uid, remove=False, groupid=None):
		if groupid==None:
			groupid = self.config["servergroups"]["full"]
		server = ts3.TS3Server(str(self.config["server"]), self.config["port"])
		server.login(str(self.config["user"]), str(self.config["password"]))
		server.use(1)
		response = server.send_command('clientgetnamefromuid', {'cluid':uid})
		if (response.data)[0] == {'': None}:
			return (False, "User not found in TS3 database")
		dbid = response.data[0]['cldbid']
		groups = server.send_command('servergroupsbyclientid', {'cldbid':dbid})
		print groups.data[0]
		sgid = groups.data[0]['sgid']
		if not remove:
			response = server.send_command('servergroupaddclient', {'sgid':int(groupid), 'cldbid':dbid})
		else:
			response = server.send_command('servergroupdelclient', {'sgid':int(groupid), 'cldbid':dbid})
		print response
		server.disconnect()
		return (True, "Permissions applied")

	def getusersofgroup(self, groupid):
		server = ts3.TS3Server(str(self.config["server"]), self.config["port"])
		server.login(str(self.config["user"]), str(self.config["password"]))
		server.use(1)
		r = server.send_command('servergroupclientlist', {'sgid':groupid}, ["names"]).data
		server.disconnect()
		return r

	def grouplist(self):
		server = ts3.TS3Server(str(self.config["server"]), self.config["port"])
		server.login(str(self.config["user"]), str(self.config["password"]))
		server.use(1)
		r = server.send_command('servergrouplist').data
		results = {}
		for item in r:
			results[item["name"]] = item
		return results


	def update_access_permissions(self, users, group):
		ids = map(lambda x:x.get_ts3ids(), users)
		ids = list(chain(*ids))
		if '' in ids:
			ids.remove('')
		if 'None' in ids:
			ids.remove('None')
		ids = set(ids)
		ts3users = self.getusersofgroup(group)
		moddedids = set(map(lambda x:x['client_unique_identifier'], ts3users))
		purgeme = moddedids - ids
		modme = ids - moddedids
		for i in purgeme:
			print "Purging", i
			self.modpermissions(i, groupid=group, remove=True)
		for i in modme:
			print "Giving rights to", i
			self.modpermissions(i, groupid=group)

	def update_groups(self, users):
		groups = self.grouplist()
		for user in users:
			c = user.corporation[0]
			ticker = getticker(c)
			if ticker in groups:
				print "adding %s to %s ticker" % (user.characterName, ticker)
				for i in user.get_ts3ids():
					self.modpermissions(i, groupid=groups[ticker]["sgid"])
			if ticker in self.config["servergroups"]:
				for i in user.get_ts3ids():
					self.modpermissions(i, groupid=self.config["servergroups"][ticker])
			for authgroup in user.get_authgroups():
				if authgroup in groups:
					for i in user.get_ts3ids():
						self.modpermissions(i, groupid=groups[authgroup]["sgid"])
				if authgroup in self.config["servergroups"]:
					for i in user.get_ts3ids():
						self.modpermissions(i, groupid=self.config["servergroups"][authgroup])




