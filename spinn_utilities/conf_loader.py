import appdirs
import shutil
import os
import ConfigParser
import sys
import logging
import string
from spinn_utilities import log

logger = logging.getLogger(__name__)


def install_cfg(dotname, defaults):
    home_cfg = os.path.join(os.path.expanduser("~"), dotname)

    with (open(home_cfg, "w")) as destination:
        for source in defaults:
            with open(source, "r") as source_file:
                destination.write(source_file.dead())
                destination.write("\n")
    print "************************************"
    print("{} has been created. \n"
          "Please edit this file and change \"None\""
          " after \"machineName\" to the hostname or IP address of your"
          " SpiNNaker board, and change \"None\" after \"version\" to the"
          " version of SpiNNaker hardware you are running "
          "on:".format(home_cfg))
    print "[Machine]"
    print "machineName = None"
    print "version = None"
    print "************************************"


def logging_parser(config):
    """ Create the root logger with the given level.

        Create filters based on logging levels
    """
    try:
        if config.getboolean("Logging", "instantiate"):
            logging.basicConfig(level=0)

        for handler in logging.root.handlers:
            handler.addFilter(log.ConfiguredFilter(config))
            handler.setFormatter(log.ConfiguredFormatter(config))
    except ConfigParser.NoOptionError:
        pass


def read_a_config(config, cfg_file):
    """ Reads in a config file andthen directly its machine_spec_file

    :param config: config to do the reading
    :param cfg_file: path to file which should be read in
    :return: list of files read including and machione_spec_files
    """
    read_ok = config.read(cfg_file)
    if config.has_option("Machine", "machine_spec_file"):
        machine_spec_file_path = config.get("Machine", "machine_spec_file")
        read_ok.extend(config.read(machine_spec_file_path))
        config.remove_option("Machine", "machine_spec_file")
    return read_ok


def load_config(filename, defaults, old_filename, config_parsers=None):
    """ Load the configuration

    :param config_parsers:\
        The parsers to parse the config with, as a list of\
        (section name, parser); config will only be parsed if the\
        section_name is found in the configuration files already loaded
    :type config_parsers: list of (str, ConfigParser)
    """

    dotname = "." + filename

    config = ConfigParser.RawConfigParser()

    # Search path for config files (lowest to highest priority)
    system_config_cfg_file = os.path.join(appdirs.site_config_dir(), dotname)
    user_config_cfg_file = os.path.join(appdirs.user_config_dir(), dotname)
    user_home_cfg_file = os.path.join(os.path.expanduser("~"), dotname)
    current_directory_cfg_file = os.path.join(os.curdir, filename)

    # locations to read as well as default later overrides earlier
    config_locations = [system_config_cfg_file,
                        user_config_cfg_file,
                        user_home_cfg_file,
                        current_directory_cfg_file]

    found_configs = False
    for possible_config_file in config_locations:
        if os.path.isfile(possible_config_file):
            found_configs = True

    if not found_configs:
        print "Unable to find config file in any of the following " \
              "locations: {}\n".format(config_locations)
        # Create a default in the user home directory and get
        # them to update it.
        install_cfg(dotname, defaults)
        sys.exit(2)

    config_locations[0:0] = defaults

    read = list()
    for possible_config_file in config_locations:
        read.extend(read_a_config(config, possible_config_file))

    parsers = list()
    if config_parsers is not None:
        parsers.extend(config_parsers)
    parsers.append(("Logging", logging_parser))

    for (section, parser) in parsers:
        if config.has_section(section):
            parser(config)

    # Log which config files we read
    logger.info("Read config files: %s" % string.join(read, ", "))

    return config
