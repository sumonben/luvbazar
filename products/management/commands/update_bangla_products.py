import os
import urllib.request
import urllib.error
import time
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product


# Mapping: product_id → (bangla_name, unsplash_query)
PRODUCT_DATA = {
    # Electronics
    1:  ('ওয়্যারলেস ব্লুটুথ হেডফোন', 'wireless+bluetooth+headphones'),
    2:  ('ইউএসবি-সি ফাস্ট চার্জার', 'usb+fast+charger'),
    11: ('গেমিং মাউস', 'gaming+mouse+computer'),
    12: ('মেকানিক্যাল কীবোর্ড', 'mechanical+keyboard'),

    # Clothing
    3:  ('প্রিমিয়াম কটন টি-শার্ট', 'cotton+tshirt+clothing'),
    4:  ('রানিং জুতা', 'running+shoes+sports'),
    13: ('শীতের জ্যাকেট', 'winter+jacket+fashion'),

    # Sports & Outdoors
    5:  ('স্টেইনলেস স্টিল পানির বোতল', 'stainless+steel+water+bottle'),
    6:  ('যোগব্যায়ামের ম্যাট', 'yoga+mat+exercise'),
    14: ('জিম ডাম্বেল সেট', 'dumbbell+gym+fitness'),

    # Home & Garden
    7:  ('এলইডি ডেস্ক ল্যাম্প', 'led+desk+lamp+office'),
    8:  ('গাছের টব সেট', 'plant+pot+garden'),
    15: ('কফি টেবিল', 'coffee+table+furniture'),

    # Books
    9:  ('পাইথন প্রোগ্রামিং বই', 'python+programming+book'),
    10: ('ওয়েব ডেভেলপমেন্ট গাইড', 'web+development+book'),

    # Vegetables
    16: ('তাজা টমেটো', 'fresh+tomatoes+vegetable'),
    17: ('জৈব গাজর', 'organic+carrots+vegetable'),
    18: ('সবুজ ক্যাপসিকাম', 'green+bell+pepper+vegetable'),
    19: ('কুরকুরে লেটুস', 'lettuce+salad+green'),
    20: ('তাজা শসা', 'cucumber+fresh+vegetable'),
    21: ('বেগুনি পেঁয়াজ', 'red+onion+purple+vegetable'),
    22: ('ব্রকোলি', 'broccoli+vegetable+fresh'),
    23: ('ফুলকপি', 'cauliflower+white+vegetable'),
    24: ('পালং শাক', 'spinach+fresh+green'),
    25: ('রসুন', 'garlic+fresh+vegetable'),
    26: ('আলু', 'potato+fresh+vegetable'),
    27: ('মিষ্টি আলু', 'sweet+potato+vegetable'),
    28: ('গাজর', 'carrot+fresh+orange+vegetable'),
    29: ('সিম/বরবটি', 'green+beans+fresh+vegetable'),
    30: ('বাঁধাকপি', 'cabbage+fresh+green+vegetable'),

    # Grocery
    31: ('বাসমতি চাল (৫ কেজি)', 'basmati+rice+grain'),
    32: ('গমের আটা (২ কেজি)', 'wheat+flour+bag'),
    33: ('ভোজ্য তেল (১ লিটার)', 'vegetable+cooking+oil+bottle'),
    34: ('অলিভ অয়েল (৫০০ মিলি)', 'olive+oil+bottle'),
    35: ('লবণ (১ কেজি)', 'salt+white+seasoning'),
    36: ('চিনি (১ কেজি)', 'sugar+white+granulated'),
    37: ('দুধ (১ লিটার)', 'fresh+milk+bottle'),
    38: ('মাখন (২৫০ গ্রাম)', 'butter+dairy+fresh'),
    39: ('ডিম (১২টি)', 'eggs+dozen+fresh'),
    40: ('চিজ ব্লক (৫০০ গ্রাম)', 'cheese+block+dairy'),
    41: ('মুরগির মাংস (১ কেজি)', 'chicken+breast+raw+meat'),
    42: ('গরুর কিমা (১ কেজি)', 'ground+beef+raw+meat'),
    43: ('পাস্তা (৫০০ গ্রাম)', 'pasta+dry+italian'),
    44: ('ক্যানড টমেটো (৪০০ গ্রাম)', 'canned+tomatoes+tin'),
    45: ('কালো মটরশুটি (৪০০ গ্রাম)', 'black+beans+legume'),
    46: ('ছোলা (৪০০ গ্রাম)', 'chickpeas+legume+protein'),
    47: ('পিনাট বাটার (৫০০ গ্রাম)', 'peanut+butter+jar'),
    48: ('মধু (৫০০ মিলি)', 'honey+jar+natural'),
    49: ('চা ব্যাগ (৫০টি)', 'tea+bags+beverage'),
    50: ('কফি (৫০০ গ্রাম)', 'coffee+beans+ground'),
    51: ('আপেলের জুস (১ লিটার)', 'apple+juice+bottle'),
    52: ('সিরিয়াল মিক্স (৪০০ গ্রাম)', 'cereal+mix+breakfast'),
    53: ('দই (৫০০ মিলি)', 'yogurt+fresh+dairy'),
    54: ('পাউরুটি', 'bread+loaf+fresh+bakery'),
    55: ('কমলার জুস (১ লিটার)', 'orange+juice+fresh'),
    56: ('কাঠবাদাম (২৫০ গ্রাম)', 'almonds+nuts+dry+fruit'),
    57: ('কাজুবাদাম (২৫০ গ্রাম)', 'cashew+nuts+dry+fruit'),
    58: ('কিশমিশ (২০০ গ্রাম)', 'raisins+dry+fruit'),
    59: ('ডার্ক চকোলেট (১০০ গ্রাম)', 'dark+chocolate+bar'),
}

