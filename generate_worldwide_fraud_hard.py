#!/usr/bin/env python3
"""
Worldwide E-Commerce Fraud Dataset - Hard/Noisy Version
3,000 highly diverse, adversarial samples designed to break ML models.

Features:
- Massive template variation (1000+ unique patterns)
- Heavy noise injection (typos, code-switching, randomization)
- Adversarial fraud (writes like legit users)
- Dynamic text generation (not just templates)
- High fraud rate (~30%) for better balance
"""

import pandas as pd
import numpy as np
import json
import random
from datetime import datetime, timedelta
import uuid
import re

np.random.seed(42)
random.seed(42)

# ============== MASSIVE TEMPLATE POOLS ==============
# 100+ variations per category to avoid repetition

FRAUD_NOTES_URGENT = [
    "URGENT need this delivered ASAP please expedite immediately",
    "Time sensitive delivery cannot be delayed under any circumstances",
    "Rush order please process right away deadline approaching fast",
    "Express shipping required must arrive by tomorrow no exceptions",
    "Priority handling needed this is extremely time critical",
    "Fast track this order please every hour counts here",
    "Need immediate processing cannot wait for standard shipping",
    "Expedite please this is for emergency situation",
    "Urgent delivery required please skip standard processing",
    "ASAP delivery needed deadline is extremely tight",
    "Please prioritize this order time is running out",
    "Critical delivery timeline must meet deadline",
    "Rush processing needed urgently please help",
    "Time critical shipment cannot afford delays",
    "Emergency order need fastest shipping available",
    "Urgent please process immediately no delays",
    "Fast delivery needed this cannot wait",
    "Priority order please handle with care urgently",
    "Need this urgently please expedite shipping",
    "Time sensitive please process right now",
    "Urgent request please deliver as soon as possible",
    "Critical timeline must arrive on time",
    "Expedited processing needed urgently please",
    "Rush this order please time is critical",
    "Need immediate attention to this delivery",
    "Please hurry with this order urgently needed",
    "Fast shipping required cannot wait long",
    "Urgent matter please process without delay",
    "Priority shipping needed time is essential",
    "Need this fast please expedite immediately",
]

FRAUD_NOTES_GIFT = [
    "This is a surprise gift do not include any pricing information",
    "Gift for family member please keep price details out of package",
    "Birthday present do not show receipt with prices visible",
    "Anniversary gift please do not include invoice in box",
    "Surprise for spouse hide all pricing and order details",
    "Gift order please no marketing materials or price tags",
    "Present for friend do not reveal cost in packaging",
    "Special occasion gift keep pricing confidential please",
    "Birthday surprise no receipts or price info in package",
    "Gift for parents do not show what I paid",
    "Surprise order please hide all cost information",
    "Present do not include bill with prices shown",
    "Gift wrapping needed hide price from recipient",
    "Do not include invoice this is a secret gift",
    "Keep pricing hidden this is for someone else",
    "Surprise delivery no order details with cost",
    "Gift please no paperwork showing price",
    "Hide cost information this is a present",
    "No receipt in package this is a gift order",
    "Confidential pricing do not show in delivery",
]

FRAUD_NOTES_BUSINESS = [
    "Corporate bulk order need proper invoice for accounting immediately",
    "Business purchase require detailed receipt with tax breakdown",
    "Office supplies for company need invoice ASAP for reimbursement",
    "Commercial order must have proper documentation for accounts",
    "Company purchase need itemized bill urgently for finance team",
    "Business expense require full invoice details immediately",
    "Corporate account need receipt with company details on it",
    "Office order must include proper invoice for bookkeeping",
    "Business transaction need detailed receipt for tax purposes",
    "Company order require invoice with GST details urgently",
    "Commercial purchase need billing documents right away",
    "Corporate buying need proper paperwork for accounts department",
    "Business order must have invoice for expense claims",
    "Office purchase require receipt with all item details",
    "Company transaction need invoice copy urgently please",
    "Bulk business order need proper billing immediately",
    "Corporate expense need receipt for finance approval",
    "Business account require invoice with PO number",
    "Commercial transaction need documentation ASAP",
    "Office order must include receipt for records",
]

FRAUD_NOTES_ADDRESS = [
    "Please deliver to different address than billing address",
    "Shipping location is not same as card billing location",
    "Send to alternate address not the one on card",
    "Delivery address differs from billing use this one instead",
    "Please ship to work address not home billing address",
    "Use shipping address provided not the billing one",
    "Different delivery location than card registration address",
    "Ship to office address billing is at home",
    "Send to new address not the old billing address",
    "Delivery at different location than payment address",
    "Please use this shipping address not billing",
    "Alternate delivery address not matching card",
    "Ship to current address billing is old one",
    "Send to this address not the registered one",
    "Different location for delivery than billing",
    "Use shipping address billing is different",
    "Deliver here not at billing address please",
    "Ship to work not home billing address",
    "New address for shipping not old billing",
    "Alternate location for delivery not billing",
]

FRAUD_NOTES_CODESWITCH = [
    "Yaar please jaldi deliver karna hai bahut zaroori hai",
    "Habibi this is very important for me okay please help",
    "Inshaallah delivery will be smooth brother thank you",
    "Mashallah great deal I am buying now please send fast",
    "Wallahi I need this urgently please understand my situation",
    "Yalla hurry up please I am waiting for long time",
    "Bhai please help me this time only I promise",
    "Mere jaan please do this for me I really need",
    "Salamat dost please expedite this order for me",
    "Shukran habibi please make this happen today",
    "Yaar urgent hai please samjho meri baat ko",
    "Dost please help karo ye urgent kaam hai",
    "Habibi yalla please make fast delivery for me",
    "Bhai log please expedite karna mat bhoolna",
    "Yaar time kam hai please jaldi se bhejo",
    "Mashallah please bhai help me out with this",
    "Inshaallah sab theek hoga please deliver fast",
    "Wallahi bahut zaroori hai please samjho",
    "Yalla habibi please make this work today",
    "Shukran yaar I really appreciate your help",
]

FRAUD_NOTES_ADVERSARIAL = [
    "Standard delivery is perfectly fine with me thank you",
    "No rush on this order I can wait for regular shipping",
    "Just normal purchase nothing urgent or special here",
    "Regular customer here been ordering for quite some time",
    "This is my usual monthly order same as always",
    "Happy with standard service no changes needed",
    "Normal delivery timeline works great for me thanks",
    "Been buying from here for years very satisfied",
    "Regular purchase as usual nothing different today",
    "Standard shipping is perfect I am not in hurry",
    "Loyal customer here continue great service please",
    "My typical order pattern same as previous times",
    "No special requests just process normally thanks",
    "Regular buyer here everything is fine as is",
    "Standard process works for me no issues at all",
    "Been a customer long time very happy always",
    "Normal order nothing unusual or different here",
    "Regular shipping timeline is completely acceptable",
    "Satisfied customer repeat purchase as expected",
    "Typical order for me process as usual please",
]

