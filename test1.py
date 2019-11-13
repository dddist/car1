# -*- coding: utf-8 -*-

import os
import sys
from threading import Thread
import time
import datetime


from kivy.app import App
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.stencilview import StencilView
from kivy.animation import Animation


#os.environ['KIVY_GL_BACKEND'] = 'gl'
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

class PropertyState(object):
    def __init__(self, last, current):
        self.last = last
        self.current = current

    def last_is_not_now(self):
        return self.last is not self.current



class MeterValues():
	def __init__(self, dashboard):
		self.dashboard = dashboard
		self.dashboard.rpm.value = 8000
		self.dashboard.speed.value = 1000
		
	


class Dashboard(FloatLayout):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
        
        # Background
        self.background_image = Image(source='img/back.png')
        self.add_widget(self.background_image)

        # BOTTOM BAR
        self.bottom_bar = Image(source='img/bottomBar.png', pos=(0, -209))
        self.add_widget(self.bottom_bar)
        
         # Center_panel BAR
        self.centre_panel = Image(source='img/centre_panel.png', pos=(0, 50))
        self.add_widget(self.centre_panel)

        
        # Spedometer
        self.speed = Gauge(file_gauge="img/speedometer640.png", do_rotation=False, do_scale=False, do_translation=False, value=0,
                         size_gauge=512, pos=(10, 180))
        self.add_widget(self.speed)
        self.speed.value = 1
        
        # Tachometer
        self.rpm = Gauge(file_gauge="img/tahometer640.png", do_rotation=False, do_scale=False, do_translation=False, value=0,
                         size_gauge=512, pos=(535, 180))
        self.add_widget(self.rpm)
        self.rpm.value = 1
        
        # KM
        self.km_label = Label(text='00123', font_name = 'Avenir.ttc', halign="right", text_size=self.size, font_size=32, pos=(-530,-150))
        self.add_widget(self.km_label)  
        
        # Moto Hour
        self.moto_hour_label = Label(text='00010', font_name = 'Avenir.ttc', halign="right", text_size=self.size, font_size=32, pos=(530,-150))
        self.add_widget(self.moto_hour_label)  
        
        # Pressure_BOM
        self.pressure_BOM = Label(text='0', font_size=35, font_name='hemi_head_bd_it.ttf', pos=(95,140))
        self.pressure_BOM.text='12'
        self.add_widget(self.pressure_BOM)
        
        # Voltage
        self.voltage = Label(text='0', font_size=35, font_name='hemi_head_bd_it.ttf', pos=(95,65))
        self.voltage.text = '24.0'
        self.add_widget(self.voltage)
        
        # Temperature_Naves
        self.temperature_naves = Label(text='0', font_size=35, font_name='hemi_head_bd_it.ttf', pos=(95,-10))
        self.temperature_naves.text = '84'
        self.add_widget(self.temperature_naves)
        
        # Air_brake_pressure
        self.air_brake_pressure = Label(text='0', font_size=35, font_name='hemi_head_bd_it.ttf', pos=(0,140))
        self.air_brake_pressure.text = '5'
        self.add_widget(self.air_brake_pressure)
        
        # Air_pressure
        self.air_pressure = Label(text='0', font_size=35, font_name='hemi_head_bd_it.ttf', pos=(0,65))
        self.air_pressure.text = '4'
        self.add_widget(self.air_pressure)
        
        # Temperature_BOM
        self.temperature_BOM = Label(text='0', font_size=35, font_name='hemi_head_bd_it.ttf', pos=(0,-10))
        self.temperature_BOM.text = '93'
        self.add_widget(self.temperature_BOM)

        # zasor_rul_grey
        self.zasor_rul_grey = Image(source='icon1/zasor_rul_grey.png', size =(64, 64), pos=(-40, -130))
        self.add_widget(self.zasor_rul_grey)
        
        # ruchnik_grey
        self.ruchnik_grey = Image(source='icon1/ruchnik_grey.png', size =(64, 64), pos=(-110, -130))
        self.add_widget(self.ruchnik_grey)

         # akb_grey
        self.akb_grey = Image(source='icon1/akb_red1.png', size =(64, 64), pos=(-180, -130))
        self.add_widget(self.akb_grey)
        
         # air_filter
        self.air_filter_grey = Image(source='icon1/air_filter_grey.png', size =(64, 64), pos=(-245, -130))
        self.add_widget(self.air_filter_grey)
        
        # zasor_kpp_grey
        self.zasor_kpp_grey = Image(source='icon1/zasor_kpp_grey.png', size =(64, 64), pos=(25, -130))
        self.add_widget(self.zasor_kpp_grey)
        
        # temper_bom_grey
        self.temper_bom_grey = Image(source='icon1/temper_bom_grey.png', size =(64, 64), pos=(90, -130))
        self.add_widget(self.temper_bom_grey)
        
        # tormoz_air_grey
        self.tormoz_air_grey = Image(source='icon1/tormoz_air_grey.png', size =(64, 64), pos=(155, -130))
        self.add_widget(self.tormoz_air_grey)
        
        # engine_pressure_grey
        self.engine_pressure_grey = Image(source='icon1/engine_pressure_grey.png', size =(64, 64), pos=(220, -130))
        self.add_widget(self.engine_pressure_grey)
        
        # povorot_p_grey
        self.povorot_p_grey = Image(source='icon1/povorot_p_grey.png', size =(64, 64), pos=(360, 260))
        self.add_widget(self.povorot_p_grey)
        
        # povorot_l_grey
        self.povorot_l_grey = Image(source='icon1/povorot_l_grey.png', size =(64, 64), pos=(-360, 260))
        self.add_widget(self.povorot_l_grey)
        
class Gauge(Scatter):
    value = NumericProperty(10)  # BoundedNumericProperty(0, min=0, max=360, errorvalue=0)
    size_gauge = BoundedNumericProperty(512, min=128, max=512, errorvalue=128)
    size_text = NumericProperty(10)
    file_gauge = StringProperty("")

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)

        self._gauge = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        _img_gauge = Image(source=self.file_gauge, size=(self.size_gauge, self.size_gauge))

        self._needle = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        _img_needle = Image(source="img/arrow512.png", size=(self.size_gauge, self.size_gauge))

        self._gauge.add_widget(_img_gauge)
        self._needle.add_widget(_img_needle)

        self.add_widget(self._gauge)
        self.add_widget(self._needle)

        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(value=self._turn)

    def _update(self, *args):
        self._gauge.pos = self.pos
        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center

    def _turn(self, *args):
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = 112-(0.028*self.value)  # 1 rpm = 0.028 gr


class RequestLoop(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.daemon = True
		self.start()
		
		
	def run(self):
		i = 0
		while True:
			i += 1
			time.sleep(1)
		return int(i * 100)
		
		
class BoxApp(App):
    def build(self):
        
        dashboard = Dashboard()
        meter = MeterValues(dashboard)
        print (RequestLoop.run)
        return dashboard

if __name__ == "__main__":
    # Send requests
    RequestLoop()    
    _old_excepthook = sys.excepthook
    
    def myexcepthook(exctype, value, traceback):
        if exctype == KeyboardInterrupt:
            print ("Handler code goes here")
        else:
            _old_excepthook(exctype, value, traceback)
    sys.excepthook = myexcepthook
    # Show dashboard
    BoxApp().run()
