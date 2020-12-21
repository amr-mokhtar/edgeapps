#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2020 Intel Corporation

""" Generate ZMQ keys and put them to the etcdctl """
import argparse
import logging
import os
import sys
import eis_integ


def parse_arguments(_cli_args):
    """ Parse argument passed to function """
    parser = argparse.ArgumentParser(description="Specify Application name")
    parser.add_argument("app", help="Name of the client application")
    parser.add_argument("--force", action='store_true',
                        help="Force putting new generated ZMQ keys without checking" +
                        "if they already exist")
    return parser.parse_args()

def main(args):
    """ Main """
    eis_integ.init_logger()

    os.environ["ETCDCTL_ENDPOINTS"] = "https://" + \
        eis_integ.extract_etcd_endpoint()

    eis_integ.check_path_variable("ETCDCTL_CACERT", os.environ.get("ETCDCTL_CACERT"))
    eis_integ.check_path_variable("ETCDCTL_CERT", os.environ.get("ETCDCTL_CERT"))
    eis_integ.check_path_variable("ETCDCTL_KEY", os.environ.get("ETCDCTL_KEY"))

    skip_gen = False
    if not args.force:
        logging.info("Check if ZMQ key pair for %s app already exists", args.app)
        skip_gen = eis_integ.check_zmqkeys(args.app)

    if not skip_gen:
        logging.info("Generate ZMQ pair keys for %s and put them to the etcd database", args.app)
        eis_integ.put_zmqkeys(args.app)
    else:
        logging.info("ZMQ pair keys generation skipped for %s app", args.app)

    return eis_integ.CODES.NO_ERROR


if __name__ == '__main__':
    try:
        sys.exit(main(parse_arguments(sys.argv[1:])).value)
    except eis_integ.EisIntegError as exception:
        logging.error("Error while generating ZMQ keys: %s", str(exception))
        sys.exit(exception.code.value)
