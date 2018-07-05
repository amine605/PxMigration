from tqdm import tqdm
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
import config
import tables as migration_tables
import logging

cnx = None
cursor = None


def get_columns(export_columns, import_columns):
    export_columns_names = []
    for item in export_columns:
        if item in import_columns:
            export_columns_names.append(item)
    return export_columns_names


def build_insert_query(columns, selected_data, export_table_name):
    return "INSERT INTO  " + export_table_name + " (" + ' ,'.join(["`" + c + "`" for c in columns]) + " ) " + "VALUES ( " + ' ,'.join([r"%s" for item in selected_data]) + " )"


def build_select_query(columns, import_table_name):
    return "SELECT " + ','.join(["`" + c + "`" for c in columns]
                                ) + " FROM " + import_table_name


def init_logger():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s - line %(lineno)d',
                        datefmt='%m-%d %H:%M',
                        filename=config.log_file_path,
                        filemode='w')
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG if config.debug_mode else logging.INFO)
    logging.getLogger('').addHandler(console)


def init_mysql_connector():
    try:
        global cnx
        cnx = mysql.connector.connect(**config.creds)
        global cursor
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with your user name or password")
            exit(1)
        else:
            logging.error('Mysql Connector Error')
            logging.error(err)
            exit(1)
    except Exception as ex:
        logging.error(ex)
        exit(1)


def main():
    try:
        init_logger()
        init_mysql_connector()
        logging.info("Get Source schema")
        import_tables_with_columns = get_tables_from_db(
            config.SOURCE__DATABASE, config.SOURCE_DATABASE_PREFIX)
        logging.info("Get Destination database schema")
        export_tables_with_columns = get_tables_from_db(
            config.RESULT_DATABASE, config.RESULT_DATABASE_PREFIX)
        migrate_db(import_tables_with_columns, export_tables_with_columns)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.info("Database does not exist")
        else:
            logging.error(err)
    except Exception as ex:
        logging.error(ex)
    else:
        cnx.close()
        exit()


def get_tables_from_db(db_name, db_prefix):
    prefix_count = len(db_prefix)
    tables = []
    result = {}
    cursor.execute(f'USE `{db_name}`')
    cursor.execute("SHOW TABLES")
    for (table_name,) in cursor:
        tables.append(table_name)
    for table in tables:
        cursor.execute("SHOW columns FROM " + table)
        result[table[prefix_count:]] = [column[0]
                                        for column in cursor.fetchall()]
    return result


def get_data_from_table(columns, table_name):
    cursor.execute(f"USE `{config.SOURCE__DATABASE}`")
    cursor.execute(build_select_query(
        columns, config.SOURCE_DATABASE_PREFIX + table_name))
    return cursor.fetchall()


def make_changes_persistent():
    print(
        "Process of migration terminated successfully, are you sure you want to make the changes permenent ? [yes|no]")
    user_input = input()
    if(user_input == 'yes'):
        cnx.commit()
    elif user_input == 'no':
        exit()
    else:
        make_changes_persistent()


def migrate_table(table_name, source_schema, destination_schema):
    if table_name in destination_schema and table_name in migration_tables.tables_to_migrate and table_name not in config.out_of_migration:
        logging.debug('Migrating : ' + table_name)
        columns = get_columns(
            destination_schema[table_name], source_schema[table_name])
        result = get_data_from_table(columns, table_name)
        cursor.execute(f"USE `{config.RESULT_DATABASE}`")
        cursor.execute(r"DELETE FROM " +
                       config.RESULT_DATABASE_PREFIX + table_name)
        for data in result:
            query = build_insert_query(
                columns, data, config.RESULT_DATABASE_PREFIX + table_name)
            cursor.execute(query, data)


def migrate_db(source_schema, destination_schema):
    logging.info("Started Migration process")
    try:
        if config.debug_mode:
            for table_name in source_schema:
                migrate_table(table_name, source_schema, destination_schema)
        else:
            for table_name in tqdm(source_schema):
                migrate_table(table_name, source_schema, destination_schema)
        make_changes_persistent()
    except mysql.connector.Error as err:
        logging.error("Error Migrating Table : " + table_name)
        logging.error(err)
        exit(1)
    logging.info("Operation terminated successfully")


if __name__ == "__main__":
    main()
