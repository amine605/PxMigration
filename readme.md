# PX Migration
#### Data migration solution for Prestashop 1.6 - 1.7
 Upgrading from Prestashop 1.6 to Prestashop 1.6 is not obvious and can be so hard sometimes specially when you have a lot of data. All solution of migration from Prestashop 1.6 to 1.7 can cause a lot of problems:
  - The existing solutions are so expensive and may cause data loss when the procedure fail
  - Proceeding manually by changing the schema can cause a lot of problems
  - changing the schema of from an exsisting database that contains the data is not a good solution

## Phexonite Migration Tool!

  - Migrates data only from prestashop 1.6 database to prestashop 1.7 database directly
  - Choose the data that you want to migrate only
  - The changes will apply only when the full requested migration is possible
  - Easy to use and to configure
  - A progression bar
  - written in python
  - logging all actions 
You can also:
  - Exclude some tables from migration
  - Activate the debug mode so you can know exactly in which step the script failed so you can manage to fix the problem

# Requirements  

> Python 3.5+ 
> All the modules in the requirement file installed before running the script

## Configuration
 
 First use pip to install all requirements  
```sh
$ pip install -r requirements.txt
```

Upadte your config file (config.py)
> the Config file is written in python, make sure to do not make syntaxe errors or extra space/tab when updating it

```python
creds = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'raise_on_warnings': True
}
log_file_path = "/tmp/PxMigration.log" # The path to the log file: make sure it's writable
SOURCE__DATABASE = '16db' 
RESULT_DATABASE = '17db'
SOURCE_DATABASE_PREFIX = 'ps_'
RESULT_DATABASE_PREFIX = 'ps_'
```
You can also:
 - Activate the debug mode
 - Update the excluded tables list (Not recommended) 
 - Add extra tables that can be migrated

> Do not forget the to specify the source and the destination databases

> Do not forgot to update the databases prefix

> Make sure the the tables names must not contain the prefix

> Do not add the configuration table (ps_configuration) to the migration process, Export the only data (customers,orders ... )
### Usage
First you have to make a fresh Prestashop 1.7 installation to get a clean database
When you finish the configuration part, you can run the script.
> It on ly works with python 3.5+

#### Running the script
```sh
$ python PxMigration
```
![Script Execution](https://preview.ibb.co/igsgSJ/exec.png)
![Script Execution](https://preview.ibb.co/fkikMd/exec2.png)

> When the migration process is fully possible, you will be asked to make the changes permanent 

> The data in the export database (The result Database) will be deleted

### Limitations
- Both export and import databases must be on the same mysql server
- The script Does not fix currepted data
- The script do not export languages by default (ps_lang table), after migration you have to add them by your self in the same order so 
you can get your translations back. this is the most recommended way using this script

### More
 * It's possible to use this script to migrate Prestashop 1.7 database to Prestashop 1.6 database
 * It's possible to migrate 
