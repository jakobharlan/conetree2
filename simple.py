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

## Parameters:
size = avango.gua.Vec2ui(2560/2, 2560*9/16)



def setup_scene(graph):

  loader = avango.gua.nodes.TriMeshLoader()

  root_node = avango.gua.nodes.TransformNode(
    Name = "Root",
    Transform = avango.gua.make_scale_mat(0.2),
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

  group_light_2 = avango.gua.nodes.TransformNode(
    Name = "group_light_2",
  )

  graph.Root.value.Children.value.append(root_node)
  root_node.Children.value.append(group_monkey)
  root_node.Children.value.append(group_light)
  root_node.Children.value.append(group_light_spheres)
  group_light.Children.value.append(group_light_2)

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
    group_light_2.Children.value.append(light)

  for lights_sphere in lights_spheres:
    group_light_spheres.Children.value.append(lights_sphere)


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


def start():

  ##initializing scene -------------------
  graph = avango.gua.nodes.SceneGraph(
    Name = "scenegraph"
  )

  setup_scene(graph)

  pipe_scene = viewing_setup_scene(graph)

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

  conetree_controller = Controller()
  conetree_controller.myConstructor(conetree)

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
    SceneGraph = "ConeTree_Graph"
  )

  ## Window Cone Tree Setup Visualization--------------------
  window2 = avango.gua.nodes.Window(
    Size = size,
    LeftResolution = size
  )

  pipe2 = avango.gua.nodes.Pipeline(
    Camera = camera2,
    Window = window2,
    EnableSsao = True,
    SsaoIntensity = 2.0,
    EnableFXAA = True,
    LeftResolution = size,
    EnableFPSDisplay = True,
    EnableBackfaceCulling = False
  )

  renderer2 = avango.gua.create_renderer(pipe2);

  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  conetree_controller.StartLocation.value = screen2.Transform.value.get_translate()

  conetree_controller.RotationSpeed.value = 0.09
  conetree_controller.MotionSpeed.value = 0.69

  screen2.Transform.connect_from(conetree_controller.OutTransform)
  conetree_controller.InMatrix.connect_from(conetree.OutMatrix)


  viewer = avango.gua.nodes.Viewer()
  viewer.Pipelines.value = [pipe_scene, pipe2]
  viewer.SceneGraphs.value = [graph, CT_graph]

  viewer.run()

if __name__ == '__main__':
  start()
