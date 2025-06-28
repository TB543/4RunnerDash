# Bluez Agent for Bluetooth pairing from https://stackoverflow.com/questions/70903233/register-a-bluetooth-agent-with-python-dbus-to-hci1-not-hci0
import threading
import pydbus
from gi.repository import GLib

BUS_NAME = 'org.bluez'
AGENT_IFACE = 'org.bluez.Agent1'
AGNT_MNGR_IFACE = 'org.bluez.AgentManager1'
ADAPTER_IFACE = 'org.bluez.Adapter1'
AGENT_PATH = '/org/bluez/anAgent'
AGNT_MNGR_PATH = '/org/bluez'
DEVICE_IFACE = 'org.bluez.Device1'
CAPABILITY = 'KeyboardDisplay'
bus = pydbus.SystemBus()


class BluezAgent:
    """
    <node>
        <interface name="org.bluez.Agent1">
            <method name="Release" />
            <method name="RequestPinCode">
                <arg name="device" direction="in" type="o" />
                <arg name="pincode" direction="out" type="s" />
            </method>
            <method name="DisplayPinCode">
                <arg name="device" direction="in" type="o" />
                <arg name="pincode" direction="in" type="s" />
            </method>
            <method name="RequestPasskey">
                <arg name="device" direction="in" type="o" />
                <arg name="passkey" direction="out" type="u" />
            </method>
            <method name="DisplayPasskey">
                <arg name="device" direction="in" type="o" />
                <arg name="passkey" direction="in" type="u" />
                <arg name="entered" direction="in" type="q" />
            </method>
            <method name="RequestConfirmation">
                <arg name="device" direction="in" type="o" />
                <arg name="passkey" direction="in" type="u" />
            </method>
            <method name="RequestAuthorization">
              <arg name="device" direction="in" type="o" />
            </method>
            <method name="AuthorizeService">
                <arg name="device" direction="in" type="o" />
                <arg name="uuid" direction="in" type="s" />
            </method>
            <method name="Cancel" />
        </interface>
    </node>
    """

    def Release(self):
        print('Release')

    def RequestPinCode(self, device):
        print('RequestPinCode', device)
        return '1234'

    def DisplayPinCode(self, device, pincode):
        print('DisplayPinCode', device, pincode)

    def RequestPasskey(self, device):
        print('RequestPasskey', device)
        return 1234

    def DisplayPasskey(self, device, passkey, entered):
        print('DisplayPasskey', device, passkey, entered)

    def RequestConfirmation(self, device, passkey):
        print('RequestConfirmation', device, passkey)

    def RequestAuthorization(self, device):
        print('RequestAuthorization', device)

    def AuthorizeService(self, device, uuid):
        print('AuthorizeService', device, uuid)

    def Cancel(self):
        return


def dbus_path_up(dbus_obj):
    return '/'.join(dbus_obj.split('/')[:-1])


def device_found(dbus_obj, properties):
    adapter = bus.get(BUS_NAME, dbus_path_up(dbus_obj))
    device = bus.get(BUS_NAME, dbus_obj)
    print('Stopping discovery')
    adapter.StopDiscovery()
    if device.Paired:
        device.Connect()
    else:
        print('Pairing procedure starting...')
        device.Pair()


def interface_added(path, ifaces):
    if DEVICE_IFACE in ifaces.keys():
        dev_name = ifaces[DEVICE_IFACE].get('Name')
        print('Device found:', dev_name)
        if dev_name == 'HC-06':
            device_found(path, ifaces[DEVICE_IFACE])


def publish_agent():
    bus.register_object(AGENT_PATH, BluezAgent(), None)
    aloop = GLib.MainLoop()
    aloop.run()
    print('Agent Registered')


def create_agent():
    thread = threading.Thread(target=publish_agent, daemon=True)
    thread.start()
    print('Agent running...')


def my_app(hci_idx=0):
    adapter_path = f'/org/bluez/hci{hci_idx}'
    mngr = bus.get(BUS_NAME, '/')
    mngr.onInterfacesAdded = interface_added

    create_agent()
    agnt_mngr = bus.get(BUS_NAME, AGNT_MNGR_PATH)[AGNT_MNGR_IFACE]
    agnt_mngr.RegisterAgent(AGENT_PATH, CAPABILITY)
    print('Agent registered...')
    adapter = bus.get(BUS_NAME, adapter_path)
    # adapter.StartDiscovery()
    mainloop = GLib.MainLoop()
    try:
        mainloop.run()
    except KeyboardInterrupt:
        mainloop.quit()
        adapter.StopDiscovery()


if __name__ == '__main__':
    my_app()
