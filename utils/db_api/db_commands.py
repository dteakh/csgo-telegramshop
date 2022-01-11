from asgiref.sync import sync_to_async

from project.djangoadmin.shopmanage.models import Users, Items, Purchases


@sync_to_async
def add_user(user_id: int):
    return Users(user_id=int(user_id)).save()


@sync_to_async
def add_users_link(user_id: int, trade_link: str):
    user = Users.objects.filter(user_id=int(user_id)).first()
    user.trade_link = trade_link
    return user.save()
