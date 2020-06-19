import signal
import sys
import os

from PyQt5 import QtBluetooth as QtBt
from PyQt5 import QtCore, QtWidgets


if sys.platform == 'darwin':
    os.environ['QT_EVENT_DISPATCHER_CORE_FOUNDATION'] = '1'

class Application(QtWidgets.QApplication):
# class Application(QtCore.QCoreApplication):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.scan_for_devices()
    self.exec()

  def display_status(self):
    print(self.agent.isActive(), self.agent.discoveredDevices())
    devices = self.agent.discoveredDevices()
    print(len(devices))
    if devices is not None:
        for d in devices:
            print(d.name())
  def foo(self, *args, **kwargs):
    print('foo', args, kwargs)

  def scan_for_devices(self):
    self.agent = QtBt.QBluetoothDeviceDiscoveryAgent(self)
    self.agent.deviceDiscovered.connect(self.foo)
    self.agent.finished.connect(self.foo)
    self.agent.error.connect(self.foo)
    self.agent.setLowEnergyDiscoveryTimeout(1000)

    timer = QtCore.QTimer(self.agent)
    timer.start(500)
    timer.timeout.connect(self.display_status)

    self.agent.start()


if __name__ == '__main__':
  import sys
  app = Application(sys.argv)
