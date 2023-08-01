from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, Session
import pandas as pd

class QueryToDataFarame:
    def __init__(self,engine) -> None:
        """create data frame from SQL Query
        Args:
            engine (_type_): _description_
        """
        self.session = Session(engine)
        self.engine = engine

    def join_query_to_df(self,class_1:declarative_base, class_2:declarative_base,columns_names:list):
        """joined queres(inner join) and filtred columns in result pd.DataFrame for representation """
        q = self.session.query(class_1, class_2)
        q = q.join(class_2)
        df = pd.read_sql(q.statement, con=self.engine)
        if columns_names:
            df = df[columns_names]
            df = df.assign(Action="")
            return df
        else:
            df = df.assign(Action="")
            return df

    def query_to_pd_df(self,db_class,columns=None):
        """read query and transform to df. columns -filtred columns. Defualt -all columns

        Args:
            query (_type_): _description_
            columns (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
            
        """
        query_ = self.session.query(db_class)
        df = pd.read_sql(query_.statement, con=self.engine)
        df = df.assign(Action="")
        if columns:
            df = df[columns]
        return df
    def model_get_val(self,db_class):
        """
        get data base and convert it to pandas df.
        """
        q = self.session.query(db_class)
        col = q.statement.columns.keys()
        all_q = q.all()
        val = []
        for k in col:
            temp = [getattr(c, k) for c in all_q]
            val.append(temp)
        d = dict(zip(col, val))
        df = pd.DataFrame(data=d)
        df['add_date'] = df['add_date'].astype(
            'datetime64[ns]').dt.strftime('%Y-%m-%d')
        df["Action"] = ""
        return df


    def get_model_columns(self,db_class):
        columns = self.session.query(db_class).statement.columns.keys()
        return columns


    def get_model_data(self,db_class):
        db_data = self.session.query(db_class).all()
        return db_data