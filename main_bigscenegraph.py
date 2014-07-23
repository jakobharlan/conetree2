#!/usr/bin/python
from Controller import *
from ConeTree import *

import examples_common.navigator
import avango
import avango.gua
import time
import math
import random
from avango.script import field_has_changed

from examples_common.GuaVE import GuaVE

def add_lights(graph, count):

  loader = avango.gua.nodes.TriMeshLoader()

  for x in range(0, count):

    randdir = avango.gua.Vec3(
      random.random() * 2.0 - 1.0,
      random.random() * 2.0 - 1.0,
      random.random() * 4.0 - 1.0
    )

    randdir.normalize()


    sphere_geometry = loader.create_geometry_from_file(
      "sphere" + str(x),
      "data/objects/light_sphere.obj",
      "data/materials/White.gmd",
      avango.gua.LoaderFlags.DEFAULTS
    )

    sphere_geometry.Transform.value = avango.gua.make_scale_mat(0.04, 0.04, 0.04)

    point_light = avango.gua.nodes.PointLightNode(
      Name = "light",
      Color = avango.gua.Color(1, 1, 1),
      Transform = avango.gua.make_identity_mat()
    )

    light_proxy = graph.Root.value.Children.value.append(avango.gua.nodes.TransformNode(
      Name = "light" + str(x),
      Transform = avango.gua.make_trans_mat(randdir[0], randdir[1], randdir[2]),
      Children = [sphere_geometry, point_light]
    ))


def setup_scene(graph, root_monkey, depth_count):

  if (depth_count > 0):
    loader = avango.gua.nodes.TriMeshLoader()

    offset = 2.0

    directions = {
      avango.gua.Vec3(0, offset, 0),
      avango.gua.Vec3(0, -offset, 0),
      avango.gua.Vec3(offset, 0, 0),
      avango.gua.Vec3(-offset, 0, 0),
      avango.gua.Vec3(0, 0, offset),
      avango.gua.Vec3(0, 0, -offset)
    };

    for direction in directions:
      monkey_geometry = loader.create_geometry_from_file(
        "monkey",
        "data/objects/monkey.obj",
        "data/materials/Stones.gmd",
        avango.gua.LoaderFlags.DEFAULTS
      )

      root_monkey.Children.value.append(monkey_geometry)
      monkey_geometry.Transform.value = avango.gua.make_trans_mat(direction[0], direction[1], direction[2]) * avango.gua.make_scale_mat(0.5, 0.5, 0.5)

      setup_scene(graph, monkey_geometry, depth_count - 1)

