import signal
import sys
import os

from PyQt5 import QtBluetooth as QtBt
from PyQt5 import QtCore, QtWidgets

service_uuid = '7b183224-9168-443e-a927-7aeea07e8105'
count_uuid = '292bd3d2-14ff-45ed-9343-55d125edb721'
rw_uuid = '56cd7757-5f47-4dcd-a787-07d648956068'
data_uuid = 'fec26ec4-6d71-4442-9f81-55bc21d658d6'
print(QtBt.QBluetoothUuid(rw_uuid))
data_uuid = QtBt.QBluetoothUuid(data_uuid)
service_uuid = QtBt.QBluetoothUuid(service_uuid)
if sys.platform == 'darwin':
    os.environ['QT_EVENT_DISPATCHER_CORE_FOUNDATION'] = '1'

class Application(QtWidgets.QApplication):
# class Application(QtCore.QCoreApplication):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # self.le_controller = QLowEnergyController
    
    self.scan_for_devices()
    print("before exec")
    self.exec()
    print("after exec")

  def display_status(self):
    print(self.agent.isActive(), self.agent.discoveredDevices())
    if False:
        devices = self.agent.discoveredDevices()
        print(len(devices))
        if devices is not None:
            for d in devices:
                print(d.name())
  def c(self, *args, **kwargs):
      print('c', *args, **kwargs)
      print('controller connected')
      self.controller.discoverServices()
  def service(self, *args, **kwargs):
      print('service discovered', args, kwargs)
      print('service uuid', args[0].toString())

  def discoveryFinished(self, *args, **kwargs):
      print('discovery finished', args, kwargs)
      services = self.controller.services()
      for s in services:
          if s==service_uuid:
              print("Found service")
              self.first = self.controller.createServiceObject(s)
              self.first.stateChanged.connect(self.stateChanged)
              print(self.first, 'state', self.first.state())
              self.first.discoverDetails()
  def stateChanged(self, *args, **kwargs):
      print('stateChanged', args, kwargs)
      print(self.first.characteristics())
      print(self.first.includedServices())
      if args[0]==QtBt.QLowEnergyService.ServiceDiscovered:
          print('*'*80)
          
  def foo(self, *args, **kwargs):
    # print('foo', args, kwargs)
    if len(args):
        if args[0].name()=='NIST0002':
            print(args[0].name())
            self.controller = QtBt.QLowEnergyController(args[0]).createCentral(args[0])
            self.controller.connected.connect(self.c)
            self.controller.serviceDiscovered.connect(self.service)
            self.controller.discoveryFinished.connect(self.discoveryFinished)
            self.controller.connectToDevice()
            print(self.controller)

  def scan_for_devices(self):
    print("scan_for_devices")
    self.agent = QtBt.QBluetoothDeviceDiscoveryAgent(self)
    self.agent.deviceDiscovered.connect(self.foo)
    self.agent.finished.connect(self.foo)
    self.agent.error.connect(self.foo)
    self.agent.setLowEnergyDiscoveryTimeout(3000)

    timer = QtCore.QTimer(self.agent)
    timer.start(5000)
    timer.timeout.connect(self.display_status)

    self.agent.start()


if __name__ == '__main__':
  import sys
  app = Application(sys.argv)
