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

class Printer(avango.script.Script):
  Matrix = avango.gua.SFMatrix4()

  @field_has_changed(Matrix)
  def do(self):
    print self.Matrix.value

def setup_scene(graph):

  loader = avango.gua.nodes.TriMeshLoader()

  root_node = avango.gua.nodes.TransformNode(
    Name = "Root",
    Transform =  avango.gua.make_trans_mat(0, 1.1, -2) * avango.gua.make_scale_mat(0.2)
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
    lights[i].Transform.value = avango.gua.make_trans_mat(x, 2, 0) * avango.gua.make_scale_mat(2)
    lights_spheres[i].Transform.value = avango.gua.make_trans_mat(x, 2, 0) * avango.gua.make_scale_mat(0.15)
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


  ##create Powerwall setup
  powerwall = LargePowerWall(graph.Root.value)
  avango.gua.create_texture("data/textures/skymap.jpg")
  for target_name in ["tracking-dlp-glasses-{0}".format(i) for i in [1, 4, 5, 6]]:
    head, pipe = powerwall.create_user(graph)

    pipe.BackgroundTexture.value = "data/textures/skymap.jpg"
    pipe.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE

    pipe.EnableRayDisplay.value = True

    headtracking = TrackingReader()
    headtracking.set_target_name(target_name)
    head.Transform.connect_from(headtracking.MatrixOut)


  ## create Cone Tree -----------------------------------
  conetree = ConeTree()
  conetree.myConstructor(graph)

  CT_root = conetree.get_root()


  CT_root.Transform.value = avango.gua.make_trans_mat(0,0.5,0) * avango.gua.make_scale_mat(1.0/110)
  CubeProp = avango.gua.nodes.TransformNode( Name = "CubeProp")
  CubeTracker = TrackingReader()
  CubeTracker.set_target_name("tracking-cube")
  CubeProp.Transform.connect_from(CubeTracker.MatrixOut)

  graph.Root.value.Children.value.append(CubeProp)
  CubeProp.Children.value.append(CT_root)


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

  conetree_picker.SceneGraph.value = graph
  conetree_picker.Ray.value = pick_ray

  guaVE = GuaVE()
  guaVE.start(locals(), globals())

  viewer = avango.gua.nodes.Viewer()

  viewer.Pipelines.value = [pipe for head, pipe in powerwall.users]
  viewer.SceneGraphs.value = [graph]

  viewer.run()

if __name__ == '__main__':
  start()

