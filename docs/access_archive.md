All the operations in the database are performed through the **Archive**. This is just a structured database that may use MySQL, PostgreSQL or SQLite as a backend. All the tables are automatically created upon connection when needed.

Note that in order to use the first two, you will need the modules specified in the [installation](index.md#Installation) section.

The Archive is initialized using key-value pairs for each of the connectors available. The keys `db_name` and `db_type` are the only ones that are always necessary, while the rest are directly passed to the connector.

## Using MySQL

Connection to a MySQL database is done through the *PyMySQL* module.

~~~python
from infocards.archive import Archive

arc = Archive(
    db_name='my_db',
    db_type='mysql',
    user='mysql_user',
    password='mysql_password',
    host='mysql_host',
    port=1234
)
~~~

## Using PostgreSQL

Connection to a PostgreSQL database is done through the *psycopg2* module.

~~~python
from infocards.archive import Archive

arc = Archive(
    db_name='my_db',
    db_type='postgres',
    user='postgres_user',
    password='postgres_password',
    host='postgres_host',
    port=1234
)
~~~

## Using SQLite

Connection to a SQLite database is done through the buil-in *sqlite3* module.

~~~python
from infocards.archive import Archive

arc = Archive(
    db_name='/path/to/db',
    db_type='sqlite',
)
~~~
