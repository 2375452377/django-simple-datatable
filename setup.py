import os
import codecs

from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)

with codecs.open(os.path.join(base_dir, 'README.md'), 'r', encoding='utf8') as f:
    long_description = f.read()

about = {}
with open(os.path.join(base_dir, 'simple_datatable', '__about__.py')) as f:
    exec (f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    long_description=long_description,
    license=about['__license__'],
    url=about['__uri__'],
    author=about['__author__'],
    author_email=about['__email__'],
    platforms=['any'],
    packages=find_packages(exclude=['ez_setup', 'tests']),
    scripts=[],
    zip_safe=False,
    install_requires=[
        'django>=1.10.*<2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
