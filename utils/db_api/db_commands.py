from asgiref.sync import sync_to_async

from project.djangoadmin.shopmanage.models import Users, Items, Purchases


@sync_to_async
def add_user(user_id: int):
    return Users(user_id=int(user_id)).save()


@sync_to_async
def add_users_tlink(user_id: int, trade_link: str):
    user = Users.objects.filter(user_id=int(user_id)).first()
    user.trade_link = trade_link
    return user.save()


@sync_to_async
def return_users_link(user_id: int):
    user = Users.objects.filter(user_id=int(user_id)).first()
    return user.trade_link


@sync_to_async
def return_all_items():
    items = Items.objects.all()
    return items


@sync_to_async
def return_users_purchases(user_id: int):
    items = Purchases.objects.filter(buyer_id=int(user_id), delivered=False)
    return items


@sync_to_async
def get_all_feedbacks():
    feedbacks = Users.objects.filter(feedback_text=not None)[3:]
    return feedbacks


@sync_to_async
def get_users_rate(user_id: int):
    rate = Users.objects.filter(user_id=user_id).first()
    return rate.feedback_rate



@sync_to_async
def set_rating(user_id: int, rate: str):
    user = Users.objects.filter(user_id=int(user_id)).first()
    user.feedback_rate = rate
    return user.save()



@sync_to_async
def write_feedback(user_id: int, text: str):
    user = Users.objects.filter(user_id=int(user_id)).first()
    user.feedback_text = text
    return user.save()