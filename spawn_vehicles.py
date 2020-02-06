#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time

def spawn_vehicle():
    actor_list = []
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    n=0
    while n<20:
        try:
            bp = random.choice(blueprint_library.filter('vehicle'))
            if bp.has_attribute('color'):
                color = random.choice(bp.get_attribute('color').recommended_values)
                bp.set_attribute('color', color)
            transform = random.choice(world.get_map().get_spawn_points())
            vehicle = world.spawn_actor(bp, transform)
            # actor_list.append(vehicle)
            print('created %s' % vehicle.type_id)
            vehicle.set_autopilot(True)
            n+=1

            time.sleep(5)

        finally:
            print('done.')


if __name__ == '__main__':

    spawn_vehicle()
