import termux
import time



#termux.API.vibrate(1000,True)
batt_stats = termux.API.battery()
print(batt_stats)

#gps = termux.API.location()
#print(gps)

termux.Camera.takephoto(0,"/data/data/com.termux/files/home/storage/downloads/dev/deebotbase/pic3.jpg")

#termux.TTS.tts_speak("picture taken")

#termux.Microphone.record("/data/data/com.termux/files/home/storage/downloads/dev/deebotbase/mic2.mp3")
'''
Record to specified file, limit in seconds. 
If no other parameters, uses default settings

Parameters
----------
file:    file to record to\n
limit:   record w/ limit (seconds, 0 = unlimited)\n
'aac',705,44100,1
encoder: record w/ encoder (aac, amr_wb, amr_nb)\n
bitrate: record w/ bitrate (in kbps)\n
rate:    record w/ sampling rate (in Hz)\n
count:   record w/ channel count (1, 2, ...)
'''   

# termux.TTS.tts_speak("mic recording started")

# time.sleep(20)

# termux.Microphone.stop()

# termux.TTS.tts_speak("mic recording stopped")

print(termux.Sensors.sensors())

# sensor_data = termux.Sensors.allSensorsData()

# for sens in sensor_data[1].keys():
#       print(sens)
#       print(sensor_data[1][sens])
# x = 0
# while x < 1000:
#       print(termux.Sensors.sensorsData('Samsung Game Rotation Vector'))
#       x = x + 1
# # termux.Sensors.liveSaveLog(sensors, limit=10)

#help(termux) #for available methods

"""
      termux.API - Misc API methods, including generic call
      termux.Camera
      termux.Clipboard
      termux.Media - Playback and media scanner
      termux.Microphone.record(
      termux.Notification
      termux.Scheduler - Job Scheduler
      termux.Sensors
      termux.Share
      termux.SMS
      termux.Telephony - make call, info of device and network
      termux.TTS - Text to speech
      termux.UI - Dialog Widgets and Toast
      termux.Wifi
      termux.Wake
"""

