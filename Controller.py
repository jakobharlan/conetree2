#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

import avango.gua
import BBVisualization

import device
import time
from Text import TextField

class Navigator(avango.script.Script):

  OutTransform = avango.gua.SFMatrix4()
  OutTransform.value = avango.gua.make_identity_mat()

  Mouse = device.MouseDevice()
  Keyboard = device.KeyboardDevice()

  RotationSpeed = avango.SFFloat()
  MotionSpeed = avango.SFFloat()

  InMatrix = avango.gua.SFMatrix4()

  StartLocation = avango.gua.SFVec3()
  StartRotation = avango.gua.SFVec2()

  __rel_rot_x = avango.SFFloat()
  __rel_rot_y = avango.SFFloat()

  def __init__(self):
    self.super(Navigator).__init__()
    self.always_evaluate(True)

    self.__rot_x = 0.0
    self.__rot_y = 0.0

    self.__location = avango.gua.Vec3(0.0, 0.0, 0.0)

    self.RotationSpeed.value = 0.1
    self.MotionSpeed.value = 0.1

    self.__rel_rot_x.connect_from(self.Mouse.RelY)
    self.__rel_rot_y.connect_from(self.Mouse.RelX)

    self.__last_time = -1

    self.keyboard_controls = True

    self.KeyF1 = False
    self.KeyUp = False
    self.KeyDown = False
    self.KeyLeft = False
    self.KeyRight = False

  def myConstructor(self, conetree):
    self.Conetree_ = conetree

  @field_has_changed(InMatrix)
  def set_location(self):
    self.__location = self.InMatrix.value.get_translate()
    self.__rot_x = 0.0
    self.__rot_y = 0.0

  @field_has_changed(StartLocation)
  def reset_location(self):
    self.__location = self.StartLocation.value

  @field_has_changed(StartRotation)
  def reset_rotation(self):
    self.__rot_x = self.StartRotation.value.x
    self.__rot_y = self.StartRotation.value.y

  def evaluate(self):

    # Key to Toggle Keyboard Controls
    if self.Keyboard.KeyF1.value and not self.KeyF1:
      self.keyboard_controls = not self.keyboard_controls
      if self.keyboard_controls:
        print "Navigator: Keyboard Controls On!"
      else:
        print "Navigator: Keyboard Controls Off!"
    self.KeyF1 = self.Keyboard.KeyF1.value

    if self.keyboard_controls:

      if self.__last_time != -1:
        current_time = time.time()
        frame_time = current_time - self.__last_time
        self.__last_time = current_time

        self.__rot_x -= self.__rel_rot_x.value
        self.__rot_y -= self.__rel_rot_y.value

        rotation = avango.gua.make_rot_mat(self.__rot_y * self.RotationSpeed.value, 0.0, 1.0, 0.0 ) * \
                   avango.gua.make_rot_mat(self.__rot_x * self.RotationSpeed.value, 1.0, 0.0, 0.0)


        if self.Keyboard.KeyW.value:
          self.__location += (rotation * \
                             avango.gua.make_trans_mat(0.0, 0.0, -self.MotionSpeed.value)).get_translate()

        if self.Keyboard.KeyS.value:
          self.__location += (rotation * \
                             avango.gua.make_trans_mat(0.0, 0.0, self.MotionSpeed.value)).get_translate()

        if self.Keyboard.KeyA.value:
          self.__location += (rotation * \
                             avango.gua.make_trans_mat(-self.MotionSpeed.value, 0.0, 0.0)).get_translate()

        if self.Keyboard.KeyD.value:
          self.__location += (rotation * \
                             avango.gua.make_trans_mat(self.MotionSpeed.value, 0.0, 0.0)).get_translate()

        target = avango.gua.make_trans_mat(self.__location) * rotation

        smoothness = frame_time * 3.0

        self.OutTransform.value = self.OutTransform.value * (1.0 - smoothness) + target * smoothness

      else:

        self.__last_time = time.time()


