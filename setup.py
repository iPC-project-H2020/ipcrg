"""Package installer."""
import os
from setuptools import setup
from setuptools import find_packages

LONG_DESCRIPTION = ''
if os.path.exists('README.md'):
    with open('README.md') as fp:
        LONG_DESCRIPTION = fp.read()

REQUIREMENTS = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as fp:
        REQUIREMENTS = [line.strip() for line in fp]

setup(
    name='ipcrg',
    version='0.0.1',
    description=(
        'iPC relational graph.'
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=(
        'Dominik Linzer, Michael Schmidt, Matteo Manica, '
        'Joris Cadow, Davide Cirillo, Marianyela Petrizzelli'
    ),
    author_email=(
        'dominik.linzner@bcs.tu-darmstadt.de, '
        'michael.schmidt@bcs.tu-darmstadt.de, '
        'drugilsberg@gmail.com, ',
        'joriscadow@gmail.com, ',
        'davide.cirillo@bsc.es, ',
        'marianyela.petrizzelli@curie.fr'
    ),
    url='https://gitlab.technikon.com/relational-graph-framework/ipcrg',
    license='MIT',
    install_requires=REQUIREMENTS,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    package_data={
        'ipcrg':
            [
                'resources/id_mapping/gene.tsv.gz',
                'resources/id_mapping/protein.tsv.gz',
            ]
    },
    packages=find_packages(),
    scripts=[
        'bin/ipcrg-entities-from-resources',
        'bin/ipcrg-parse-edge-list',
        'bin/ipcrg-create-indexes',
    ]
)
