import glob
import os
import sys
import csv

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

def spawn_pedestrians():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    bp = random.choice(blueprint_library.filter('walker'))

    # n=0
    # while n<20:
    transform = random.choice(world.get_map().get_spawn_points())

    transform = carla.Transform(
        carla.Location(
        x=180,
        y=220,
        z=10),
        carla.Rotation(
        pitch=0,
        yaw=0,
        roll=0))

    print(transform)
    pedestrian = world.spawn_actor(bp, transform)
    print('created %s' % pedestrian.type_id)


    while True:
        control=carla.WalkerControl()
        control.speed = 0.1
        control.direction.y=10
        control.direction.x=0
        control.direction.z=0
        pedestrian.apply_control(control)
        time.sleep(2)
        control=carla.WalkerControl()
        control.speed = 0.1
        control.direction.y=0
        control.direction.x=10
        control.direction.z=0
        pedestrian.apply_control(control)
        time.sleep(2)
        control=carla.WalkerControl()
        control.speed = 0.1
        control.direction.y=-10
        control.direction.x=0
        control.direction.z=0
        pedestrian.apply_control(control)
        time.sleep(2)
        control=carla.WalkerControl()
        control.speed = 0.1
        control.direction.y=0
        control.direction.x=-10
        control.direction.z=0
        pedestrian.apply_control(control)
        time.sleep(2)

    time.sleep(5)
    n+=1

if __name__ == '__main__':
    n=0
    while n<20:
        spawn_pedestrians()
        n+=1
