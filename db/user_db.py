import config
import psycopg2
import psycopg2.extras

try:
    with psycopg2.connect(
            host=config.hostname,
            dbname=config.database,
            user=config.admin_name,
            password=config.password,
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            command = ''
            create_script = '''
                CREATE TABLE IF NOT EXISTS all_users(
                name varchar,
                email varchar,
                phone varchar
                )
            '''
            cur.execute(create_script)
            cur.execute('SELECT * FROM all_users')


            def printall():
                for record in cur.fetchall():
                    print(record['name'], record['email'], record['phone'])
                return None


            def add_user(name, email, phone):
                insert_script = 'INSERT INTO all_users (name, email, phone) VALUES (%s, %s, %s)'
                cur.execute(insert_script, (name, email, phone))
                print(f'{name} added')

except Exception as error:
    print(error)
