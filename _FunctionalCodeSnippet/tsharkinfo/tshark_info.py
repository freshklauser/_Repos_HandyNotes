# -*- coding: utf-8 -*-
# @Author   : Administrator
# @DateTime : 2020/6/26 13:55
# @FileName : tshark_info.py
# @SoftWare : PyCharm


import os
import re
import subprocess
import sys
from distutils.version import LooseVersion

from pyshark.tshark.tshark import TSharkVersionException, TSharkNotFoundException

from tsharkinfo.config import get_config


def get_process_path(tshark_path=None, process_name="tshark"):
    """Finds the path of the tshark executable.

    If the user has provided a path
    or specified a location in config.ini it will be used. Otherwise default
    locations will be searched.

    :param tshark_path: Path of the tshark binary
    :raises TSharkNotFoundException in case TShark is not found in any location.
    """
    config = get_config()
    possible_paths = [config.get(process_name, "%s_path" % process_name)]

    # Add the user provided path to the search list
    if tshark_path is not None:
        possible_paths.insert(0, tshark_path)

    # Windows search order: configuration file"s path, common paths.
    if sys.platform.startswith("win"):
        for env in ("ProgramFiles(x86)", "ProgramFiles"):
            # program_files = os.getenv(env)
            program_files = "D:\\Program Files\\"
            if program_files is not None:
                possible_paths.append(
                    os.path.join(program_files, "Wireshark", "%s.exe" % process_name)
                )
    # Linux, etc. search order: configuration file's path, the system's path
    else:
        os_path = os.getenv(
            "PATH",
            "/usr/bin:/usr/sbin:/usr/lib/tshark:/usr/local/bin"
        )
        for path in os_path.split(":"):
            possible_paths.append(os.path.join(path, process_name))

    for path in possible_paths:
        if os.path.exists(path):
            if sys.platform.startswith("win"):
                path = path.replace("\\", "/")
            return path
    raise TSharkNotFoundException(
        "TShark not found. Try adding its location to the configuration file. "
        "Searched these paths: {}".format(possible_paths)
    )


def get_tshark_version(tshark_path=None):
    parameters = [get_process_path(tshark_path), "-v"]
    with open(os.devnull, "w") as null:
        version_output = subprocess.check_output(parameters, stderr=null).decode("ascii")

    version_line = version_output.splitlines()[0]
    pattern = '.*\s(\d+\.\d+\.\d+).*'  # match " #.#.#" version pattern
    m = re.match(pattern, version_line)
    if not m:
        raise TSharkVersionException("Unable to parse TShark version from: {}".format(version_line))
    version_string = m.groups()[0]  # Use first match found

    return LooseVersion(version_string)
