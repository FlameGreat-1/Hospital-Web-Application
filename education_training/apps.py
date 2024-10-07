from django.apps import AppConfig


class EducationTrainingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'education_training'


class EducationTrainingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'education_training'

    def ready(self):
        import education_training.signals
