from mmo import status


class Device(object):
    """
    General ancestor for devices. Logs device attachment
    """
    def attach_handler(self, event):
        attached_device = event.device
        serial_number = attached_device.getSerialNum()
        device_name = attached_device.getDeviceName()
        print("Connected to Device: {0}, Serial Number: {1}".format(str(device_name), str(serial_number)))
        status["{} connected".format(device_name)] = True

    def detach_handler(self, event):
        detached_device = event.device
        serial_number = detached_device.getSerialNum()
        device_name = detached_device.getDeviceName()
        print("Disconnected from Device: {0}, Serial Number: {1}".format(str(device_name), str(serial_number)))
        status["{} connected".format(device_name)] = False