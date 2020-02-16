# Copyright (C) 2020 Dimitrios-Georgios Akestoridis
#
# This file is part of Zigator.
#
# Zigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 only,
# as published by the Free Software Foundation.
#
# Zigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zigator. If not, see <https://www.gnu.org/licenses/>.

"""
Configuration module for the zigator package
"""

import logging
import os

from scapy.all import conf

from . import db
from . import fs


# Define the path of the configuration directory
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "zigator")

# Define the filepaths of configuration files
NETWORK_FILEPATH = os.path.join(CONFIG_DIR, "network_keys.tsv")
LINK_FILEPATH = os.path.join(CONFIG_DIR, "link_keys.tsv")
INSTALL_FILEPATH = os.path.join(CONFIG_DIR, "install_codes.tsv")

# Initialize the global variables
network_keys = {}
link_keys = {}
install_codes = {}
devices = {}
addresses = {}
networks = {}
entry = {column_name: None for column_name in db.PKT_COLUMN_NAMES}


def init(debug):
    global network_keys
    global link_keys
    global install_codes

    # Configure the logging system
    if debug:
        logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            level=logging.DEBUG)
    else:
        logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            level=logging.INFO)

    # Make sure that the configuration directory exists
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # Load network keys
    network_keys = fs.load_enc_keys(NETWORK_FILEPATH, optional=True)
    logging.info("Loaded {} network keys".format(len(network_keys)))

    # Load link keys
    link_keys = fs.load_enc_keys(LINK_FILEPATH, optional=True)
    logging.info("Loaded {} link keys".format(len(link_keys)))

    # Load install codes and derive link keys from them
    install_codes, derived_keys = fs.load_install_codes(INSTALL_FILEPATH,
                                                        optional=True)
    logging.info("Loaded {} install codes".format(len(install_codes)))

    # Add link keys, derived from install codes, that are not already loaded
    added_keys = 0
    for key_name in derived_keys.keys():
        if derived_keys[key_name] in link_keys.values():
            logging.debug("The derived link key {} was already loaded"
                          "".format(derived_keys[key_name].hex()))
        elif key_name in link_keys.keys():
            logging.warning("The derived link key {} was not added because "
                            "its name \"{}\" is also used by the link key {}"
                            "".format(derived_keys[key_name].hex(),
                                      key_name,
                                      link_keys[key_name].hex()))
        else:
            link_keys[key_name] = derived_keys[key_name]
            added_keys += 1
    logging.info("Added {} link keys that were derived from install codes"
                 "".format(added_keys))

    # Configure Scapy to assume that Zigbee is above the MAC layer
    conf.dot15d4_protocol = "zigbee"


def reset_entries(keep=[]):
    global entry

    # Reset all data entries in the shared dictionary except
    # the ones that were requested to maintain their values
    if keep is None:
        keep = []
    for column_name in db.PKT_COLUMN_NAMES:
        if column_name not in keep:
            entry[column_name] = None


def custom_sorter(var_value):
    str_repr = []
    for i in range(len(var_value)):
        if var_value[i] is None:
            str_repr.append(" "*80)
        elif isinstance(var_value[i], int):
            str_repr.append(str(var_value[i]).zfill(80))
        elif isinstance(var_value[i], str):
            str_repr.append(var_value[i].ljust(80))
        else:
            raise ValueError("Unexpected type: {}".format(type(var_value[i])))
    return ",".join(str_repr)


def update_devices(extendedaddr, macdevtype, nwkdevtype):
    global devices

    # Sanity checks
    if extendedaddr is None:
        raise ValueError("The extended address is required")
    elif macdevtype not in {None, "Full-Function Device",
                            "Reduced-Function Device"}:
        raise ValueError("Unexpected MAC device type")
    elif nwkdevtype not in {None, "Zigbee Coordinator", "Zigbee Router",
                            "Zigbee End Device"}:
        raise ValueError("Unexpected NWK device type")

    # Check whether it is a previously unknown device or not
    if extendedaddr not in devices.keys():
        devices[extendedaddr] = {
            "macdevtype": macdevtype,
            "nwkdevtype": nwkdevtype,
        }
    else:
        # Check whether the device's information should be updated or not
        if macdevtype is not None:
            if devices[extendedaddr]["macdevtype"] is None:
                devices[extendedaddr]["macdevtype"] = macdevtype
            elif devices[extendedaddr]["macdevtype"] != macdevtype:
                raise ValueError("Conflicting MAC device type")

        if nwkdevtype is not None:
            if devices[extendedaddr]["nwkdevtype"] is None:
                devices[extendedaddr]["nwkdevtype"] = nwkdevtype
            elif devices[extendedaddr]["nwkdevtype"] != nwkdevtype:
                raise ValueError("Conflicting NWK device type")


