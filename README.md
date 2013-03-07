# EJudge Scripts

## insert scripts into problems folder:
```bash
problems:

  problem_name1

    tests

      01

      01.a

      02

      02.a

    check.dpr

  problem_name2

    001

    001.a

    002

    002.a

    Check.java

  ....

  make_tests.py

  make_contest.py
```

## run scripts
$ ./make_contest.py 129
$ ./make_tests.py

## Copy files to ejudge server (using ejudge user)
- insert 0000**.xml into /home/judges/data/contests/
- insert serve.xml into /home/judges/000**/conf/
- insert directories `checkers` & `tests` into /home/judges/000**/
