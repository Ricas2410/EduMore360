from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset auto-increment sequences for SQLite database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Get the current maximum ID from the accounts_user table
            cursor.execute("SELECT MAX(id) FROM accounts_user")
            max_id = cursor.fetchone()[0] or 0
            
            # Reset the SQLite sequence for the accounts_user table
            self.stdout.write(f"Current max user ID: {max_id}")
            cursor.execute(f"UPDATE sqlite_sequence SET seq = {max_id} WHERE name = 'accounts_user'")
            
            # Verify the change
            cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = 'accounts_user'")
            new_seq = cursor.fetchone()[0]
            self.stdout.write(f"New sequence value: {new_seq}")
            
            self.stdout.write(self.style.SUCCESS('Successfully reset the accounts_user sequence'))