def map_addresses(shortaddr, panid, extendedaddr):
    global addresses

    # Sanity checks
    if panid is None:
        raise ValueError("The PAN ID of the device is required")
    elif shortaddr is None or extendedaddr is None:
        raise ValueError("Both addresses of the device are required")
    elif int(panid, 16) < 0 or int(panid, 16) > 65534:
        # Ignore invalid PAN IDs
        return
    elif int(shortaddr, 16) < 0 or int(shortaddr, 16) > 65527:
        # Ignore invalid device short addresses
        return

    # Update the shared dictionary of addresses
    if (shortaddr, panid) not in addresses.keys():
        addresses[(shortaddr, panid)] = extendedaddr
    elif addresses[(shortaddr, panid)] != extendedaddr:
        raise ValueError("Conflicting mapping of addresses")


def map_networks(epid, panid):
    global networks

    # Sanity checks
    if epid is None or panid is None:
        raise ValueError("Both network IDs are required")
    elif int(panid, 16) < 0 or int(panid, 16) > 65534:
        # Ignore invalid PAN IDs
        return

    # Update the shared dictionary of networks
    if epid not in networks.keys():
        networks[epid] = set([panid])
    else:
        networks[epid].add(panid)


def add_encryption_keys(filepath, key_type):
    global network_keys
    global link_keys

    # Distinguish network keys from link keys
    if key_type.lower() == "network":
        loaded_keys = network_keys
        loaded_filepath = NETWORK_FILEPATH
    elif key_type.lower() == "link":
        loaded_keys = link_keys
        loaded_filepath = LINK_FILEPATH
    else:
        raise ValueError("Unknown key type \"{}\"".format(key_type))

    # Add the encryption keys that are not already loaded
    tmp_keys = fs.load_enc_keys(filepath, optional=False)
    added_keys = 0
    for key_name in tmp_keys.keys():
        if tmp_keys[key_name] in loaded_keys.values():
            logging.debug("The encryption key {} from \"{}\" "
                          "was already loaded"
                          "".format(tmp_keys[key_name].hex(), filepath))
        elif key_name in loaded_keys.keys():
            logging.warning("The encryption key {} from \"{}\" "
                            "was not added because its name \"{}\" is "
                            "also used by the encryption key {}"
                            "".format(tmp_keys[key_name].hex(),
                                      filepath,
                                      key_name,
                                      loaded_keys[key_name].hex()))
        else:
            loaded_keys[key_name] = tmp_keys[key_name]
            added_keys += 1

            # Save the encryption key in a configuration file
            with open(loaded_filepath, "a") as fp:
                fp.write("{}\t{}\n".format(loaded_keys[key_name].hex(),
                                           key_name))
    logging.info("Added {} {} keys from \"{}\""
                 "".format(added_keys, key_type.lower(), filepath))


def add_install_codes(filepath):
    global install_codes

    # Add the install codes that are not already loaded
    tmp_codes, _ = fs.load_install_codes(filepath, optional=False)
    added_codes = 0
    for code_name in tmp_codes.keys():
        if tmp_codes[code_name] in install_codes.values():
            logging.debug("The install code {} from \"{}\" was already loaded"
                          "".format(tmp_codes[code_name].hex(), filepath))
        elif code_name in install_codes.keys():
            logging.warning("The install code {} from \"{}\" "
                            "was not added because its name \"{}\" is "
                            "also used by the install code {}"
                            "".format(tmp_codes[code_name].hex(),
                                      filepath,
                                      code_name,
                                      install_codes[code_name].hex()))
        else:
            install_codes[code_name] = tmp_codes[code_name]
            added_codes += 1

            # Save the install code in a configuration file
            with open(INSTALL_FILEPATH, "a") as fp:
                fp.write("{}\t{}\n".format(install_codes[code_name].hex(),
                                           code_name))
    logging.info("Added {} install codes from \"{}\""
                 "".format(added_codes, filepath))


def add_sniffed_key(key_bytes, key_type):
    global network_keys
    global link_keys

    # Distinguish network keys from link keys
    if key_type.lower() == "network":
        loaded_keys = network_keys
    elif key_type.lower() == "link":
        loaded_keys = link_keys
    else:
        raise ValueError("Unknown key type \"{}\"".format(key_type))

    # Add the sniffed key if it is not already loaded
    if key_bytes not in loaded_keys.values():
        # Give it a name
        key_name = "_sniffed_{}".format(len(loaded_keys))

        # Make sure that its name is unique before adding it
        if key_name in loaded_keys.keys():
            logging.warning("The sniffed key {} was not added because "
                            "its name \"{}\" is also used by the {} key {}"
                            "".format(key_bytes.hex(),
                                      key_name,
                                      key_type.lower(),
                                      loaded_keys[key_name].hex()))
        else:
            loaded_keys[key_name] = key_bytes
            logging.info("Added a sniffed {} key: {}"
                         "".format(key_type.lower(), key_bytes.hex()))
