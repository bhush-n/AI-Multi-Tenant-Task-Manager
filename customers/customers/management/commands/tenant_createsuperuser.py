from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context


class Command(BaseCommand):
    help = "Create superuser for a specific tenant schema"

    def add_arguments(self, parser):
        parser.add_argument("--schema", required=True, help="Tenant schema name")

    def handle(self, *args, **options):
        schema = options["schema"]
        User = get_user_model()

        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")

        with schema_context(schema):
            User.objects.create_superuser(username, email, password)

        self.stdout.write(
            self.style.SUCCESS(f"Tenant superuser created in schema '{schema}'")
        )
