import os

class SQLiteStorage(object):
	def __init__(self, repo):
		self._import_modules()
		self.repo = repo
		self.dbfn = os.path.join(self.repo, 'pmxbot.sqlite')
		self.db = sqlite.connect(self.dbfn, isolation_level=None, timeout=20.0)
		self.init_tables()

	def init_tables(self):
		pass

	def _import_modules(self):
		try:
			from pysqlite2 import dbapi2 as sqlite
		except ImportError:
			from sqlite3 import dbapi2 as sqlite
		globals().update(sqlite=sqlite)

class MongoDBStorage(object):
	def __init__(self, host_uri):
		# for now do a delayed import to avoid interfering with
		# canonical logging module.
		globals().update(pymongo=__import__('pymongo'))
		self.db = pymongo.Connection(host_uri).pmxbot[self.collection_name]

def migrate_all(source, dest):
	migrate_logs(source, dest)

def migrate_logs(source, dest):
	source_db = botbase.get_logger_db(source)
	dest_db = botbase.get_logger_db(dest)
	for msg in source_db.all_messages():
		dest_db.import_message(msg)