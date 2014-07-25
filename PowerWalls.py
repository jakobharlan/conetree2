#!/usr/bin/env python2

# avango and guacamole imports
import avango
import avango.gua


class PowerWall:

  def __init__(self, name, parent_node, screen_size, screen_transform, resolution):
    self.name             = name
    self.screen_size      = screen_size
    self.screen_transform = screen_transform
    self.resolution       = resolution
    self.window_size      = avango.gua.Vec2ui(2 * resolution.x, resolution.y)

    # create group node containing all nodes of this display
    self.group_node = avango.gua.nodes.TransformNode(Name = self.name)
    parent_node.Children.value.append(self.group_node)

    # create screen
    self.screen = avango.gua.nodes.ScreenNode(Name = "screen")
    self.screen.Width.value     = self.screen_size.x
    self.screen.Height.value    = self.screen_size.y
    self.screen.Transform.value = self.screen_transform
    self.group_node.Children.value.append(self.screen)

    self.users          = []
    self.displaystrings = []
    self.warpmatrices   = []


  def create_eyes(self, distance = 0.064):
    left_eye = avango.gua.nodes.TransformNode(Name = "left_eye")
    left_eye.Transform.value = avango.gua.make_trans_mat(-0.5 * distance,  0.0, 0.0)

    right_eye = avango.gua.nodes.TransformNode(Name = "right_eye")
    right_eye.Transform.value = avango.gua.make_trans_mat(0.5 * distance,  0.0, 0.0)

    return (left_eye, right_eye)


  def create_head(self, left_eye, right_eye):
    head = avango.gua.nodes.TransformNode(Name = "head")
    head.Transform.value = avango.gua.make_trans_mat(0.0, 1.75, 2.0)  # default transformation
    head.Children.value = [left_eye, right_eye]

    return head


  def create_window(self, displaystring):
    window = avango.gua.nodes.Window()
    window.Size.value                  = self.window_size
    window.Title.value                 = self.name + str(len(self.users))
    window.LeftResolution.value        = self.resolution
    window.LeftPosition.value          = avango.gua.Vec2ui(0, 0)
    window.RightResolution.value       = self.resolution
    window.RightPosition.value         = avango.gua.Vec2ui(int(self.window_size.x * 0.5), 0)
    window.StereoMode.value            = avango.gua.StereoMode.SIDE_BY_SIDE
    window.Display.value               = displaystring

    if len(self.warpmatrices) == 6:
      self.set_warpmatrices(window, self.warpmatrices)

    return window


  def create_camera(self, scenegraph, left_eye, right_eye):
    camera = avango.gua.nodes.Camera()
    camera.SceneGraph.value   = scenegraph.Name.value
    camera.LeftScreen.value   = self.screen.Path.value
    camera.RightScreen.value  = self.screen.Path.value
    camera.LeftEye.value      = left_eye.Path.value
    camera.RightEye.value     = right_eye.Path.value

    return camera


  def create_pipeline(self, window, camera):
    return avango.gua.nodes.Pipeline(
        Window = window
      , LeftResolution = self.window_size
      , RightResolution = self.window_size
      , Camera = camera
      , EnableStereo = True
    )


  def set_warpmatrices(self, window, warpmatrices):
    window.WarpMatrixRedRight.value    = warpmatrices[0]
    window.WarpMatrixGreenRight.value  = warpmatrices[1]
    window.WarpMatrixBlueRight.value   = warpmatrices[2]
    window.WarpMatrixRedLeft.value     = warpmatrices[3]
    window.WarpMatrixGreenLeft.value   = warpmatrices[4]
    window.WarpMatrixBlueLeft.value    = warpmatrices[5]


  def create_user(self, scenegraph):

    if len(self.users) < len(self.displaystrings):

      print "creating user number {0} on display {1}".format(len(self.users), self.displaystrings[len(self.users)])

      left_eye, right_eye = self.create_eyes()
      head    = self.create_head(left_eye, right_eye)

      user_node = avango.gua.nodes.TransformNode(Name = "User{0}".format(len(self.users)))
      self.group_node.Children.value.append(user_node)
      user_node.Children.value.append(head)

      window  = self.create_window(self.displaystrings[len(self.users)])
      camera  = self.create_camera(scenegraph, left_eye, right_eye)
      pipe    = self.create_pipeline(window, camera)

      self.users.append( (head, pipe) )

      return (head, pipe)

    else:   # no more free slots

      return None



class SmallPowerWall(PowerWall):

  def __init__(self, parent_node):
    PowerWall.__init__(self
      , name = "LargePowerWall"
      , parent_node = parent_node
      , screen_size = avango.gua.Vec2(3.0, 1.98)
      , screen_transform = avango.gua.make_trans_mat(0.0, 1.42, 0.0)
      , resolution = avango.gua.Vec2ui(1920, 1200)
    )

    self.warpmatrices = \
      ["/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(len(self.users) * 2 + 2)] * 3 + \
      ["/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(len(self.users) * 2 + 1)] * 3

    self.displaystrings = [":0.0", ":0.1"]


class LargePowerWall(PowerWall):

  def __init__(self, parent_node):
    PowerWall.__init__(self
      , name = "LargePowerWall"
      , parent_node = parent_node
      , screen_size = avango.gua.Vec2(4.16, 2.61)
      , screen_transform = avango.gua.make_trans_mat(0.0, 1.57, 0.0)
      , resolution = avango.gua.Vec2ui(1920, 1200)
    )

    self.warpmatrices = ["/opt/dlp-warpmatrices/dlp_6_warp_P{0}.warp".format(i) for i in [4, 5, 6, 1, 2, 3]]

    self.displaystrings = [":0.0", ":0.1", ":0.2", ":0.3"]
