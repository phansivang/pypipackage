from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ismscode',
  version='0.0.3',
  description='VIRTUAL NUMBER AND RECEIVER SMS',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Phansivang',
  author_email='Phansivang@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Virtual number', 
  packages=find_packages(),
  install_requires=['forex-python','requests','beautifulsoup4' ] 
)
