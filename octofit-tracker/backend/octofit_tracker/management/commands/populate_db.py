from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create teams
        teams = [
            {'name': 'Marvel', 'description': 'Team Marvel'},
            {'name': 'DC', 'description': 'Team DC'}
        ]
        db.teams.insert_many(teams)

        # Create users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'}
        ]
        db.users.insert_many(users)
        db.users.create_index([('email', 1)], unique=True)

        # Create activities
        activities = [
            {'user': 'Iron Man', 'activity': 'Running', 'duration': 30},
            {'user': 'Batman', 'activity': 'Cycling', 'duration': 45},
            {'user': 'Wonder Woman', 'activity': 'Swimming', 'duration': 60},
            {'user': 'Captain America', 'activity': 'Pushups', 'duration': 20}
        ]
        db.activities.insert_many(activities)

        # Create leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 100},
            {'team': 'DC', 'points': 90}
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {'name': 'Morning Cardio', 'suggestion': 'Run 5km'},
            {'name': 'Strength', 'suggestion': '50 pushups'}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
