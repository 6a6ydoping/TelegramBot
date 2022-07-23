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
            def create_db():
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


            def add_user(user_array_info):
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    print('start of add_user')
                    name, phone, email = user_array_info[0], user_array_info[1], user_array_info[2]
                    insert_script = 'INSERT INTO all_users (name, phone, email) VALUES (%s, %s, %s)'
                    cur.execute(insert_script, (name, phone, email))
                    print('End of add_user')
                    print(f'{name} added')
                    conn.commit()

except Exception as error:
    print(error)
