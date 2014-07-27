#!/usr/bin/python

from ConeTree import *
from Controller import *
from PowerWalls import *
from Tracking import *

import avango
import avango.gua
import time
import math
import random
from avango.script import field_has_changed

from examples_common.GuaVE import GuaVE

## Parameters:
size = avango.gua.Vec2ui(2560/2, 2560*9/16)

class TimedRotate(avango.script.Script):
  TimeIn = avango.SFFloat()
  MatrixOut = avango.gua.SFMatrix4()

  @field_has_changed(TimeIn)
  def update(self):
    # self.MatrixOut.value = avango.gua.make_rot_mat(self.TimeIn.value*2.0, 0.0, 0.0, 1.0)
    self.MatrixOut.value = avango.gua.make_rot_mat(90, 0.0, 0.0, 1.0)

def setup_scene(graph):

  pass
  # root_node = avango.gua.nodes.TransformNode(
  #   Name = "Root",
  #   Transform =  avango.gua.make_trans_mat(0, 1.1, -2) * avango.gua.make_scale_mat(0.2)
  # )

  # group_monkey = avango.gua.nodes.TransformNode(
  #   Name = "group_monkey",
  # )

  # group_light = avango.gua.nodes.TransformNode(
  #   Name = "group_light",
  # )

  # group_light_spheres = avango.gua.nodes.TransformNode(
  #   Name = "group_light_spheres",
  # )

  # group_light_2 = avango.gua.nodes.TransformNode(
  #   Name = "group_light_2",
  # )

  # graph.Root.value.Children.value.append(root_node)
  # root_node.Children.value.append(group_monkey)
  # root_node.Children.value.append(group_light)
  # root_node.Children.value.append(group_light_spheres)
  # group_light.Children.value.append(group_light_2)

  # # make a buitifull scene
  # monkeys = []
  # lights = []
  # lights_spheres = []
  # for i in range(16):
  #   monkeys.append(
  #                   loader.create_geometry_from_file(
  #                   "ape" + str(i),
  #                   "data/objects/monkey.obj",
  #                   "data/materials/Stones.gmd",
  #                   avango.gua.LoaderFlags.DEFAULTS)
  #                 )

  #   lights.append(
  #                   avango.gua.nodes.PointLightNode(
  #                   Name = "light" + str(i),
  #                   Color = avango.gua.Color(1, 1, 1))
  #                 )

  #   lights_spheres.append(
  #                         loader.create_geometry_from_file(
  #                         "sphere" + str(i),
  #                         "data/objects/light_sphere.obj",
  #                         "data/materials/White.gmd",
  #                         avango.gua.LoaderFlags.DEFAULTS)
  #   )


  # x = (len(monkeys) / 2) - len(monkeys)
  # for i in range(len(monkeys)):
  #   monkeys[i].Transform.value = avango.gua.make_trans_mat(x, 0, 0)
  #   lights[i].Transform.value = avango.gua.make_trans_mat(x, 2, 0) * avango.gua.make_scale_mat(2)
  #   lights_spheres[i].Transform.value = avango.gua.make_trans_mat(x, 2, 0) * avango.gua.make_scale_mat(0.15)
  #   x += 1

  # for monkey in monkeys:
  #   group_monkey.Children.value.append(monkey)

  # for light in lights:
  #   group_light.Children.value.append(light)
  #   group_light_2.Children.value.append(light)

  # for lights_sphere in lights_spheres:
  #   group_light_spheres.Children.value.append(lights_sphere)


def viewing_setup_scene(graph):

  screen = avango.gua.nodes.ScreenNode(
    Name = "screen",
    Width = 1.6/2,
    Height = 0.9,
    Transform = avango.gua.make_trans_mat(0.0, 0.0, 5)
  )

  eye = avango.gua.nodes.TransformNode(
    Name = "eye",
    Transform = avango.gua.make_trans_mat(0.0, 0.0, 2.5)
  )

  screen.Children.value = [eye]

  graph.Root.value.Children.value.append(screen)

  camera = avango.gua.nodes.Camera(
    LeftEye = "/screen/eye",
    RightEye = "/screen/eye",
    LeftScreen = "/screen",
    RightScreen = "/screen",
    SceneGraph = "scenegraph"
  )


  window = avango.gua.nodes.Window(
    Size = size,
    LeftResolution = size
  )

  pipe = avango.gua.nodes.Pipeline(
    Camera = camera,
    Window = window,
    EnableSsao = True,
    SsaoIntensity = 2.0,
    EnableBloom = True,
    BloomThreshold = 0.8,
    BloomRadius = 10.0,
    BloomIntensity = 0.8,
    EnableHDR = True,
    HDRKey = 5,
    LeftResolution = size,
    EnableFPSDisplay = True
  )

  return pipe


