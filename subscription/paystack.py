"""
Paystack integration for EduMore360 subscription system.
"""
import hmac
import hashlib
import json
import logging
import requests
from decimal import Decimal

from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)


class PaystackAPI:
    """
    Class for interacting with the Paystack API.
    """
    BASE_URL = "https://api.paystack.co"

    def __init__(self):
        self.refresh_keys()

    def refresh_keys(self):
        """
        Refresh API keys from SystemConfiguration or settings.
        Call this method when keys might have been updated in the admin dashboard.
        """
        # Try to get keys from SystemConfiguration first
        try:
            from core.models import SystemConfiguration
            system_config = SystemConfiguration.get_settings()
            self.secret_key = system_config.paystack_secret_key
            self.public_key = system_config.paystack_public_key

            # If keys are empty in SystemConfiguration, fall back to settings
            if not self.secret_key or not self.public_key:
                self.secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
                self.public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
                logger.info("Using Paystack keys from settings.py (fallback)")
            else:
                logger.info("Using Paystack keys from SystemConfiguration")
        except Exception as e:
            # If there's any error with SystemConfiguration, fall back to settings
            logger.warning(f"Error getting Paystack keys from SystemConfiguration: {str(e)}")
            self.secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
            self.public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
            logger.info("Using Paystack keys from settings.py (fallback)")

        if not self.secret_key or not self.public_key:
            logger.error("Paystack API keys not configured in either SystemConfiguration or settings")

    def _headers(self):
        """
        Return the headers for API requests.
        """
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def verify_transaction(self, reference):
        """
        Verify a transaction with Paystack.

        Args:
            reference (str): The transaction reference.

        Returns:
            dict: The response data if successful, None otherwise.
        """
        if not self.secret_key:
            logger.error("Paystack secret key not configured")
            return None

        url = f"{self.BASE_URL}/transaction/verify/{reference}"

        try:
            response = requests.get(url, headers=self._headers(), timeout=10)

            if response.status_code != 200:
                logger.error(f"Paystack API returned status code {response.status_code}: {response.text}")
                return None

            response_data = response.json()

            if not response_data.get('status'):
                logger.error(f"Paystack API returned error: {response_data.get('message')}")
                return None

            return response_data.get('data')

        except requests.exceptions.Timeout:
            logger.error(f"Timeout while verifying transaction {reference}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error while verifying transaction {reference}: {str(e)}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON response from Paystack for transaction {reference}")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error while verifying transaction {reference}: {str(e)}")
            return None

    def initialize_transaction(self, email, amount, callback_url=None, metadata=None, currency='USD'):
        """
        Initialize a transaction with Paystack.

        Args:
            email (str): The customer's email.
            amount (float): The amount to charge in the main currency unit (will be converted to kobo/cents).
            callback_url (str, optional): The URL to redirect to after payment.
            metadata (dict, optional): Additional data to include with the transaction.
            currency (str, optional): The currency of the amount (USD or GHS). Default is USD.

        Returns:
            dict: The response data if successful, None otherwise.
        """
        if not self.secret_key:
            logger.error("Paystack secret key not configured")
            return None

        url = f"{self.BASE_URL}/transaction/initialize"

        # Convert USD to GHS if needed (Paystack accepts GHS)
        # Current exchange rate (as of May 2023) is approximately 1 USD = 11.5 GHS
        # This should be updated with a real-time exchange rate API in production
        if currency.upper() == 'USD':
            # Get the exchange rate from settings or use a default
            exchange_rate = getattr(settings, 'USD_TO_GHS_RATE', 11.5)
            amount = amount * exchange_rate
            logger.info(f"Converted {amount/exchange_rate} USD to {amount} GHS using rate {exchange_rate}")

        # Convert amount to pesewas (smallest GHS currency unit)
        amount_in_pesewas = int(Decimal(str(amount)) * 100)

        payload = {
            'email': email,
            'amount': amount_in_pesewas,
            'currency': 'GHS',  # Paystack's default currency for Ghana
        }

        if callback_url:
            payload['callback_url'] = callback_url

        if metadata:
            payload['metadata'] = metadata

        # Add original currency and amount to metadata for reference
        if currency.upper() == 'USD':
            if not metadata:
                metadata = {}
            metadata.update({
                'original_currency': 'USD',
                'original_amount': amount / exchange_rate
            })
            payload['metadata'] = metadata

        try:
            response = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=10
            )

            if response.status_code != 200:
                logger.error(f"Paystack API returned status code {response.status_code}: {response.text}")
                return None

            response_data = response.json()

            if not response_data.get('status'):
                logger.error(f"Paystack API returned error: {response_data.get('message')}")
                return None

            return response_data.get('data')

        except requests.exceptions.Timeout:
            logger.error("Timeout while initializing transaction")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error while initializing transaction: {str(e)}")
            return None
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from Paystack")
            return None
        except Exception as e:
            logger.exception(f"Unexpected error while initializing transaction: {str(e)}")
            return None

    def create_subscription(self, customer_email, plan_code):
        """
        Create a subscription for a customer.

        Args:
            customer_email (str): The customer's email.
            plan_code (str): The Paystack plan code.

        Returns:
            dict: The response data if successful, None otherwise.
        """
        if not self.secret_key:
            logger.error("Paystack secret key not configured")
            return None

        url = f"{self.BASE_URL}/subscription"

        payload = {
            'customer': customer_email,
            'plan': plan_code,
        }

        try:
            response = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=10
            )

            if response.status_code != 200:
                logger.error(f"Paystack API returned status code {response.status_code}: {response.text}")
                return None

            response_data = response.json()

            if not response_data.get('status'):
                logger.error(f"Paystack API returned error: {response_data.get('message')}")
                return None

            return response_data.get('data')

        except Exception as e:
            logger.exception(f"Error creating subscription: {str(e)}")
            return None

    def cancel_subscription(self, subscription_code):
        """
        Cancel a subscription.

        Args:
            subscription_code (str): The Paystack subscription code.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.secret_key:
            logger.error("Paystack secret key not configured")
            return False

        url = f"{self.BASE_URL}/subscription/disable"

        payload = {
            'code': subscription_code,
        }

        try:
            response = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=10
            )

            if response.status_code != 200:
                logger.error(f"Paystack API returned status code {response.status_code}: {response.text}")
                return False

            response_data = response.json()

            if not response_data.get('status'):
                logger.error(f"Paystack API returned error: {response_data.get('message')}")
                return False

            return True

        except Exception as e:
            logger.exception(f"Error cancelling subscription: {str(e)}")
            return False

    def verify_webhook_signature(self, payload, signature):
        """
        Verify the signature of a webhook payload.

        Args:
            payload (bytes): The raw request body.
            signature (str): The X-Paystack-Signature header value.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        if not self.secret_key:
            logger.error("Paystack secret key not configured")
            return False

        computed_signature = hmac.new(
            self.secret_key.encode('utf-8'),
            payload,
            hashlib.sha512
        ).hexdigest()

        return computed_signature == signature

    def get_payment_link(self, request, subscription):
        """
        Generate a payment link for a subscription.

        Args:
            request: The HTTP request object.
            subscription: The Subscription object.

        Returns:
            str: The payment link if successful, None otherwise.
        """
        if not self.public_key:
            logger.error("Paystack public key not configured")
            return None

        if not self.secret_key:
            logger.error("Paystack secret key not configured")
            return None

        # Log API key information (partial for security)
        logger.info(f"Using Paystack public key: {self.public_key[:4]}...{self.public_key[-4:] if len(self.public_key) > 8 else ''}")
        logger.info(f"Using Paystack secret key: {self.secret_key[:4]}...{self.secret_key[-4:] if len(self.secret_key) > 8 else ''}")

        # Calculate amount (in USD)
        amount = float(subscription.plan.price)
        logger.info(f"Original amount in USD: {amount}")

        # Generate callback URL
        callback_url = request.build_absolute_uri(
            reverse('subscription:payment_success', args=[subscription.id])
        )
        logger.info(f"Callback URL: {callback_url}")

        # Generate metadata
        metadata = {
            'subscription_id': str(subscription.id),
            'plan_name': subscription.plan.name,
            'plan_type': subscription.plan.plan_type,
            'billing_cycle': subscription.plan.billing_cycle,
            'user_id': str(subscription.user.id),
            'user_email': subscription.user.email,
            'display_currency': 'USD',
            'display_amount': amount,
        }

        # Get the exchange rate from settings or use a default
        exchange_rate = getattr(settings, 'USD_TO_GHS_RATE', 11.5)
        amount_ghs = amount * exchange_rate
        logger.info(f"Converted amount to GHS: {amount_ghs} using rate {exchange_rate}")

        try:
            # Create a direct payment link using the Paystack API
            url = f"{self.BASE_URL}/transaction/initialize"

            payload = {
                'email': subscription.user.email,
                'amount': int(amount_ghs * 100),  # Convert to pesewas
                'currency': 'GHS',
                'callback_url': callback_url,
                'metadata': metadata,
                'channels': ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']
            }

            logger.info(f"Sending request to Paystack: {url} with payload: {payload}")

            response = requests.post(
                url,
                headers=self._headers(),
                json=payload,
                timeout=10
            )

            logger.info(f"Paystack response status: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"Paystack API error: {response.text}")
                return None

            response_data = response.json()

            if not response_data.get('status'):
                logger.error(f"Paystack API returned error: {response_data.get('message')}")
                return None

            authorization_url = response_data.get('data', {}).get('authorization_url')
            logger.info(f"Generated payment link: {authorization_url}")

            return authorization_url

        except Exception as e:
            logger.exception(f"Error generating payment link: {str(e)}")
            return None


# Create a singleton instance
paystack = PaystackAPI()
