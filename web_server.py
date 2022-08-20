from flask import Flask, render_template
from pyusbip import UsbIpServer

app = Flask(__name__)

@app.route("/")
def home():
    return u.get_devices_list()

@app.route("/devices")
def device_list():
    return render_template('devices.html', devices=u.get_devices_list())


if __name__ == "__main__":
    u = UsbIpServer()
    app.run("0.0.0.0")
