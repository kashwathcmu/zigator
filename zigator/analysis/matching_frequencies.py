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

import os

from .. import config


CONDITION_MATCHES = set([
    (
        "phy_length--routerecord.tsv",
        (
            "phy_length",
        ),
        (
            ("error_msg", None),
            ("nwk_cmd_id", "NWK Route Record"),
        ),
    ),
    (
        "phy_length--linkstatus.tsv",
        (
            "phy_length",
        ),
        (
            ("error_msg", None),
            ("nwk_cmd_id", "NWK Link Status"),
        ),
    ),
])


def custom_sorter(var_value):
    str_repr = []
    for i in range(len(var_value)):
        if var_value[i] is None:
            str_repr.append("")
        elif isinstance(var_value[i], int):
            str_repr.append(str(var_value[i]).zfill(10))
        else:
            str_repr.append(var_value[i].zfill(80))
    return ", ".join(str_repr)


def matching_frequencies(out_dirpath):
    """Compute matching frequency of some conditions in the database table."""
    # Make sure that the output directory exists
    os.makedirs(out_dirpath, exist_ok=True)

    for condition_match in CONDITION_MATCHES:
        # Derive the path of the output file, the varying columns,
        # and the matching conditions
        out_filepath = os.path.join(out_dirpath, condition_match[0])
        var_columns = condition_match[1]
        conditions = condition_match[2]

        # Compute the distinct values of the varying columns
        var_values = config.distinct_values(var_columns, conditions)
        var_values.sort(key=custom_sorter)

        # Compute the matching frequency for each set of conditions
        results = []
        for var_value in var_values:
            var_conditions = list(conditions)
            for i in range(len(var_value)):
                var_conditions.append((var_columns[i], var_value[i]))
            matches = config.matching_frequency(var_conditions)
            results.append((var_value, matches))

        # Write the matching frequencies in the output file
        config.write_tsv(results, out_filepath)