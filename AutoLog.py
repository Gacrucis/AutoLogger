import os
from sys import platform
import time
import datetime as dt
from AppUtils import Logger

# zoommtg://zoom.us/join?confno=93589976726&pwd=655909

class AutoLogger:

    week_days = {
    0 : 'LUNES',
    1 : 'MARTES',
    2 : 'MIERCOLES',
    3 : 'JUEVES',
    4 : 'VIERNES',
    5 : 'SABADO',
    6 : 'DOMINGO',
    }

    lesson_id_prefix = r'zoommtg://zoom.us/join?confno='
    lesson_pw_prefix = r'&pwd='   

    def __init__(self, schedule):

        self.schedule = schedule

    def get_week_day(self):
        weed_day_id = dt.datetime.now().weekday()
        return AutoLogger.week_days[weed_day_id]

    def get_closest_lesson(self):

        closest_lesson = {}

        current_hour = dt.datetime.now().hour
        current_day_schedule = self.schedule[self.get_week_day()]

        min_delta = None
        closest_lesson_hour = 0

        for lesson_hour in current_day_schedule:
            time_delta = abs(lesson_hour - current_hour)       

            if  min_delta is None or time_delta < min_delta:
                min_delta = time_delta
                closest_lesson = current_day_schedule[lesson_hour]
                closest_lesson_hour = lesson_hour
        
        if min_delta is None:
            min_delta = 0

        return (closest_lesson, min_delta, closest_lesson_hour)
    
    def log(self, max_delta=2):

        weekday = self.get_week_day()

        Logger.course_log('Encontrando la clase mas cercana')

        closest_lesson, min_delta, closest_lesson_hour = self.get_closest_lesson()

        if min_delta > max_delta:
            Logger.info_log(f'La clase mas cercana esta demasiado lejos de la hora actual [{min_delta} horas]')
            return
        
        lesson_id = closest_lesson['id']
        lesson_pw = closest_lesson['password']

        zoom_url = f'{AutoLogger.lesson_id_prefix}{lesson_id}{AutoLogger.lesson_pw_prefix}{lesson_pw}'
        
        if platform == 'linux' or platform == 'linux2':
            lesson_command = f"xdg-open '{zoom_url}'"
            print(zoom_url)
        
        else:
            lesson_command = f'explorer "{zoom_url}"'

        print(f'Ejecutando comando de consola: {lesson_command}')
        
        Logger.info_log(f'Clase mas cercana : {weekday} {closest_lesson_hour}:00')
        Logger.animated_course_log(f'Ingresando a la clase {weekday} {closest_lesson_hour}:00', os.system, lesson_command)
        Logger.info_log('Se ha ingresado a la clase de manera exitosa!')
        Logger.animated_course_log('Saliendo', time.sleep, 1)

