sudo apt-get install python-mysqldb

Use clean virtualenv and build your own python-mysql package.

First create virtualenv:

# virtualenv myvirtualenv
# source myvirtualenv/bin/activate
Then install build dependencies:

# sudo apt-get build-dep python-mysqldb
Now you can install python-mysql

# pip install mysql-python
