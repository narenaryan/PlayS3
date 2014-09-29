PlayS3
======

A python library for working with Amazon S3 buckets.It is the minimalstic approach for the developers newly
started working with Amazon S3 and python

A very simple and light weight wrapper that takes out all the pain of working with Amazon S3 buckets.The simple API provides a better way to access,modify,delete the buckets.

Only secret_id,secret_password of Amazon S3 account are required.Just create an object of S3Account() and sit cool.

PlayS3 supports following features:

1. creating a bucket

2. deleting a bucket

3. deleting contents of bucket

4. modifying the keys in a bucket

5. fetching all buckets

6. fetching all keys from a bucket

7. Large file uploading with chunked data
  
   and many more.

It sits upon boto framework and provides the full access to boto API.

For installing using pip just use this command:

sudo pip install PlayS3
