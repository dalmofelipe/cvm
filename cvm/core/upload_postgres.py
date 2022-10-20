import psycopg2

from cvm.config import settings


conn = psycopg2.connect(
    database=settings.database.name, 
    user=settings.database.user, 
    password=settings.database.password, 
    host=settings.database.host, 
    port=settings.database.port,
    options=settings.database.options,
)

conn.autocommit = True
cursor = conn.cursor()

create_scheme_query = f"""create schema {settings.database.name}"""
#cursor.execute(create_scheme_query)


sql = f'''CREATE TABLE {settings.database.name}.TB_USERS(
    user_id serial,
    user_name char(20),
    user_email varchar(100), 
    user_password varchar(30),
    primary key(user_id)
);'''

#cursor.execute(sql)


sql2 = """INSERT INTO TB_USERS(user_name, user_email, user_password) values 
('Dalmo', 'dalmo@email.com', '123123'),
('Felipe', 'felipe@email.com', '123456'),
('Torres', 'torres@email.com', '654321'),
('Paula', 'paula@email.com', '098098');"""

cursor.execute(sql2)

# sql2 = '''COPY details(user_id,employee_name,\
# employee_email,employee_salary)
# FROM '/private/tmp/details.csv'
# DELIMITER ','
# CSV HEADER;'''
  
# cursor.execute(sql2)

sql3 = f'''select * from {settings.database.name}.TB_USERS;'''
cursor.execute(sql3)
for i in cursor.fetchall():
    print(i)
  
conn.commit()
conn.close()