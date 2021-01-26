# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Graz University of Technology
#
# medra-to-datacite is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""DOI Minting using datacite v4."""

import json
import os
from datacite import DataCiteRESTClient, schema43
from flask import current_app
from jsonschema import ValidationError

class DoiMinting:
    """DOI minting invenioRDM records."""
    
    def validate(self, metadata):
        """Validate the json object."""

        if schema43.validate(metadata):
            return True

        try:
            schema43.validator.validate(metadata)
        except ValidationError as e:
            print(e.args[0])

        return False

    def map_doi(self, metadata):
        """Mapping the metadata."""
        print(metadata['resource_type']['type'])

        # Types - are not matcing to datacite
        # this is how you can change to first letter cap
        # metadata['resource_type']['type'].capitalize()
        data = {
        "identifiers": [
            {
                "identifier": "10.5281/zenodo.4061232",
                "scheme": "doi",
                "identifierType": "DOI",
            }
        ],
        "creators": metadata['creators'],
        "titles": [{"title": metadata['title'],}
        ],
        "publisher": metadata['publisher'],
        "publicationYear": metadata['publication_date'],
        "types": {
            "resourceType": "other",
            "resourceTypeGeneral": "Other"
        },
        'schemaVersion': 'http://datacite.org/schema/kernel-4',
        }

        # validate json
        self.validate(data)
        print(self.validate(data))

        return data

    def get_config(self):
        """Get the configuration variables from the environment."""
        username = current_app.config['INVENIO_CONFIG_DATACITE_API_USERNAME']
        password = current_app.config['INVENIO_CONFIG_DATACITE_API_PASSWORD']
        prod_prefix = current_app.config['INVENIO_CONFIG_DATACITE_PREFIX']
        test_prefix = current_app.config['INVENIO_CONFIG_DATACITE_TEST_PREFIX']

        return (username, password, prod_prefix, test_prefix)

    def post_draft_doi(self, metadata):
        """Post draft."""
        
        # get configs
        username, password, prod_prefix, test_prefix = self.get_config()

        d = DataCiteRESTClient(
            username=username,
            password=password,
            test_mode="test_mode",
            prefix=test_prefix,
            )

        return d.draft_doi(metadata=metadata)
