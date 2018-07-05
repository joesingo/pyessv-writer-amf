    # -*- coding: utf-8 -*-

"""
.. module:: write_cv.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps raw NCAS AMF vocab files to normalized pyessv format.
.. moduleauthor:: Ag Stephens <ag.stephens@stfc.ac.uk>
"""
import argparse
import json
import os
import re

import arrow

import pyessv



# Define command line options.
_ARGS = argparse.ArgumentParser('Maps raw NCAS AMF vocab files to normalized pyessv CV format.')
_ARGS.add_argument(
    '--source',
    help='Path from which raw NCAS AMF vocab files will be read.',
    dest='source',
    type=str
    )

# Ensure we use fixed creation date.
_CREATE_DATE = arrow.get('2018-03-09 00:00:00.000000+0000').datetime

# CV authority = NCAS.
_AUTHORITY = pyessv.create_authority(
    'NCAS',
    'NCAS Atmospheric Measurement Facility CVs',
    label='NCAS',
    url='https://www.ncas.ac.uk/en/about-amf',
    create_date=_CREATE_DATE
    )

# CV scope = AMF.
_SCOPE_AMF = pyessv.create_scope(_AUTHORITY,
    'AMF',
    'Controlled Vocabularies (CVs) for use in AMF',
    label='AMF',
    url='https://github.com/agstephens/AMF_CVs',
    create_date=_CREATE_DATE
    )

# CV scope = GLOBAL.
_SCOPE_GLOBAL = pyessv.create_scope(_AUTHORITY,
    'GLOBAL',
    'Global controlled Vocabularies (CVs)',
    url='https://github.com/agstephens/AMF_CVs',
    create_date=_CREATE_DATE
    )

def _get_collection_amf_config(source_dir):
    """
    Build a map of AMF collections to data factories / name pre-formatters
    for each CV JSON file in the source directory.
    """
    collections = {}
    data_fact_func = lambda obj, name: obj[name]

    # Regex to product name from filename
    json_filename_regex = re.compile("AMF_([a-zA-Z0-9_]+).json")

    for fname in os.listdir(source_dir):
        match = json_filename_regex.match(fname)
        if match:
            product_name = match.groups(1)[0]
            collections[product_name] = {"data_factory": data_fact_func}

    return collections

# Map of AMF collections to data factories / name pre-formatters.
_COLLECTIONS_GLOBAL = {
}

def _main(args):
    """Main entry point.
    """
    if not os.path.isdir(args.source):
        raise ValueError('NCAS vocab directory does not exist')

    # Create AMF collections.
    for typeof, parsers in _get_collection_amf_config(args.source).items():
        _create_collection_amf(args.source, typeof, parsers)

    # Create GLOBAL collections.
    for typeof, handlers in _COLLECTIONS_GLOBAL.items():
        _create_collection_global(args.source, typeof, parsers)

    # Add to the archive and save to file system.
    pyessv.archive(_AUTHORITY)


def _create_collection_amf(source, collection_type, collection_info):
    """Creates amf collection from a NCAS JSON files.
    """
    # Create collection.
    collection = pyessv.create_collection(
        _SCOPE_AMF,
        collection_type,
        "NCAS AMF CV collection: ".format(collection_type),
        create_date=_CREATE_DATE,
        term_regex=collection_info.get('term_regex')
        )

    # Load NCAS json data.
    ncas_cv_data = _get_ncas_cv(source, collection_type, 'AMF_')

    # Create terms.
    data_factory = collection_info['data_factory']
    for name in ncas_cv_data:
        pyessv.create_term(
            collection,
            name,
            label=name,
            create_date=_CREATE_DATE,
            data=data_factory(ncas_cv_data, name) if data_factory else None
            )


def _create_collection_global(source, collection_type, parsers):
    """Creates global collection from a NCAS JSON files.
    """
    # Create collection.
    collection = pyessv.create_collection(
        _SCOPE_GLOBAL,
        collection_type,
        'NCAS GLOBAL CV collection: '.format(collection_type),
        create_date=_CREATE_DATE
        )

    # Unpack parsers.
    data_factory = parsers['data_factory']

    # Load NCAS json data.
    ncas_cv_data = _get_ncas_cv(source, collection_type)

    # Create terms.
    for name in ncas_cv_data:
        pyessv.create_term(
            collection,
            name,
            create_date=_CREATE_DATE,
            data=data_factory(ncas_cv_data, name) if data_factory else None
            )


def _get_ncas_cv(source, collection_type, prefix=''):
    """Returns raw NCAS CV data.
    """
    fname = '{}{}.json'.format(prefix, collection_type)
    fpath = os.path.join(source, fname)
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())[collection_type]


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
