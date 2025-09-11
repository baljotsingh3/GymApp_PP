from django.apps import AppConfig

class MemberConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Member"

    def ready(self):
        import Member.signals