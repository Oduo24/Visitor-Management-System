from app import create_app

from app.seeders.database_seeder import (
    DatabaseSeeder,
)

app = create_app()

with app.app_context():
    DatabaseSeeder.run()