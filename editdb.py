#!/usr/bin/python

defname='editdb.defaults'

docstring =	"""Sqlite Database Editor "editdb.py"
      Author: fyngyrz  (Ben)
     Contact: fyngyrz@gmail.com
              (bugs, feature requests, kudos, bitter rejections)
     Project: editdb.py
    Homepage: https://github.com/fyngyrz/editdb
     License: None. It's free. *Really* free.
              Defy invalid social and legal norms.
 Disclaimers: 1) Probably completely broken. Do Not Use.
                 You were explicitly warned. Phbbbbt.
              2) My code is blackbox, meaning I wrote it without reference
                 to OPC (other people's code.)
              3) I can't check other people's contributions effectively,
                 so if you use any version of editdb.py that incorporates
                 accepted commits from others, you are risking the use of
                 OPC, which may or may not be protected by copyright,
                 patent, and the like, because our intellectual property
                 system is pathological. The risks and responsibilities and
                 any subsequent consequences are entirely yours. Have you
                 written your congresscritter about patent and copyright
                 reform yet?
  Incep Date: December 1st, 2016
     LastRev: December 14th, 2015
  LastDocRev: December 14th, 2015
 Tab spacing: 4 (set your editor to this for sane formatting while reading)
     Dev Env: OS X 10.6.8, Python 2.6.1
   Add'l Env: Debian 8.6, Python 2.7.9
	  Status: BETA
    Policies: 1) I will make every effort to never remove functionality or
                 alter existing functionality once past BETA stage. Anything
                 new will be implemented as something new, thus preserving all
                 behavior. The only intentional exceptions to this are if a
                 bug is found that does not match the intended behavior,
                 or I determine there is some kind of security risk. Remember,
                 this only applies to production code. Until the BETA status
                 is removed, ANYTHING may change.
       Usage: Run in shell like so:    python editdb.py
     1st-Rel: 1.0.0
     Version: 1.0.0 Beta
     History:
	 	1.0.0 - initial released

	Todo:
		More DB commands
 Example session:
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
		-->: q
		
		"""

import os,sys
from aa_sqlite import dbl
try:    import readline
except: readl = False
else:   readl = True

quedcmd = ['s']
thedb = None
theqs = None
displayDbl = False
validate = False

def lcmp(parm,s):
	l = len(parm)
	if s[0:l] == parm:
		return True,l
	return False,0


def readdefaults():
	global defname,theqs,thedb
	try:
		fh = open(defname)
	except:
		print 'Cannot open "'+defname+'", falling back to generic settings'
	else:
		for line in fh:
			line = line.strip()
			f,r = lcmp('thedb=',line)
			if f == True:
				thedb = line[r:]
			f,r = lcmp('theqs=',line)
			if f == True:
				theqs = line[r:]
		fh.close()

def writedefaults():
	global defname,theqs,thedb
	try:
		fh = open(defname,'w')
	except:
		print 'could not open"'+defname+'", cannot save states'
	else:
		try:
			if thedb != None:	fh.write('thedb='+str(thedb)+'\n')
			if theqs != None: 	fh.write('theqs='+str(theqs)+'\n')
		except:
			print 'could not finish writing to "'+defname+'", cannot save states'
		try:
			fh.close()
		except:
			print 'Could not close "'+defname+'"file!'

def boolr(p):
	if p == 't' or p == 'true' or p == 'y' or p == 'yes': return True,True
	if p == 'f' or p == 'false' or p == 'n' or p == 'no': return True,False
	print 'Don\'t understand "'+p+'"'
	return False,False

def uhelp():
	tfs = 't|true|y|yes|f|false|n|no'
	print 'quit q stop finish -- Exit'
	print 'help h ? ------------ Displays this help'
	print 'State state s ------- Displays settings'
	print ' diag --------------- Displays state of DB object diagnosis flag'
	print ' diag='+tfs+': - print db object upon query'
	print '  val --------------- Displays state of entry validation flag'
	print '  val='+tfs+': - confirm settings when entered'
	print '   db=Database ------ Set database to work with'
	print '   db --------------- Displays database'
	print 'tables -------------- Display DB tables'
	print '   qs=SQL ----------- Set query/command string'
	print '   qs --------------- Displays query/command SQL string'
	print 'x exec -------------- Execute qs upon db'

if len(sys.argv) != 1:
	if readl:
		print 'Command history is available within the context of "'+sys.argv[0]+'"'
		print 'On startup, command history is set to the previous query string (qs=)'
	print '"'+sys.argv[0]+'" has no command line parameters. Commands are:'
	uhelp()
	raise SystemExit

readdefaults()

if readl:
	print 'Command history available'
	if (theqs != '' and theqs != None):
		readline.add_history('qs='+theqs)

run = 1
while run == 1:
	if quedcmd == []:
		ui = raw_input("-->: ")
	else:
		ui = quedcmd.pop()
	if ui == 'quit' or ui == 'q' or ui == 'stop' or ui == 'finish': break

	elif ui == 'help' or ui == '?' or ui == 'h': uhelp()

	elif ui == 's' or ui == 'state':
		quedcmd += ['val']
		quedcmd += ['diag']
		quedcmd += ['qs']
		quedcmd += ['db']

	elif ui == 'x' or ui == 'exec':
		if thedb != None:
			if theqs != None:
				a = dbl(thedb,theqs)
				if a.mode == 'Query mode':
					for tup in a.tuples:
						print str(tup)
					if displayDbl == True:
						print str(a)
				elif a.mode == 'CMD mode':
					print 'ok'
				else:
					print str(a)
					print 'Cannot display results'

	elif ui == 't' or ui == 'tables':
		a = dbl(thedb,'SELECT name FROM sqlite_master ORDER BY name')
		if a.rows != 0:
			for tup in a.tuples:
				tbl = str(tup[0])
				print tbl
				b = dbl(thedb,"SELECT sql FROM sqlite_master WHERE tbl_name = '"+tbl+"' AND type = 'table'")
				if b.rows != 0:
					craw = str(b.tuples[0][0])
					junk,cols = craw.split('(',1)
					cols = cols[:-1]
					clist = cols.split(',')
					for el in clist:
						print '    '+el.strip()
		else:
			print 'No tables found'

	elif ui[0:4] == 'val=':
		pf,r = boolr(ui[4:])
		if pf == True:
			validate = r
			if validate == True:
				quedcmd += ['val']
	elif ui == 'val':
		print 'val='+str(validate)

	elif ui[0:5] == 'diag=':
		pf,r = boolr(ui[5:])
		if pf == True:
			displayDbl = r
			if validate == True:
				quedcmd += ['diag']
	elif ui == 'diag':
		print 'diag='+str(displayDbl)

	elif ui[0:3] == 'db=':
		parm = ui[3:]
		if parm == '': parm = None
		thedb = parm
		if validate == True:
			quedcmd += ['db']
	elif ui == 'db':
		print 'db="'+str(thedb)+'"'

	elif ui[0:3] == 'qs=':
		parm = ui[3:]
		if parm == '': parm = None
		theqs = parm
		if validate == True:
			quedcmd += ['db']
	elif ui == 'qs':
		print 'qs="'+str(theqs)+'"'

	else:
		if ui != '':
			print 'Unknown input: "'+ui+'"'

writedefaults()