class KeyController(avango.script.Script):

  CAMERAMODE_FREE = 0
  CAMERAMODE_FOLLOW_SMOOTH = 1
  CAMERAMODE_COUNT = 2

  Keyboard = device.KeyboardDevice()

  def __init__(self):
    self.super(KeyController).__init__()
    self.always_evaluate(True)

    self.camera_mode = KeyController.CAMERAMODE_FREE
    self.keyboard_controls = True

    self.KeyF1 = False
    self.KeyUp = False
    self.KeyDown = False
    self.KeyLeft = False
    self.KeyRight = False
    self.KeyC = False
    self.KeyF = False
    self.KeyX = False
    self.KeyP = False

  def myConstructor(self, conetree):
    self.Conetree_ = conetree

  def evaluate_CT_controll(self):
    reset_camera_focus = False

    # Key Left for next focus edge
    if self.Keyboard.KeyLeft.value and not self.KeyLeft:
      self.Conetree_.focus_prev_edge()
    self.KeyLeft = self.Keyboard.KeyLeft.value

    # Key Right for prev focus edge
    if self.Keyboard.KeyRight.value and not self.KeyRight:
      self.Conetree_.focus_next_edge()
    self.KeyRight = self.Keyboard.KeyRight.value

    # Key UP for next level focus
    if self.Keyboard.KeyDown.value and not self.KeyDown:
      self.Conetree_.go_deep_at_focus()
      reset_camera_focus = True
    self.KeyDown = self.Keyboard.KeyDown.value

    # Key Down for next level focus
    if self.Keyboard.KeyUp.value and not self.KeyUp:
      self.Conetree_.level_up()
      reset_camera_focus = True
    self.KeyUp = self.Keyboard.KeyUp.value

    # Key F for changing camera mode
    if self.Keyboard.KeyF.value and not self.KeyF:
      self.camera_mode = (self.camera_mode + 1) % KeyController.CAMERAMODE_COUNT
      print "Cameramode now: " + str(self.camera_mode)
    self.KeyF = self.Keyboard.KeyF.value

    # Key C for collapse focused
    if self.Keyboard.KeyC.value and not self.KeyC:
      self.Conetree_.flip_collapse_at_focus()
      reset_camera_focus = True
    self.KeyC = self.Keyboard.KeyC.value

    # Key X for changing color mode
    if self.Keyboard.KeyX.value and not self.KeyX:
      self.Conetree_.set_colormode(flip = True)
      self.Conetree_.reapply_materials()
    self.KeyX = self.Keyboard.KeyX.value

    # Key L for Label
    if self.Keyboard.KeyL.value and not self.KeyL:
      self.Conetree_.flip_showlabel()
    self.KeyL = self.Keyboard.KeyL.value

    # Key P for printing Cone Tree
    if self.Keyboard.KeyP.value and not self.KeyP:
      self.Conetree_.print_ConeTree()
    self.KeyP = self.Keyboard.KeyP.value

    # if needed, redo the camera position
    if reset_camera_focus and self.camera_mode == KeyController.CAMERAMODE_FOLLOW_SMOOTH:
      # self.Conetree_.set_camera_on_Focus()
      self.Conetree_.scale()
      self.Conetree_.reposition()
      self.Conetree_.layout()

  def evaluate(self):

    # Key to Toggle Keyboard Controls
    if self.Keyboard.KeyF1.value and not self.KeyF1:
      self.keyboard_controls = not self.keyboard_controls
      if self.keyboard_controls:
        print "Keyboard Controls On!"
      else:
        print "Keyboard Controls Off!"
    self.KeyF1 = self.Keyboard.KeyF1.value

    if self.keyboard_controls:
      self.evaluate_CT_controll()


