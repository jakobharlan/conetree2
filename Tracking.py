#!/usr/bin/env python2

# avango and guacamole imports
import avango
import avango.gua
import avango.script
import avango.daemon

class TrackingReader(avango.script.Script):

  MatrixOut = avango.gua.SFMatrix4()

  TransmitterOffset = avango.gua.SFMatrix4()
  TransmitterOffset.value = avango.gua.make_trans_mat(0.0, 0.043, 1.6)


  def __init__(self):
    self.super(TrackingReader).__init__()
    self.tracking_sensor = avango.daemon.nodes.DeviceSensor(
        DeviceService = avango.daemon.DeviceService()
      , TransmitterOffset = self.TransmitterOffset.value
    )
    self.MatrixOut.connect_from(self.tracking_sensor.Matrix)


  def set_target_name(self, target_name):
    self.tracking_sensor.Station.value = target_name
