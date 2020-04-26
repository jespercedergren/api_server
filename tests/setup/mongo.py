from clients.mongo import MongoDBConnectionManager


class MongoDBSetup:
    """
    Class that removes all databases in Mongo.
    """

    def __init__(self, client_arg):

        self.secrets = client_arg

    def reset_db(self):
        primary_dbs = ["admin", "config", "local"]

        with MongoDBConnectionManager(self.secrets) as mongo:
            dbs = mongo.connection.list_database_names()
            remove_dbs = [x for x in dbs if x not in primary_dbs]
            for db in remove_dbs:
                mongo.connection.drop_database(db)
