import psycopg2
from tests.server.setup import project_dir


class WrongDataBase(Exception):
    pass


class PostgresSetup:
    """
    Class that sets up a connection to a Postgres database using the credentials passed when instantiated, and resets
    the database according to the setup sql script passed in the setup_tables method.
    This class could be used to setup any database.
    """
    def __init__(self, **kwargs):
        self.conn = None
        self.db_credentials = kwargs
        self.connect(**self.db_credentials)

    def connect(self, **kwargs):
        self.conn = psycopg2.connect(**kwargs)

    def close_connection(self):
        self.conn.close()

    def reset_connection(self):
        self.conn.close()
        # start connection
        self.connect(**self.db_credentials)

    def setup_tables(self):
        input_file = project_dir + '/scripts/POSTGRES_DATABASE_SETUP.sql'
        with self.conn.cursor() as cur:
            with open(input_file) as f:
                sql = f.read()

            cur.execute(sql)

        self.conn.commit()

    def reset_db(self):
        # Clear out all database contents
        self.setup_tables()
