from boto.s3.connection import S3Connection
from boto.s3.key import Key
import math, os ,sys
from filechunkio import FileChunkIO

class S3Account:
	def __init__(self,secret_id,secret_key):
		#creates a connection object on which all operations for S3 were done
		self.conn = S3Connection(secret_id,secret_key)

	#returns boto connection object
	def connection(self):
		return self.conn 
	
	#returns a boto connection object
	def bucket(self,name):
		buck=self.conn.get_bucket(name,validate=False)
		return buck
	
	#delete all the contents from a given bucket
	def deleteBucketContents(self,name):
		bucket=self.conn.get_bucket(name,validate=False)
		for key in bucket.list():
			key.delete()
	
	#deletes a key from the selected bucket
	def deleteKey(self,name,delkey):
		bucket=self.conn.get_bucket(name,validate=False)
		for key in bucket.list():
			if key.name==delkey:
				return key.delete()

	def value(self,name,key):
		bucket=self.conn.get_bucket(name,validate=False)
		k=Key(bucket)
		k.key=key
		return k.get_contents_as_string()

	#delete entire bucket from s3
	def deleteBucket(self,name):
		self.conn.delete_bucket(name)

	#creates a new bucket with the given name.Same name will throw S3CreateError
	def createBucket(self,name):
		bucket=self.conn.create_bucket(name)
		return bucket
	
	#arguments are buckname,key,string=False then file will be created as in the same name it saved.
	def getKeyContent(self,name,key,string=True,path=None):
		bucket=self.conn.get_bucket(name,validate=False)
		k=Key(bucket)
		k.key=key
		if string:
			return k.get_contents_as_string()
		else:
			if not path:
				try:
					if k.get_metadata('file'):
						path=k.get_metadata('file')
				except Exception:
					print "Forgot to give the filename"
					sys.exit(0) 
				return k.get_contents_to_filename(path)
			else:
				return k.get_contents_to_filename(path)
	
	#Returns a generator which yields a key at a time
	def listKeys(self,name):
		bucket=self.conn.get_bucket(name,validate=False)
		for item in bucket.list():
			yield item

	#lists all availlale buckets
	def listBuckets(self):
		for bucket in self.conn.get_all_buckets():
			yield bucket

	#args are bucket name,key,string=False then key content is from a file.value='path to file' 
	def storeKey(self,bucket_name,key,value,string=True):
		bucket=self.conn.get_bucket(bucket_name,validate=False)
		k=Key(bucket)
		k.key=key
		if string:
			k.set_contents_from_string(value)
		else:
			k.set_metadata('file',value)
			k.set_contents_from_filename(value)

	#For uploading large files.chose Chunked uploading.Default chunk size is 50MB.
	def uploadChunk(self,bucket_name,path,chunk_size=52428800):
		bucket=self.conn.get_bucket(bucket_name,validate=False)
		source_path=path
		source_size=os.stat(source_path).st_size
		chunk_count = int(math.ceil(source_size / chunk_size))
		mp = bucket.initiate_multipart_upload(os.path.basename(source_path))
		for i in range(chunk_count + 1):
			offset = chunk_size * i
			bytes = min(chunk_size, source_size - offset)
			with FileChunkIO(source_path, 'r', offset=offset,bytes=bytes) as fp:
				mp.upload_part_from_file(fp, part_num=i + 1)
		mp.complete_upload()
