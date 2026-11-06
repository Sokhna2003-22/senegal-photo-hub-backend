 from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed data migrated from Render'

    def handle(self, *args, **options):
        if User.objects.filter(username='sokhna_niang').exists():
            self.stdout.write('Already seeded.')
            return
        with transaction.atomic():
            users = [
                (1,'pbkdf2_sha256$1500000$twJNZX0KI1gUQk44l1XYrr$1j1VnhUZpYfBMSmpuqGjE5TSi1oK7uZNzAjwK9ilMAk=','sokhna_niang','Sokhna','Niang','niangsokhnambathie@gmail.com','client','770809745','2026-10-30T22:19:06.959387Z'),
                (2,'pbkdf2_sha256$1500000$pMqNz3Ggg1uwJn0fAyinvU$8yjOB2HgO94Jcv4st6Xb1Lyci8smzZ0gg+QJ+Xz2738=','Elkhalill','Khalilll','Dione','ibradione25@gmail.com','client','775078965','2026-10-30T22:38:40.847956Z'),
                (3,'pbkdf2_sha256$1500000$agq36dR0mU6CJocdVv7hel$bydqPJMXSj42XXzJEA2vC8V7EkSQy2RNb5rUZ86Y9Lc=','abdou_niang','Abdou','Niang','niangsokhnambathie@gmail.com','photographer','773692391','2026-10-30T22:52:46.900747Z'),
                (4,'pbkdf2_sha256$1500000$OWPxwMEVMifUJLY27v7gLd$te2+iniXjFF94V5ksO1D4GOu/VFxo3zKRggRUV1aVxo=','ayana','Ayanokoji','Ayanokoji','syyoussou630@gmail.com','client','781344771','2026-10-31T10:49:53.51366Z'),
                (5,'pbkdf2_sha256$1500000$1dnQWESJUyx7kBKzFQyxeN$SMfh1JRmE129pMCbqh70eSzYU/2B0Yv3ApJI7Ocv8/g=','quelafamille','Malick','Cisse','quelafamille2024@gmail.com','client','','2026-11-02T20:06:43.149514Z'),
            ]
            for uid,pwd,uname,fn,ln,email,role,phone,dj in users:
                User.objects.update_or_create(id=uid, defaults=dict(password=pwd,username=uname,first_name=fn,last_name=ln,email=email,role=role,phone=phone,date_joined=dj,is_active=True))
            from apps.accounts.models import PhotographerProfile
            PhotographerProfile.objects.update_or_create(id=1,defaults=dict(bio='',city='',instagram='',is_verified=False,plan='free',user_id=3,website=''))
            from apps.orders.models import Order
            Order.objects.update_or_create(id=1,defaults=dict(client_id=1,event_date='2026-11-08T00:00:00Z',location='kms',message="J'ai un evenment",photographer_id=3,price=None,service_type='evenement',status='confirmed'))
            from apps.messaging.models import Message
            Message.objects.update_or_create(id=1,defaults=dict(content='bonsoir',is_read=False,receiver_id=3,sender_id=1))
        self.stdout.write(self.style.SUCCESS('Migration complete!'))
