# editdb.py

`editdb.py` is a Python 2 application that allows you to work with
sqlite databases. You can get a list of session commands from the
command line with...

    ./editdb.py help

...or within the application with...

    ?

This is what you'll get from the command line:

```
Command history is available within the context of "./editdb.py"
On startup, command history is set to the previous query string (qs=)
"./editdb.py" has no command line parameters. Commands are:
quit q stop finish -- Exit
help h ? ------------ Displays this help
State state s ------- Displays settings / status
 diag --------------- Displays state of DB object diagnosis flag
 diag=t|true|y|yes|f|false|n|no: - print db object upon query
  val --------------- Displays state of entry validation flag
  val=t|true|y|yes|f|false|n|no: - confirm settings when entered
   db=Database ------ Set database to work with
   db --------------- Displays database
tables -------------- Display DB tables
   qs=SQL ----------- Set query/command string
   qs --------------- Displays query/command SQL string
write w ------------- Writes the results of last query to ofile
ofile=OutputFile ---- Sets the name of the output file
ofile --------------- Reports output file name
x exec -------------- Execute qs upon db
```

## Example Session:

```
./editdb.py
-->: db=test.db
-->: qs=create table tfu(thename text,thecount integer)
-->: x
ok
-->: qs=insert into tfu (thename,thecount) values ('Ben',7)
-->: x
ok
-->: qs=insert into tfu (thename,thecount) values ('Jerry',2)
-->: x
ok
-->: qs=insert into tfu (thename,thecount) values ('Arianne',9)
-->: x
ok
-->: qs=select thename,thecount from tfu order by thename
-->: x
(u'Arianne', 9)
(u'Ben', 7)
(u'Jerry', 2)
-->: qs=select thename,thecount from tfu order by thecount
-->: x
(u'Jerry', 2)
(u'Ben', 7)
(u'Arianne', 9)
-->: q
```

