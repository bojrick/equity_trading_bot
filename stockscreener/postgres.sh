sudo apt-get remove --purge postgresql-12
sudo apt-get install postgresql-12
pg_ctlcluster 12 main start
su -c "psql" - postgres