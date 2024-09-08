from sqlalchemy import create_engine,text, MetaData, Table,update,func
from sqlalchemy.orm import registry, Session, mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
Base = automap_base()
dbEngine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)
metadata = MetaData()
session = Session(dbEngine)
conn = session.bind
InitDF = Table('init_df', metadata, autoload=True,
               autoload_with=dbEngine)
Base.prepare(dbEngine, reflect=True)
update(InitDF).where(InitDF.c.S_level == "Этаж 01").values(test_column1='user #5')
session.commit()
session.close()

customer1 = session.query(InitDF, func.sum(InitDF.c.S_area)).where(InitDF.c.S_level == "Этаж 01").group_by(
	InitDF.c.E_ex_name).all()
print(pd.DataFrame(customer1))