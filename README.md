# pyusbip
PyUSBIP


## Requirements

- Python 3
- USBIP package
- Flask

## Server Setup

edit `/etc/modules` with additional lines

```
usbip_host
```


or load modules with

```
sudo modprobe usbip_host
```

validate the drivers with 
```
ls /lib/modules/$(uname -r)/kernel/drivers/usb/usbip
```
