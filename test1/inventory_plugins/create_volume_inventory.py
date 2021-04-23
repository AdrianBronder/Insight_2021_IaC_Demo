from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
        name: create_volume_inventory
        plugin_type: inventory
        author: Mirko Van Colen
        version_added: "0.1"
        short_description: import external data
        description:
            - This script returns external data
        options:
          plugin:
              description: Name of the plugin
              required: true
              choices: ['create_volume_inventory']
        notes:
          - notes
"""

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.utils.display import Display
import argparse
import json
import yaml

display = Display()

class InventoryModule(BaseInventoryPlugin):
    NAME = 'create_volume_inventory'

    def _import_yaml(self,path):
        with open(path) as file:
            display.display("import yaml file : " + path)
            return yaml.load(file, Loader=yaml.FullLoader)

    def _parse_extra_vars(self):

        # use argument parser to parse the playbook arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-i','--inventory',  required=False, dest="inventory_script")
        parser.add_argument('-e','--extra_vars', required=False, dest="extra_vars")
        parser.add_argument('--list', action = 'store_true', required=False, dest="list_inventory")
        parser.add_argument('--host', action = 'store', required=False, dest="ansible_host")
        parser.add_argument('args', nargs=argparse.REMAINDER)
        self.args, self.unknown_args = parser.parse_known_args()

        # parsing extra vars
        display.display("extravars argument = " + self.args.extra_vars)

        # if json format
        if self.args.extra_vars.startswith("{"):
            display.display("extravars argument is json format")
            self.extra_vars = json.loads(self.args.extra_vars)

        # if yaml file
        elif self.args.extra_vars.startswith("@"):
            yaml_file = self.args.extra_vars[1:]
            display.display("extravars argument is a yaml file : " + yaml_file)
            self.extra_vars = self._import_yaml(yaml_file)

    def _populate(self):
        '''Return the hosts and groups'''
        display.display("Running dynamic inventory")
        display.display("input = " + str(self.extra_vars))

        # create a new inventory object
        self.inventory.add_host(host='localhost')
        self.inventory.set_variable('localhost','ansible_python_interpreter','/usr/bin/python3')

        ############################################
        # Convert functional data to technical data
        ############################################

        mapping = self._import_yaml("mapping.yaml")
        display.display(str(mapping))
        country = mapping[self.extra_vars["country"]]
        city    = country[self.extra_vars["city"]]
        cluster = city["resources"][0]["cluster"]
        vserver = city["resources"][0]["vserver"]
        volume_name = country["short"] + "_" + city["short"] + "_" + self.extra_vars["vol_name"]


        self.inventory.set_variable('localhost','cluster',cluster)
        self.inventory.set_variable('localhost','vserver',vserver)
        self.inventory.set_variable('localhost','volume_name',volume_name)
        self.inventory.set_variable('localhost','size_mb',self.extra_vars["size_mb"])

    def parse(self, inventory, loader, path, cache):
       '''Return dynamic inventory from source '''
       super(InventoryModule, self).parse(inventory, loader, path, cache)

       # Call our internal helper to populate the dynamic inventory
       #config = self._read_config_data(path)
       self._parse_extra_vars()
       self._populate()

