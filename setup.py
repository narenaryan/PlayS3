from setuptools import setup

setup(name='PlayS3',
      version='0.2',
      description='Python library for working directly on Amazon S3',
      url='',
      author='Naren Arya',
      author_email='narenarya@live.com',
      license='MIT',
      packages=['PlayS3'],
      install_requires=[
          'FileChunkIO',
          'boto',
      ],
       classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX :: Linux'],
      zip_safe=False)