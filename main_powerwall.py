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


def setup_scene(graph):

  loader = avango.gua.nodes.TriMeshLoader()

  root_node = avango.gua.nodes.TransformNode(
    Name = "Root",
    Transform = avango.gua.make_trans_mat(0.0, 2.0, -20) * avango.gua.make_scale_mat(2)
  )

  group_monkey = avango.gua.nodes.TransformNode(
    Name = "group_monkey",
  )

  group_light = avango.gua.nodes.TransformNode(
    Name = "group_light",
  )

  group_light_spheres = avango.gua.nodes.TransformNode(
    Name = "group_light_spheres",
  )

  graph.Root.value.Children.value.append(root_node)
  root_node.Children.value.append(group_monkey)
  root_node.Children.value.append(group_light)
  root_node.Children.value.append(group_light_spheres)

  # make a buitifull scene
  monkeys = []
  lights = []
  lights_spheres = []
  for i in range(16):
    monkeys.append(
                    loader.create_geometry_from_file(
                    "ape" + str(i),
                    "data/objects/monkey.obj",
                    "data/materials/Stones.gmd",
                    avango.gua.LoaderFlags.DEFAULTS)
                  )

    lights.append(
                    avango.gua.nodes.PointLightNode(
                    Name = "light" + str(i),
                    Color = avango.gua.Color(1, 1, 1))
                  )

    lights_spheres.append(
                          loader.create_geometry_from_file(
                          "sphere" + str(i),
                          "data/objects/light_sphere.obj",
                          "data/materials/White.gmd",
                          avango.gua.LoaderFlags.DEFAULTS)
    )


  x = (len(monkeys) / 2) - len(monkeys)
  for i in range(len(monkeys)):
    monkeys[i].Transform.value = avango.gua.make_trans_mat(x, 0, 0)
    lights[i].Transform.value = avango.gua.make_trans_mat(x, 1, 1) * avango.gua.make_scale_mat(3)
    lights_spheres[i].Transform.value = avango.gua.make_trans_mat(x, 1, 1) * avango.gua.make_scale_mat(0.04)
    x += 1

  for monkey in monkeys:
    group_monkey.Children.value.append(monkey)

  for light in lights:
    group_light.Children.value.append(light)

  for lights_sphere in lights_spheres:
    group_light_spheres.Children.value.append(lights_sphere)


