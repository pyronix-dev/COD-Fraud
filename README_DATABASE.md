# Worldwide E-Commerce Fraud Dataset - Database Documentation

## Dataset Overview

File: data.csv
Rows: 3,000 transactions
Columns: 40
Fraud Rate: 28.8%
Countries: 50
Date Range: Jan 2024 - Dec 2025

## Column Reference

### Identifiers

**transaction_id** (string)
Unique transaction ID (format: TXN + 12 hex chars)

**user_id** (string)
Unique user ID (format: USR + 10 hex chars)

### Time

**timestamp_utc** (datetime)
Transaction time in UTC (ISO 8601 format)

### Financial

**amount** (float)
Transaction amount in local currency

**currency** (string)
3-letter currency code (USD, EUR, INR, CNY, BRL, etc.)

**avg_item_price** (float)
Average price per item (amount divided by items_count)

### Location

**country** (string)
2-letter country code (US, GB, DE, IN, NG, etc.)

**shipping_city** (string)
Delivery city

**billing_city** (string)
Billing address city

**shipping_billing_match** (int)
1 = cities match, 0 = mismatch

### Payment

**payment_method** (string)
Payment type (credit_card, debit_card, paypal, alipay, wechat_pay, upi, paytm, phonepe, pix, boleto, mpesa, bank_transfer, crypto, apple_pay, google_pay, klarna, afterpay, sofort, giropay, ideal, bancontact, gopay, grabpay, ovo, dana, shopeepay, venmo, amazon_pay, flutterwave, paystack, airtel_money, truemoney, mercadopago, pagseguro, jd_pay, eps, ussd, mobile_money, cod)

**card_present** (int)
1 = physical card present, 0 = card-not-present

**card_age_days** (int)
Age of card in days (1-3650)

### Device

**device_type** (string)
Device used (mobile, desktop, tablet)

**browser** (string)
Browser name (Chrome, Safari, Firefox, Edge, Opera, Brave, Samsung Internet, UC Browser, Yandex, DuckDuckGo)

**os_type** (string)
Operating system (Windows, macOS, iOS, Android, Linux, ChromeOS)

### Merchant

**merchant_category** (string)
Product category (25 categories: Electronics, Fashion, Home & Garden, Sports & Outdoors, Beauty & Health, Toys & Games, Books & Media, Automotive, Food & Beverages, Pet Supplies, Office Supplies, Jewelry, Baby Products, Musical Instruments, Art & Collectibles, Travel & Tickets, Digital Services, Software & Apps, Fitness Equipment, Outdoor Gear, Luxury Goods, Vintage Items, Wholesale Bulk, Subscription Box, Gift Cards)

**items_count** (int)
Number of items purchased (1-12)

### Network

**ip_address** (string)
IP address (IPv4 format)

**ip_risk_score** (float)
Risk score for IP (0-100)

### User History

**email** (string)
Full email address

**email_domain** (string)
Email domain only (gmail.com, yahoo.com, web.de, qq.com, tempmail.com, etc.)

**user_account_age_days** (int)
Account age in days (1-2000)

**user_prev_chargebacks** (int)
1 = has previous chargebacks, 0 = none

**user_is_high_risk** (int)
1 = flagged as high risk, 0 = normal

**transactions_last_24h** (int)
User's transactions in last 24 hours (0-18)

**transactions_last_1h** (int)
User's transactions in last 1 hour (0-10)

### Time Features

**local_hour** (int)
Hour of transaction in local time (0-23)

**odd_hour** (int)
1 = transaction between midnight-6am or 11pm-midnight, 0 = normal hours

### Fraud Labels (Target)

**is_fraud** (int)
TARGET VARIABLE: 1 = fraud, 0 = legitimate

**fraud_type** (string)
Type of fraud (stolen_card, friendly_fraud, account_takeover, triangulation, clean_fraud, merchant_fraud, promotion_abuse, return_fraud, chargeback_fraud, synthetic_identity, bot_attack, card_testing) or "none" for legitimate transactions

### Text Fields (NLP)

**transaction_notes** (string)
Customer's order notes/instructions (contains typos, code-switching, and noise in fraud cases)

**support_chat** (string, JSON format)
Multi-turn support conversation between user and agent

**merchant_description** (string)
Merchant's product/store description

**product_review** (string)
Customer's product review

**dispute_reason** (string)
Reason for dispute/chargeback (empty if no dispute)

### Text Statistics (Pre-computed)

**note_word_count** (int)
Number of words in transaction_notes

**note_uppercase_ratio** (float)
Ratio of uppercase letters in transaction_notes (0.0-1.0)

**note_exclamation_count** (int)
Number of exclamation marks in transaction_notes

**chat_turn_count** (int)
Number of messages in support_chat

## Class Distribution

Legitimate (is_fraud = 0): 2,137 rows (71.2%)
Fraud (is_fraud = 1): 863 rows (28.8%)

## Fraud Type Distribution

promotion_abuse: 91
account_takeover: 86
chargeback_fraud: 81
clean_fraud: 76
return_fraud: 73
triangulation: 72
synthetic_identity: 71
bot_attack: 69
merchant_fraud: 66
friendly_fraud: 66
card_testing: 59
stolen_card: 53
none: 2,137 (legitimate transactions)

## Data Types

String columns (20):
transaction_id, user_id, timestamp_utc, currency, country, payment_method, browser, os_type, merchant_category, shipping_city, billing_city, ip_address, email, email_domain, fraud_type, transaction_notes, support_chat, merchant_description, product_review, dispute_reason

Float columns (4):
amount, avg_item_price, ip_risk_score, note_uppercase_ratio

Int columns (16):
items_count, shipping_billing_match, card_present, card_age_days, user_account_age_days, user_prev_chargebacks, user_is_high_risk, transactions_last_24h, transactions_last_1h, local_hour, odd_hour, is_fraud, note_word_count, note_exclamation_count, chat_turn_count

## Missing Values

dispute_reason: ~92% missing (only populated for fraud cases and some legitimate disputes)
All other columns: 0% missing

## Quick Start (Python)

```python
import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Check shape
print(df.shape)  # (3000, 40)

# Check target distribution
print(df['is_fraud'].value_counts())

# View first rows
print(df.head())

# Check for missing values
print(df.isnull().sum())
```