LEGIT_NOTES = [
    "Standard delivery is fine thank you very much",
    "Please leave at door if I am not home",
    "Regular monthly purchase nothing special",
    "Nothing special just a normal everyday order",
    "Gift wrap if available otherwise totally okay",
    "Preferred delivery time is evening after 5pm",
    "Please call before delivery if possible",
    "Leave with building security if not home",
    "No rush at all deliver anytime this week",
    "Thanks for the great service as always",
    "Been buying here for years very happy",
    "Good prices will definitely recommend to friends",
    "Quality is important to me thank you",
    "Hope this arrives in good condition please",
    "First time trying this product excited",
    "Normal order process everything is fine",
    "Regular customer here keep up good work",
    "Standard shipping works perfectly for me",
    "No special instructions just deliver normally",
    "Appreciate the service thank you team",
    "Please handle with care fragile items inside",
    "Delivery anytime during weekdays is fine",
    "Weekend delivery preferred if possible",
    "Morning delivery would be great thanks",
    "Afternoon slot works best for my schedule",
    "Evening delivery is most convenient for me",
    "Please ring doorbell I will be home",
    "Do not ring doorbell baby is sleeping",
    "Leave at front porch if not answering",
    "Hand delivery preferred if possible please",
    "Contactless delivery is perfectly fine",
    "Signature required please do not leave",
    "Safe place delivery is acceptable thanks",
    "Please confirm before delivery call me",
    "Text message before arrival would help",
    "Normal packaging is absolutely fine",
    "Extra packaging appreciated if possible",
    "Eco friendly packaging option if available",
    "Gift packaging needed please wrap nicely",
    "No gift wrap needed just plain packaging",
    "Combine with my other orders if possible",
    "Separate shipment is fine no problem",
    "Partial delivery acceptable if items unavailable",
    "Wait for all items no partial shipment",
    "Standard return policy is understood",
    "Extended warranty option if available",
    "Installation service needed please advise",
    "Assembly required or comes pre assembled",
    "Product manual in English please",
    "Color may vary from picture understood",
    "Size chart was helpful thank you",
    "Fits as expected based on reviews",
    "Material quality looks good in photos",
    "Hope durability matches the price point",
    "Brand reputation influenced my purchase",
    "Reviews convinced me to buy this one",
    "Comparing with similar products before",
    "Best price I found after searching",
    "Discount code applied successfully thanks",
    "Loyalty points used for this purchase",
    "Cashback offer was the deciding factor",
    "Free shipping sealed the deal for me",
    "Return window is adequate for testing",
    "Exchange policy is clear and fair",
    "Customer service was helpful earlier",
    "Previous experience was positive overall",
    "Recommending to family and friends",
    "Will write review after using product",
    "Photos after unboxing will share",
    "Video review coming soon on my channel",
    "Social media tag when I post about this",
    "Influencer discount code used thanks",
    "Bulk order for my small business",
    "Reselling these items online later",
    "Dropshipping arrangement if possible",
    "Wholesale pricing for future orders",
    "Corporate gifting for employees soon",
    "Event supplies for upcoming function",
    "Seasonal purchase for holiday celebration",
    "Birthday party items needed urgently",
    "Wedding related purchase for ceremony",
    "Festival shopping for family gathering",
    "Back to school supplies for kids",
    "Home renovation project materials",
    "DIY project supplies for weekend",
    "Hobby related purchase for personal use",
    "Sports equipment for regular training",
    "Fitness gear for home gym setup",
    "Outdoor adventure gear for trip",
    "Travel accessories for upcoming vacation",
    "Work from home setup improvements",
    "Study materials for online course",
    "Art supplies for creative projects",
    "Music equipment for practice sessions",
    "Gaming accessories for setup upgrade",
    "Tech gadgets for productivity boost",
    "Kitchen appliances for cooking experiments",
    "Garden tools for weekend landscaping",
    "Pet supplies for my furry friend",
    "Baby items for expecting family member",
    "Elderly care products for parents",
    "Health supplements for wellness routine",
    "Beauty products for self care regimen",
    "Fashion items for wardrobe refresh",
    "Jewelry as personal treat milestone",
    "Watch collection addition for special date",
    "Shoes for specific occasion coming",
    "Bags for work and travel needs",
    "Accessories to complete the outfit",
    "Home decor for room makeover project",
    "Furniture for new apartment setup",
    "Appliances for kitchen upgrade soon",
    "Electronics for entertainment system",
    "Books for personal library expansion",
    "Games for family game nights",
    "Toys for children birthday gifts",
    "Craft supplies for hobby projects",
    "Stationery for bullet journal hobby",
    "Plants for indoor garden collection",
    "Tools for home improvement projects",
    "Car accessories for road trip prep",
    "Bike gear for cycling hobby",
    "Camping equipment for outdoor trips",
    "Beach gear for summer vacation",
    "Winter clothing for ski trip",
    "Swimming gear for pool activities",
    "Yoga equipment for daily practice",
    "Meditation supplies for mindfulness",
    "Cooking ingredients for recipe testing",
    "Baking supplies for weekend projects",
    "Coffee equipment for home barista",
    "Tea collection for tasting sessions",
    "Wine accessories for dinner parties",
    "Entertainment for hosting guests",
    "Party supplies for celebration event",
    "Decoration items for special occasion",
    "Photography equipment for hobby",
    "Video equipment for content creation",
    "Streaming setup for online presence",
    "Podcast equipment for new show",
    "Writing supplies for book project",
    "Language learning materials for study",
    "Professional development resources",
    "Certification exam preparation materials",
    "Career transition related purchase",
    "Side hustle supplies for business",
    "Investment in personal growth",
    "Self improvement related items",
    "Wellness journey supporting products",
    "Sustainability focused purchase choice",
    "Ethical brand selection intentional",
    "Local business support intentional",
    "Small business encouragement purchase",
    "Handmade item appreciation purchase",
    "Vintage find for collection addition",
    "Limited edition for collector value",
    "Exclusive release for early access",
    "Pre-order for anticipated product",
    "Restock purchase for favorite item",
    "Replacement for broken item",
    "Upgrade from old version",
    "Complement to existing purchase",
    "Accessory for main product",
    "Spare for backup purposes",
    "Gift card for flexible choosing",
    "Subscription for ongoing convenience",
    "Membership for exclusive benefits",
    "Premium tier for additional features",
    "Trial purchase before commitment",
    "Sample size for testing first",
    "Full size after positive trial",
    "Bundle deal for better value",
    "Multi-pack for cost savings",
    "Refill for sustainable choice",
    "Reusable alternative for eco reasons",
    "Zero waste option for environment",
    "Organic choice for health reasons",
    "Natural ingredients for safety",
    "Cruelty-free for ethical reasons",
    "Vegan option for lifestyle choice",
    "Halal certified for religious needs",
    "Kosher option for dietary requirements",
    "Gluten-free for health necessity",
    "Allergen-free for safety concerns",
    "Hypoallergenic for sensitive skin",
    "Dermatologist tested for confidence",
    "Clinically proven for effectiveness",
    "Scientifically backed for trust",
    "Research-based for credibility",
    "Expert recommended for assurance",
    "Professional grade for quality",
    "Commercial use for business needs",
    "Industrial strength for durability",
    "Heavy duty for long-term use",
    "Lightweight for portability needs",
    "Compact for space constraints",
    "Portable for travel convenience",
    "Foldable for storage efficiency",
    "Modular for customization options",
    "Adjustable for flexibility needs",
    "Multi-function for versatility",
    "All-in-one for convenience",
    "Standalone for simplicity",
    "Integrated for seamless experience",
    "Compatible with existing setup",
    "Universal fit for broad use",
    "Specific model for exact match",
    "Custom fit for precision needs",
    "Made-to-order for personalization",
    "Personalized for uniqueness",
    "Engraved for sentimental value",
    "Monogrammed for elegance touch",
    "Customized for specific requirements",
    "Tailored for exact specifications",
    "Bespoke for luxury experience",
    "Artisan crafted for quality",
    "Hand-finished for attention detail",
    "Machine-made for consistency",
    "Mass-produced for affordability",
    "Limited-run for exclusivity",
    "Seasonal for timely relevance",
    "Holiday-themed for celebration",
    "Anniversary edition for milestone",
    "Commemorative for memory keeping",
    "Collectible for investment value",
    "Rare find for uniqueness",
    "One-of-a-kind for specialness",
    "Unique piece for individuality",
    "Statement item for expression",
    "Conversation starter for social",
    "Trending item for relevance",
    "Classic choice for timelessness",
    "Timeless design for longevity",
    "Modern style for contemporary",
    "Traditional look for heritage",
    "Minimalist aesthetic for simplicity",
    "Maximalist design for boldness",
    "Colorful option for vibrancy",
    "Neutral tone for versatility",
    "Bold pattern for attention",
    "Subtle design for understatement",
    "Textured finish for tactile appeal",
    "Smooth surface for easy cleaning",
    "Matte finish for sophistication",
    "Glossy look for shine",
    "Metallic accent for luxury",
    "Natural finish for authenticity",
    "Distressed look for character",
    "Pristine condition for perfection",
    "Refurbished for value conscious",
    "Open-box for deal hunting",
    "Clearance for bargain finding",
    "Sale purchase for savings",
    "Flash deal for urgency",
    "Lightning offer for quick decision",
    "Daily deal for routine shopping",
    "Weekly special for planned purchase",
    "Monthly promotion for timing",
    "Seasonal sale for opportunistic",
    "Year-end clearance for timing",
    "New year deal for fresh start",
    "Spring collection for renewal",
    "Summer essentials for season",
    "Fall favorites for transition",
    "Winter must-haves for preparation",
]

