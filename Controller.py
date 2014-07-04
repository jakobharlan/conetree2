#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

import avango.gua

import device
import time


class Controller(avango.script.Script):
  
  Keyboard = device.KeyboardDevice()
  
  def __init__(self):
    self.super(Controller).__init__()
    self.always_evaluate(True)
    self.KeyUp = False
    self.KeyDown = False
    self.KeyLeft = False
    self.KeyRight = False
    
  def MyConstructor(self, conetree):
    self.Conetree_ = conetree

  def evaluate(self):
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
    self.KeyDown = self.Keyboard.KeyDown.value

    # Key PgUp for next level focus 
    if self.Keyboard.KeyUp.value and not self.KeyUp:
      self.Conetree_.level_up()
    self.KeyUp = self.Keyboard.KeyUp.value

    # Key C for collapse focused
    if self.Keyboard.KeyC.value and not self.KeyC:
      self.Conetree_.flip_collapse_at_focus()
    self.KeyC = self.Keyboard.KeyC.value