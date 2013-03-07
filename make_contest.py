#!/usr/bin/python

usage = """USAGE:
./make_contest.py <contest_id>
"""

import os, string, sys

if len(sys.argv) < 2:
  print usage
  exit()

contest_data = {
  "contest_id": int(sys.argv[1])
}

bad_problem_names = ['tests', 'checkers', '..', '.']

problem_names = []
for name in os.listdir('.'):
  if name in bad_problem_names: continue
  if not os.path.isdir(name): continue
  problem_names.append(name)

problem_strings = []

for index in range(len(problem_names)):
  pstr = """[problem]
id = %d
super = "Generic"
short_name = "%s"
long_name = "%s"
"""
  problem_strings.append(pstr % (index + 1, string.ascii_uppercase[index], problem_names[index]))

contest_data['problems'] = "\n".join(problem_strings)

result = """
# -*- coding: utf-8 -*-
# $Id$
contest_id = {contest_id}

contest_time = 180
score_system = acm
board_fog_time = 0
board_unfog_time = 0

compile_dir = "../../compile/var/compile"

team_enable_src_view
team_enable_ce_view
ignore_compile_errors
problem_navigation

stand_fancy_style

rounding_mode = floor
cr_serialization_key = 22723
enable_runlog_merge
detect_violations
enable_memory_limit_error
enable_l10n
team_download_time = 0
cpu_bogomips = 5667

[language]
id = 1
short_name = "fpc"
long_name = "Free Pascal 2.4.4-2ubuntu1"
src_sfx = ".pas"

[language]
id = 3
short_name = "g++"
long_name = "GNU C++ 4.6.1"
src_sfx = ".cpp"

[language]
id = 13
short_name = "python"
long_name = "Python 2.7.2+"
arch = "linux-shared"
src_sfx = ".py"

[language]
id = 18
short_name = "javac"
long_name = "Java JDK 1.6.0_23"
arch = "java"
src_sfx = ".java"
exe_sfx = ".jar"

[language]
id = 21
short_name = "ruby"
long_name = "Ruby 1.8.7"
arch = "linux-shared"
src_sfx = ".rb"

[problem]
abstract
short_name = "Generic"
input_file = "%Pl.in"
output_file = "%Pl.out"
test_dir = "%Pl"
use_corr
corr_dir = "%Pl"
corr_sfx = ".a"
info_dir = "%Ps"
tgz_dir = "%Ps"
time_limit = 2
real_time_limit = 20
max_vm_size = 64M
check_cmd = "check_%lPl"

{problems}

[tester]
name = Generic
arch = ""
abstract
no_core_dump
enable_memory_limit_error
kill_signal = KILL
memory_limit_type = "default"
secure_exec_type = "static"
clear_env
start_env = "PATH=/usr/local/bin:/usr/bin:/bin"
start_env = "HOME"

[tester]
name = Linux-shared
arch = "linux-shared"
abstract
no_core_dump
enable_memory_limit_error
kill_signal = KILL
memory_limit_type = "default"
secure_exec_type = "dll"
clear_env
start_env = "PATH=/usr/local/bin:/usr/bin:/bin"
start_env = "HOME"

[tester]
name = Linux-java
arch = "java"
abstract
no_core_dump
kill_signal = TERM
memory_limit_type = "java"
secure_exec_type = "java"
start_cmd = "runjava"
start_env = "LANG=C"
start_env = "EJUDGE_PREFIX_DIR"

[tester]
any
super = Generic

[tester]
any
super = Linux-shared
arch = linux-shared

[tester]
any
super = Linux-java
arch = java

# audit: created 2013/03/06 18:25:31 1 (admin) 92.46.55.10
# audit: edited 2013/03/06 18:27:16 1 (admin) 92.46.55.10
# audit: edited 2013/03/06 18:28:59 1 (admin) 92.46.55.10
"""

result_contest = """<?xml version="1.0" encoding="utf-8" ?>

<!-- put it into /home/judges/data/contests -->

<!-- $Id$ -->
<contest id="{contest_id}"
         autoregister="yes"
         disable_team_password="yes"
         simple_registration="yes"
         managed="yes"
         run_managed="yes">
  <name>KBTU {contest_id}</name>
  <name_en>KBTU {contest_id}</name_en>
  <problems_url>/problems/{contest_id}.pdf</problems_url>
  <logo_url>http://acm.kbtu.kz/sites/all/themes/sky/logo_square.png</logo_url>
  <register_access default="allow"/>
  <users_access default="allow"/>
  <master_access default="allow"/>
  <judge_access default="allow"/>
  <team_access default="allow"/>
  <serve_control_access default="allow"/>
  <caps>
    <cap login = "admin">
      FULL_SET,
    </cap>
  </caps>
  <field id="inst_en" mandatory="no"/>
  <field id="fac_en" mandatory="no"/>
  <field id="city_en" mandatory="no"/>
  <field id="languages" mandatory="no"/>
</contest>
<!-- audit: created 2013/03/06 18:25:31 1 (admin) 92.46.55.10 -->
"""

f = open("%06d.xml" % contest_data['contest_id'], 'w')
f.write(result_contest.format(**contest_data))
f.close()

f = open("serve.cfg", 'w')
f.write(result.format(**contest_data))
f.close()