# ============== GLOBAL CONFIGURATIONS ==============
COUNTRIES = {
    'US': {'currency': 'USD', 'lang': 'en', 'weight': 20, 'fraud_rate': 0.25},
    'GB': {'currency': 'GBP', 'lang': 'en', 'weight': 10, 'fraud_rate': 0.28},
    'DE': {'currency': 'EUR', 'lang': 'de', 'weight': 8, 'fraud_rate': 0.22},
    'FR': {'currency': 'EUR', 'lang': 'fr', 'weight': 7, 'fraud_rate': 0.25},
    'IN': {'currency': 'INR', 'lang': 'hi', 'weight': 10, 'fraud_rate': 0.35},
    'CN': {'currency': 'CNY', 'lang': 'zh', 'weight': 8, 'fraud_rate': 0.30},
    'BR': {'currency': 'BRL', 'lang': 'pt', 'weight': 6, 'fraud_rate': 0.38},
    'NG': {'currency': 'NGN', 'lang': 'en', 'weight': 5, 'fraud_rate': 0.42},
    'RU': {'currency': 'RUB', 'lang': 'ru', 'weight': 5, 'fraud_rate': 0.33},
    'JP': {'currency': 'JPY', 'lang': 'ja', 'weight': 4, 'fraud_rate': 0.18},
    'MX': {'currency': 'MXN', 'lang': 'es', 'weight': 4, 'fraud_rate': 0.35},
    'ID': {'currency': 'IDR', 'lang': 'id', 'weight': 3, 'fraud_rate': 0.30},
    'TR': {'currency': 'TRY', 'lang': 'tr', 'weight': 3, 'fraud_rate': 0.32},
    'SA': {'currency': 'SAR', 'lang': 'ar', 'weight': 3, 'fraud_rate': 0.28},
    'ZA': {'currency': 'ZAR', 'lang': 'en', 'weight': 2, 'fraud_rate': 0.36},
    'KR': {'currency': 'KRW', 'lang': 'ko', 'weight': 4, 'fraud_rate': 0.20},
    'IT': {'currency': 'EUR', 'lang': 'it', 'weight': 4, 'fraud_rate': 0.26},
    'ES': {'currency': 'EUR', 'lang': 'es', 'weight': 4, 'fraud_rate': 0.26},
    'CA': {'currency': 'CAD', 'lang': 'en', 'weight': 5, 'fraud_rate': 0.22},
    'AU': {'currency': 'AUD', 'lang': 'en', 'weight': 4, 'fraud_rate': 0.24},
    'PH': {'currency': 'PHP', 'lang': 'en', 'weight': 2, 'fraud_rate': 0.33},
    'VN': {'currency': 'VND', 'lang': 'vi', 'weight': 2, 'fraud_rate': 0.30},
    'TH': {'currency': 'THB', 'lang': 'th', 'weight': 2, 'fraud_rate': 0.28},
    'MY': {'currency': 'MYR', 'lang': 'en', 'weight': 2, 'fraud_rate': 0.30},
    'SG': {'currency': 'SGD', 'lang': 'en', 'weight': 2, 'fraud_rate': 0.18},
    'AE': {'currency': 'AED', 'lang': 'ar', 'weight': 2, 'fraud_rate': 0.26},
    'EG': {'currency': 'EGP', 'lang': 'ar', 'weight': 2, 'fraud_rate': 0.34},
    'KE': {'currency': 'KES', 'lang': 'en', 'weight': 2, 'fraud_rate': 0.38},
    'PK': {'currency': 'PKR', 'lang': 'ur', 'weight': 2, 'fraud_rate': 0.35},
    'BD': {'currency': 'BDT', 'lang': 'bn', 'weight': 2, 'fraud_rate': 0.36},
    'UA': {'currency': 'UAH', 'lang': 'uk', 'weight': 2, 'fraud_rate': 0.40},
    'PL': {'currency': 'PLN', 'lang': 'pl', 'weight': 2, 'fraud_rate': 0.26},
    'AR': {'currency': 'ARS', 'lang': 'es', 'weight': 2, 'fraud_rate': 0.36},
    'CL': {'currency': 'CLP', 'lang': 'es', 'weight': 1, 'fraud_rate': 0.30},
    'CO': {'currency': 'COP', 'lang': 'es', 'weight': 2, 'fraud_rate': 0.34},
    'IL': {'currency': 'ILS', 'lang': 'he', 'weight': 1, 'fraud_rate': 0.24},
    'GR': {'currency': 'EUR', 'lang': 'el', 'weight': 1, 'fraud_rate': 0.28},
    'PT': {'currency': 'EUR', 'lang': 'pt', 'weight': 1, 'fraud_rate': 0.24},
    'CZ': {'currency': 'CZK', 'lang': 'cs', 'weight': 1, 'fraud_rate': 0.24},
    'RO': {'currency': 'RON', 'lang': 'ro', 'weight': 1, 'fraud_rate': 0.32},
    'HU': {'currency': 'HUF', 'lang': 'hu', 'weight': 1, 'fraud_rate': 0.26},
    'NZ': {'currency': 'NZD', 'lang': 'en', 'weight': 1, 'fraud_rate': 0.22},
    'IE': {'currency': 'EUR', 'lang': 'en', 'weight': 1, 'fraud_rate': 0.22},
    'SE': {'currency': 'SEK', 'lang': 'sv', 'weight': 2, 'fraud_rate': 0.20},
    'NO': {'currency': 'NOK', 'lang': 'no', 'weight': 1, 'fraud_rate': 0.18},
    'DK': {'currency': 'DKK', 'lang': 'da', 'weight': 1, 'fraud_rate': 0.18},
    'FI': {'currency': 'EUR', 'lang': 'fi', 'weight': 1, 'fraud_rate': 0.18},
    'NL': {'currency': 'EUR', 'lang': 'nl', 'weight': 2, 'fraud_rate': 0.22},
    'BE': {'currency': 'EUR', 'lang': 'nl', 'weight': 1, 'fraud_rate': 0.22},
    'AT': {'currency': 'EUR', 'lang': 'de', 'weight': 1, 'fraud_rate': 0.20},
}

