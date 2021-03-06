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
Database module for the zigator package
"""

import logging
import sqlite3
import string


# Define the columns of the packets table in the database
PKT_COLUMNS = [
    ("pcap_directory", "TEXT"),
    ("pcap_filename", "TEXT"),
    ("pkt_num", "INTEGER"),
    ("pkt_time", "REAL"),
    ("pkt_bytes", "TEXT"),
    ("pkt_show", "TEXT"),
    ("phy_length", "INTEGER"),
    ("mac_fcs", "TEXT"),
    ("mac_frametype", "TEXT"),
    ("mac_security", "TEXT"),
    ("mac_framepending", "TEXT"),
    ("mac_ackreq", "TEXT"),
    ("mac_panidcomp", "TEXT"),
    ("mac_dstaddrmode", "TEXT"),
    ("mac_frameversion", "TEXT"),
    ("mac_srcaddrmode", "TEXT"),
    ("mac_seqnum", "INTEGER"),
    ("mac_dstpanid", "TEXT"),
    ("mac_dstshortaddr", "TEXT"),
    ("mac_dstextendedaddr", "TEXT"),
    ("mac_srcpanid", "TEXT"),
    ("mac_srcshortaddr", "TEXT"),
    ("mac_srcextendedaddr", "TEXT"),
    ("mac_cmd_id", "TEXT"),
    ("mac_cmd_payloadlength", "INTEGER"),
    ("mac_assocreq_apc", "TEXT"),
    ("mac_assocreq_devtype", "TEXT"),
    ("mac_assocreq_powsrc", "TEXT"),
    ("mac_assocreq_rxidle", "TEXT"),
    ("mac_assocreq_seccap", "TEXT"),
    ("mac_assocreq_allocaddr", "TEXT"),
    ("mac_assocrsp_shortaddr", "TEXT"),
    ("mac_assocrsp_status", "TEXT"),
    ("mac_disassoc_reason", "TEXT"),
    ("mac_realign_panid", "TEXT"),
    ("mac_realign_coordaddr", "TEXT"),
    ("mac_realign_channel", "INTEGER"),
    ("mac_realign_shortaddr", "TEXT"),
    ("mac_realign_page", "INTEGER"),
    ("mac_gtsreq_length", "INTEGER"),
    ("mac_gtsreq_dir", "TEXT"),
    ("mac_gtsreq_chartype", "TEXT"),
    ("mac_beacon_beaconorder", "INTEGER"),
    ("mac_beacon_sforder", "INTEGER"),
    ("mac_beacon_finalcap", "INTEGER"),
    ("mac_beacon_ble", "INTEGER"),
    ("mac_beacon_pancoord", "TEXT"),
    ("mac_beacon_assocpermit", "TEXT"),
    ("mac_beacon_gtsnum", "INTEGER"),
    ("mac_beacon_gtspermit", "INTEGER"),
    ("mac_beacon_gtsmask", "INTEGER"),
    ("mac_beacon_nsap", "INTEGER"),
    ("mac_beacon_neap", "INTEGER"),
    ("mac_beacon_shortaddresses", "TEXT"),
    ("mac_beacon_extendedaddresses", "TEXT"),
    ("nwk_beacon_protocolid", "INTEGER"),
    ("nwk_beacon_stackprofile", "INTEGER"),
    ("nwk_beacon_protocolversion", "TEXT"),
    ("nwk_beacon_routercap", "TEXT"),
    ("nwk_beacon_devdepth", "INTEGER"),
    ("nwk_beacon_edcap", "TEXT"),
    ("nwk_beacon_epid", "TEXT"),
    ("nwk_beacon_txoffset", "INTEGER"),
    ("nwk_beacon_updateid", "INTEGER"),
    ("nwk_frametype", "TEXT"),
    ("nwk_protocolversion", "TEXT"),
    ("nwk_discroute", "TEXT"),
    ("nwk_multicast", "TEXT"),
    ("nwk_security", "TEXT"),
    ("nwk_srcroute", "TEXT"),
    ("nwk_extendeddst", "TEXT"),
    ("nwk_extendedsrc", "TEXT"),
    ("nwk_edinitiator", "TEXT"),
    ("nwk_dstshortaddr", "TEXT"),
    ("nwk_srcshortaddr", "TEXT"),
    ("nwk_radius", "INTEGER"),
    ("nwk_seqnum", "INTEGER"),
    ("nwk_dstextendedaddr", "TEXT"),
    ("nwk_srcextendedaddr", "TEXT"),
    ("nwk_srcroute_relaycount", "INTEGER"),
    ("nwk_srcroute_relayindex", "INTEGER"),
    ("nwk_srcroute_relaylist", "TEXT"),
    ("nwk_aux_seclevel", "TEXT"),
    ("nwk_aux_keytype", "TEXT"),
    ("nwk_aux_extnonce", "TEXT"),
    ("nwk_aux_framecounter", "INTEGER"),
    ("nwk_aux_srcaddr", "TEXT"),
    ("nwk_aux_keyseqnum", "INTEGER"),
    ("nwk_aux_deckey", "TEXT"),
    ("nwk_aux_decsrc", "TEXT"),
    ("nwk_aux_decpayload", "TEXT"),
    ("nwk_aux_decshow", "TEXT"),
    ("nwk_cmd_id", "TEXT"),
    ("nwk_cmd_payloadlength", "INTEGER"),
    ("nwk_routerequest_mto", "TEXT"),
    ("nwk_routerequest_ed", "TEXT"),
    ("nwk_routerequest_mc", "TEXT"),
    ("nwk_routerequest_id", "INTEGER"),
    ("nwk_routerequest_dstshortaddr", "TEXT"),
    ("nwk_routerequest_pathcost", "INTEGER"),
    ("nwk_routerequest_dstextendedaddr", "TEXT"),
    ("nwk_routereply_eo", "TEXT"),
    ("nwk_routereply_er", "TEXT"),
    ("nwk_routereply_mc", "TEXT"),
    ("nwk_routereply_id", "INTEGER"),
    ("nwk_routereply_origshortaddr", "TEXT"),
    ("nwk_routereply_respshortaddr", "TEXT"),
    ("nwk_routereply_pathcost", "INTEGER"),
    ("nwk_routereply_origextendedaddr", "TEXT"),
    ("nwk_routereply_respextendedaddr", "TEXT"),
    ("nwk_networkstatus_code", "TEXT"),
    ("nwk_networkstatus_dstshortaddr", "TEXT"),
    ("nwk_leave_rejoin", "TEXT"),
    ("nwk_leave_request", "TEXT"),
    ("nwk_leave_rmch", "TEXT"),
    ("nwk_routerecord_relaycount", "INTEGER"),
    ("nwk_routerecord_relaylist", "TEXT"),
    ("nwk_rejoinreq_apc", "TEXT"),
    ("nwk_rejoinreq_devtype", "TEXT"),
    ("nwk_rejoinreq_powsrc", "TEXT"),
    ("nwk_rejoinreq_rxidle", "TEXT"),
    ("nwk_rejoinreq_seccap", "TEXT"),
    ("nwk_rejoinreq_allocaddr", "TEXT"),
    ("nwk_rejoinrsp_shortaddr", "TEXT"),
    ("nwk_rejoinrsp_status", "TEXT"),
    ("nwk_linkstatus_count", "INTEGER"),
    ("nwk_linkstatus_first", "TEXT"),
    ("nwk_linkstatus_last", "TEXT"),
    ("nwk_linkstatus_addresses", "TEXT"),
    ("nwk_linkstatus_incomingcosts", "TEXT"),
    ("nwk_linkstatus_outgoingcosts", "TEXT"),
    ("nwk_networkreport_count", "INTEGER"),
    ("nwk_networkreport_type", "TEXT"),
    ("nwk_networkreport_epid", "TEXT"),
    ("nwk_networkreport_info", "TEXT"),
    ("nwk_networkupdate_count", "INTEGER"),
    ("nwk_networkupdate_type", "TEXT"),
    ("nwk_networkupdate_epid", "TEXT"),
    ("nwk_networkupdate_updateid", "INTEGER"),
    ("nwk_networkupdate_newpanid", "TEXT"),
    ("nwk_edtimeoutreq_reqtime", "TEXT"),
    ("nwk_edtimeoutreq_edconf", "INTEGER"),
    ("nwk_edtimeoutrsp_status", "TEXT"),
    ("nwk_edtimeoutrsp_poll", "TEXT"),
    ("nwk_edtimeoutrsp_timeout", "TEXT"),
    ("aps_frametype", "TEXT"),
    ("aps_delmode", "TEXT"),
    ("aps_ackformat", "TEXT"),
    ("aps_security", "TEXT"),
    ("aps_ackreq", "TEXT"),
    ("aps_exthdr", "TEXT"),
    ("aps_dstendpoint", "INTEGER"),
    ("aps_groupaddr", "TEXT"),
    ("aps_clusterid", "TEXT"),
    ("aps_clustername", "TEXT"),
    ("aps_profileid", "TEXT"),
    ("aps_profilename", "TEXT"),
    ("aps_srcendpoint", "INTEGER"),
    ("aps_counter", "INTEGER"),
    ("aps_fragmentation", "TEXT"),
    ("aps_blocknumber", "INTEGER"),
    ("aps_ackbitfield", "INTEGER"),
    ("aps_aux_seclevel", "TEXT"),
    ("aps_aux_keytype", "TEXT"),
    ("aps_aux_extnonce", "TEXT"),
    ("aps_aux_framecounter", "INTEGER"),
    ("aps_aux_srcaddr", "TEXT"),
    ("aps_aux_keyseqnum", "INTEGER"),
    ("aps_aux_deckey", "TEXT"),
    ("aps_aux_decsrc", "TEXT"),
    ("aps_aux_decpayload", "TEXT"),
    ("aps_aux_decshow", "TEXT"),
    ("aps_cmd_id", "TEXT"),
    ("aps_transportkey_stdkeytype", "TEXT"),
    ("aps_transportkey_key", "TEXT"),
    ("aps_transportkey_keyseqnum", "INTEGER"),
    ("aps_transportkey_dstextendedaddr", "TEXT"),
    ("aps_transportkey_srcextendedaddr", "TEXT"),
    ("aps_transportkey_prtextendedaddr", "TEXT"),
    ("aps_transportkey_initflag", "TEXT"),
    ("aps_updatedevice_extendedaddr", "TEXT"),
    ("aps_updatedevice_shortaddr", "TEXT"),
    ("aps_updatedevice_status", "TEXT"),
    ("aps_removedevice_extendedaddr", "TEXT"),
    ("aps_requestkey_reqkeytype", "TEXT"),
    ("aps_requestkey_prtextendedaddr", "TEXT"),
    ("aps_switchkey_keyseqnum", "INTEGER"),
    ("aps_tunnel_dstextendedaddr", "TEXT"),
    ("aps_tunnel_frametype", "TEXT"),
    ("aps_tunnel_delmode", "TEXT"),
    ("aps_tunnel_ackformat", "TEXT"),
    ("aps_tunnel_security", "TEXT"),
    ("aps_tunnel_ackreq", "TEXT"),
    ("aps_tunnel_exthdr", "TEXT"),
    ("aps_tunnel_counter", "INTEGER"),
    ("aps_verifykey_stdkeytype", "TEXT"),
    ("aps_verifykey_extendedaddr", "TEXT"),
    ("aps_verifykey_keyhash", "TEXT"),
    ("aps_confirmkey_status", "TEXT"),
    ("aps_confirmkey_stdkeytype", "TEXT"),
    ("aps_confirmkey_extendedaddr", "TEXT"),
    ("zdp_seqnum", "INTEGER"),
    ("zcl_frametype", "TEXT"),
    ("zcl_manufspecific", "TEXT"),
    ("zcl_direction", "TEXT"),
    ("zcl_disdefrsp", "TEXT"),
    ("zcl_manufcode", "TEXT"),
    ("zcl_seqnum", "INTEGER"),
    ("zcl_cmd_id", "TEXT"),
    ("der_same_macnwkdst", "TEXT"),
    ("der_same_macnwksrc", "TEXT"),
    ("der_tx_type", "TEXT"),
    ("der_mac_dsttype", "TEXT"),
    ("der_mac_srctype", "TEXT"),
    ("der_nwk_dsttype", "TEXT"),
    ("der_nwk_srctype", "TEXT"),
    ("der_mac_dstpanid", "TEXT"),
    ("der_mac_dstshortaddr", "TEXT"),
    ("der_mac_dstextendedaddr", "TEXT"),
    ("der_mac_srcpanid", "TEXT"),
    ("der_mac_srcshortaddr", "TEXT"),
    ("der_mac_srcextendedaddr", "TEXT"),
    ("der_nwk_dstpanid", "TEXT"),
    ("der_nwk_dstshortaddr", "TEXT"),
    ("der_nwk_dstextendedaddr", "TEXT"),
    ("der_nwk_srcpanid", "TEXT"),
    ("der_nwk_srcshortaddr", "TEXT"),
    ("der_nwk_srcextendedaddr", "TEXT"),
    ("warning_msg", "TEXT"),
    ("error_msg", "TEXT"),
]

# Define a list that contains only the column names for each table
PKT_COLUMN_NAMES = [column[0] for column in PKT_COLUMNS]

# Define sets that will be used to construct valid column definitions
ALLOWED_CHARACTERS = set(string.ascii_letters + string.digits + "_")
ALLOWED_TYPES = set(["TEXT", "INTEGER", "REAL", "BLOB"])
CONSTRAINED_PKT_COLUMNS = set([
    "pcap_directory",
    "pcap_filename",
    "pkt_num",
    "pkt_time",
    "pkt_bytes",
    "pkt_show",
])

# Initialize global variables for interacting with the database
connection = None
cursor = None


def connect(db_filepath):
    global connection
    global cursor

    # Open a connection with the database
    connection = sqlite3.connect(db_filepath)
    connection.text_factory = str
    cursor = connection.cursor()


def create_table(tablename):
    global connection
    global cursor

    if tablename == "packets":
        columns = PKT_COLUMNS
        constrained_columns = CONSTRAINED_PKT_COLUMNS
    else:
        raise ValueError("Unknown table name \"{}\"".format(tablename))

    # Drop the table if it already exists
    table_drop_command = "DROP TABLE IF EXISTS {}".format(tablename)
    cursor.execute(table_drop_command)

    # Create the table
    table_creation_command = "CREATE TABLE {}(".format(tablename)
    delimiter_needed = False
    for column in columns:
        if delimiter_needed:
            table_creation_command += ", "
        else:
            delimiter_needed = True

        column_name = column[0]
        column_type = column[1]

        for i in range(len(column_name)):
            if column_name[i] not in ALLOWED_CHARACTERS:
                raise ValueError("The character \"{}\" in the name of the "
                                 "column \"{}\" is not allowed"
                                 "".format(column_name[i], column_name))

        if column_name[0].isdigit():
            raise ValueError("The name of the column \"{}\" is not allowed "
                             "because it starts with a digit"
                             "".format(column_name))

        table_creation_command += column_name

        if column_type not in ALLOWED_TYPES:
            raise ValueError("The column type \"{}\" is not in the "
                             "set of allowed column types {}"
                             "".format(column_type, ALLOWED_TYPES))

        table_creation_command += " " + column_type

        if column_name in constrained_columns:
            table_creation_command += " NOT NULL"
    table_creation_command += ")"

    # Execute the constructed command
    cursor.execute(table_creation_command)


def insert_pkt(entry):
    global cursor

    # Insert the parsed data into the database
    cursor.execute("INSERT INTO packets VALUES ({})"
                   "".format(", ".join("?"*len(PKT_COLUMNS))),
                   tuple(entry[column_name]
                         for column_name in PKT_COLUMN_NAMES))


def commit():
    global connection

    connection.commit()


def grouped_count(selected_columns, count_errors):
    global cursor

    # Sanity checks
    if len(selected_columns) == 0:
        raise ValueError("At least one selected column is required")
    for column_name in selected_columns:
        if column_name not in PKT_COLUMN_NAMES:
            raise ValueError("Unknown column name \"{}\"".format(column_name))

    # Construct the selection command
    column_csv = ", ".join(selected_columns)
    select_command = "SELECT {}, COUNT(*) FROM packets".format(column_csv)
    if not count_errors:
        select_command += " WHERE error_msg IS NULL"
    select_command += " GROUP BY {}".format(column_csv)

    # Return the results of the constructed command
    cursor.execute(select_command)
    return cursor.fetchall()


def fetch_values(selected_columns, conditions, distinct):
    global cursor

    # Sanity checks
    if len(selected_columns) == 0:
        raise ValueError("At least one selected column is required")
    for column_name in selected_columns:
        if column_name not in PKT_COLUMN_NAMES:
            raise ValueError("Unknown column name \"{}\"".format(column_name))

    # Construct the selection command
    column_csv = ", ".join(selected_columns)
    if distinct:
        select_command = "SELECT DISTINCT {} FROM packets".format(column_csv)
    else:
        select_command = "SELECT {} FROM packets".format(column_csv)
    expr_statements = []
    expr_values = []
    if conditions is not None:
        select_command += " WHERE "
        for condition in conditions:
            param = condition[0]
            value = condition[1]
            if param[0] == "!":
                neq = True
                param = param[1:]
            else:
                neq = False
            if param not in PKT_COLUMN_NAMES:
                raise ValueError("Unknown column name \"{}\"".format(param))
            elif value is None:
                if neq:
                    expr_statements.append("{} IS NOT NULL".format(param))
                else:
                    expr_statements.append("{} IS NULL".format(param))
            else:
                if neq:
                    expr_statements.append("{}!=?".format(param))
                else:
                    expr_statements.append("{}=?".format(param))
                expr_values.append(value)
        select_command += " AND ".join(expr_statements)

    # Return the results of the constructed command
    cursor.execute(select_command, tuple(expr_values))
    return cursor.fetchall()


def matching_frequency(conditions):
    global cursor

    # Construct the selection command
    select_command = "SELECT COUNT(*) FROM packets"
    expr_statements = []
    expr_values = []
    if conditions is not None:
        select_command += " WHERE "
        for condition in conditions:
            param = condition[0]
            value = condition[1]
            if param[0] == "!":
                neq = True
                param = param[1:]
            else:
                neq = False
            if param not in PKT_COLUMN_NAMES:
                raise ValueError("Unknown column name \"{}\"".format(param))
            elif value is None:
                if neq:
                    expr_statements.append("{} IS NOT NULL".format(param))
                else:
                    expr_statements.append("{} IS NULL".format(param))
            else:
                if neq:
                    expr_statements.append("{}!=?".format(param))
                else:
                    expr_statements.append("{}=?".format(param))
                expr_values.append(value)
        select_command += " AND ".join(expr_statements)

    # Return the results of the constructed command
    cursor.execute(select_command, tuple(expr_values))
    return cursor.fetchall()[0][0]


def store_networks(networks):
    global cursor

    # Drop the table if it already exists
    cursor.execute("DROP TABLE IF EXISTS networks")

    # Create the table
    cursor.execute("CREATE TABLE networks(epid TEXT NOT NULL, panids TEXT)")

    # Insert the data into the database
    for epid in networks.keys():
        cursor.execute("INSERT INTO networks VALUES (?, ?)",
                       tuple([epid, ",".join(networks[epid])]))


def store_devices(devices):
    global cursor

    # Drop the table if it already exists
    cursor.execute("DROP TABLE IF EXISTS devices")

    # Create the table
    cursor.execute("CREATE TABLE devices(extendedaddr TEXT NOT NULL, "
                   "macdevtype TEXT, nwkdevtype TEXT)")

    # Insert the data into the database
    for extendedaddr in devices.keys():
        cursor.execute("INSERT INTO devices VALUES (?, ?, ?)",
                       tuple([extendedaddr,
                              devices[extendedaddr]["macdevtype"],
                              devices[extendedaddr]["nwkdevtype"]]))


def store_addresses(addresses):
    global cursor

    # Drop the table if it already exists
    cursor.execute("DROP TABLE IF EXISTS addresses")

    # Create the table
    cursor.execute("CREATE TABLE addresses(shortaddr TEXT NOT NULL, "
                   "panid TEXT NOT NULL, extendedaddr TEXT)")

    # Insert the data into the database
    for addrpan in addresses.keys():
        cursor.execute("INSERT INTO addresses VALUES (?, ?, ?)",
                       tuple([addrpan[0], addrpan[1], addresses[addrpan]]))


def store_pairs(pairs):
    global cursor

    # Drop the table if it already exists
    cursor.execute("DROP TABLE IF EXISTS pairs")

    # Create the table
    cursor.execute("CREATE TABLE pairs(srcaddr TEXT NOT NULL, "
                   "dstaddr TEXT NOT NULL, panid TEXT NOT NULL, "
                   "first REAL, last REAL)")

    # Insert the data into the database
    for pairpan in pairs.keys():
        cursor.execute("INSERT INTO pairs VALUES (?, ?, ?, ?, ?)",
                       tuple([pairpan[0],
                              pairpan[1],
                              pairpan[2],
                              pairs[pairpan]["first"],
                              pairs[pairpan]["last"]]))


def get_macdevtype(shortaddr=None, panid=None, extendedaddr=None):
    global cursor

    # Make sure that the extended address of the device is known
    if extendedaddr is None:
        cursor.execute("SELECT extendedaddr FROM addresses WHERE shortaddr=? "
                       "AND panid=?", tuple([shortaddr, panid]))
        results = cursor.fetchall()
        if len(results) == 0:
            return None
        elif len(results) != 1:
            return "Conflicting Data"
        elif results[0][0] == "Conflicting Data":
            return "Conflicting Data"
        else:
            extendedaddr = results[0][0]

    # Use the extended address of the device to determine its MAC device type
    cursor.execute("SELECT macdevtype FROM devices WHERE extendedaddr=?",
                   tuple([extendedaddr]))
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    elif len(results) != 1:
        return "Conflicting Data"
    else:
        return results[0][0]


def get_nwkdevtype(shortaddr=None, panid=None, extendedaddr=None):
    global cursor

    # Make sure that the extended address of the device is known
    if extendedaddr is None:
        cursor.execute("SELECT extendedaddr FROM addresses WHERE shortaddr=? "
                       "AND panid=?", tuple([shortaddr, panid]))
        results = cursor.fetchall()
        if len(results) == 0:
            return None
        elif len(results) != 1:
            return "Conflicting Data"
        elif results[0][0] == "Conflicting Data":
            return "Conflicting Data"
        else:
            extendedaddr = results[0][0]

    # Use the extended address of the device to determine its NWK device type
    cursor.execute("SELECT nwkdevtype FROM devices WHERE extendedaddr=?",
                   tuple([extendedaddr]))
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    elif len(results) != 1:
        return "Conflicting Data"
    else:
        return results[0][0]


def update_table(selected_columns, selected_values, conditions):
    global connection
    global cursor

    # Sanity checks
    if len(selected_columns) == 0:
        raise ValueError("At least one selected column is required")
    elif len(selected_columns) != len(selected_values):
        raise ValueError("The number of selected columns does not match "
                         "the number of selected values")
    for column_name in selected_columns:
        if column_name not in PKT_COLUMN_NAMES:
            raise ValueError("Unknown column name \"{}\"".format(column_name))

    # Update the table
    set_statements = ["{} = ?".format(x) for x in selected_columns]
    update_command = "UPDATE packets SET {}".format(", ".join(set_statements))
    expr_statements = []
    expr_values = list(selected_values)
    if conditions is not None:
        update_command += " WHERE "
        for condition in conditions:
            param = condition[0]
            value = condition[1]
            if param[0] == "!":
                neq = True
                param = param[1:]
            else:
                neq = False
            if param not in PKT_COLUMN_NAMES:
                raise ValueError("Unknown column name \"{}\"".format(param))
            elif value is None:
                if neq:
                    expr_statements.append("{} IS NOT NULL".format(param))
                else:
                    expr_statements.append("{} IS NULL".format(param))
            else:
                if neq:
                    expr_statements.append("{}!=?".format(param))
                else:
                    expr_statements.append("{}=?".format(param))
                expr_values.append(value)
        update_command += " AND ".join(expr_statements)

    # Execute the constructed command
    cursor.execute(update_command, tuple(expr_values))


def update_packets():
    global cursor

    # Check for conflicting addresses
    cursor.execute("SELECT DISTINCT shortaddr, panid FROM addresses "
                   "WHERE extendedaddr=\"Conflicting Data\"")
    results = cursor.fetchall()
    for result in results:
        shortaddr = result[0]
        panid = result[1]
        logging.warning("Observed conflicting data regarding the "
                        "extended address of the device that uses "
                        "{} as its short address and {} as its PAN ID"
                        "".format(shortaddr, panid))

        # Update the "MAC Destination Type" column
        update_columns = (
            "der_mac_dstextendedaddr",
            "der_mac_dsttype",
        )
        update_values = (
            "Conflicting Data",
            "MAC Dst Type: Conflicting Data",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("mac_dstaddrmode", "Short destination MAC address"),
            ("der_mac_dstpanid", panid),
            ("der_mac_dstshortaddr", shortaddr),
            ("!der_mac_dsttype", "MAC Dst Type: Conflicting Data"),
        )
        update_table(update_columns, update_values, conditions)

        # Update the "MAC Source Type" column
        update_columns = (
            "der_mac_srcextendedaddr",
            "der_mac_srctype",
        )
        update_values = (
            "Conflicting Data",
            "MAC Src Type: Conflicting Data",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("mac_srcaddrmode", "Short source MAC address"),
            ("der_mac_srcpanid", panid),
            ("der_mac_srcshortaddr", shortaddr),
            ("!der_mac_srctype", "MAC Src Type: Conflicting Data"),
        )
        update_table(update_columns, update_values, conditions)

        # Update the "NWK Destination Type" column
        update_columns = (
            "der_nwk_dstextendedaddr",
            "der_nwk_dsttype",
        )
        update_values = (
            "Conflicting Data",
            "NWK Dst Type: Conflicting Data",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("!nwk_dstshortaddr", None),
            ("der_nwk_dstpanid", panid),
            ("der_nwk_dstshortaddr", shortaddr),
            ("!der_nwk_dsttype", "NWK Dst Type: Conflicting Data"),
        )
        update_table(update_columns, update_values, conditions)

        # Update the "NWK Source Type" column
        update_columns = (
            "der_nwk_srcextendedaddr",
            "der_nwk_srctype",
        )
        update_values = (
            "Conflicting Data",
            "NWK Src Type: Conflicting Data",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("!nwk_srcshortaddr", None),
            ("der_nwk_srcpanid", panid),
            ("der_nwk_srcshortaddr", shortaddr),
            ("!der_nwk_srctype", "NWK Src Type: Conflicting Data"),
        )
        update_table(update_columns, update_values, conditions)

    # Check for previously unknown MAC Destination extended addresses
    cursor.execute("SELECT DISTINCT der_mac_dstpanid, "
                   "der_mac_dstshortaddr FROM packets "
                   "WHERE der_mac_dsttype=\"MAC Dst Type: None\" "
                   "AND der_mac_dstextendedaddr IS NULL")
    results = cursor.fetchall()
    logging.debug("Trying to identify {} previously unknown "
                  "MAC Destination extended addresses..."
                  "".format(len(results)))
    for result in results:
        panid = result[0]
        shortaddr = result[1]
        cursor.execute("SELECT extendedaddr FROM addresses "
                       "WHERE shortaddr=? AND panid=?",
                       (shortaddr, panid))
        fetched_addresses = cursor.fetchall()
        if len(fetched_addresses) == 0:
            continue
        elif len(fetched_addresses) != 1:
            update_values = (
                "Conflicting Data",
                "MAC Dst Type: Conflicting Data",
            )
        elif fetched_addresses[0][0] == "Conflicting Data":
            update_values = (
                "Conflicting Data",
                "MAC Dst Type: Conflicting Data",
            )
        else:
            extendedaddr = fetched_addresses[0][0]
            cursor.execute("SELECT nwkdevtype FROM devices "
                           "WHERE extendedaddr=?",
                           tuple([extendedaddr]))
            fetched_nwkdevtype = cursor.fetchall()
            if len(fetched_nwkdevtype) == 0:
                update_values = (
                    extendedaddr,
                    "MAC Dst Type: None",
                )
            elif len(fetched_nwkdevtype) != 1:
                update_values = (
                    extendedaddr,
                    "MAC Dst Type: Conflicting Data",
                )
            else:
                update_values = (
                    extendedaddr,
                    "MAC Dst Type: {}".format(fetched_nwkdevtype[0][0]),
                )
        update_columns = (
            "der_mac_dstextendedaddr",
            "der_mac_dsttype",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("mac_dstaddrmode", "Short destination MAC address"),
            ("der_mac_dstpanid", panid),
            ("der_mac_dstshortaddr", shortaddr),
            ("der_mac_dstextendedaddr", None),
            ("der_mac_dsttype", "MAC Dst Type: None"),
        )
        update_table(update_columns, update_values, conditions)

    # Check for previously unknown MAC Source extended addresses
    cursor.execute("SELECT DISTINCT der_mac_srcpanid, "
                   "der_mac_srcshortaddr FROM packets "
                   "WHERE der_mac_srctype=\"MAC Src Type: None\" "
                   "AND der_mac_srcextendedaddr IS NULL")
    results = cursor.fetchall()
    logging.debug("Trying to identify {} previously unknown "
                  "MAC Source extended addresses..."
                  "".format(len(results)))
    for result in results:
        panid = result[0]
        shortaddr = result[1]
        cursor.execute("SELECT extendedaddr FROM addresses "
                       "WHERE shortaddr=? AND panid=?",
                       (shortaddr, panid))
        fetched_addresses = cursor.fetchall()
        if len(fetched_addresses) == 0:
            continue
        elif len(fetched_addresses) != 1:
            update_values = (
                "Conflicting Data",
                "MAC Src Type: Conflicting Data",
            )
        elif fetched_addresses[0][0] == "Conflicting Data":
            update_values = (
                "Conflicting Data",
                "MAC Src Type: Conflicting Data",
            )
        else:
            extendedaddr = fetched_addresses[0][0]
            cursor.execute("SELECT nwkdevtype FROM devices "
                           "WHERE extendedaddr=?",
                           tuple([extendedaddr]))
            fetched_nwkdevtype = cursor.fetchall()
            if len(fetched_nwkdevtype) == 0:
                update_values = (
                    extendedaddr,
                    "MAC Src Type: None",
                )
            elif len(fetched_nwkdevtype) != 1:
                update_values = (
                    extendedaddr,
                    "MAC Src Type: Conflicting Data",
                )
            else:
                update_values = (
                    extendedaddr,
                    "MAC Src Type: {}".format(fetched_nwkdevtype[0][0]),
                )
        update_columns = (
            "der_mac_srcextendedaddr",
            "der_mac_srctype",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("mac_srcaddrmode", "Short source MAC address"),
            ("der_mac_srcpanid", panid),
            ("der_mac_srcshortaddr", shortaddr),
            ("der_mac_srcextendedaddr", None),
            ("der_mac_srctype", "MAC Src Type: None"),
        )
        update_table(update_columns, update_values, conditions)

    # Check for previously unknown NWK Destination extended addresses
    cursor.execute("SELECT DISTINCT der_nwk_dstpanid, "
                   "der_nwk_dstshortaddr FROM packets "
                   "WHERE der_nwk_dsttype=\"NWK Dst Type: None\" "
                   "AND der_nwk_dstextendedaddr IS NULL")
    results = cursor.fetchall()
    logging.debug("Trying to identify {} previously unknown "
                  "NWK Destination extended addresses..."
                  "".format(len(results)))
    for result in results:
        panid = result[0]
        shortaddr = result[1]
        cursor.execute("SELECT extendedaddr FROM addresses "
                       "WHERE shortaddr=? AND panid=?",
                       (shortaddr, panid))
        fetched_addresses = cursor.fetchall()
        if len(fetched_addresses) == 0:
            continue
        elif len(fetched_addresses) != 1:
            update_values = (
                "Conflicting Data",
                "NWK Dst Type: Conflicting Data",
            )
        elif fetched_addresses[0][0] == "Conflicting Data":
            update_values = (
                "Conflicting Data",
                "NWK Dst Type: Conflicting Data",
            )
        else:
            extendedaddr = fetched_addresses[0][0]
            cursor.execute("SELECT nwkdevtype FROM devices "
                           "WHERE extendedaddr=?",
                           tuple([extendedaddr]))
            fetched_nwkdevtype = cursor.fetchall()
            if len(fetched_nwkdevtype) == 0:
                update_values = (
                    extendedaddr,
                    "NWK Dst Type: None",
                )
            elif len(fetched_nwkdevtype) != 1:
                update_values = (
                    extendedaddr,
                    "NWK Dst Type: Conflicting Data",
                )
            else:
                update_values = (
                    extendedaddr,
                    "NWK Dst Type: {}".format(fetched_nwkdevtype[0][0]),
                )
        update_columns = (
            "der_nwk_dstextendedaddr",
            "der_nwk_dsttype",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("!nwk_dstshortaddr", None),
            ("der_nwk_dstpanid", panid),
            ("der_nwk_dstshortaddr", shortaddr),
            ("der_nwk_dstextendedaddr", None),
            ("der_nwk_dsttype", "NWK Dst Type: None"),
        )
        update_table(update_columns, update_values, conditions)

    # Check for previously unknown NWK Source extended addresses
    cursor.execute("SELECT DISTINCT der_nwk_srcpanid, "
                   "der_nwk_srcshortaddr FROM packets "
                   "WHERE der_nwk_srctype=\"NWK Src Type: None\" "
                   "AND der_nwk_srcextendedaddr IS NULL")
    results = cursor.fetchall()
    logging.debug("Trying to identify {} previously unknown "
                  "NWK Source extended addresses..."
                  "".format(len(results)))
    for result in results:
        panid = result[0]
        shortaddr = result[1]
        cursor.execute("SELECT extendedaddr FROM addresses "
                       "WHERE shortaddr=? AND panid=?",
                       (shortaddr, panid))
        fetched_addresses = cursor.fetchall()
        if len(fetched_addresses) == 0:
            continue
        elif len(fetched_addresses) != 1:
            update_values = (
                "Conflicting Data",
                "NWK Src Type: Conflicting Data",
            )
        elif fetched_addresses[0][0] == "Conflicting Data":
            update_values = (
                "Conflicting Data",
                "NWK Src Type: Conflicting Data",
            )
        else:
            extendedaddr = fetched_addresses[0][0]
            cursor.execute("SELECT nwkdevtype FROM devices "
                           "WHERE extendedaddr=?",
                           tuple([extendedaddr]))
            fetched_nwkdevtype = cursor.fetchall()
            if len(fetched_nwkdevtype) == 0:
                update_values = (
                    extendedaddr,
                    "NWK Src Type: None",
                )
            elif len(fetched_nwkdevtype) != 1:
                update_values = (
                    extendedaddr,
                    "NWK Src Type: Conflicting Data",
                )
            else:
                update_values = (
                    extendedaddr,
                    "NWK Src Type: {}".format(fetched_nwkdevtype[0][0]),
                )
        update_columns = (
            "der_nwk_srcextendedaddr",
            "der_nwk_srctype",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("!nwk_srcshortaddr", None),
            ("der_nwk_srcpanid", panid),
            ("der_nwk_srcshortaddr", shortaddr),
            ("der_nwk_srcextendedaddr", None),
            ("der_nwk_srctype", "NWK Src Type: None"),
        )
        update_table(update_columns, update_values, conditions)

    # Check for conflicting device types
    cursor.execute("SELECT DISTINCT extendedaddr FROM devices")
    results = cursor.fetchall()
    for result in results:
        extendedaddr = result[0]
        if get_macdevtype(extendedaddr=extendedaddr) == "Conflicting Data":
            logging.warning("Observed conflicting data regarding the "
                            "MAC device type of the device that uses "
                            "{} as its extended address".format(extendedaddr))

        if get_nwkdevtype(extendedaddr=extendedaddr) == "Conflicting Data":
            logging.warning("Observed conflicting data regarding the "
                            "NWK device type of the device that uses "
                            "{} as its extended address".format(extendedaddr))

            # Update the "MAC Destination Type" column
            update_columns = (
                "der_mac_dsttype",
            )
            update_values = (
                "MAC Dst Type: Conflicting Data",
            )
            conditions = (
                ("error_msg", None),
                ("mac_panidcomp",
                    "The source PAN ID is the same as the destination PAN ID"),
                ("mac_dstaddrmode", "Short destination MAC address"),
                ("der_mac_dstextendedaddr", extendedaddr),
                ("!der_mac_dsttype", "MAC Dst Type: Conflicting Data"),
            )
            update_table(update_columns, update_values, conditions)

            # Update the "MAC Source Type" column
            update_columns = (
                "der_mac_srctype",
            )
            update_values = (
                "MAC Src Type: Conflicting Data",
            )
            conditions = (
                ("error_msg", None),
                ("mac_panidcomp",
                    "The source PAN ID is the same as the destination PAN ID"),
                ("mac_srcaddrmode", "Short source MAC address"),
                ("der_mac_srcextendedaddr", extendedaddr),
                ("!der_mac_srctype", "MAC Src Type: Conflicting Data"),
            )
            update_table(update_columns, update_values, conditions)

            # Update the "NWK Destination Type" column
            update_columns = (
                "der_nwk_dsttype",
            )
            update_values = (
                "NWK Dst Type: Conflicting Data",
            )
            conditions = (
                ("error_msg", None),
                ("mac_panidcomp",
                    "The source PAN ID is the same as the destination PAN ID"),
                ("!nwk_dstshortaddr", None),
                ("der_nwk_dstextendedaddr", extendedaddr),
                ("!der_nwk_dsttype", "NWK Dst Type: Conflicting Data"),
            )
            update_table(update_columns, update_values, conditions)

            # Update the "NWK Source Type" column
            update_columns = (
                "der_nwk_srctype",
            )
            update_values = (
                "NWK Src Type: Conflicting Data",
            )
            conditions = (
                ("error_msg", None),
                ("mac_panidcomp",
                    "The source PAN ID is the same as the destination PAN ID"),
                ("!nwk_srcshortaddr", None),
                ("der_nwk_srcextendedaddr", extendedaddr),
                ("!der_nwk_srctype", "NWK Src Type: Conflicting Data"),
            )
            update_table(update_columns, update_values, conditions)

    # Check for previously unknown MAC Destination Types
    cursor.execute("SELECT DISTINCT der_mac_dstextendedaddr FROM packets "
                   "WHERE der_mac_dsttype=\"MAC Dst Type: None\" "
                   "AND der_mac_dstextendedaddr IS NOT NULL "
                   "AND der_mac_dstextendedaddr!=\"Conflicting Data\"")
    results = cursor.fetchall()
    logging.debug("Trying to identify {} previously unknown "
                  "MAC Destination Types..."
                  "".format(len(results)))
    for result in results:
        extendedaddr = result[0]
        cursor.execute("SELECT nwkdevtype FROM devices "
                       "WHERE extendedaddr=?",
                       tuple([extendedaddr]))
        fetched_nwkdevtype = cursor.fetchall()
        if len(fetched_nwkdevtype) == 0:
            continue
        elif len(fetched_nwkdevtype) != 1:
            update_values = (
                "MAC Dst Type: Conflicting Data",
            )
        else:
            nwkdevtype = fetched_nwkdevtype[0][0]
            if nwkdevtype is None:
                continue
            else:
                update_values = (
                    "MAC Dst Type: {}".format(nwkdevtype),
                )
        update_columns = (
            "der_mac_dsttype",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("mac_dstaddrmode", "Short destination MAC address"),
            ("der_mac_dstextendedaddr", extendedaddr),
            ("der_mac_dsttype", "MAC Dst Type: None"),
        )
        update_table(update_columns, update_values, conditions)

    # Check for previously unknown MAC Source Types
    cursor.execute("SELECT DISTINCT der_mac_srcextendedaddr FROM packets "
                   "WHERE der_mac_srctype=\"MAC Src Type: None\" "
                   "AND der_mac_srcextendedaddr IS NOT NULL "
                   "AND der_mac_srcextendedaddr!=\"Conflicting Data\"")
    results = cursor.fetchall()
    logging.debug("Trying to identify {} previously unknown "
                  "MAC Source Types..."
                  "".format(len(results)))
    for result in results:
        extendedaddr = result[0]
        cursor.execute("SELECT nwkdevtype FROM devices "
                       "WHERE extendedaddr=?",
                       tuple([extendedaddr]))
        fetched_nwkdevtype = cursor.fetchall()
        if len(fetched_nwkdevtype) == 0:
            continue
        elif len(fetched_nwkdevtype) != 1:
            update_values = (
                "MAC Src Type: Conflicting Data",
            )
        else:
            nwkdevtype = fetched_nwkdevtype[0][0]
            if nwkdevtype is None:
                continue
            else:
                update_values = (
                    "MAC Src Type: {}".format(nwkdevtype),
                )
        update_columns = (
            "der_mac_srctype",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("mac_srcaddrmode", "Short source MAC address"),
            ("der_mac_srcextendedaddr", extendedaddr),
            ("der_mac_srctype", "MAC Src Type: None"),
        )
        update_table(update_columns, update_values, conditions)

    # Check for previously unknown NWK Destination Types
    cursor.execute("SELECT DISTINCT der_nwk_dstextendedaddr FROM packets "
                   "WHERE der_nwk_dsttype=\"NWK Dst Type: None\" "
                   "AND der_nwk_dstextendedaddr IS NOT NULL "
                   "AND der_nwk_dstextendedaddr!=\"Conflicting Data\"")
    results = cursor.fetchall()
    logging.debug("Trying to identify {} previously unknown "
                  "NWK Destination Types..."
                  "".format(len(results)))
    for result in results:
        extendedaddr = result[0]
        cursor.execute("SELECT nwkdevtype FROM devices "
                       "WHERE extendedaddr=?",
                       tuple([extendedaddr]))
        fetched_nwkdevtype = cursor.fetchall()
        if len(fetched_nwkdevtype) == 0:
            continue
        elif len(fetched_nwkdevtype) != 1:
            update_values = (
                "NWK Dst Type: Conflicting Data",
            )
        else:
            nwkdevtype = fetched_nwkdevtype[0][0]
            if nwkdevtype is None:
                continue
            else:
                update_values = (
                    "NWK Dst Type: {}".format(nwkdevtype),
                )
        update_columns = (
            "der_nwk_dsttype",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("!nwk_dstshortaddr", None),
            ("der_nwk_dstextendedaddr", extendedaddr),
            ("der_nwk_dsttype", "NWK Dst Type: None"),
        )
        update_table(update_columns, update_values, conditions)

    # Check for previously unknown NWK Source Types
    cursor.execute("SELECT DISTINCT der_nwk_srcextendedaddr FROM packets "
                   "WHERE der_nwk_srctype=\"NWK Src Type: None\" "
                   "AND der_nwk_srcextendedaddr IS NOT NULL "
                   "AND der_nwk_srcextendedaddr!=\"Conflicting Data\"")
    results = cursor.fetchall()
    logging.debug("Trying to identify {} previously unknown "
                  "NWK Source Types..."
                  "".format(len(results)))
    for result in results:
        extendedaddr = result[0]
        cursor.execute("SELECT nwkdevtype FROM devices "
                       "WHERE extendedaddr=?",
                       tuple([extendedaddr]))
        fetched_nwkdevtype = cursor.fetchall()
        if len(fetched_nwkdevtype) == 0:
            continue
        elif len(fetched_nwkdevtype) != 1:
            update_values = (
                "NWK Src Type: Conflicting Data",
            )
        else:
            nwkdevtype = fetched_nwkdevtype[0][0]
            if nwkdevtype is None:
                continue
            else:
                update_values = (
                    "NWK Src Type: {}".format(nwkdevtype),
                )
        update_columns = (
            "der_nwk_srctype",
        )
        conditions = (
            ("error_msg", None),
            ("mac_panidcomp",
                "The source PAN ID is the same as the destination PAN ID"),
            ("!nwk_srcshortaddr", None),
            ("der_nwk_srcextendedaddr", extendedaddr),
            ("der_nwk_srctype", "NWK Src Type: None"),
        )
        update_table(update_columns, update_values, conditions)


def disconnect():
    global connection
    global cursor

    # Close the connection with the database
    cursor.close()
    connection.close()
    connection = None
    cursor = None
