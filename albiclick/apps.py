from django.apps import AppConfig
#importante para os signalss
class AlbiclickAppConfig(AppConfig):
    name = 'albiclick'

    def ready(self):
        import orders.signals