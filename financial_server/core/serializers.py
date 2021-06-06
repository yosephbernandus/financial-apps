from typing import Dict

import calendar

from financial_server.apps.users.models import User
from financial_server.apps.categories.models import Category


def serialize_user(user: User) -> Dict:
    photo_url = user.profile.photo.url if user.profile.photo else None

    id_card_photo_url = user.profile.id_card_photo.url \
        if user.profile.id_card_photo else None

    data = {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'nik': user.nik,
        'phone': user.phone,
        'dateJoined': calendar.timegm(user.date_joined.utctimetuple()),
        'photoUrl': photo_url,
        'idCardPhotoUrl': id_card_photo_url,
        'birthday': user.profile.birthday.strftime("%Y-%m-%d") if user.profile.birthday else None,
        'gender': user.profile.gender,
        'address': user.profile.address,
    }

    return data


def serialize_category(category: Category) -> Dict:
    category_url = category.logo.url if category.logo else None

    data = {
        'id': category.id,
        'name': category.name,
        'logo_url': category_url
    }

    return data
