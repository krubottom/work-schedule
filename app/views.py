from app import app
import os.path
import socket
import json

@app.route("/")
@app.route("/index")
def index():
    #return "Hello from " + socket.gethostname()
	return render_template('index.html', title='Home')

@app.route("/cameraview", methods=['GET', 'POST'])
def cameraview():
	form = CameraInfo()
	if form.validate_on_submit():
		# flash('IP Address: %s' % (form.FormCameraAddress.data))
		CameraFirmware = axislib.GetAxisFirmwareVersion(form.FormCameraAddress.data, form.FormCameraPasswd.data)
		CameraTemp = axislib.GetAxisTemp(form.FormCameraAddress.data,form.FormCameraPasswd.data)
		CameraModel = axislib.GetAxisCameraModel(form.FormCameraAddress.data,form.FormCameraPasswd.data)
		return render_template('camerainfo.html', title='Camera Info', firmware=CameraFirmware, temp=CameraTemp, model=CameraModel)
	return render_template('cameraview.html', title='Camera View', form=form)

@app.route("/weather")
def weather():
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?zip=82834,us&apikey=af0f8b985d0c16be86d217ec968c9118'
    f = urllib2.urlopen(weather_url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    weather_description = parsed_json['weather'][0]['description']
    weather_name = parsed_json['name']
    f.close()
    weather_string = "Current weather in " + weather_name + " is " + weather_description
    return render_template('weather.html', title='Weather', weather=weather_string)
