#!/usr/bin/python

from ConeTree import *
from Controller import *

import avango
import avango.gua
import avango.oculus
import time
import math
import random
from avango.script import field_has_changed

from examples_common.GuaVE import GuaVE

class ConetreeAndOculusMorphHelperClass(avango.script.Script):
  RotateIn = avango.gua.SFMatrix4()
  TransformIn = avango.gua.SFMatrix4()
  MatrixOut = avango.gua.SFMatrix4()

  def evaluate(self):
    self.MatrixOut.value = self.TransformIn.value * self.RotateIn.value
    # print self.RotateIn.value


def start():

  ##initializing scene -------------------
  graph = avango.gua.nodes.SceneGraph(
    Name = "big_scenegraph"
  )

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




  ## Viewing Cone Tree Visualization ---------OCCULUS----

  # oculus data (for the development kit)
  eye_distance = 0.064  # in meters
  oculus_resolution = avango.gua.Vec2ui(1280, 800)  # in pixels
  oculus_screensize = avango.gua.Vec2(0.16, 0.1)    # in meters

  # viewing setup for the OculusRift
  head = avango.gua.nodes.TransformNode(Name = "head")
  head.Transform.value = avango.gua.make_trans_mat(0.0, -5, 300)

  eye_left = avango.gua.nodes.TransformNode(Name = "eye_left")
  eye_left.Transform.value = avango.gua.make_trans_mat(-0.5 * eye_distance, 0.0, 0.0)

  eye_right = avango.gua.nodes.TransformNode(Name = "eye_right")
  eye_right.Transform.value = avango.gua.make_trans_mat(0.5 * eye_distance, 0.0, 0.0)

  screen_left = avango.gua.nodes.ScreenNode(Name = "screen_left")
  screen_left.Width.value = 0.5 * oculus_screensize.x
  screen_left.Height.value = oculus_screensize.y
  screen_left.Transform.value = avango.gua.make_trans_mat(-0.04, 0.0, -0.05)

  screen_right = avango.gua.nodes.ScreenNode(Name = "screen_right")
  screen_right.Width.value = 0.5 * oculus_screensize.x
  screen_right.Height.value = oculus_screensize.y
  screen_right.Transform.value = avango.gua.make_trans_mat(0.04, 0.0, -0.05)

  head.Children.value = [eye_left, eye_right, screen_left, screen_right]


  ## create Cone Tree -----------------------------------
  conetree = ConeTree()
  conetree.myConstructor(graph, screen_left, eye_left)
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

  CT_graph.Root.value.Children.value.append(head)


  # Light for the Cone Tree
  sun = avango.gua.nodes.SunLightNode(
    Name = "sun",
    Color = avango.gua.Color(1, 1, 1),
    Transform = avango.gua.make_rot_mat(-80, 1, 0, 0)
  )

  CT_graph.Root.value.Children.value.append(sun)

  # setup a stereo camera
  camera_oc = avango.gua.nodes.Camera()
  camera_oc.LeftEye.value = "/head/eye_left"
  camera_oc.RightEye.value = "/head/eye_right"
  camera_oc.LeftScreen.value = "/head/screen_left"
  camera_oc.RightScreen.value = "/head/screen_right"
  camera_oc.SceneGraph.value = "ConeTree_Graph"

  # create an OculusRift window with the barrel distortion
  window_oc = avango.oculus.nodes.OculusWindow()
  window_oc.Size.value = oculus_resolution
  window_oc.LeftResolution.value = avango.gua.Vec2ui(oculus_resolution.x / 2, oculus_resolution.y)
  window_oc.RightResolution.value = avango.gua.Vec2ui(oculus_resolution.x / 2, oculus_resolution.y)

  # setup the pipe
  pipe_oc = avango.gua.nodes.Pipeline()
  pipe_oc.Camera.value = camera_oc
  pipe_oc.Window.value = window_oc
  pipe_oc.LeftResolution.value = window_oc.LeftResolution.value
  pipe_oc.RightResolution.value = window_oc.RightResolution.value
  pipe_oc.EnableStereo.value = True
  pipe_oc.EnableRayDisplay.value = True


  # PICKING
  pick_ray = avango.gua.nodes.RayNode(Name = "pick_ray")
  pick_ray.Transform.value = avango.gua.make_trans_mat(0.0, -0.45, 0.0) * \
                             avango.gua.make_scale_mat(1.0, 1.0, 500.0)

  head.Children.value.append(pick_ray)

  conetree_picker.SceneGraph.value = CT_graph
  conetree_picker.Ray.value = pick_ray


  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  conetree_navigator.StartLocation.value = head.Transform.value.get_translate()

  conetree_navigator.RotationSpeed.value = 0.09
  conetree_navigator.MotionSpeed.value = 0.69

  # connect oculus rotation to head node
  oculus_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
  oculus_sensor.Station.value = "oculus-0"

  helper = ConetreeAndOculusMorphHelperClass()

  helper.TransformIn.connect_from(conetree_navigator.OutTransform)
  helper.RotateIn.connect_from(oculus_sensor.Matrix)
  head.Transform.connect_from(helper.MatrixOut)

  conetree_navigator.InMatrix.connect_from(conetree.OutMatrix)

  viewer = avango.gua.nodes.Viewer()
  viewer.Pipelines.value = [pipe_oc]
  # viewer.Pipelines.value = [pipe, pipe2]
  viewer.SceneGraphs.value = [CT_graph]
  # viewer.SceneGraphs.value = [graph, CT_graph]



  viewer.run()

if __name__ == '__main__':
  start()