CITIES = {
    'US': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'Seattle', 'Denver', 'Boston', 'Portland', 'Las Vegas'],
    'GB': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Liverpool', 'Newcastle', 'Sheffield', 'Bristol', 'Edinburgh', 'Leicester', 'Nottingham', 'Brighton', 'Cardiff', 'Belfast'],
    'DE': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne', 'Stuttgart', 'Dusseldorf', 'Leipzig', 'Dortmund', 'Essen', 'Dresden', 'Hanover', 'Nuremberg', 'Bremen', 'Bonn'],
    'FR': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille', 'Rennes', 'Grenoble', 'Toulon', 'Saint-Etienne', 'Dijon'],
    'IN': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane'],
    'CN': ['Shanghai', 'Beijing', 'Guangzhou', 'Shenzhen', 'Chengdu', 'Hangzhou', 'Wuhan', 'Xian', 'Suzhou', 'Zhengzhou', 'Nanjing', 'Tianjin', 'Shenyang', 'Harbin', 'Qingdao'],
    'BR': ['Sao Paulo', 'Rio de Janeiro', 'Brasilia', 'Salvador', 'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre', 'Goiania', 'Belem', 'Guarulhos', 'Campinas', 'Sao Luis'],
    'NG': ['Lagos', 'Abuja', 'Kano', 'Ibadan', 'Port Harcourt', 'Benin City', 'Kaduna', 'Maiduguri', 'Zaria', 'Aba', 'Jos', 'Ilorin', 'Oyo', 'Enugu', 'Abeokuta'],
    'RU': ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan', 'Nizhny Novgorod', 'Chelyabinsk', 'Samara', 'Omsk', 'Rostov', 'Ufa', 'Krasnoyarsk', 'Voronezh', 'Perm', 'Volgograd'],
    'JP': ['Tokyo', 'Osaka', 'Yokohama', 'Nagoya', 'Sapporo', 'Fukuoka', 'Kobe', 'Kyoto', 'Kawasaki', 'Saitama', 'Hiroshima', 'Sendai', 'Kitakyushu', 'Chiba', 'Sakai'],
    'MX': ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana', 'Leon', 'Juarez', 'Zapopan', 'Merida', 'San Luis Potosi', 'Aguascalientes', 'Hermosillo', 'Saltillo', 'Mexicali', 'Culiacan'],
    'ID': ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang', 'Makassar', 'Palembang', 'Tangerang', 'Depok', 'Batam', 'Bogor', 'Pekanbaru', 'Bandar Lampung', 'Padang', 'Malang'],
    'TR': ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya', 'Adana', 'Konya', 'Gaziantep', 'Mersin', 'Diyarbakir', 'Kayseri', 'Eskisehir', 'Urfa', 'Samsun', 'Denizli'],
    'SA': ['Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Dammam', 'Khobar', 'Tabuk', 'Buraydah', 'Khamis Mushait', 'Hail', 'Najran', 'Jubail', 'Yanbu', 'Abha', 'Taif'],
    'ZA': ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth', 'Bloemfontein', 'East London', 'Pietermaritzburg', 'Benoni', 'Vereeniging', 'Kimberley', 'Polokwane', 'Nelspruit', 'Rustenburg', 'Soweto'],
    'KR': ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon', 'Gwangju', 'Suwon', 'Ulsan', 'Changwon', 'Goyang', 'Yongin', 'Seongnam', 'Bucheon', 'Cheongju', 'Jeonju'],
    'IT': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Bari', 'Catania', 'Venice', 'Verona', 'Messina', 'Padua', 'Trieste'],
    'ES': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza', 'Malaga', 'Murcia', 'Palma', 'Las Palmas', 'Bilbao', 'Alicante', 'Cordoba', 'Valladolid', 'Vigo', 'Gijon'],
    'CA': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City', 'Hamilton', 'Kitchener', 'London', 'Victoria', 'Halifax', 'Oshawa', 'Windsor'],
    'AU': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Newcastle', 'Canberra', 'Sunshine Coast', 'Wollongong', 'Hobart', 'Geelong', 'Townsville', 'Cairns', 'Darwin'],
    'PH': ['Manila', 'Quezon City', 'Davao', 'Caloocan', 'Cebu City', 'Zamboanga', 'Taguig', 'Antipolo', 'Pasig', 'Cagayan de Oro', 'Paranaque', 'Dasmarinas', 'Valenzuela', 'Bacoor', 'General Santos'],
    'VN': ['Ho Chi Minh City', 'Hanoi', 'Da Nang', 'Bien Hoa', 'Hue', 'Nha Trang', 'Can Tho', 'Rach Gia', 'Qui Nhon', 'Vung Tau', 'Nam Dinh', 'Phan Thiet', 'Long Xuyen', 'Thai Nguyen', 'Thanh Hoa'],
    'TH': ['Bangkok', 'Nonthaburi', 'Pak Kret', 'Hat Yai', 'Chiang Mai', 'Phuket', 'Pattaya', 'Udon Thani', 'Nakhon Ratchasima', 'Khon Kaen', 'Surat Thani', 'Ubon Ratchathani', 'Nakhon Si Thammarat', 'Chon Buri', 'Rayong'],
    'MY': ['Kuala Lumpur', 'George Town', 'Ipoh', 'Shah Alam', 'Petaling Jaya', 'Johor Bahru', 'Malacca City', 'Kota Kinabalu', 'Kuching', 'Seremban', 'Kuantan', 'Taiping', 'Alor Setar', 'Miri', 'Tawau'],
    'SG': ['Singapore'],
    'AE': ['Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Ajman', 'Ras Al Khaimah', 'Fujairah', 'Umm Al Quwain', 'Khor Fakkan', 'Dibba Al-Fujairah'],
    'EG': ['Cairo', 'Alexandria', 'Giza', 'Shubra El Kheima', 'Port Said', 'Suez', 'Luxor', 'Mansoura', 'El Mahalla El Kubra', 'Tanta', 'Asyut', 'Ismailia', 'Faiyum', 'Zagazig', 'Aswan'],
    'KE': ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Ruiru', 'Kikuyu', 'Kangundo-Tala', 'Malindi', 'Thika', 'Kitui', 'Machakos', 'Karuri', 'Nyeri', 'Meru'],
    'PK': ['Karachi', 'Lahore', 'Faisalabad', 'Rawalpindi', 'Multan', 'Gujranwala', 'Hyderabad', 'Peshawar', 'Islamabad', 'Quetta', 'Bahawalpur', 'Sargodha', 'Sialkot', 'Sukkur', 'Larkana'],
    'BD': ['Dhaka', 'Chittagong', 'Khulna', 'Rajshahi', 'Sylhet', 'Rangpur', 'Barisal', 'Comilla', 'Mymensingh', 'Narayanganj', 'Gazipur', 'Tongi', 'Jessore', 'Coxs Bazar', 'Bogra'],
    'UA': ['Kyiv', 'Kharkiv', 'Odessa', 'Dnipro', 'Donetsk', 'Zaporizhzhia', 'Lviv', 'Kryvyi Rih', 'Mykolaiv', 'Mariupol', 'Luhansk', 'Vinnytsia', 'Simferopol', 'Kherson', 'Poltava'],
    'PL': ['Warsaw', 'Krakow', 'Lodz', 'Wroclaw', 'Poznan', 'Gdansk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Katowice', 'Bialystok', 'Gdynia', 'Czestochowa', 'Radom', 'Sosnowiec'],
    'AR': ['Buenos Aires', 'Cordoba', 'Rosario', 'Mendoza', 'La Plata', 'San Miguel de Tucuman', 'Mar del Plata', 'Salta', 'Santa Fe', 'San Juan', 'Resistencia', 'Neuquen', 'Santiago del Estero', 'Corrientes', 'Bahia Blanca'],
    'CL': ['Santiago', 'Valparaiso', 'Concepcion', 'La Serena', 'Antofagasta', 'Temuco', 'Rancagua', 'Talca', 'Arica', 'Chillan', 'Iquique', 'Los Angeles', 'Puerto Montt', 'Calama', 'Coquimbo'],
    'CO': ['Bogota', 'Medellin', 'Cali', 'Barranquilla', 'Cartagena', 'Cucuta', 'Bucaramanga', 'Pereira', 'Santa Marta', 'Ibague', 'Pasto', 'Manizales', 'Neiva', 'Soledad', 'Armenia'],
    'IL': ['Jerusalem', 'Tel Aviv', 'Haifa', 'Rishon LeZion', 'Petah Tikva', 'Ashdod', 'Netanya', 'Beersheba', 'Holon', 'Bnei Brak', 'Ramat Gan', 'Ashkelon', 'Rehovot', 'Bat Yam', 'Beit Shemesh'],
    'GR': ['Athens', 'Thessaloniki', 'Patras', 'Heraklion', 'Larissa', 'Volos', 'Rhodes', 'Ioannina', 'Chania', 'Chalcis', 'Agrinio', 'Kalamata', 'Kavala', 'Katerini', 'Trikala'],
    'PT': ['Lisbon', 'Porto', 'Amadora', 'Braga', 'Setubal', 'Coimbra', 'Queluz', 'Funchal', 'Cacem', 'Vila Nova de Gaia', 'Loures', 'Evora', 'Rio de Mouro', 'Odivelas', 'Aveiro'],
    'CZ': ['Prague', 'Brno', 'Ostrava', 'Plzen', 'Liberec', 'Olomouc', 'Ceske Budejovice', 'Hradec Kralove', 'Usti nad Labem', 'Pardubice', 'Zlin', 'Kladno', 'Most', 'Opava', 'Frydek-Mistek'],
    'RO': ['Bucharest', 'Cluj-Napoca', 'Timisoara', 'Iasi', 'Constanta', 'Craiova', 'Brasov', 'Galati', 'Ploiesti', 'Oradea', 'Braila', 'Arad', 'Pitesti', 'Sibiu', 'Bacau'],
    'HU': ['Budapest', 'Debrecen', 'Szeged', 'Miskolc', 'Pecs', 'Gyor', 'Nyiregyhaza', 'Kecskemet', 'Szekesfehervar', 'Szombathely', 'Sopron', 'Eger', 'Tatabanya', 'Kaposvar', 'Veszprem'],
    'NZ': ['Auckland', 'Wellington', 'Christchurch', 'Hamilton', 'Tauranga', 'Napier-Hastings', 'Dunedin', 'Palmerston North', 'Nelson', 'Rotorua', 'New Plymouth', 'Whangarei', 'Invercargill', 'Whanganui', 'Gisborne'],
    'IE': ['Dublin', 'Cork', 'Limerick', 'Galway', 'Waterford', 'Drogheda', 'Dundalk', 'Swords', 'Bray', 'Navan', 'Ennis', 'Kilkenny', 'Carlow', 'Tralee', 'Newbridge'],
    'SE': ['Stockholm', 'Gothenburg', 'Malmo', 'Uppsala', 'Vasteras', 'Orebro', 'Linkoping', 'Helsingborg', 'Jonkoping', 'Norrkoping', 'Lund', 'Umea', 'Gavle', 'Boras', 'Sodertalje'],
    'NO': ['Oslo', 'Bergen', 'Stavanger', 'Trondheim', 'Drammen', 'Fredrikstad', 'Kristiansand', 'Sandnes', 'Tromso', 'Sarpsborg', 'Skien', 'Alesund', 'Sandefjord', 'Haugesund', 'Tonsberg'],
    'DK': ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg', 'Esbjerg', 'Randers', 'Kolding', 'Horsens', 'Vejle', 'Roskilde', 'Herning', 'Silkeborg', 'Naestved', 'Fredericia', 'Viborg'],
    'FI': ['Helsinki', 'Espoo', 'Tampere', 'Vantaa', 'Oulu', 'Turku', 'Jyvaskyla', 'Lahti', 'Kuopio', 'Pori', 'Joensuu', 'Lappeenranta', 'Hameenlinna', 'Vaasa', 'Rovaniemi'],
    'NL': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 'Breda', 'Nijmegen', 'Enschede', 'Haarlem', 'Arnhem', 'Zaanstad', 'Amersfoort'],
    'BE': ['Brussels', 'Antwerp', 'Ghent', 'Charleroi', 'Liege', 'Bruges', 'Namur', 'Leuven', 'Mons', 'Mechelen', 'Aalst', 'La Louviere', 'Kortrijk', 'Ostend', 'Sint-Niklaas'],
    'AT': ['Vienna', 'Graz', 'Linz', 'Salzburg', 'Innsbruck', 'Klagenfurt', 'Villach', 'Wels', 'Sankt Polten', 'Dornbirn', 'Steyr', 'Wiener Neustadt', 'Feldkirch', 'Bregenz', 'Leonding'],
}

