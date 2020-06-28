from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from demo.models import Score, Rank


# Create your views here.

@csrf_exempt
def upload(request):
    if request.method == 'GET':
        return render(request, 'upload/upload.html', {'user': request.user, })
    if request.method == 'POST':

        score = request.POST.get('score', '')
        if score:

            old_scor = Score.objects.filter(client=request.user).first()
            if old_scor:
                if old_scor.score != score:
                    old_scor.score = score
                    old_scor.save()
            else:
                Score.objects.create(client=request.user, score=score)

            Rank.objects.all().delete()
            score_li = [score_obj.id for score_obj in Score.objects.all().order_by('-score')]
            n = 1
            for i in score_li:
                Rank.objects.create(c_id_id=i, rank=n)
                n = n + 1
            return JsonResponse({'status': 'sucess'})
        return JsonResponse({'status': 'error'})


@csrf_exempt
def show(request):
    context = {'scores': [{'ranking': scor.rank.rank, 'client': scor.client, 'score': scor.score} for scor in
                          Score.objects.all().order_by('-score')]}
    if request.method == 'GET':
        count = Score.objects.all().count()
        uscore = Score.objects.filter(client=request.user).first()
        uscore = {'ranking': uscore.rank.rank, 'score': uscore.score}
        return render(request, 'show/show.html', {'context': context, 'count': count, 'uscore': uscore})
    if request.method == 'POST':
        try:
            start = int(request.POST.get('start'))
            end = int(request.POST.get('end'))
        except ValueError as e1:
            return JsonResponse({'status': 'error'})
        context = {'scores': [{'ranking': scor.rank.rank, 'client': scor.client, 'score': scor.score} for scor in
                              Score.objects.all().order_by('-score')[start - 1:end]]}
        return JsonResponse({'status': 'ok', 'context': context})
