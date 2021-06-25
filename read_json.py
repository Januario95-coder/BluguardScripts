import os
import json


class ManageJson:
    def __init__(self, band_mac=None):
        """Checks if band_mac is not None.
        If band_mac is None, filename will be set to band_mac.
        Otherwise, filename will be raw_data.json.

        If band_mac is specified, it will be used as filename.
        If the banc_mac filename does not exists, it will
        be created automatically.
        """
        if not band_mac:
            self.filename = 'C:/Users/hayysoft/Documents/Scripts/interview/media/raw_data.json'
        else:
            self.band_mac = band_mac
            self.filename = f'C:/Users/hayysoft/Documents/Scripts/interview/media/{self.band_mac}.json'
            if not os.path.exists(self.filename):
                os.system(f'type nul > C:/Users/hayysoft/Documents/Scripts/interview/media/{self.band_mac}.json')

    def save_json(self, data):
        """Accept data and append to self.filename."""
        with open(self.filename, mode='w') as fp:
            if isinstance(data, dict):
                data = [data]
                fp.write(json.dumps(data, indent=4))
            else:
                fp.write(json.dumps(data, indent=4))

    def load_json(self):
        """Checks if self.filemane is empty.
        If self.filename is empty, just write an empty array, [].

        Otherwise, loads and return data from self.filename.
        """
        if self.is_empty():
            with open(self.filename, 'w') as fp:
                fp.write('[]')
                return []

        with open(self.filename) as fp:
            data = json.loads(fp.read())

        return data

    def is_empty(self):
        """Returns True if size of self.filename is 0.
        Otherwise, returns False.
        """
        return os.path.getsize(self.filename) == 0

