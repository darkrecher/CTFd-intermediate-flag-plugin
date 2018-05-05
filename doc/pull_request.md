# Bug reproduction steps

 - Log in as an admin
 - Create a multiquestionchallenge
 - Log in as a user
 - Solve the challenge
 - Log again as an admin
 - Delete the challenge
 - Try to create a new multiquestionchallenge
 - The server answers a message "Internal server error"

For the example described in this document, we suppose the CTFd server has already 4 existing standard challenges, with their id 1, 2, 3, 4.
We also suppose the id of the removed multiquestionchallenge was 5.

# Log analysis

`cat /opt/CTFd/CTFd/logs/error.log`

The challenge deletion threw this error :

```
[2018-05-01 22:26:40,201] ERROR in app: Exception on /admin/chal/delete [POST]
Traceback (most recent call last):
...
  File "/opt/CTFd/CTFd/plugins/CTFd-multi-question-plugin/__init__.py", line 172, in delete
    Partialsolve.query.filter_by(chalid=chalid).delete()
NameError: global name 'chalid' is not defined
```

The challenge creation attempt threw this error :

```
[2018-05-01 22:27:17,984] ERROR in app: Exception on /admin/chal/new [POST]
Traceback (most recent call last):
...
  File "/usr/local/lib/python2.7/site-packages/sqlalchemy/engine/default.py", line 507, in do_execute
    cursor.execute(statement, parameters)
IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: multi_question_challenge_model.id [SQL: u'INSERT INTO multi_question_challenge_model (id) VALUES (?)'] [parameters: (5,)] (Background on this error at: http://sqlalche.me/e/gkpj)
```

# database analysis

(Do `apk add sqlite`, or get the file `/opt/CTFd/CTFd/ctfd.db` and open it in any SQLite DB Administrator).

```
cd /opt/CTFd/CTFd

sqlite3

sqlite> .open ctfd.db

sqlite> select * from multi_question_challenge_model;
5

sqlite> select * from partialsolve;
1|5|1|192.168.199.23|{"Pourquoi ?": true, "Qu'est-ce qui est jaune ?": true, "2+3 ?": true}|2018-05-01 22:24:59.658593

sqlite> select id from challenges;
1
2
3
4
```

The tables `multi_question_challenge_model` and `partialsolve` were not properly cleaned.

# Bugfix

Correction in method `MultiQuestionChallenge.delete(challenge)`. See commit content.

To test : do the bugfix reproduction steps. There should be no error at the end, and the new challenge should be created and functional.

Before testing, you may need to clean manually the database :
```
delete from multi_question_challenge_model where id = {the_id_of_the_deleted_challenge};
delete from partialsolve where chalid = {the_id_of_the_deleted_challenge};
```

Bye.
