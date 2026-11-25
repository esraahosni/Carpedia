from django.core.management.base import BaseCommand

from cars.models import Car

# Sample data: realistic popular models for the Egyptian market.
# Prices are rough USD figures (the site shows "$") and are placeholders to edit in the admin.
CARS = [
    ('Toyota', 'new', 'Corolla Cross', 2024, 28500, '1.8L 4-cylinder', 140, 'Petrol', 'Automatic (CVT)', 'corolla',
     'Compact crossover with a roomy cabin, strong resale value and low running costs. Full agency service history, cruise control, reverse camera and 8-inch touchscreen.'),
    ('Hyundai', 'new', 'Tucson', 2024, 36000, '1.6L Turbo', 180, 'Petrol', 'Automatic (7-speed DCT)', 'tucson',
     'Modern family SUV with panoramic roof, digital cluster, six airbags and lane-keeping assist. Very popular in Egypt for comfort and features.'),
    ('Skoda', 'new', 'Octavia', 2024, 32000, '1.4L TSI Turbo', 150, 'Petrol', 'Automatic (DSG)', 'octavia',
     'Spacious liberty-style liftback with a huge trunk, premium interior and excellent fuel economy. Agency warranty included.'),
    ('Kia', 'used', 'Cerato', 2021, 17500, '1.6L MPI', 128, 'Petrol', 'Automatic (6-speed)', 'cerato',
     'Clean one-owner sedan, 62,000 km, full service record. Sunroof, alloy wheels, rear parking sensors. No accidents.'),
    ('Hyundai', 'used', 'Elantra', 2020, 15500, '1.6L MPI', 128, 'Petrol', 'Automatic (6-speed)', 'elantra',
     'Reliable family sedan, 78,000 km, automatic AC, Bluetooth, cruise control. Original paint, serviced at the agency.'),
    ('Nissan', 'used', 'Sunny', 2019, 9500, '1.5L', 99, 'Petrol', 'Automatic (CVT)', 'sunny',
     'Economical city sedan, 95,000 km. Very low maintenance cost and strong spare-parts availability. Great first car.'),
    ('Renault', 'used', 'Logan', 2018, 7000, '1.6L', 105, 'Petrol', 'Manual (5-speed)', 'logan',
     'Practical budget sedan, 110,000 km, large trunk, simple mechanics. Ideal for daily commuting or ride-hailing.'),
    ('Suzuki', 'used', 'Swift', 2022, 14000, '1.2L Dualjet', 90, 'Petrol', 'Automatic (CVT)', 'swift',
     'Light and agile hatchback, 38,000 km, excellent fuel economy (about 5.5 L/100 km). Touchscreen, rear camera, one owner.'),
    ('Mercedes-Benz', 'used', 'C200', 2017, 24000, '2.0L Turbo', 184, 'Petrol', 'Automatic (9G-Tronic)', 'cclass',
     'Luxury sedan, 85,000 km, leather seats, AMG line exterior, ambient lighting, navigation. Regular specialist servicing.'),
    ('BMW', 'used', '320i', 2016, 19500, '2.0L Turbo', 184, 'Petrol', 'Automatic (8-speed)', 'bmw3',
     'Sport sedan, 92,000 km, M-sport steering wheel, xenon lights, iDrive with navigation. Smooth and fun to drive.'),
]


class Command(BaseCommand):
    help = 'Add sample cars (safe to run twice: existing sample cars are skipped).'

    def handle(self, *args, **options):
        added = 0
        for brand, cond, model, year, price, engine, hp, fuel, trans, img, desc in CARS:
            _, created = Car.objects.get_or_create(
                brand=brand, model_name=model, year=year,
                defaults=dict(condition=cond, price=price, engine=engine, horsepower=hp,
                              fuel_type=fuel, transmission=trans, description=desc,
                              main_image=f'seed/{img}.jpg'))
            added += created
        self.stdout.write(f'Added {added} sample cars.')
