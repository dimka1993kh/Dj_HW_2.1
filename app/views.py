from collections import Counter

from django.shortcuts import render
from django.http import HttpResponse

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    landing = request.GET.get('from-landing', '')
    counter_click[landing] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    
    lending = request.GET.get('ab-test-arg','')
    if lending == 'original':
        template = 'landing' 
    elif lending == 'test':
        template = 'landing_alternate'
    else:
        return HttpResponse("Что-то пошло не так")
    
    counter_show[lending] += 1

    return render(request, f'{template}.html')



def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    test_conversion = 0
    original_conversion = 0
    if counter_show['test']:
        test_conversion = counter_click['test'] / counter_show['test']
    if counter_show['original'] :
        original_conversion = counter_click['original'] / counter_show['original']
        
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })