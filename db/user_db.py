import config
import psycopg2
import psycopg2.extras
import openpyxl
from openpyxl.styles import Font

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
                            phone varchar,
                            status varchar
                            )
                        '''
                    cur.execute(create_script)
                    cur.execute('SELECT * FROM all_users')
                    conn.commit()


            def add_user(user_array_info):
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    print('start of add_user')
                    name, phone, email = user_array_info[0], user_array_info[1], user_array_info[2]
                    insert_script = 'INSERT INTO all_users (name, phone, email, status) VALUES (%s, %s, %s, %s)'
                    cur.execute(insert_script, (name, phone, email, '0%'))
                    print('End of add_user')
                    print(f'{name} added')
                    conn.commit()


            def is_user_in_db(username):
                with conn.cursor() as cur:
                    existence_script = f"SELECT name FROM all_users WHERE name = '{username}'"
                    cur.execute(existence_script)
                    userlist = []
                    for i in cur:
                        userlist.append(i)
                    if userlist:
                        return True
                    else:
                        return False

            def get_status(username):
                with conn.cursor() as cur:
                    get_status_script = f"SELECT status FROM all_users WHERE name = {username}"
                    cur.execute(get_status_script)
                    print(cur)


            def export_to_excel():
                with conn.cursor() as cur:
                    script = 'SELECT * FROM all_users'
                    SQL_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(script)
                    t_path_n_file = "C:\\Users\\Али\\PycharmProjects\\botv1\\db\\some_file.csv"
                    try:
                        with open(t_path_n_file, 'w') as f_output:
                            cur.copy_expert(SQL_for_file_output, f_output)
                            print('DONE')
                    except psycopg2.Error as e:
                        t_message = "Error: " + e + "/n query we ran: " + script + "/n t_path_n_file: " + t_path_n_file
                        return 'DB ERROR'


except Exception as error:
    print(error)
