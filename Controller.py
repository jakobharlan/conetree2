#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

import avango.gua

import device
import time


class Controller(avango.script.Script):


  CAMERAMODE_FREE = 0
  CAMERAMODE_FOLLOW_SMOOTH = 1
  CAMERAMODE_COUNT = 2

  OutTransform = avango.gua.SFMatrix4()

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
    self.super(Controller).__init__()
    self.always_evaluate(True)

    self.__rot_x = 0.0
    self.__rot_y = 0.0

    self.__location = avango.gua.Vec3(0.0, 0.0, 0.0)

    self.RotationSpeed.value = 0.1
    self.MotionSpeed.value = 0.1

    self.__rel_rot_x.connect_from(self.Mouse.RelY)
    self.__rel_rot_y.connect_from(self.Mouse.RelX)

    self.__last_time = -1

    self.camera_mode = Controller.CAMERAMODE_FREE

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

    # Key PgDown for next level focus
    if self.Keyboard.KeyDown.value and not self.KeyDown:
      self.Conetree_.go_deep_at_focus()
      reset_camera_focus = True
    self.KeyDown = self.Keyboard.KeyDown.value

    # Key PgUp for next level focus
    if self.Keyboard.KeyUp.value and not self.KeyUp:
      self.Conetree_.level_up()
      reset_camera_focus = True
    self.KeyUp = self.Keyboard.KeyUp.value

    # Key F for changing camera mode
    if self.Keyboard.KeyF.value and not self.KeyF:
      self.camera_mode = (self.camera_mode + 1) % Controller.CAMERAMODE_COUNT
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

    # Key P for printing Cone Tree
    if self.Keyboard.KeyP.value and not self.KeyP:
      self.Conetree_.print_ConeTree()
    self.KeyP = self.Keyboard.KeyP.value

    if reset_camera_focus and self.camera_mode == Controller.CAMERAMODE_FOLLOW_SMOOTH:
      self.Conetree_.set_camera_on_Focus()

  def evaluate(self):

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

    self.evaluate_CT_controll()