PAYMENT_METHODS = {
    'US': ['credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay', 'afterpay', 'klarna', 'venmo'],
    'EU': ['credit_card', 'debit_card', 'paypal', 'sofort', 'giropay', 'ideal', 'bancontact', 'klarna', 'eps'],
    'CN': ['alipay', 'wechat_pay', 'unionpay', 'credit_card', 'jd_pay'],
    'IN': ['upi', 'paytm', 'phonepe', 'credit_card', 'debit_card', 'cod', 'google_pay', 'amazon_pay'],
    'BR': ['boleto', 'pix', 'credit_card', 'debit_card', 'pagseguro'],
    'NG': ['bank_transfer', 'card', 'ussd', 'mobile_money', 'flutterwave', 'paystack'],
    'KE': ['mpesa', 'card', 'bank_transfer', 'airtel_money'],
    'SEA': ['grabpay', 'gopay', 'ovo', 'dana', 'shopeepay', 'truemoney'],
    'LATAM': ['oxxo', 'rapipago', 'pagofacil', 'efectivo', 'credit_card', 'mercadopago'],
    'global': ['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'crypto'],
}

MERCHANT_CATEGORIES = [
    'Electronics', 'Fashion', 'Home & Garden', 'Sports & Outdoors', 
    'Beauty & Health', 'Toys & Games', 'Books & Media', 'Automotive',
    'Food & Beverages', 'Pet Supplies', 'Office Supplies', 'Jewelry',
    'Baby Products', 'Musical Instruments', 'Art & Collectibles',
    'Travel & Tickets', 'Digital Services', 'Software & Apps',
    'Fitness Equipment', 'Outdoor Gear', 'Luxury Goods', 'Vintage Items',
    'Wholesale Bulk', 'Subscription Box', 'Gift Cards'
]

BROWSERS = ['Chrome', 'Safari', 'Firefox', 'Edge', 'Opera', 'Brave', 'Samsung Internet', 'UC Browser', 'Yandex', 'DuckDuckGo']
DEVICE_TYPES = ['mobile', 'desktop', 'tablet']
OS_TYPES = ['Windows', 'macOS', 'iOS', 'Android', 'Linux', 'ChromeOS']

FRAUD_TYPES = [
    'stolen_card', 'friendly_fraud', 'account_takeover', 'triangulation',
    'clean_fraud', 'merchant_fraud', 'promotion_abuse', 'return_fraud',
    'chargeback_fraud', 'synthetic_identity', 'bot_attack', 'card_testing'
]

# ============== NOISE INJECTION FUNCTIONS ==============
def inject_typos(text, intensity=0.15):
    """Inject realistic typos with varying intensity."""
    typo_map = {
        'the': ['teh', 'hte', 'th', 'teh'],
        'please': ['plz', 'pls', 'plese', 'pleaze'],
        'urgent': ['urgnt', 'urjent', 'urgant', 'rgent'],
        'delivery': ['dlivery', 'delivry', 'delivary', 'delyvery'],
        'thank': ['thnx', 'thakn', 'thanks', 'thnks'],
        'very': ['vry', 'veyr', 'vre', 'veery'],
        'need': ['ned', 'nead', 'nee', 'nede'],
        'want': ['wnt', 'wan', 'wnat', 'waht'],
        'have': ['hav', 'haev', 'hve', 'ahve'],
        'will': ['wil', 'wll', 'wiil', 'wull'],
        'can': ['cn', 'ca', 'cna', 'can'],
        'you': ['u', 'yo', 'yuo', 'oyu'],
        'for': ['fr', 'fo', 'forr', 'fopr'],
        'with': ['w/', 'wit', 'wiht', 'with'],
        'this': ['ths', 'tihs', 'this', 'htis'],
        'that': ['tht', 'taht', 'that', 'thhat'],
        'from': ['frm', 'form', 'from', 'fomr'],
        'are': ['r', 'ar', 'are', 'aer'],
        'not': ['nt', 'no', 'not', 'nott'],
        'but': ['bt', 'but', 'buit', 'but'],
        'what': ['wat', 'wht', 'what', 'waht'],
        'when': ['wen', 'whn', 'when', 'wneh'],
        'where': ['wer', 'whr', 'where', 'whee'],
        'which': ['wch', 'whcih', 'which', 'whihc'],
        'time': ['tm', 'tim', 'time', 'tiem'],
        'some': ['sm', 'som', 'some', 'smoe'],
        'would': ['wd', 'woudl', 'would', 'wouod'],
        'could': ['cd', 'coudl', 'could', 'coudl'],
        'should': ['sd', 'shoudl', 'should', 'shoudl'],
        'there': ['thr', 'ther', 'there', 'htere'],
        'their': ['thr', 'thier', 'their', 'hteir'],
        'they': ['thy', 'tehy', 'they', 'tey'],
        'them': ['tm', 'thm', 'them', 'tehm'],
        'then': ['tn', 'thn', 'then', 'hten'],
        'about': ['abt', 'aobut', 'about', 'baout'],
        'after': ['aft', 'aftr', 'after', 'afer'],
        'before': ['b4', 'befor', 'before', 'beofre'],
        'between': ['btn', 'betwen', 'between', 'beetween'],
        'because': ['bcuz', 'becuase', 'because', 'beacuse'],
        'through': ['thru', 'htrough', 'through', 'htrough'],
        'during': ['dur', 'druing', 'during', 'duirng'],
        'while': ['wl', 'whlie', 'while', 'wihle'],
        'against': ['agst', 'agaist', 'against', 'agianst'],
        'within': ['w/in', 'withing', 'within', 'wihtin'],
        'without': ['w/o', 'withou', 'without', 'wihtout'],
        'order': ['ord', 'ordr', 'order', 'oder'],
        'shipping': ['shp', 'shpping', 'shipping', 'shiping'],
        'product': ['prod', 'produkt', 'product', 'produc'],
        'price': ['$', 'pirce', 'price', 'pirce'],
        'item': ['itm', 'tiem', 'item', 'tiem'],
        'package': ['pkg', 'pakage', 'package', 'pakcage'],
        'address': ['addr', 'adress', 'address', 'addres'],
        'payment': ['pmt', 'paymnt', 'payment', 'paymet'],
        'card': ['cd', 'card', 'crad', 'card'],
        'email': ['eml', 'eamil', 'email', 'emial'],
        'phone': ['ph', 'phnoe', 'phone', 'phoen'],
        'name': ['nm', 'mae', 'name', 'nmae'],
        'number': ['num', 'nuber', 'number', 'numbr'],
        'date': ['dt', 'date', 'date', 'daet'],
        'time': ['tm', 'time', 'tiem', 'tim'],
    }
    
    words = text.split()
    result = []
    for word in words:
        if random.random() < intensity:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word in typo_map:
                typo = random.choice(typo_map[clean_word])
                # Preserve capitalization
                if word[0].isupper():
                    typo = typo.capitalize()
                result.append(typo)
            else:
                result.append(word)
        else:
            result.append(word)
    return ' '.join(result)

def inject_code_switching(text, lang='en', intensity=0.2):
    """Inject code-switching based on region."""
    fillers = {
        'en': ['yaar', 'habibi', 'inshaallah', 'wallahi', 'bhai', 'yalla', 'macha', 'khalas', 'salamat', 'shukran', 'dost', 'mere jaan', 'oye', 'arre'],
        'es': ['oye', 'vale', 'tío', 'hombre', 'mujer', 'por favor', 'gracias', 'rápido', 'urgente', 'ahora'],
        'fr': ['écoute', 'mec', 'mec', 'vite', 'maintenant', 's\'il te plaît', 'merci', 'urgent', 'rapide'],
        'de': ['hör mal', 'mann', 'schnell', 'jetzt', 'bitte', 'danke', 'dringend', 'eilig'],
        'hi': ['yaar', 'bhai', 'did', 'jaldi', 'abhi', 'please', 'thank you', 'urgent', 'zaroori'],
        'ar': ['habibi', 'yalla', 'inshaallah', 'wallahi', 'shukran', 'afwan', 'min fadlak', 'urgently'],
        'zh': ['朋友', '快点', '现在', '请', '谢谢', '紧急', '马上', '兄弟'],
        'ja': ['ねえ', '早く', '今', ' please', 'ありがとう', '緊急', 'すぐに', '兄弟'],
        'ko': ['야', '빨리', '지금', '제발', '감사', '긴급', '바로', '형'],
        'pt': ['cara', 'rápido', 'agora', 'por favor', 'obrigado', 'urgente', 'já', 'irmão'],
        'ru': ['слушай', 'быстро', 'сейчас', 'пожалуйста', 'спасибо', 'срочно', 'брат', 'друг'],
    }
    
    words = text.split()
    if random.random() < intensity and len(words) > 3:
        pos = random.randint(1, len(words) - 1)
        filler = random.choice(fillers.get(lang, fillers['en']))
        words.insert(pos, filler)
    return ' '.join(words)

def inject_punctuation_variation(text, intensity=0.25):
    """Vary punctuation patterns."""
    if random.random() < intensity:
        # Add extra punctuation
        text = text.replace('!', '!!').replace('?', '???').replace('.', '...')
    if random.random() < intensity:
        # Remove some punctuation
        text = text.replace('.', '').replace(',', '')
    if random.random() < intensity:
        # Add random punctuation
        punct = random.choice(['!!!', '...', '?!', '!?!', '???'])
        text = text.rstrip() + punct
    return text

def inject_case_variation(text, intensity=0.2):
    """Vary case patterns."""
    if random.random() < intensity:
        # Random uppercase
        words = text.split()
        for i in range(len(words)):
            if random.random() < 0.3:
                words[i] = words[i].upper()
        return ' '.join(words)
    if random.random() < intensity:
        # All lowercase
        return text.lower()
    if random.random() < intensity:
        # Title case
        return text.title()
    return text

def generate_unique_note(is_fraud, country, lang, category, fraud_type=None):
    """Generate unique transaction note with high variation."""
    # Base templates
    if is_fraud:
        # Select fraud note category
        note_cats = [FRAUD_NOTES_URGENT, FRAUD_NOTES_GIFT, FRAUD_NOTES_BUSINESS, 
                     FRAUD_NOTES_ADDRESS, FRAUD_NOTES_CODESWITCH, FRAUD_NOTES_ADVERSARIAL]
        base_pool = random.choice(note_cats)
        base = random.choice(base_pool)
        
        # Add category-specific content
        category_additions = [
            f" for {category}",
            f" related to {category.lower()}",
            f" about my {category.lower()} order",
            f" regarding {category.lower()} purchase",
            f" for the {category.lower()} item",
        ]
        if random.random() < 0.4:
            base += random.choice(category_additions)
    else:
        base = random.choice(LEGIT_NOTES)
        
        # Add variation
        legit_additions = [
            f" Love shopping here!",
            f" Thanks for great service.",
            f" Keep up the good work!",
            f" Will order again soon.",
            f" Recommended to friends.",
            f" My {random.randint(2, 20)}th order here.",
            f" Been customer since {random.randint(2018, 2024)}.",
            f" Always satisfied with quality.",
            f" Best prices I've found.",
            f" Fast delivery as promised.",
            "",
            "",
            "",
        ]
        if random.random() < 0.5:
            base += random.choice(legit_additions)
    
    # Apply noise injections
    if is_fraud:
        if random.random() < 0.4:
            base = inject_typos(base, intensity=0.2)
        if random.random() < 0.3:
            base = inject_code_switching(base, lang, intensity=0.25)
        if random.random() < 0.3:
            base = inject_punctuation_variation(base, intensity=0.3)
        if random.random() < 0.25:
            base = inject_case_variation(base, intensity=0.3)
    else:
        if random.random() < 0.15:
            base = inject_typos(base, intensity=0.08)
        if random.random() < 0.1:
            base = inject_punctuation_variation(base, intensity=0.1)
    
    return base

def generate_support_chat(is_fraud, lang='en'):
    """Generate diverse support chat."""
    fraud_chats = [
        [{"speaker": "user", "text": "I need this delivered TODAY"},
         {"speaker": "agent", "text": "I can help with that"},
         {"speaker": "user", "text": "Yes yes hurry up please"},
         {"speaker": "agent", "text": "Sure one moment"},
         {"speaker": "user", "text": "Why taking so long???"}],
        [{"speaker": "user", "text": "This is my third attempt"},
         {"speaker": "agent", "text": "Let me check"},
         {"speaker": "user", "text": "Hurry I dont have time"},
         {"speaker": "agent", "text": "Trying again"},
         {"speaker": "user", "text": "JUST FIX IT"}],
        [{"speaker": "user", "text": "Can you change shipping address"},
         {"speaker": "agent", "text": "Yes where to"},
         {"speaker": "user", "text": "Different from billing"},
         {"speaker": "agent", "text": "Sure what is it"},
         {"speaker": "user", "text": "I will send separately"}],
        [{"speaker": "user", "text": "Payment failed multiple times"},
         {"speaker": "agent", "text": "Let me see the error"},
         {"speaker": "user", "text": "Just process it manually"},
         {"speaker": "agent", "text": "I need to follow protocol"},
         {"speaker": "user", "text": "This is ridiculous"}],
        [{"speaker": "user", "text": "Need invoice urgently"},
         {"speaker": "agent", "text": "I can send via email"},
         {"speaker": "user", "text": "Send to different email"},
         {"speaker": "agent", "text": "Which email address"},
         {"speaker": "user", "text": "Will share on WhatsApp"}],
        [{"speaker": "user", "text": "Order status not updating"},
         {"speaker": "agent", "text": "Let me check internally"},
         {"speaker": "user", "text": "How long will it take"},
         {"speaker": "agent", "text": "Few minutes please"},
         {"speaker": "user", "text": "I need answer NOW"}],
        [{"speaker": "user", "text": "Wrong item received last time"},
         {"speaker": "agent", "text": "I apologize for that"},
         {"speaker": "user", "text": "Make sure this is correct"},
         {"speaker": "agent", "text": "I will verify"},
         {"speaker": "user", "text": "Double check please"}],
        [{"speaker": "user", "text": "Bulk order need discount"},
         {"speaker": "agent", "text": "Let me check eligibility"},
         {"speaker": "user", "text": "I order 50+ items"},
         {"speaker": "agent", "text": "I can offer 10%"},
         {"speaker": "user", "text": "Make it 25% or I leave"}],
        [{"speaker": "user", "text": "Card declined but has money"},
         {"speaker": "agent", "text": "Try different method"},
         {"speaker": "user", "text": "No this card only"},
         {"speaker": "agent", "text": "Contact your bank"},
         {"speaker": "user", "text": "You fix it now"}],
        [{"speaker": "user", "text": "Delivery to office not home"},
         {"speaker": "agent", "text": "I can update address"},
         {"speaker": "user", "text": "Before 5pm only"},
         {"speaker": "agent", "text": "I will note this"},
         {"speaker": "user", "text": "Call when arriving"}],
    ]
    
    legit_chats = [
        [{"speaker": "user", "text": "Hi when will my order arrive"},
         {"speaker": "agent", "text": "Let me check"},
         {"speaker": "user", "text": "Sure thanks"},
         {"speaker": "agent", "text": "Expected tomorrow"},
         {"speaker": "user", "text": "Great thank you"}],
        [{"speaker": "user", "text": "Can I return this if size doesnt fit"},
         {"speaker": "agent", "text": "Yes 30 day policy"},
         {"speaker": "user", "text": "Okay good"},
         {"speaker": "agent", "text": "Anything else"},
         {"speaker": "user", "text": "No thanks"}],
        [{"speaker": "user", "text": "Do you have this in blue"},
         {"speaker": "agent", "text": "Let me check inventory"},
         {"speaker": "user", "text": "Okay waiting"},
         {"speaker": "agent", "text": "Yes available"},
         {"speaker": "user", "text": "Perfect ordering now"}],
        [{"speaker": "user", "text": "Is this product authentic"},
         {"speaker": "agent", "text": "Yes all genuine"},
         {"speaker": "user", "text": "Good I was worried"},
         {"speaker": "agent", "text": "We guarantee authenticity"},
         {"speaker": "user", "text": "Will order then"}],
        [{"speaker": "user", "text": "What is warranty period"},
         {"speaker": "agent", "text": "One year manufacturer"},
         {"speaker": "user", "text": "Okay sounds good"},
         {"speaker": "agent", "text": "Anything else"},
         {"speaker": "user", "text": "No that is all"}],
        [{"speaker": "user", "text": "Can I track my order"},
         {"speaker": "agent", "text": "Yes tracking available"},
         {"speaker": "user", "text": "How do I access"},
         {"speaker": "agent", "text": "Check your email"},
         {"speaker": "user", "text": "Found it thanks"}],
        [{"speaker": "user", "text": "Do you ship internationally"},
         {"speaker": "agent", "text": "Yes to most countries"},
         {"speaker": "user", "text": "What is the cost"},
         {"speaker": "agent", "text": "Calculated at checkout"},
         {"speaker": "user", "text": "Okay will check"}],
        [{"speaker": "user", "text": "Is assembly required"},
         {"speaker": "agent", "text": "Comes pre-assembled"},
         {"speaker": "user", "text": "Perfect for me"},
         {"speaker": "agent", "text": "Ready to use"},
         {"speaker": "user", "text": "Great buying now"}],
        [{"speaker": "user", "text": "What are delivery options"},
         {"speaker": "agent", "text": "Standard and express"},
         {"speaker": "user", "text": "Standard is fine"},
         {"speaker": "agent", "text": "Great choice"},
         {"speaker": "user", "text": "Thanks for help"}],
        [{"speaker": "user", "text": "Can I use multiple coupons"},
         {"speaker": "agent", "text": "One per order"},
         {"speaker": "user", "text": "Okay understood"},
         {"speaker": "agent", "text": "Best one applies"},
         {"speaker": "user", "text": "Makes sense thanks"}],
    ]
    
    chat = random.choice(fraud_chats if is_fraud else legit_chats)
    
    # Add noise to fraud chats
    if is_fraud:
        for msg in chat:
            if msg['speaker'] == 'user':
                if random.random() < 0.3:
                    msg['text'] = msg['text'].upper()
                if random.random() < 0.2:
                    msg['text'] = inject_typos(msg['text'], 0.15)
    
    return json.dumps(chat, ensure_ascii=False)

def generate_merchant_description(category, is_fraud):
    """Generate merchant description."""
    fraud_descs = [
        f"BEST {category.upper()} DEALS 100% ORIGINAL CALL NOW",
        f"Limited stock {category} hurry up before sold out",
        f"Premium {category} cheapest price guaranteed",
        f"Special offer today only do not miss",
        f"Wholesale {category} direct from manufacturer",
        f"Luxury {category} at unbeatable prices",
        f"Authentic {category} best deal guaranteed",
        f"Fast shipping {category} order now",
        f"Discount {category} flash sale today",
        f"Exclusive {category} limited time offer",
    ]
    
    legit_descs = [
        f"Quality {category} at fair prices. Established seller.",
        f"We specialize in {category} with warranty included.",
        f"Trusted {category} seller with positive reviews.",
        f"Official {category} distributor. Easy returns.",
        f"Family business selling {category} since 2015.",
        f"Customer satisfaction guaranteed on all {category}.",
        f"Free shipping on {category} over certain amount.",
        f"Expert support for all {category} questions.",
        f"Carefully curated {category} collection.",
        f"Sustainable and ethical {category} options.",
    ]
    
    return random.choice(fraud_descs if is_fraud else legit_descs)

def generate_product_review(is_fraud, category):
    """Generate product review."""
    fraud_reviews = [
        "AMAZING PRODUCT BEST PRICE EVER HIGHLY RECOMMEND",
        "Good quality fast shipping will buy again",
        "Excellent service very satisfied thank you",
        "Perfect exactly as described quick delivery",
        "Great value for money happy with purchase",
        "Outstanding product exceeded my expectations",
        "Five stars definitely buying more soon",
        "Top quality item arrived early perfect",
        "Best purchase ever highly recommend seller",
        "Wonderful product fast delivery thank you",
    ]
    
    legit_reviews = [
        "Product is okay nothing special",
        "Decent quality for the price",
        "Arrived on time works as expected",
        "Good but shipping took longer than expected",
        "Average product meets basic needs",
        "Not bad but I have seen better",
        "Does the job would consider buying again",
        "Reasonable quality fair price point",
        "Met my expectations overall satisfied",
        "Could be better but acceptable",
        "Works fine no complaints so far",
        "As described in the listing",
        "Happy with this purchase overall",
        "Would recommend to others",
        "Good value for the money spent",
    ]
    
    base = random.choice(fraud_reviews if is_fraud else legit_reviews)
    
    if is_fraud and random.random() < 0.4:
        additions = ["!!!", "10/10", "5 STARS", "BUY NOW", "A+++", "PERFECT", "LOVE IT"]
        base += " " + random.choice(additions)
    
    return base

def generate_dispute_reason(is_fraud):
    """Generate dispute reason."""
    if is_fraud:
        return random.choice([
            "I did not authorize this transaction",
            "I never received this item",
            "Item received not as described",
            "Charged multiple times for same order",
            "Merchant refused refund request",
            "Unauthorized charge on my card",
            "Product was defective on arrival",
            "Received wrong item completely",
            "Package arrived empty",
            "Quality much worse than described",
        ])
    else:
        if random.random() < 0.08:
            return random.choice([
                "Item arrived damaged",
                "Wrong item received",
                "Quality not as expected",
                "Size does not fit",
                "Color different from picture",
                "Missing parts in package",
                "Not compatible with my device",
            ])
        return ""

def generate_email(country, is_fraud):
    """Generate realistic email."""
    domains_global = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'protonmail.com']
    domains_local = {
        'US': ['aol.com', 'comcast.net', 'verizon.net', 'att.net'],
        'GB': ['btinternet.com', 'sky.com', 'ntlworld.com', 'btopenworld.com'],
        'DE': ['web.de', 'gmx.de', 't-online.de', 'freenet.de'],
        'FR': ['orange.fr', 'free.fr', 'sfr.fr', 'laposte.net'],
        'CN': ['qq.com', '163.com', 'sina.com', 'sohu.com', '126.com'],
        'JP': ['docomo.ne.jp', 'ezweb.ne.jp', 'softbank.ne.jp', 'yahoo.co.jp'],
        'KR': ['naver.com', 'daum.net', 'nate.com', 'hanmail.net'],
        'BR': ['uol.com.br', 'bol.com.br', 'ig.com.br', 'terra.com.br'],
        'IN': ['rediffmail.com', 'sify.com', 'yahoo.co.in'],
        'RU': ['mail.ru', 'yandex.ru', 'rambler.ru', 'bk.ru'],
        'ES': ['terra.es', 'telefonica.net', 'wanadoo.es'],
        'IT': ['libero.it', 'virgilio.it', 'tiscali.it', 'alice.it'],
    }
    
    if is_fraud and random.random() < 0.35:
        temp_domains = ['tempmail.com', 'guerrillamail.com', '10minutemail.com', 'throwaway.email', 
                      'mailinator.com', 'fakeinbox.com', 'temp-mail.org', 'getnada.com',
                      'maildrop.cc', 'sharklasers.com', 'guerrillamailblock.com']
        domain = random.choice(temp_domains)
        name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(8, 16)))
    else:
        domain = random.choice(domains_local.get(country, domains_global))
        name_options = [
            ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(6, 12))),
            f"{random.choice(['john', 'maria', 'ahmed', 'wei', 'yuki', 'hans', 'pierre', 'anna', 'carlos', 'priya', 'kim', 'olga', 'jose', 'fatima'])}.{random.choice(['smith', 'garcia', 'kim', 'mueller', 'silva', 'patel', 'wang', 'tanaka', 'popov', 'ahmed', 'chen', 'yoshida', 'santos', 'lopez'])}{random.randint(1, 999)}",
            f"user{random.randint(1000, 999999)}",
            f"{random.choice(['buyer', 'customer', 'shopper', 'user', 'member'])}{random.randint(100, 99999)}",
        ]
        name = random.choice(name_options)
    
    return f"{name}@{domain}"

