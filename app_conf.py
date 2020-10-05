#!/usr/bin/env python3
from passlib.hash import sha256_crypt
INSTAPY_USERNAME = 'jasminecreamery'
INSTAPY_PASSWORD = 'JCream2018'
INSTAPY_SECRET = sha256_crypt.hash('jasminecreameryJCream2018')