def start():

  ##initializing scene -------------------
  graph = avango.gua.nodes.SceneGraph(
    Name = "big_scenegraph"
  )

  loader = avango.gua.nodes.TriMeshLoader()

  root_node = avango.gua.nodes.TransformNode(
    Name = "Root",
    Transform = avango.gua.make_scale_mat(0.5, 0.5, 0.5)
  )

  root_monkey = loader.create_geometry_from_file(
    "root_ape",
    "data/objects/monkey.obj",
    "data/materials/Stones.gmd",
    avango.gua.LoaderFlags.DEFAULTS
  )

  root_monkey2 = loader.create_geometry_from_file(
    "root_ape2",
    "data/objects/monkey.obj",
    "data/materials/Stones.gmd",
    avango.gua.LoaderFlags.DEFAULTS
  )

  root_monkey3 = loader.create_geometry_from_file(
    "root_ape3",
    "data/objects/monkey.obj",
    "data/materials/Stones.gmd",
    avango.gua.LoaderFlags.DEFAULTS
  )

  root_monkey4 = loader.create_geometry_from_file(
    "root_ape4",
    "data/objects/monkey.obj",
    "data/materials/Stones.gmd",
    avango.gua.LoaderFlags.DEFAULTS
  )

  root_monkey5 = loader.create_geometry_from_file(
    "root_ape5",
    "data/objects/monkey.obj",
    "data/materials/Stones.gmd",
    avango.gua.LoaderFlags.DEFAULTS
  )
  root_node.Children.value = [root_monkey, root_monkey2, root_monkey3, root_monkey4, root_monkey5]
  graph.Root.value.Children.value.append(root_node)

  add_lights(graph, 20)
  setup_scene(graph, root_monkey, 3)
  setup_scene(graph, root_monkey2, 3)
  setup_scene(graph, root_monkey3, 3)
  setup_scene(graph, root_monkey4, 3)
  setup_scene(graph, root_monkey5, 3)

  ## Viewing Setup Scene ---------------------------------
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
    SceneGraph = "big_scenegraph"
  )


  ## Window Setup Scene--------------------------------
  size = avango.gua.Vec2ui(2560/2, 2560*9/16)
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

  #renderer = avango.gua.create_renderer(pipe);

  ## Viewing Cone Tree Visualization ----------------------
  screen2 = avango.gua.nodes.ScreenNode(
    Name = "screen",
    Width = 1.6/2,
    Height = 0.9,
    Transform = avango.gua.make_trans_mat(0.0, -5, 300)
  )

  eye2 = avango.gua.nodes.TransformNode(
    Name = "eye",
    Transform = avango.gua.make_trans_mat(0.0, 0.0, 1.0)
  )

  screen2.Children.value = [eye2]



  ## create Cone Tree -----------------------------------
  conetree = ConeTree()
  conetree.myConstructor(graph, screen2, eye2)
  CT_graph = avango.gua.nodes.SceneGraph(
      Name = "ConeTree_Graph"
  )
  CT_root = conetree.get_root()
  CT_graph.Root.value.Children.value.append(CT_root)

  conetree_controller = KeyController()
  conetree_controller.myConstructor(conetree)

  conetree_navigator = Navigator()
  conetree_navigator.myConstructor(conetree)

  conetree_picker = PickController()
  conetree_picker.myConstructor(conetree)

  CT_graph.Root.value.Children.value.append(screen2)

  # Light for the Cone Tree
  sun = avango.gua.nodes.SunLightNode(
    Name = "sun",
    Color = avango.gua.Color(1, 1, 1),
    Transform = avango.gua.make_rot_mat(-80, 1, 0, 0)
  )

  CT_graph.Root.value.Children.value.append(sun)

  camera2 = avango.gua.nodes.Camera(
    LeftEye = "/screen/eye",
    RightEye = "/screen/eye",
    LeftScreen = "/screen",
    RightScreen = "/screen",
    SceneGraph = "ConeTree_Graph",
  )

  ## Window Cone Tree Setup Visualization--------------------
  window2 = avango.gua.nodes.Window(
    Size = size,
    LeftResolution = size
  )

  pipe2 = avango.gua.nodes.Pipeline(
      Camera = camera2
    , Window = window2
    , EnableFXAA = True
    , LeftResolution = size
    , EnableFPSDisplay = True
    , EnableBackfaceCulling = False
    , EnableRayDisplay = True
    , FarClip = 10000.0
  )

  # #renderer2 = avango.gua.create_renderer(pipe2);

  # # Final Viewing setup!
  # final_graph = avango.gua.nodes.SceneGraph(Name = "final_scenegraph")

  # quad_left = avango.gua.nodes.TexturedQuadNode()

  # final_screen = avango.gua.nodes.ScreenNode(
  #   Name = "final_screen",
  #   Width = 1.6,
  #   Height = 0.9,
  #   Transform = avango.gua.make_trans_mat(0.0, 0, 0)
  # )

  # final_eye = avango.gua.nodes.TransformNode(
  #   Name = "final_eye",
  #   Transform = avango.gua.make_trans_mat(0.0, 0.0, 1.0)
  # )

  # final_graph.Root.value.Children.value.append(final_screen)
  # final_screen.Children.value = [final_eye]

  # final_size = avango.gua.Vec2ui(2560, 2560*9/16)

  # final_window = avango.gua.nodes.Window(
  #   Size = final_size,
  #   LeftResolution = final_size
  # )

  # final_pipe = avango.gua.nodes.Pipeline(
  #     Camera = avango.gua.nodes.Camera(
  #         LeftEye = "/final_screen/final_eye"
  #       , RightEye = "/final_screen/final_eye"
  #       , LeftScreen = "/final_screen"
  #       , RightScreen = "/final_screen"
  #       , SceneGraph = "final_scenegraph"
  #     )
  #   , Window = final_window
  #   #, PreRenderPipelines = [prepipe]
  #   , LeftResolution = final_size
  # )


  # PICKING
  pick_ray = avango.gua.nodes.RayNode(Name = "pick_ray")
  pick_ray.Transform.value = avango.gua.make_trans_mat(0.0, -0.45, 0.0) * \
                             avango.gua.make_scale_mat(1.0, 1.0, 500.0)

  screen2.Children.value.append(pick_ray)

  conetree_picker.SceneGraph.value = CT_graph
  conetree_picker.Ray.value = pick_ray


  conetree_navigator.StartLocation.value = screen2.Transform.value.get_translate()

  conetree_navigator.RotationSpeed.value = 0.09
  conetree_navigator.MotionSpeed.value = 0.69

  screen2.Transform.connect_from(conetree_navigator.OutTransform)
  conetree_navigator.InMatrix.connect_from(conetree.OutMatrix)

  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  viewer = avango.gua.nodes.Viewer()
  # viewer.Pipelines.value = [pipe, pipe2, final_pipe]
  viewer.Pipelines.value = [pipe, pipe2]
  # viewer.SceneGraphs.value = [graph, CT_graph,final_graph]
  viewer.SceneGraphs.value = [graph, CT_graph]

  viewer.run()

if __name__ == '__main__':
  start()

