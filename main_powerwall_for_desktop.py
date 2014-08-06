#!/usr/bin/python

from ConeTree import *
from Controller import *

import avango
import avango.gua
import time
import math
import random
from avango.script import field_has_changed

from examples_common.GuaVE import GuaVE

def setup_scene(graph):
  loader = avango.gua.nodes.TriMeshLoader()
  Scene = avango.gua.nodes.TransformNode( Name = "Scene" )
  rotate_node = avango.gua.nodes.TransformNode( Name = "rotate_node" )

  frame = loader.create_geometry_from_file(
    "frame"
    ,"/opt/3d_models/vehicle/cars/clio/frame.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(frame)

  front = loader.create_geometry_from_file(
    "front"
    ,"/opt/3d_models/vehicle/cars/clio/front.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(front)

  back = loader.create_geometry_from_file(
    "back"
    ,"/opt/3d_models/vehicle/cars/clio/back.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(back)

  backdoor = loader.create_geometry_from_file(
    "backdoor"
    ,"/opt/3d_models/vehicle/cars/clio/backdoor.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(backdoor)

  left_door = loader.create_geometry_from_file(
    "left_door"
    ,"/opt/3d_models/vehicle/cars/clio/left_door.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(left_door)

  # right_door = loader.create_geometry_from_file(
  #   "right_door"
  #   ,"/opt/3d_models/vehicle/cars/clio/right_door.obj"
  #   ,"data/materials/Hans.gmd"
  #   ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  # )
  # rotate_node.Children.value.append(right_door)

  # dashboard = loader.create_geometry_from_file(
  #   "dashboard"
  #   ,"/opt/3d_models/vehicle/cars/clio/dashboard.obj"
  #   ,"data/materials/Hans.gmd"
  #   ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  # )
  # rotate_node.Children.value.append(dashboard)

  hood = loader.create_geometry_from_file(
    "hood"
    ,"/opt/3d_models/vehicle/cars/clio/hood.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(hood)

  driver_seat = loader.create_geometry_from_file(
    "driver_seat"
    ,"/opt/3d_models/vehicle/cars/clio/driver_seat.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(driver_seat)

  nondriver_seat = loader.create_geometry_from_file(
    "nondriver_seat"
    ,"/opt/3d_models/vehicle/cars/clio/nondriver_seat.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(nondriver_seat)

  backseats = loader.create_geometry_from_file(
    "backseats"
    ,"/opt/3d_models/vehicle/cars/clio/backseats.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(backseats)

  left_back_tire = loader.create_geometry_from_file(
    "left_back_tire"
    ,"/opt/3d_models/vehicle/cars/clio/left_back_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(left_back_tire)

  right_back_tire = loader.create_geometry_from_file(
    "right_back_tire"
    ,"/opt/3d_models/vehicle/cars/clio/right_back_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(right_back_tire)

  left_front_tire = loader.create_geometry_from_file(
    "left_front_tire"
    ,"/opt/3d_models/vehicle/cars/clio/left_front_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(left_front_tire)

  right_front_tire = loader.create_geometry_from_file(
    "right_front_tire"
    ,"/opt/3d_models/vehicle/cars/clio/right_front_tire.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(right_front_tire)

  underbody = loader.create_geometry_from_file(
    "underbody"
    ,"/opt/3d_models/vehicle/cars/clio/underbody.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(underbody)

  rest = loader.create_geometry_from_file(
    "rest"
    ,"/opt/3d_models/vehicle/cars/clio/rest.obj"
    ,"data/materials/Hans.gmd"
    ,avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE
  )
  rotate_node.Children.value.append(rest)


  Scene.Transform.value = avango.gua.make_trans_mat(0, -6, -20) \
                        * avango.gua.make_rot_mat(-90, 1, 0 ,0) \
                        * avango.gua.make_scale_mat(0.15)
                        # * avango.gua.make_rot_mat(-120, 0,0,1) \

  Scene.Children.value.append(rotate_node)
  graph.Root.value.Children.value.append(Scene)

  sun = avango.gua.nodes.SunLightNode(
    Name = "sun",
    Color = avango.gua.Color(1, 1, 1),
    Transform = avango.gua.make_rot_mat(-80, 1, 0, 0)
  )
  graph.Root.value.Children.value.append(sun)



def start():

  ##initializing scene -------------------
  graph = avango.gua.nodes.SceneGraph(
    Name = "scenegraph"
  )

  setup_scene(graph)

  screen = avango.gua.nodes.ScreenNode(
    Name = "screen",
    Width = 1.6,
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

  size = avango.gua.Vec2ui(1920, 1920*9/16)

  window = avango.gua.nodes.Window(
    Size = size,
    LeftResolution = size
  )

  pipe = avango.gua.nodes.Pipeline(
    Camera = camera,
    Window = window,
    LeftResolution = size,
    EnableRayDisplay = True,
    EnableFPSDisplay = True
  )



  # create Cone Tree -----------------------------------
  conetree = ConeTree()
  conetree.myConstructor(graph)

  conetree.create_scenegraph_structure()
  CT_root = conetree.get_root()

  CT = avango.gua.nodes.TransformNode( Name = "CT")
  CT.Children.value = [CT_root]
  CT.Transform.value = avango.gua.make_trans_mat(0.3,-0.2,0)
  screen.Children.value.append(CT)

  ## Navigation----------------------
  conetree_navigator = Navigator()
  conetree_navigator.myConstructor(conetree)
  conetree_navigator.StartLocation.value = screen.Transform.value.get_translate()
  conetree_navigator.RotationSpeed.value = 0.09
  conetree_navigator.MotionSpeed.value = 0.69
  screen.Transform.connect_from(conetree_navigator.OutTransform)


  # # reference--------------------------
  # reference_cubes = []
  # for i in range(4):
  #   reference_cubes.append( loader.create_geometry_from_file(
  #     "reference_cube",
  #     "data/objects/cube.obj",
  #     "data/materials/Red.gmd",
  #     avango.gua.LoaderFlags.DEFAULTS,
  #   ))

  # reference_cubes[0].Transform.value = avango.gua.make_trans_mat(-0.25, 0.0 ,0.0) * avango.gua.make_scale_mat(0.1)
  # reference_cubes[1].Transform.value = avango.gua.make_trans_mat( 0.25, 0.0 ,0.0) * avango.gua.make_scale_mat(0.1)
  # reference_cubes[2].Transform.value = avango.gua.make_trans_mat(-0.25, 0.5 ,0.0) * avango.gua.make_scale_mat(0.1)
  # reference_cubes[3].Transform.value = avango.gua.make_trans_mat( 0.25, 0.5 ,0.0) * avango.gua.make_scale_mat(0.1)
  # CubeProp.Children.value.append(reference_cubes[0])
  # CubeProp.Children.value.append(reference_cubes[1])
  # CubeProp.Children.value.append(reference_cubes[2])
  # CubeProp.Children.value.append(reference_cubes[3])
  # #-----------------------

  conetree_picker = PickController()
  conetree_picker.myConstructor(conetree)

  BBUpdater = BoundingBoxController()
  BBUpdater.FocusNode.connect_from(conetree.FocusSceneNode)
  BBUpdater.TargetSceneGraph.value = graph

  TextUpdater = TextController()
  TextUpdater.FocusNode.connect_from(conetree.FocusSceneNode)
  TextUpdater.TextNode.Transform.value = avango.gua.make_trans_mat(-0.8, -0.43 , 0) * avango.gua.make_scale_mat(0.02)
  screen.Children.value.append(TextUpdater.TextNode)

  # PICKING
  pick_ray = avango.gua.nodes.RayNode(Name = "pick_ray")
  pick_ray.Transform.value = avango.gua.make_trans_mat(0, -0.45, 0) * avango.gua.make_scale_mat(0.5, 0.5, 50)
  screen.Children.value.append(pick_ray)


  ## Pickray append to Screen

  conetree_picker.PickedSceneGraph.value = graph
  conetree_picker.Ray.value = pick_ray

  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  viewer = avango.gua.nodes.Viewer()

  viewer.Pipelines.value = [pipe]
  viewer.SceneGraphs.value = [graph]

  viewer.run()

if __name__ == '__main__':
  start()

