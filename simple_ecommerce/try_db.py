from sqlalchemy import create_engine
from sqlalchemy.sql import text


e = create_engine('mysql+pymysql://root:admin@localhost/mydb')

statement = text("""
CREATE TABLE product (id MEDIUMINT NOT NULL AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2),
    currency VARCHAR(1),
    description VARCHAR(700),
    image VARCHAR(2084),
    PRIMARY KEY(id));
""")


conn = e.connect()
t = conn.begin()
e.execute(statement)
t.commit()
conn.close()
