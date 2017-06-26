import mmo


class Device(object):
    """
    General ancestor for devices. Logs device attachment
    """

    def attach_handler(self, event):
        attached_device = event.device
        serial_number = attached_device.getSerialNum()
        device_name = attached_device.getDeviceName()
        mmo.logger.info("Connected to Device: {0}, Serial Number: {1}".format(str(device_name), str(serial_number)))

    def detach_handler(self, event):
        detached_device = event.device
        serial_number = detached_device.getSerialNum()
        device_name = detached_device.getDeviceName()
        mmo.logger.info("Disconnected from Device: {0}, Serial Number: {1}".format(str(device_name), str(serial_number)))
