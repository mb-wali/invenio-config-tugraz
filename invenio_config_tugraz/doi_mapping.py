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


class DoiMinting():
    """DOI minting invenioRDM records."""

    def map_doi(metadata):
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

        # validate the json
        isvalid = valid(data)
        
        return data

    def validate(metadata):
        """Validate the json object."""

        if schema43.validate(metadata):
            return True

        try:
            schema43.validator.validate(metadata)
        except ValidationError as e:
            print(e.args[0])

        return False

    def post_draft_doi():
        return "posting here."
