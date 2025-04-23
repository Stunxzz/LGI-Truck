from django.apps import AppConfig

class DeliveryNoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delivery_note'

    def ready(self):
        import delivery_note.signals