def get_rotation_between_vectors(VEC1, VEC2):

  VEC1.normalize()
  VEC2.normalize()

  _angle = math.degrees(math.acos(VEC1.dot(VEC2)))
  _axis = VEC1.cross(VEC2)

  return avango.gua.make_rot_mat(_angle, _axis)

def calc_transform_connection(START_VEC, END_VEC):

  # calc the vector in between the two points, the resulting center of the line segment and the scaling needed to connect both points
  _vec = avango.gua.Vec3( END_VEC.x - START_VEC.x, END_VEC.y - START_VEC.y, END_VEC.z - START_VEC.z)
  _center = START_VEC + (_vec * 0.5)
  _scale  = _vec.length()

  # calc the rotation according negative z-axis
  _rotation_mat = get_rotation_between_vectors(avango.gua.Vec3(0, 0, -1), _vec)

  # build the complete matrix
  return avango.gua.make_trans_mat(_center) * _rotation_mat * avango.gua.make_scale_mat(0.1, 0.1, _scale)


def start():


  ##initializing scene -------------------
  graph = avango.gua.nodes.SceneGraph(
    Name = "scenegraph"
  )

  setup_scene(graph)

  loader = avango.gua.nodes.TriMeshLoader()
  Scene = avango.gua.nodes.TransformNode( Name = "Scene" )
  rotate_node = avango.gua.nodes.TransformNode( Name = "rotate_node" )

  frame = loader.create_geometry_from_file(
    "frame"
    ,"/opt/3d_models/vehicle/cars/clio/frame.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(frame)

  front = loader.create_geometry_from_file(
    "front"
    ,"/opt/3d_models/vehicle/cars/clio/front.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(front)

  back = loader.create_geometry_from_file(
    "back"
    ,"/opt/3d_models/vehicle/cars/clio/back.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(back)

  backdoor = loader.create_geometry_from_file(
    "backdoor"
    ,"/opt/3d_models/vehicle/cars/clio/backdoor.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(backdoor)

  left_door = loader.create_geometry_from_file(
    "left_door"
    ,"/opt/3d_models/vehicle/cars/clio/left_door.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(left_door)

  # right_door = loader.create_geometry_from_file(
  #   "right_door"
  #   ,"/opt/3d_models/vehicle/cars/clio/right_door.obj"
  #   ,"data/materials/Hans.gmd"
  #   ,avango.gua.LoaderFlags.LOAD_MATERIALS
  # )
  # rotate_node.Children.value.append(right_door)

  dashboard = loader.create_geometry_from_file(
    "dashboard"
    ,"/opt/3d_models/vehicle/cars/clio/dashboard.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(dashboard)

  hood = loader.create_geometry_from_file(
    "hood"
    ,"/opt/3d_models/vehicle/cars/clio/hood.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(hood)

  driver_seat = loader.create_geometry_from_file(
    "driver_seat"
    ,"/opt/3d_models/vehicle/cars/clio/driver_seat.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(driver_seat)

  nondriver_seat = loader.create_geometry_from_file(
    "nondriver_seat"
    ,"/opt/3d_models/vehicle/cars/clio/nondriver_seat.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(nondriver_seat)

  backseats = loader.create_geometry_from_file(
    "backseats"
    ,"/opt/3d_models/vehicle/cars/clio/backseats.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(backseats)

  left_back_tire = loader.create_geometry_from_file(
    "left_back_tire"
    ,"/opt/3d_models/vehicle/cars/clio/left_back_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(left_back_tire)

  right_back_tire = loader.create_geometry_from_file(
    "right_back_tire"
    ,"/opt/3d_models/vehicle/cars/clio/right_back_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(right_back_tire)

  left_front_tire = loader.create_geometry_from_file(
    "left_front_tire"
    ,"/opt/3d_models/vehicle/cars/clio/left_front_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(left_front_tire)

  right_front_tire = loader.create_geometry_from_file(
    "right_front_tire"
    ,"/opt/3d_models/vehicle/cars/clio/right_front_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(right_front_tire)

  underbody = loader.create_geometry_from_file(
    "underbody"
    ,"/opt/3d_models/vehicle/cars/clio/underbody.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(underbody)

  rest = loader.create_geometry_from_file(
    "rest"
    ,"/opt/3d_models/vehicle/cars/clio/rest.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS
  )
  rotate_node.Children.value.append(rest)


  Scene.Transform.value = avango.gua.make_trans_mat(0, -6, -20) \
                        * avango.gua.make_rot_mat(-90, 1, 0 ,0) \
                        * avango.gua.make_scale_mat(0.15)
                        # * avango.gua.make_rot_mat(-120, 0,0,1) \


  rotator = TimedRotate()
  timer = avango.nodes.TimeSensor()
  rotator.TimeIn.connect_from(timer.Time)
  rotate_node.Transform.connect_from(rotator.MatrixOut)

  Scene.Children.value.append(rotate_node)
  graph.Root.value.Children.value.append(Scene)

  # # # OLD FASHION CITY
  # Scene = loader.create_geometry_from_file(
  #   "Scene_root"
  #   ,"/opt/3d_models/architecture/old fashion town/old town block.obj"
  #   ,"data/materials/Grey.gmd"
  #   ,avango.gua.LoaderFlags.LOAD_MATERIALS or avango.gua.LoaderFlags.NORMALIZE_SCALE
  # )
  # Scene.Transform.value = avango.gua.make_trans_mat(0, 0.0, -6) * avango.gua.make_scale_mat(0.015)
  # graph.Root.value.Children.value.append(Scene)

  # # WEIMARER STADT MODELL
  # Scene = loader.create_geometry_from_file(
  #   "Scene_root"
  #   ,"/opt/3d_models/architecture/weimar_geometry/weimar_stadtmodell_latest_version/weimar_stadtmodell_final.obj"
  #   ,"data/materials/Grey.gmd"
  #   ,avango.gua.LoaderFlags.LOAD_MATERIALS or avango.gua.LoaderFlags.NORMALIZE_SCALE
  # )
  # Scene.Transform.value = avango.gua.make_trans_mat(0, 0, -6) * avango.gua.make_scale_mat(0.02)
  # graph.Root.value.Children.value.append(Scene)

  sun = avango.gua.nodes.SunLightNode(
    Name = "sun",
    Color = avango.gua.Color(1, 1, 1),
    Transform = avango.gua.make_rot_mat(-80, 1, 0, 0)
  )

  graph.Root.value.Children.value.append(sun)

  ##create Powerwall setup
  powerwall = LargePowerWall(graph.Root.value)
  avango.gua.create_texture("data/textures/skymap.jpg")
  for target_name in ["tracking-dlp-glasses-{0}".format(i) for i in [1, 4, 5, 6]]:
    head, pipe = powerwall.create_user(graph)

    pipe.BackgroundTexture.value = "data/textures/skymap.jpg"
    pipe.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE

    pipe.EnableBackFaceCulling = True

    pipe.EnableRayDisplay.value = True

    headtracking = TrackingReader()
    headtracking.set_target_name(target_name)
    head.Transform.connect_from(headtracking.MatrixOut)


  # create Cone Tree -----------------------------------
  conetree = ConeTree()
  conetree.myConstructor(graph)

  conetree.create_scenegraph_structure()
  CT_root = conetree.get_root()

  CT = avango.gua.nodes.TransformNode( Name = "CT")
  CT.Children.value = [CT_root]
  CT.Transform.value = avango.gua.make_trans_mat(0,0.25,0) * avango.gua.make_scale_mat(1.0 / 200)
  CubeProp = avango.gua.nodes.TransformNode( Name = "CubeProp")
  CubeTracker = TrackingReader()
  CubeTracker.set_target_name("tracking-cube")
  CubeProp.Transform.connect_from(CubeTracker.MatrixOut)

  graph.Root.value.Children.value.append(CubeProp)
  CubeProp.Children.value.append(CT)


  conetree_picker = PickController()
  conetree_picker.myConstructor(conetree)


  # Light for the Cone Tree
  sun = avango.gua.nodes.SunLightNode(
    Name = "sun",
    Color = avango.gua.Color(1, 1, 1),
    Transform = avango.gua.make_rot_mat(-80, 1, 0, 0)
  )

  graph.Root.value.Children.value.append(sun)




  # PICKING
  pick_ray = avango.gua.nodes.RayNode(Name = "pick_ray")
  pick_ray.Transform.value = avango.gua.make_scale_mat(0.3, 0.3, 0.1)

  PointerProp = avango.gua.nodes.TransformNode( Name = "PointerProp")
  PointerTracker = TrackingReader()
  PointerTracker.set_target_name("tracking-dlp-pointer1")
  PointerProp.Transform.connect_from(PointerTracker.MatrixOut)

  PointerProp.Children.value.append(pick_ray)
  graph.Root.value.Children.value.append(PointerProp)

  conetree_picker.PickedSceneGraph.value = graph
  conetree_picker.TargetSceneGraph.value = graph
  conetree_picker.Ray.value = pick_ray

  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  viewer = avango.gua.nodes.Viewer()

  viewer.Pipelines.value = [pipe for head, pipe in powerwall.users]
  viewer.SceneGraphs.value = [graph]

  viewer.run()

if __name__ == '__main__':
  start()

