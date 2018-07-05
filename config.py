creds = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'raise_on_warnings': True
}

log_file_path = "/tmp/PxMigration.log" # The path to the log file: make sure it's writable

SOURCE__DATABASE = '16db' # import detabase
RESULT_DATABASE = '17db' # Export database
SOURCE_DATABASE_PREFIX = 'ps_'
RESULT_DATABASE_PREFIX = 'ps_'

debug_mode = False

# The tables in this list are going to be ignored in the migration process.
# It's recommended to keep those tables out of the migration process.
out_of_migration = [
    "connections",
    "lang",
    "access",
    "shop",
    "shop_url",
    "configuration"
]

'''
    The Migration process does not cover all Prestashop tables (Modules and hooks are not included).
    You can add them to this list, but make sure that they really exist in both databases, otherwise they're going to be ignored.
        For example : if it's a module table, install the module on the result prestashop instance.
'''
# Write the table names without their prefix
extra_tables = []
