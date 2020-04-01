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

def car_with_camera():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2000)
    world = client.get_world()

    #this is a spectator camera that lwill be spawned at the actor's location
    spectator = world.get_spectator()

    #vehicle is the actor, first get blueprint for actor, then random location to spawn, fillowed by both acting as arguments to spawn
    vehicle_bp = random.choice(world.get_blueprint_library().filter('vehicle.bmw.*'))
    transform = random.choice(world.get_map().get_spawn_points())
    vehicle = world.try_spawn_actor(vehicle_bp, transform)

    #spawn actor sensors that will attach to vehicle
    rgb_camera_bp = world.get_blueprint_library().filter('sensor.camera.rgb')
    lidar_bp = world.get_blueprint_library().filter('sensor.lidar.ray_cast')
    sensor_gnss_bp = world.get_blueprint_library().filter('sensor.other.gnss')
    sensor_collision_bp = world.get_blueprint_library().filter('sensor.other.collision')
    sensor_lane_invasion_bp = world.get_blueprint_library().filter('sensor.other.lane_invasion')
    # Default attachment:  Attachment.Rigid
    camera = world.spawn_actor(rgb_camera_bp, transform, attach_to=vehicle, attachment_type=Attachment.SpringArm)
    gnss_sensor = world.spawn_actor(sensor_gnss_bp, transform, attach_to=vehicle)
    collision_sensor = world.spawn_actor(sensor_collision_bp, transform, attach_to=vehicle)
    lane_invasion_sensor = world.spawn_actor(sensor_lane_invasion_bp, transform, attach_to=vehicle)

    #setting atttributes for the camera
    rgb_camera_bp.set_attribute('image_size_x', 600)
    rgb_camera_bp.set_attribute('image_size_y', 600)
    
    # Wait for world to get the vehicle actor
    world.tick()

    world_snapshot = world.wait_for_tick()
    actor_snapshot = world_snapshot.find(vehicle.id)

    # Set spectator at given transform (vehicle transform) ie location
    spectator.set_transform(actor_snapshot.get_transform())