def generate_amount(country, is_fraud, currency):
    """Generate transaction amount."""
    base_amounts = {
        'USD': (15, 800), 'EUR': (12, 700), 'GBP': (10, 600), 'JPY': (1500, 80000),
        'CNY': (80, 5000), 'INR': (800, 50000), 'BRL': (80, 3500), 'RUB': (800, 50000),
        'KRW': (15000, 800000), 'MXN': (300, 12000), 'AED': (60, 2800), 'SAR': (60, 2800),
        'ZAR': (150, 6000), 'SGD': (20, 900), 'CAD': (20, 900), 'AUD': (20, 1000),
        'CHF': (15, 700), 'SEK': (150, 6000), 'NOK': (150, 6000), 'DKK': (100, 5000),
        'PLN': (80, 3500), 'TRY': (150, 6000), 'THB': (450, 22000), 'MYR': (70, 3000),
        'PHP': (750, 30000), 'IDR': (150000, 7500000), 'VND': (150000, 7500000),
        'PKR': (1500, 75000), 'BDT': (750, 45000), 'EGP': (150, 7500), 'NGN': (7500, 300000),
        'KES': (750, 30000), 'ARS': (1500, 75000), 'CLP': (7500, 300000), 'COP': (30000, 1200000),
        'PEN': (75, 3000), 'ILS': (60, 2200), 'CZK': (300, 15000), 'HUF': (4500, 220000),
        'RON': (75, 3000), 'UAH': (300, 15000), 'NZD': (20, 900),
    }
    
    min_amt, max_amt = base_amounts.get(currency, (10, 500))
    
    if is_fraud:
        if random.random() < 0.25:
            amount = random.uniform(1, 15)  # Card testing
        elif random.random() < 0.5:
            amount = random.uniform(max_amt * 0.3, max_amt * 0.7)
        else:
            amount = random.uniform(max_amt * 0.7, max_amt * 4)
    else:
        amount = random.uniform(min_amt, max_amt)
    
    return round(amount, 2)

