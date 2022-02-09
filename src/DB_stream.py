import pandas as pd
from bioml import DB_connection as DBC
from Data_stream import Data_stream
from psycopg2 import sql
import numpy as np
import psycopg2

class DB_stream(Data_stream):
    """
    DB_stream class can be thought of as an interface for creating a datastream from a DB. It creates a connection
    to the Database and prepares statements to query the DB. The queries can then be initiated
    """
    def __init__(self, gen_params):
        """
        _constructor
        creates a connection to the DB and prepares a query statements according to the given parameters
        :param gen_params: dictonary of parameters needed to connect to DB and to query
        """
        super().__init__()

        params = gen_params["dbparam"]

        self.tbname = gen_params["tbname"]
        self.allchannels = np.append(np.array("index"), gen_params["channels"])
        self.subj = gen_params["subj"]
        self.cdt_nb = gen_params["cdt_nb"]
        self.window_length = gen_params["win_len"]

        engine, conn, cur, exp_info, subj_info = DBC.connect_DB(params)

        self.engine = engine
        self.conn = conn
        self.cur = cur ## Hmmm

        snip = sql.SQL(', ').join(sql.Identifier(n) for n in self.allchannels)

        self.query_statement = sql.SQL(
            "SELECT {0} FROM {1} WHERE subject_id = $1 AND condition  = $2 ORDER BY index DESC LIMIT $3 ").format(
            snip,
            sql.Identifier(self.tbname),
        )
        prepare_statement = "PREPARE myplan AS "

        self.cur.execute(prepare_statement + self.query_statement.as_string(self.cur))





    def get_Window(self):
        """
        Overwritten function from Data_stream that executes the prepared statement with the set parameters.
        :return: A dataframe with the result from the query
        """
        window = pd.read_sql_query("EXECUTE myplan (%s,%s,%s)", self.conn, params = (self.subj, self.cdt_nb, self.window_length))
        return window

    def set_winLen(self, length: int):
        """
        Enables one to set the window_length attribute and therefore change the query statement. Usually this function
        is called from the outside of this class by the RT_Heatmap class for example.
        :param length: window_lenght in number of elements
        :return: No return
        """
        self.window_length = length

    def get_winLen(self):
        """
        Returns the current window length
        :return: window length in number of elements
        """
        return self.window_length










