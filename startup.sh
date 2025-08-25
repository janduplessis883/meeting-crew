#!/bin/bash
# Install newer SQLite
wget https://www.sqlite.org/2023/sqlite-autoconf-3430100.tar.gz
tar -xvf sqlite-autoconf-3430100.tar.gz
cd sqlite-autoconf-3430100
./configure
make
make install

# Confirm installed version
sqlite3 --version
