from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset auto-increment sequences for all tables in the database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Get a list of all tables in the database
            cursor.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            # For each table, reset the sequence to the max id + 1
            for table in tables:
                # Skip tables that don't have an id column
                cursor.execute(f"""
                    SELECT column_name FROM information_schema.columns
                    WHERE table_name = '{table}' AND column_name = 'id'
                """)
                if not cursor.fetchone():
                    continue
                
                # Reset the sequence
                self.stdout.write(f"Resetting sequence for table {table}...")
                cursor.execute(f"""
                    SELECT setval(
                        pg_get_serial_sequence('{table}', 'id'),
                        COALESCE((SELECT MAX(id) FROM {table}), 0) + 1,
                        false
                    )
                """)
            
            self.stdout.write(self.style.SUCCESS('Successfully reset all sequences'))
