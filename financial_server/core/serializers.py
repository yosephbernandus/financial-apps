from typing import Dict

import calendar
from django.conf import settings

from financial_server.apps.users.models import User
from financial_server.apps.categories.models import Category
from financial_server.apps.financial_goals.models import FinancialGoal, GoalSavingsTransaction
from financial_server.apps.transactions.models import Transaction


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

    if settings.SHOW_IMAGE_FROM_LOCAL and photo_url:
        data['photoUrl'] = f"{settings.HOST}{photo_url}"

    return data


def serialize_category(category: Category) -> Dict:
    category_url = category.logo.thumbnails.size_140x140.url if category.logo else None

    data = {
        'id': category.id,
        'name': category.name,
        'logo_url': category_url
    }

    # TODO: Change use furl
    if settings.SHOW_IMAGE_FROM_LOCAL and category_url:
        data['logo_url'] = f"{settings.HOST}{category_url}"

    return data


def serialize_financial_goals(goal: FinancialGoal) -> Dict:
    data = {
        'id': goal.id,
        'category_id': goal.category.id if goal.category else None,
        'amount': goal.amount,
        'name': goal.goal_name,
        'achievement_date': goal.achievement_date.strftime("%Y-%m-%d"),
        'deposit_cycle': goal.deposit_cycle,
        'deposit_amount_per_cycle': round(goal.deposit_amount_per_cycle()),
    }

    if goal.transactions.exists():
        data['transactions'] = [serialize_goal_savings_transaction(transaction) for transaction in goal.transactions.order_by('id')]

    return data


def serialize_goal_savings_transaction(transaction: GoalSavingsTransaction) -> Dict:
    return {
        'id': transaction.id,
        'amount': transaction.amount,
        'created': transaction.created.strftime("%Y-%m-%d") if transaction.created else None
    }


def serialize_transactions(transaction: Transaction) -> Dict:
    data = {
        'id': transaction.id,
        'name': transaction.name,
        'type': transaction.type,
        'amount': transaction.amount,
        'notes': transaction.notes,
        'category_id': transaction.category.id if transaction.category else None,
        'created': transaction.created.strftime("%Y-%m-%d"),
    }

    return data
