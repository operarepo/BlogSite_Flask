from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine


# app.config['SQLALCHEMY_DATABASE_URI'] = 
# db = SQLAlchemy(app)

session = create_engine('sqlite:///site.db', echo=True)
metadata_obj = MetaData()

# Base.metadata.create_all(session)
if 'users' not in inspector.get_table_names():
    users_table = Table(
        'users',
        metadata_obj,
        Column('id', Integer, primary_key=True),
        Column('name', String(30)),
        Column('age', Integer),
    )
metadata_obj.create_all(session)
