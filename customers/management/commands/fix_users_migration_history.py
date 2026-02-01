"""
One-off command to fix InconsistentMigrationHistory when admin.0001_initial
is applied before its dependency users.0001_initial on the public schema.

This happens when AUTH_USER_MODEL points to a custom User in a TENANT_APP
(tasks.users) that was added after the public schema was already migrated.
We record users.0001_initial as applied on the public schema so the
dependency graph is consistent. The users app is tenant-only, so we never
actually run its migrations on public—we only satisfy the dependency.
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django_tenants.utils import get_public_schema_name


class Command(BaseCommand):
    help = "Record users.0001_initial as applied on the public schema to fix migration dependency order."

    def handle(self, *args, **options):
        schema_name = get_public_schema_name()
        connection.set_schema(schema_name)
        recorder = MigrationRecorder(connection)
        applied = recorder.applied_migrations()
        if ("users", "0001_initial") in applied:
            self.stdout.write(self.style.WARNING("users.0001_initial is already recorded as applied."))
        else:
            recorder.record_applied("users", "0001_initial")
            self.stdout.write(self.style.SUCCESS("Recorded users.0001_initial as applied on schema %r." % schema_name))
        connection.set_schema_to_public()
