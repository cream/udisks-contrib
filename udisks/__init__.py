import cream.ipc
from cream.ipc import properties
import dbus

class Device(dbus.Interface):
    def __init__(self, path):
        dbus.Interface.__init__(self,
            cream.ipc.SYSTEM_BUS.get_object('org.freedesktop.UDisks', path),
            'org.freedesktop.UDisks.Device'
        )

    @property
    def fstype(self):
        return properties.get(self, self.dbus_interface, 'IdType')

    def mount(self, fstype, options):
        return self.FilesystemMount(fstype, options)

class UDisks(dbus.Interface):
    def __init__(self):
        dbus.Interface.__init__(self,
            cream.ipc.SYSTEM_BUS.get_object('org.freedesktop.UDisks', '/org/freedesktop/UDisks'),
            'org.freedesktop.UDisks'
        )
        self.connect_to_signal('DeviceAdded', self.on_device_added)

    def on_device_added(self, path):
        device = Device(path)
        if device.fstype:
            device.mount(device.fstype, [])

if __name__ == '__main__':
    from dbus.mainloop.glib import DBusGMainLoop
    DBusGMainLoop(set_as_default=True)

    udisks = UDisks()

    import gobject
    mainloop = gobject.MainLoop()
    mainloop.run()