class PickController(avango.script.Script):

  PickedSceneGraph = avango.gua.SFSceneGraph()
  Ray        = avango.gua.SFRayNode()
  Options    = avango.SFInt()
  Mask       = avango.SFString()
  Results    = avango.gua.MFPickResult()

  def __init__(self):
    self.super(PickController).__init__()
    self.always_evaluate(True)

    self.PickedSceneGraph.value = avango.gua.nodes.SceneGraph()
    self.Ray.value  = avango.gua.nodes.RayNode()
    self.Options.value = avango.gua.PickingOptions.PICK_ONLY_FIRST_OBJECT \
                       | avango.gua.PickingOptions.PICK_ONLY_FIRST_FACE

    self.Mask.value = ""

  def myConstructor(self, conetree, ray_scale):
    self.Conetree_ = conetree
    self.ray_scale = ray_scale

  @field_has_changed(Results)
  def update_pickresults(self):
    if len(self.Results.value) > 0:
      node = self.Results.value[0].Object.value
      # self.Conetree_.focus_in_focuscone(node)

  def evaluate(self):
    results = self.PickedSceneGraph.value.ray_test(self.Ray.value,
                                             self.Options.value,
                                             self.Mask.value)
    self.Conetree_.highlight_closest_edge(self.Ray.value, self.ray_scale)
    self.Results.value = results.value


class PointerController(avango.script.Script):

  Pointer = device.PointerDevice()
  Pointer.device_sensor.Station.value = "device-pointer1"
  RayTransformOut = avango.gua.SFMatrix4()
  RayTransformOut.value = avango.gua.make_scale_mat(0.15, 0.15, 0.2)

  def __init__(self):
    self.super(PointerController).__init__()
    self.always_evaluate(True)
    self.KeyUp = False
    self.KeyDown = False
    self.KeyCenter = False

  def myConstructor(self, conetree):
    self.Conetree_ = conetree

  def evaluate(self):

    if self.Pointer.KeyUp.value and not self.KeyUp:
      self.Conetree_.level_up()
    self.KeyUp = self.Pointer.KeyUp.value

    if self.Pointer.KeyDown.value and not self.KeyDown:
      self.Conetree_.scale()
      self.Conetree_.reposition()
    self.KeyDown = self.Pointer.KeyDown.value

    if self.Pointer.KeyCenter.value and not self.KeyCenter:
      self.RayTransformOut.value = avango.gua.make_scale_mat(0.15, 0.15, 30)
    self.KeyCenter = self.Pointer.KeyCenter.value


class BoundingBoxController(avango.script.Script):
  oldFocusNode = avango.gua.SFNode()
  FocusNode = avango.gua.SFNode()
  TargetSceneGraph = avango.gua.SFSceneGraph()
  BBNode     = avango.gua.SFNode()

  def __init__(self):
    self.super(BoundingBoxController).__init__()

  @field_has_changed(FocusNode)
  def focus_node_changed(self):
    if not (self.FocusNode.value == None or self.FocusNode.value == self.oldFocusNode.value) :
      bbvisu = BBVisualization.BoundingBoxVisualization()
      bbvisu.my_constructor(self.FocusNode.value , self.TargetSceneGraph.value,"data/materials/White.gmd")

      self.TargetSceneGraph.value.Root.value.Children.value.remove(self.BBNode.value)

      self.TargetSceneGraph.value.Root.value.Children.value.append(bbvisu.edge_group)
      self.BBNode.value = bbvisu.edge_group
    self.oldFocusNode.value = self.FocusNode.value


class TextController(avango.script.Script):

  FocusNode = avango.gua.SFNode()

  def __init__(self):
    self.super(TextController).__init__()
    avango.gua.load_materials_from("data/materials/font")
    self.TextNode  = avango.gua.nodes.TransformNode(Name = "TextDisplay")
    self.Label_ = TextField()
    self.Label_.my_constructor(self.TextNode)

  @field_has_changed(FocusNode)
  def focus_node_changed(self):
    if not self.FocusNode.value == None:
      self.Label_.sf_text.value = self.FocusNode.value.Path.value

