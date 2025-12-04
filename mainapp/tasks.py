from mainapp.models import AdApproved
from datetime import date

def remove_expired_ads():
    expired_ads = AdApproved.objects.all()
    for ad in expired_ads:
        if ad.has_expired():
            ad.delete()
