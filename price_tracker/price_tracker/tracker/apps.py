from django.apps import AppConfig
import sys
'''
class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'
    def ready(self):
        if 'runserver' in sys.argv and '--noreload' not in sys.argv:
            print("We are in reloader mode, skipping.")
            return
        else:
            print("Not in reloader mode.")
        
        print("Ready from tracker config")
'''
        