def start():

  ##initializing scene -------------------
  graph = avango.gua.nodes.SceneGraph(
    Name = "scenegraph"
  )

  loader = avango.gua.nodes.TriMeshLoader()
  Scene = avango.gua.nodes.TransformNode( Name = "Scene" )

  setup_scene(graph)

  frame = loader.create_geometry_from_file(
    "frame"
    ,"/opt/3d_models/vehicle/cars/clio/frame.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(frame)

  front = loader.create_geometry_from_file(
    "front"
    ,"/opt/3d_models/vehicle/cars/clio/front.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(front)

  back = loader.create_geometry_from_file(
    "back"
    ,"/opt/3d_models/vehicle/cars/clio/back.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(back)

  backdoor = loader.create_geometry_from_file(
    "backdoor"
    ,"/opt/3d_models/vehicle/cars/clio/backdoor.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(backdoor)

  left_door = loader.create_geometry_from_file(
    "left_door"
    ,"/opt/3d_models/vehicle/cars/clio/left_door.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(left_door)

  # right_door = loader.create_geometry_from_file(
  #   "right_door"
  #   ,"/opt/3d_models/vehicle/cars/clio/right_door.obj"
  #   ,"data/materials/Hans.gmd"
  #   ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  # )
  # Scene.Children.value.append(right_door)

  # dashboard = loader.create_geometry_from_file(
  #   "dashboard"
  #   ,"/opt/3d_models/vehicle/cars/clio/dashboard.obj"
  #   ,"data/materials/Hans.gmd"
  #   ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  # )
  # Scene.Children.value.append(dashboard)

  hood = loader.create_geometry_from_file(
    "hood"
    ,"/opt/3d_models/vehicle/cars/clio/hood.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(hood)

  driver_seat = loader.create_geometry_from_file(
    "driver_seat"
    ,"/opt/3d_models/vehicle/cars/clio/driver_seat.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(driver_seat)

  nondriver_seat = loader.create_geometry_from_file(
    "nondriver_seat"
    ,"/opt/3d_models/vehicle/cars/clio/nondriver_seat.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(nondriver_seat)

  backseats = loader.create_geometry_from_file(
    "backseats"
    ,"/opt/3d_models/vehicle/cars/clio/backseats.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(backseats)

  left_back_tire = loader.create_geometry_from_file(
    "left_back_tire"
    ,"/opt/3d_models/vehicle/cars/clio/left_back_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(left_back_tire)

  right_back_tire = loader.create_geometry_from_file(
    "right_back_tire"
    ,"/opt/3d_models/vehicle/cars/clio/right_back_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(right_back_tire)

  left_front_tire = loader.create_geometry_from_file(
    "left_front_tire"
    ,"/opt/3d_models/vehicle/cars/clio/left_front_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(left_front_tire)

  right_front_tire = loader.create_geometry_from_file(
    "right_front_tire"
    ,"/opt/3d_models/vehicle/cars/clio/right_front_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(right_front_tire)

  underbody = loader.create_geometry_from_file(
    "underbody"
    ,"/opt/3d_models/vehicle/cars/clio/underbody.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(underbody)

  rest = loader.create_geometry_from_file(
    "rest"
    ,"/opt/3d_models/vehicle/cars/clio/rest.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  Scene.Children.value.append(rest)


  Scene.Transform.value = avango.gua.make_trans_mat(0, -8, -20) \
                        * avango.gua.make_rot_mat(-90, 1, 0 ,0) \
                        * avango.gua.make_rot_mat(-120, 0,0,1) \
                        * avango.gua.make_scale_mat(0.15) 


  graph.Root.value.Children.value.append(Scene)

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
  # for target_name in ["tracking-dlp-glasses-{0}".format(i) for i in [1]]:
    head, pipe = powerwall.create_user(graph)

    pipe.BackgroundTexture.value = "data/textures/skymap.jpg"
    pipe.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE

    pipe.EnableBackfaceCulling.value = True
    pipe.EnableFXAA.value = False
    pipe.EnableFPSDisplay.value = True


    pipe.EnableRayDisplay.value = True

    headtracking = TrackingReader()
    headtracking.set_target_name(target_name)
    head.Transform.connect_from(headtracking.MatrixOut)


  # create Cone Tree and put it on top of the spheron ------------------------------
  conetree = ConeTree()
  conetree.myConstructor(graph.Root.value)

  conetree.create_scenegraph_structure()
  CT_root = conetree.get_root()

  CT = avango.gua.nodes.TransformNode( Name = "CT")
  CT.Children.value = [CT_root]
  CT.Transform.value = avango.gua.make_trans_mat(0,-0.4,0)
  # Spheron = avango.gua.nodes.TransformNode( Name = "Spheron")
  # CubeTracker = TrackingReader()
  # CubeTracker.set_target_name('tracking-new-spheron')
  # Spheron.Transform.connect_from(CubeTracker.MatrixOut)

  # graph.Root.value.Children.value.append(Spheron)
  powerwall.screen.Children.value.append(CT)

  # pickray 
  pick_ray = avango.gua.nodes.RayNode(Name = "pick_ray")

  PointerProp = avango.gua.nodes.TransformNode( Name = "PointerProp")
  PointerTracker = TrackingReader()
  PointerTracker.set_target_name("tracking-dlp-pointer1")
  PointerProp.Transform.connect_from(PointerTracker.MatrixOut)

  PointerProp.Children.value.append(pick_ray)
  graph.Root.value.Children.value.append(PointerProp)

  # initializing the Pick Controller, Pointer Controller, Bounding Box Updater and Test Updater -----
  conetree_picker = PickController()
  conetree_picker.myConstructor(conetree, avango.gua.Vec3(0.15, 0.15, 0.2))
  conetree_picker.Ray.value = pick_ray

  contree_pointer = PointerController()
  contree_pointer.myConstructor(conetree)
  pick_ray.Transform.connect_from(contree_pointer.RayTransformOut)

  BBUpdater = BoundingBoxController()
  BBUpdater.FocusNode.connect_from(conetree.FocusSceneNode)
  BBUpdater.TargetSceneGraph.value = graph

  TextUpdater = TextController()
  TextUpdater.FocusNode.connect_from(conetree.FocusSceneNode)
  TextUpdater.TextNode.Transform.value = avango.gua.make_trans_mat(-1.8, 1.1, 0) * avango.gua.make_scale_mat(0.05)
  powerwall.screen.Children.value.append(TextUpdater.TextNode)


  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  viewer = avango.gua.nodes.Viewer()

  viewer.Pipelines.value = [pipe for head, pipe in powerwall.users]
  viewer.SceneGraphs.value = [graph]

  viewer.run()

if __name__ == '__main__':
  start()