# Unsplash source URLs with specific photo IDs for reliable, high-quality images
PRODUCT_IMAGES = {
    1:  'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80',  # headphones
    2:  'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&q=80',  # charger
    3:  'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80',  # t-shirt
    4:  'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80',  # running shoes
    5:  'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&q=80',  # water bottle
    6:  'https://images.unsplash.com/photo-1601925228988-71c0dd78dec0?w=600&q=80',  # yoga mat
    7:  'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&q=80',  # desk lamp
    8:  'https://images.unsplash.com/photo-1463320898484-cdee8141c787?w=600&q=80',  # plant pot
    9:  'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600&q=80',  # programming book
    10: 'https://images.unsplash.com/photo-1432821596592-e2c18b78144f?w=600&q=80',  # web book
    11: 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=600&q=80',  # gaming mouse
    12: 'https://images.unsplash.com/photo-1561112078-7d24e04c3407?w=600&q=80',  # keyboard
    13: 'https://images.unsplash.com/photo-1539185441755-769473a23570?w=600&q=80',  # jacket
    14: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',  # dumbbells
    15: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&q=80',  # coffee table
    16: 'https://images.unsplash.com/photo-1546094096-0df4bcabd337?w=600&q=80',  # tomatoes
    17: 'https://images.unsplash.com/photo-1447175008436-054170c2e979?w=600&q=80',  # carrots
    18: 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=600&q=80',  # bell pepper
    19: 'https://images.unsplash.com/photo-1556801712-76c2eb163e7f?w=600&q=80',  # lettuce
    20: 'https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=600&q=80',  # cucumber
    21: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600&q=80',  # purple onion
    22: 'https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?w=600&q=80',  # broccoli
    23: 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=600&q=80',  # cauliflower
    24: 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=600&q=80',  # spinach
    25: 'https://images.unsplash.com/photo-1540148426945-6cf22a6b2383?w=600&q=80',  # garlic
    26: 'https://images.unsplash.com/photo-1518977956812-cd3dbadaaf31?w=600&q=80',  # potato
    27: 'https://images.unsplash.com/photo-1596097635121-14b63b7a0c19?w=600&q=80',  # sweet potato
    28: 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=600&q=80',  # carrot
    29: 'https://images.unsplash.com/photo-1567375698348-5d9d5ae99de0?w=600&q=80',  # green beans
    30: 'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=600&q=80',  # cabbage
    31: 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=600&q=80',  # rice
    32: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600&q=80',  # flour
    33: 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=600&q=80',  # vegetable oil
    34: 'https://images.unsplash.com/photo-1598511726623-d2e9996892f0?w=600&q=80',  # olive oil
    35: 'https://images.unsplash.com/photo-1518110925495-5fe2fda0442c?w=600&q=80',  # salt
    36: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',  # sugar
    37: 'https://images.unsplash.com/photo-1563636619-e9143da7973b?w=600&q=80',  # milk
    38: 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=600&q=80',  # butter
    39: 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=600&q=80',  # eggs
    40: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=600&q=80',  # cheese
    41: 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=600&q=80',  # chicken
    42: 'https://images.unsplash.com/photo-1602470520998-f4a52199a3d6?w=600&q=80',  # ground beef
    43: 'https://images.unsplash.com/photo-1551462147-37885acc36f1?w=600&q=80',  # pasta
    44: 'https://images.unsplash.com/photo-1608686207856-001b95cf60ca?w=600&q=80',  # canned tomatoes
    45: 'https://images.unsplash.com/photo-1587411768638-ec71f8e33b78?w=600&q=80',  # black beans
    46: 'https://images.unsplash.com/photo-1515543904379-3d757abe528c?w=600&q=80',  # chickpeas
    47: 'https://images.unsplash.com/photo-1558770147-a0e2842c5ea1?w=600&q=80',  # peanut butter
    48: 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=600&q=80',  # honey
    49: 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&q=80',  # tea
    50: 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=600&q=80',  # coffee
    51: 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80',  # apple juice
    52: 'https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?w=600&q=80',  # cereal
    53: 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&q=80',  # yogurt
    54: 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80',  # bread
    55: 'https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=600&q=80',  # orange juice
    56: 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=600&q=80',  # almonds
    57: 'https://images.unsplash.com/photo-1563412885-139e4045ec52?w=600&q=80',  # cashews
    58: 'https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=600&q=80',  # raisins
    59: 'https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=600&q=80',  # dark chocolate
}


