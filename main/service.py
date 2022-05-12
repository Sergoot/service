from main.models import Training


def get_subcriptions(request):
    all_trains = []
    for subscription in request.user.subscriptions.all():
        sub_user_trainings = Training.objects.filter(user=subscription.user).order_by('-pub_date')
        for training in sub_user_trainings:
            all_trains.append(training)
    return all_trains