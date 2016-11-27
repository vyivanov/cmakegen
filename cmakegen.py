#!/usr/bin/env python3.5

"""TODO: add module description"""

#
# MIT License
#
# Copyright (c) 2016 Vladimir Yu. Ivanov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


import re
import os
import sys
import logging
import argparse
import textwrap
import yaml


LOGGER = logging.getLogger("cmakegen")
LOGGER_CONFIGS = {
    'FMT': {
        'MESG': "[%(asctime)s][%(levelname)-8s] - %(message)s",
        'DATE': "%y-%m-%d %H:%M:%S",
    },
    'LVL': {
        'DBG': logging.DEBUG,
        'INF': logging.INFO,
        'ERR': logging.ERROR,
        'CRT': logging.CRITICAL,
    },
}

STATUS = {
    'CONFIG_FILE_IS_NOT_EXIST': 0x01,
    'CONFIG_FILE_IS_NOT_VALID': 0x02,
}


class SourceParser(object):
    """TODO: add class description"""

    def __init__(self, configuration):
        """
        @brief TODO: add ctor description.

        @param configuration Project scan settings
               'paths': ("/abs/path/to/dir0", "/abs/path/to/dir1", ...)
               'rmacroses': ("MACRO0", "MACRO1", ...)
               'vmacroses': (
                   {"MACRO0": "VALUE0"},
                   {"MACRO1": "VALUE1"},
                   ...)
               'fmacroses': (
                   {"MACRO0": "VALUE0"},
                   {"MACRO1": "VALUE1"},
                   ...)
        """
        self.__includes = set()     # Abs path to include directories
        self.__sources = set()      # Abs paths to sources
        self.__cmakelist = list()   # CMake file lines
        # Abs paths to project directories to be scaned
        self.__paths = configuration['paths']
        # Regular macroses to be defined
        self.__rmacroses = configuration['rmacroses']
        # Value-driven macroses to be defined
        self.__vmacroses = configuration['vmacroses']
        # Function-like macroses to be defined
        self.__fmacroses = configuration['fmacroses']
        # Log configuration
        for path in self.__paths:
            LOGGER.info("Path to be scaned '%s'", path)
        for rmacros in self.__rmacroses:
            LOGGER.info("Regular macros to be defined '-D%s'", rmacros)
        for vmacros in self.__vmacroses:
            assert len(vmacros.keys()) == 1 and len(vmacros.values()) == 1
            LOGGER.info("Value-driven macros to be defined '-D%s=%s'",
                        [k for k in vmacros.keys()][0],
                        [v for v in vmacros.values()][0])
        for fmacros in self.__fmacroses:
            assert len(fmacros.keys()) == 1 and len(fmacros.values()) == 1
            LOGGER.info("Function-like macros to be defined '-D%s()=%s'",
                        [k for k in fmacros.keys()][0],
                        [v for v in fmacros.values()][0])
        # Fill header of the CMake file
        self.__cmakelist.append("cmake_minimum_required(VERSION 2.8)\n")
        self.__cmakelist.append("project(dummy)\n")

    def __scan_path(self, path):
        """
        @brief TODO: add method description

        @param path Abs path to directory to be scaned recursively
        """
        LOGGER.info("Scanning path '%s'", path)
        for root, directories, files in os.walk(path):
            for directory in directories:
                self.__scan_path(directory)
            for filepath in files:
                if re.search("\\.(h|hpp)$", filepath) is not None:
                    LOGGER.debug("\tFound include directory '%s'", root)
                    self.__includes.add(root)
                elif re.search("\\.(c|cpp)$", filepath) is not None:
                    filepath = os.path.join(root, filepath)
                    LOGGER.debug("\tFound source '%s'", filepath)
                    self.__sources.add(filepath)

    def __process_project(self):
        """
        @brief Scan all project directories to find includes and sources
        """
        for path in self.__paths:
            self.__scan_path(path)

    def __compose_definitions(self):
        LOGGER.info("Composing definitions")
        self.__cmakelist.append("add_definitions(\n")
        for rmacros in self.__rmacroses:
            self.__cmakelist.append("\t-D{0}\n".format(rmacros))
        for vmacros in self.__vmacroses:
            self.__cmakelist.append("\t-D{0}={1}\n".format(
                [k for k in vmacros.keys()][0],
                [v for v in vmacros.values()][0]))
        for fmacros in self.__fmacroses:
            self.__cmakelist.append("\t-D\"{0}()={1}\"\n".format(
                [k for k in fmacros.keys()][0],
                [v for v in fmacros.values()][0]))
        self.__cmakelist.append(")\n")

    def __compose_includes(self):
        LOGGER.info("Composing includes")
        self.__cmakelist.append("include_directories(\n")
        for directory in sorted(self.__includes):
            self.__cmakelist.append("\t{0}\n".format(
                directory.replace('\\', '/')))
        self.__cmakelist.append(")\n")

    def __compose_sources(self):
        LOGGER.info("Composing sources")
        self.__cmakelist.append("add_executable(executable\n")
        for filepath in sorted(self.__sources):
            self.__cmakelist.append("\t{0}\n".format(
                filepath.replace('\\', '/')))
        self.__cmakelist.append(")\n")

    def gen_cmake_file(self, name="CMakeLists.txt"):
        """
        @brief TODO: add description
        """
        self.__process_project()
        self.__compose_definitions()
        self.__compose_includes()
        self.__compose_sources()
        open(name, 'w').write(''.join(self.__cmakelist))


def main():
    """
    @brief Main entry point
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
            CMake file generator for C/C++ projects
            """),
        epilog="Support: inbox@vova-ivanov.info"
    )
    parser.add_argument(
        "config", help="YAML configuration file")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logs")
    args = parser.parse_args()
    inflvl = LOGGER_CONFIGS['LVL']['INF']
    dbglvl = LOGGER_CONFIGS['LVL']['DBG']
    logging.basicConfig(
        format=LOGGER_CONFIGS['FMT']['MESG'],
        datefmt=LOGGER_CONFIGS['FMT']['DATE'],
        level=inflvl if not args.debug else dbglvl
    )
    if not os.path.exists(args.config):
        LOGGER.critical("Config file '%s' is not exist", args.config)
        sys.exit(STATUS['CONFIG_FILE_IS_NOT_EXIST'])
    with open(args.config, 'r') as config:
        yaml_config = yaml.load(config)
        try:
            paths = yaml_config['pathToScan']
            rmacroses = yaml_config['rmacrosToDefine']
            vmacroses = yaml_config['vmacrosToDefine']
            fmacroses = yaml_config['fmacrosToDefine']
        except KeyError as error:
            LOGGER.critical("Config field %s is not exist in '%s' file",
                            error, args.config)
            sys.exit(STATUS['CONFIG_FILE_IS_NOT_VALID'])
    SourceParser(
        {
            'paths': paths,
            'rmacroses': rmacroses,
            'vmacroses': vmacroses,
            'fmacroses': fmacroses,
        }
    ).gen_cmake_file()


if __name__ == "__main__":
    main()
