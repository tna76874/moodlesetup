# Moodle user/course setup

This python skript is a quick and dirty way to get csv-files suitable for the batch setup process of course and user creation.

### Usage

You need to have a python 3.x environment installed and pip. First install the needed libarys.

```bash
$ pip install -r requirements.txt
```

Copy the example folder to data:

```bash
$ cp -r example data
```

Adapt the content of `schuelerliste.xls` and create the moodle-tables.

```bash
$ ./moodlesetup.py -c
```

Now there are three files in the export folder:

| File 	| Description 	|
|-	|-	|
| courses.csv 	| You can drag and drop this file in the moodle admin-section to batch create all needed courses. **Do this first.** 	|
| users.csv 	| Via crag and drop of this file you can create all moodle-users and enrol them in courses 	|
| print.csv 	| An overview over the created users + passwords. Format and print this if you want. 	|

### Config-File

In the config file `config.ini` is stored, from which excel-list the data will be imported. You can put multiple tables in the data folder and write into the config-file wich to use. The `seed` parameter gets randomly generated on the first run of the programm. This ensures, that for a given username the generated password is always the same. In this way you can adapt the script and re-run it without changing the credentials of the enroled users.