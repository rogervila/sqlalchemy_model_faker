from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='sqlalchemy_model_faker',
    packages=['sqlalchemy_model_faker'],
    version='CURRENT_VERSION',
    license='MIT',
    description='Generate SQLAlchemy models with fake data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Roger Vilà',
    author_email='rogervila@me.com',
    url='https://github.com/rogervila/sqlalchemy_model_faker',
    download_url='https://github.com/rogervila/sqlalchemy_model_faker/archive/CURRENT_VERSION.tar.gz',
    keywords=['sqlalchemy fake model', 'sqlalchemy fake data'],
    install_requires=[
        'sqlalchemy >= 1.4.32',
        'Faker >= 13.3.4',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
