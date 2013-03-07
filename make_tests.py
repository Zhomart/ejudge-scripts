#!/usr/bin/python

# == Structure of files:
#
# problems/
#   problem_name_1/
#     tests/
#       01
#       01.a
#   problem_name_2/
#     tests/
#       01.in
#       01.out
#   problem_name_3/
#     01
#     01.a
#    make_correct_tests.py
#
# == Run
# $ ./make_correct_tests.py
#
# Written by Zhomart Mukhamejanov, 2013, KBTU

import os
import re
import shutil
import stat

if not os.path.exists('tests'):
	os.mkdir('tests')

if not os.path.exists('checkers'):
	os.mkdir('checkers')

def copy_java_checker(problem, the_file):
	from_file = problem+'/'+the_file
	to_file = 'checkers/Check' + problem.capitalize()+'.java'
	exe_name = 'checkers/check_' + problem.lower()

	# == REMOVE java keyword public
	f = open(from_file)
	source_code = f.read()
	f.close()

	class_name = 'Check%s' % problem.capitalize()

	source_code = re.sub(r'(public)? *class\s*\S*Check\S*', 'public class %s' % class_name, source_code, re.I)

	f = open(from_file, "w")
	f.write(source_code)
	f.close()

	# == copy to checkers
	shutil.copy(from_file, to_file)

	# == generate sh
	f = open(exe_name, "w")
	f.write("#! /bin/sh\n" + ('exec java -cp `dirname $0`:`dirname $0`/testlib4j.jar ru.ifmo.testlib.CheckerFramework %s "$@"' % class_name))
	# f.write("#! /bin/sh\n" + ('exec java -cp \"`dirname $0`;`dirname $0`\\*.jar\" %s "$@"' % class_name))
	f.close()

	# == add chmod +x
	st = os.stat(exe_name)
	os.chmod(exe_name, st.st_mode | stat.S_IEXEC)

def make_3(tdir, p):
	if not os.path.exists(tdir): return

	if tdir[-1:] != '/': tdir += '/'

	for k in os.listdir(tdir):
		t = re.match('^(input)?(\d{2,3})(\.tst$|\.txt$|\.dat$|$)', k, re.I)
		if t:
			tmp = t.group(2)
			if len(tmp) == 2: tmp = '0'+ tmp
			shutil.move(tdir+k, tdir+tmp)
		t = re.match('^(answer|output)?(\d{2,3})(\.ans$|\.txt$|\.a$)', k, re.I)
		if t:
			tmp = t.group(2)
			if len(tmp) == 2: tmp = '0'+ tmp
			shutil.move(tdir+k, tdir+tmp+'.a')
		if re.match('^\d{3}$', k) and not os.path.exists(tdir+k+'.a'): open(tdir+k+'.a','w').close()

	if not os.path.exists('tests/'+p): os.mkdir('tests/'+p)

	for f in os.listdir(tdir):
		if re.match('^\d{3}(\.a)?$', f):
			shutil.copy(tdir+f, 'tests/'+p+'/'+f)
		t = re.match('check.*\.(\w{3})',f,re.I)
		if t:
			ext = t.group(1).lower()
			if ext == 'dpr': ext = 'pas'
			if ext in ('cpp', 'pas'):
				shutil.copy(tdir+f, 'checkers/check_'+p.lower()+'.'+ext)

	for f in os.listdir(p):
		t = re.match('check.*\.(\w{1,4})',f,re.I)
		if t:
			ext = t.group(1).lower()
			if ext == 'dpr': ext = 'pas'
			if ext in ('cpp', 'pas', 'c'):
				shutil.copy(p+'/'+f, 'checkers/check_'+p.lower()+'.'+ext)
			if ext in ('java'):
				copy_java_checker(p, f)


for d in os.listdir('.'):
	if os.path.isdir(d) and d not in ('tests', 'checkers'):
		dr = d
		if os.path.exists(d+'/tests'): dr += '/tests'
		make_3(dr, d)

