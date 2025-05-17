/**
 * EduMore360 Payment Processing Functionality
 * 
 * This file contains the JavaScript functionality for processing payments.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Stripe Elements
    initStripeElements();
    
    // Initialize Paystack
    initPaystack();
    
    // Initialize Mobile Money
    initMobileMoney();
    
    // Initialize payment method tabs
    initPaymentMethodTabs();
});

/**
 * Initialize Stripe Elements
 */
function initStripeElements() {
    const stripePublicKey = document.querySelector('meta[name="stripe-public-key"]')?.content;
    if (!stripePublicKey) return;
    
    const cardElement = document.getElementById('card-element');
    if (!cardElement) return;
    
    // Initialize Stripe
    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    
    // Create card element
    const card = elements.create('card', {
        style: {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        }
    });
    
    // Mount the card element
    card.mount('#card-element');
    
    // Handle real-time validation errors
    card.addEventListener('change', function(event) {
        const displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });
    
    // Handle form submission
    const form = document.getElementById('payment-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            // Disable the submit button to prevent multiple submissions
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.classList.add('loading');
            
            // Get cardholder name
            const cardholderName = document.getElementById('card-holder-name')?.value;
            
            // Create payment method
            stripe.createPaymentMethod({
                type: 'card',
                card: card,
                billing_details: {
                    name: cardholderName
                }
            }).then(function(result) {
                if (result.error) {
                    // Show error to customer
                    const errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                    
                    // Re-enable the submit button
                    submitButton.disabled = false;
                    submitButton.classList.remove('loading');
                } else {
                    // Send payment method ID to server
                    stripeTokenHandler(result.paymentMethod.id);
                }
            });
        });
    }
    
    // Submit the form with the payment method ID
    function stripeTokenHandler(paymentMethodId) {
        // Insert the payment method ID into the form
        const hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'payment_method_id');
        hiddenInput.setAttribute('value', paymentMethodId);
        form.appendChild(hiddenInput);
        
        // Submit the form
        form.submit();
    }
}

/**
 * Initialize Paystack
 */
function initPaystack() {
    const paystackButton = document.getElementById('paystack-button');
    if (!paystackButton) return;
    
    const paystackPublicKey = document.querySelector('meta[name="paystack-public-key"]')?.content;
    if (!paystackPublicKey) return;
    
    // Get payment details
    const email = document.querySelector('meta[name="user-email"]')?.content;
    const amount = document.querySelector('meta[name="payment-amount"]')?.content;
    const currency = document.querySelector('meta[name="payment-currency"]')?.content || 'NGN';
    const subscriptionId = document.querySelector('meta[name="subscription-id"]')?.content;
    const callbackUrl = document.querySelector('meta[name="payment-callback-url"]')?.content;
    
    if (!email || !amount || !subscriptionId || !callbackUrl) return;
    
    // Handle Paystack button click
    paystackButton.addEventListener('click', function() {
        const handler = PaystackPop.setup({
            key: paystackPublicKey,
            email: email,
            amount: parseFloat(amount) * 100, // Paystack amount is in kobo (1/100 of the currency)
            currency: currency,
            ref: 'ps_' + Math.floor((Math.random() * 1000000000) + 1),
            callback: function(response) {
                // Redirect to success page with reference
                window.location.href = `${callbackUrl}?reference=${response.reference}`;
            },
            onClose: function() {
                console.log('Payment window closed');
            }
        });
        
        handler.openIframe();
    });
}

/**
 * Initialize Mobile Money
 */
function initMobileMoney() {
    const mobileMoneyButton = document.getElementById('mobile-money-button');
    if (!mobileMoneyButton) return;
    
    const mobileMoneyForm = document.getElementById('mobile-money-form');
    if (!mobileMoneyForm) return;
    
    // Handle Mobile Money button click
    mobileMoneyButton.addEventListener('click', function() {
        // Show the Mobile Money form
        document.querySelectorAll('.payment-method-form').forEach(form => {
            form.classList.add('hidden');
        });
        
        mobileMoneyForm.classList.remove('hidden');
    });
    
    // Handle Mobile Money form submission
    mobileMoneyForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Disable the submit button to prevent multiple submissions
        const submitButton = mobileMoneyForm.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.classList.add('loading');
        
        // Get form data
        const formData = new FormData(mobileMoneyForm);
        
        // Send the form data to the server
        fetch('/subscription/process-mobile-money/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                const successMessage = document.createElement('div');
                successMessage.classList.add('alert', 'alert-success', 'mt-4');
                successMessage.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>${data.message}</span>
                `;
                
                mobileMoneyForm.appendChild(successMessage);
                
                // Redirect to success page after a delay
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 3000);
            } else {
                // Show error message
                const errorMessage = document.createElement('div');
                errorMessage.classList.add('alert', 'alert-error', 'mt-4');
                errorMessage.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>${data.message}</span>
                `;
                
                mobileMoneyForm.appendChild(errorMessage);
                
                // Re-enable the submit button
                submitButton.disabled = false;
                submitButton.classList.remove('loading');
            }
        })
        .catch(error => {
            console.error('Error processing mobile money payment:', error);
            
            // Show error message
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('alert', 'alert-error', 'mt-4');
            errorMessage.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>An error occurred while processing your payment. Please try again.</span>
            `;
            
            mobileMoneyForm.appendChild(errorMessage);
            
            // Re-enable the submit button
            submitButton.disabled = false;
            submitButton.classList.remove('loading');
        });
    });
}

/**
 * Initialize payment method tabs
 */
function initPaymentMethodTabs() {
    const paymentMethodTabs = document.querySelectorAll('.payment-method-tab');
    if (paymentMethodTabs.length === 0) return;
    
    // Handle tab clicks
    paymentMethodTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            paymentMethodTabs.forEach(t => {
                t.classList.remove('tab-active');
            });
            
            // Add active class to clicked tab
            this.classList.add('tab-active');
            
            // Show the corresponding form
            const paymentMethod = this.dataset.paymentMethod;
            document.querySelectorAll('.payment-method-form').forEach(form => {
                form.classList.add('hidden');
            });
            
            const form = document.getElementById(`${paymentMethod}-form`);
            if (form) {
                form.classList.remove('hidden');
            }
        });
    });
}

/**
 * Get CSRF token from cookies
 * 
 * @param {string} name - The name of the cookie
 * @returns {string} The cookie value
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
