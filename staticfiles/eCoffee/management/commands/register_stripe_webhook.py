import stripe
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
import os

class Command(BaseCommand):
    help = 'Register a webhook endpoint with Stripe'

    def handle(self, *args, **kwargs):
        
        load_dotenv()
        
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

        try:
            endpoint = stripe.WebhookEndpoint.create(
                url='http://127.0.0.1:8000/webhook/', 
                enabled_events=[
                    'payment_intent.payment_failed',
                    'payment_intent.succeeded',
                ],
            )
            self.stdout.write(self.style.SUCCESS(f"Webhook endpoint created: {endpoint.id}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating webhook endpoint: {e}"))