class Command(BaseCommand):
    help = 'Update product names to Bangla and download real product images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--names-only',
            action='store_true',
            help='Only update names, skip image download',
        )
        parser.add_argument(
            '--images-only',
            action='store_true',
            help='Only download images, skip name update',
        )

    def handle(self, *args, **options):
        names_only = options['names_only']
        images_only = options['images_only']

        products = Product.objects.filter(id__in=PRODUCT_DATA.keys())
        total = products.count()
        self.stdout.write(f'Found {total} products to update.\n')

        for product in products:
            pid = product.id
            if pid not in PRODUCT_DATA:
                continue

            bangla_name, _ = PRODUCT_DATA[pid]
            updated_fields = []

            # Update name
            if not images_only:
                product.name = bangla_name
                updated_fields.append('name')

            # Download and save image
            if not names_only and pid in PRODUCT_IMAGES:
                url = PRODUCT_IMAGES[pid]
                try:
                    req = urllib.request.Request(
                        url,
                        headers={
                            'User-Agent': (
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/120.0.0.0 Safari/537.36'
                            )
                        }
                    )
                    with urllib.request.urlopen(req, timeout=15) as response:
                        image_data = response.read()

                    ext = 'jpg'
                    content_type = response.headers.get('Content-Type', '')
                    if 'webp' in content_type:
                        ext = 'webp'
                    elif 'png' in content_type:
                        ext = 'png'

                    filename = f'product_{pid}_bangla.{ext}'
                    product.image.save(filename, ContentFile(image_data), save=False)
                    updated_fields.append('image')
                    self.stdout.write(f'  ✓ Image downloaded for {bangla_name}')
                    time.sleep(0.3)  # be polite to the server
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  ✗ Image failed for id={pid}: {e}')
                    )

            if updated_fields:
                product.save(update_fields=updated_fields)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated [{pid}] → {bangla_name}')
                )

        self.stdout.write(self.style.SUCCESS('\nDone! All products updated.'))
