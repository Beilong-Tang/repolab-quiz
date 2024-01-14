from simple_judge.models import Post


def deleteForum():
    for p in Post.objects.all():
        p.delete()
    pass