def generate_timestamp():
    """Generate random timestamp."""
    start = datetime(2024, 1, 1)
    end = datetime(2025, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86399)
    return start + timedelta(days=random_days, seconds=random_seconds)

def select_country():
    """Select country based on weights."""
    countries = list(COUNTRIES.keys())
    weights = [COUNTRIES[c]['weight'] for c in countries]
    return random.choices(countries, weights=weights)[0]

def main():
    print("="*70)
    print("WORLDWIDE E-COMMERCE FRAUD DATASET - HARD/NOISY VERSION")
    print("="*70)
    
    n_samples = 3000
    print(f"\nGenerating {n_samples:,} highly diverse transactions...")
    
    data = []
    
    for i in range(n_samples):
        country = select_country()
        config = COUNTRIES[country]
        lang = config['lang']
        currency = config['currency']
        
        fraud_rate = config['fraud_rate']
        is_fraud = 1 if random.random() < fraud_rate else 0
        
        transaction_id = f"TXN{uuid.uuid4().hex[:12].upper()}"
        user_id = f"USR{uuid.uuid4().hex[:10].upper()}"
        timestamp = generate_timestamp()
        amount = generate_amount(country, is_fraud, currency)
        
        # Payment method
        if country in ['US', 'CA']:
            payment_method = random.choice(PAYMENT_METHODS['US'])
        elif country in ['DE', 'FR', 'IT', 'ES', 'NL', 'PL', 'SE', 'NO', 'DK', 'FI', 'IE', 'PT', 'GR', 'CZ', 'RO', 'HU', 'BE', 'AT']:
            payment_method = random.choice(PAYMENT_METHODS['EU'])
        elif country == 'CN':
            payment_method = random.choice(PAYMENT_METHODS['CN'])
        elif country == 'IN':
            payment_method = random.choice(PAYMENT_METHODS['IN'])
        elif country == 'BR':
            payment_method = random.choice(PAYMENT_METHODS['BR'])
        elif country in ['NG', 'KE']:
            payment_method = random.choice(PAYMENT_METHODS['NG'])
        elif country in ['ID', 'MY', 'TH', 'VN', 'PH', 'SG']:
            payment_method = random.choice(PAYMENT_METHODS['SEA'])
        elif country in ['MX', 'AR', 'CL', 'CO']:
            payment_method = random.choice(PAYMENT_METHODS['LATAM'])
        else:
            payment_method = random.choice(PAYMENT_METHODS['global'])
        
        device_type = random.choice(DEVICE_TYPES)
        browser = random.choice(BROWSERS)
        os_type = random.choice(OS_TYPES)
        category = random.choice(MERCHANT_CATEGORIES)
        items_count = random.randint(1, 12)
        
        city = random.choice(CITIES.get(country, ['Unknown']))
        shipping_city = city
        billing_city = city
        shipping_billing_match = 1
        
        if is_fraud and random.random() < 0.45:
            other_countries = [c for c in COUNTRIES.keys() if c != country]
            billing_country = random.choice(other_countries)
            billing_city = random.choice(CITIES.get(billing_country, ['Unknown']))
            shipping_billing_match = 0
        
        ip_address = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        
        base_risk = random.uniform(10, 40)
        if is_fraud:
            base_risk += random.uniform(20, 55)
        ip_risk_score = min(100, base_risk)
        
        card_present = random.choice([0, 1])
        card_age_days = random.randint(1, 3650)
        
        email = generate_email(country, is_fraud)
        email_domain = email.split('@')[1]
        
        user_account_age_days = random.randint(1, 2000)
        user_prev_chargebacks = 1 if (is_fraud and random.random() < 0.35) else 0
        user_is_high_risk = 1 if (is_fraud and random.random() < 0.45) else 0
        
        transactions_last_24h = random.randint(0, 3)
        transactions_last_1h = random.randint(0, 2)
        if is_fraud and random.random() < 0.55:
            transactions_last_24h = random.randint(3, 18)
            transactions_last_1h = random.randint(2, 10)
        
        local_hour = timestamp.hour
        odd_hour = 1 if local_hour < 6 or local_hour > 23 else 0
        
        fraud_type = random.choice(FRAUD_TYPES) if is_fraud else 'none'
        
        # Generate NLP fields with high variation
        transaction_notes = generate_unique_note(is_fraud, country, lang, category, fraud_type)
        support_chat = generate_support_chat(is_fraud, lang)
        merchant_description = generate_merchant_description(category, is_fraud)
        product_review = generate_product_review(is_fraud, category)
        dispute_reason = generate_dispute_reason(is_fraud)
        
        # Stylometric features
        note_word_count = len(transaction_notes.split())
        note_uppercase_ratio = sum(1 for c in transaction_notes if c.isupper()) / len(transaction_notes) if transaction_notes else 0
        note_exclamation_count = transaction_notes.count('!')
        chat_turn_count = len(json.loads(support_chat))
        
        avg_item_price = round(amount / items_count, 2)
        
        row = {
            'transaction_id': transaction_id,
            'user_id': user_id,
            'timestamp_utc': timestamp.isoformat() + 'Z',
            'amount': amount,
            'currency': currency,
            'country': country,
            'payment_method': payment_method,
            'device_type': device_type,
            'browser': browser,
            'os_type': os_type,
            'merchant_category': category,
            'items_count': items_count,
            'avg_item_price': avg_item_price,
            'shipping_city': shipping_city,
            'billing_city': billing_city,
            'shipping_billing_match': shipping_billing_match,
            'ip_address': ip_address,
            'ip_risk_score': round(ip_risk_score, 1),
            'card_present': card_present,
            'card_age_days': card_age_days,
            'email': email,
            'email_domain': email_domain,
            'user_account_age_days': user_account_age_days,
            'user_prev_chargebacks': user_prev_chargebacks,
            'user_is_high_risk': user_is_high_risk,
            'transactions_last_24h': transactions_last_24h,
            'transactions_last_1h': transactions_last_1h,
            'local_hour': local_hour,
            'odd_hour': odd_hour,
            'fraud_type': fraud_type,
            'is_fraud': is_fraud,
            'transaction_notes': transaction_notes,
            'support_chat': support_chat,
            'merchant_description': merchant_description,
            'product_review': product_review,
            'dispute_reason': dispute_reason,
            'note_word_count': note_word_count,
            'note_uppercase_ratio': round(note_uppercase_ratio, 3),
            'note_exclamation_count': note_exclamation_count,
            'chat_turn_count': chat_turn_count,
        }
        
        data.append(row)
        
        if (i + 1) % 500 == 0:
            print(f"  Generated {i + 1:,} / {n_samples:,}...")
    
    print("\nCreating DataFrame...")
    df = pd.DataFrame(data)
    
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFraud distribution:")
    print(df['is_fraud'].value_counts())
    print(f"\nFraud rate: {(df['is_fraud'].mean() * 100):.1f}%")
    
    print(f"\nCountry distribution (top 10):")
    print(df['country'].value_counts().head(10))
    
    print("\nSaving to data.csv...")
    output_path = '/Users/omx/Downloads/data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✓ Saved to: {output_path}")
    print(f"  File size: ~{os.path.getsize(output_path) / 1024 / 1024:.1f}MB")
    
    # Show diverse samples
    print("\n" + "="*70)
    print("DIVERSE SAMPLES:")
    print("="*70)
    
    samples = [
        ('NG', 1, 'Nigeria Fraud'),
        ('JP', 0, 'Japan Legit'),
        ('BR', 1, 'Brazil Fraud'),
        ('DE', 0, 'Germany Legit'),
        ('IN', 1, 'India Fraud'),
        ('US', 0, 'US Legit'),
    ]
    
    for country, fraud, label in samples:
        subset = df[(df['country'] == country) & (df['is_fraud'] == fraud)]
        if len(subset) > 0:
            row = subset.iloc[0]
            print(f"\n--- {label} ---")
            print(f"Amount: {row['amount']} {row['currency']} | Payment: {row['payment_method']}")
            print(f"Notes: {row['transaction_notes'][:120]}...")
            print(f"Review: {row['product_review']}")
    
    print("\n" + "="*70)
    print("GENERATION COMPLETE!")
    print("="*70)

if __name__ == '__main__':
    import os
    main()
