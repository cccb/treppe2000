#!/usr/bin/env python3

import subprocess
from argparse import ArgumentParser

from llama import mqtt


POWER_STATE_CHANGED = "power_state_changed"
POWER_ON = "power_on"
POWER_OFF = "power_off"

_state = 0

def get_power_state(gpio):
    """Read GPIO pin, get power state"""
    result = subprocess.check_output([gpio, "read", "29"])
    try:
        return int(result.strip())
    except:
        return 0


def power_on(gpio):
    """Set GPIO pin, get power state"""
    result = subprocess.check_output([gpio, "write", "29", "1"])
    try:
        return int(result.strip())
    except:
        return 0


def power_off(gpio):
    """Set GPIO pin, return next power state"""
    result = subprocess.check_output([gpio, "write", "29", "0"])
    try:
        return int(result.strip())
    except:
        return 0


def parse_args():
    """Parse commandline arguments"""
    parser = ArgumentParser()
    parser.add_argument(
        "-t", "--topic",
        default="v1/treppe/power")
    parser.add_argument(
        "-b", "--broker",
        default="mqtt.club.berlin.ccc.de:1883")
    parser.add_argument(
        "-g", "--gpio",
        default="gpio")

    return parser.parse_args()


def handle(dispatch, actions):
    """React to incoming actions"""
    for action in actions:
        print(action)


def main(args):
    # Connect to MQTT broker and start dispatch loop
    dispatch, receive = mqtt.connect(args.broker, {
        "treppe.power": args.topic,
        })

    handle(dispatch, receive())

if __name__ == "__main__":
    args = parse_args()
    main(args)

