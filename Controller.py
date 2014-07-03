#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

import avango.gua

import device
import time


class Controller(avango.script.Script):
  
  Keyboard = device.KeyboardDevice()
  KeyUp = avango.SFBool()
  KeyDown = avango.SFBool()
  
  def __init__(self):
    self.super(Controller).__init__()
    #self.always_evaluate(True)
    self.KeyUp.connect_from(self.Keyboard.KeyUp)
    self.KeyDown.connect_from(self.Keyboard.KeyDown)
    
  def MyConstructor(self, conetree):
    self.Conetree_ = conetree

  @field_has_changed(KeyUp)
  def key_up_changed(self):
    print "KeyUP" + str(self.KeyUp.value)
  
  @field_has_changed(KeyDown)
  def key_down_changed(self):
    if self.KeyDown.value:
      self.Conetree_.go_deep_at_focus()

  def evaluate(self):
    if self.Keyboard.KeyLeft.value:
      self.Conetree_.focus_next_edge()

    if self.Keyboard.KeyRight.value:
      self.Conetree_.focus_prev_edge()
