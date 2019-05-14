#!/usr/bin/env python3

import subprocess
from argparse import ArgumentParser

from llama import mqtt


POWER_STATE_CHANGED = "@treppe.power/POWER_STATE_CHANGED"
POWER_STATE = "@treppe.power/POWER_STATE"
POWER_ON = "@treppe.power/POWER_ON"
POWER_OFF = "@treppe.power/POWER_OFF"

def gpio_setup(gpio):
    """Enable pin as output"""
    subprocess.run([gpio, "mode", "29", "out"])


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


def power_state_changed(state):
    return {
        "type": POWER_STATE_CHANGED,
        "payload": {
            "state": state,
        }
    }


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


def handle(gpio, dispatch, actions):
    """React to incoming actions"""
    state = get_power_state(gpio)

    for action in actions:
        if action["type"] == POWER_ON:
            print("Setting power state: ON")
            dispatch(power_state_changed(power_on(gpio)))
        elif action["type"] == POWER_OFF:
            print("Setting power state: OFF")
            dispatch(power_state_changed(power_off(gpio)))
        elif action["type"] == POWER_STATE:
            print("Getting power state.")
            dispatch(power_state_changed(get_power_state(gpio)))


def main(args):
    gpio_setup(args.gpio)

    # Connect to MQTT broker and start dispatch loop
    dispatch, receive = mqtt.connect(args.broker, {
        "treppe.power": args.topic,
    })

    handle(args.gpio, dispatch, receive())

if __name__ == "__main__":
    args = parse_args()
    main(args)

