from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactUsForm
from .models import ContactUs, Answer


def contact_us_view(request):
    context = {}

    form = ContactUsForm()
    context['form'] = form

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            context['done'] = 'We received your question check our blog later!'
    return render(request, 'blog/contact_us.html', context=context)


def get_message_unread(request):
    messages = ContactUs.objects.all()
    if request.method == 'POST':
        id = request.POST.get('q_id')
        q_description = request.POST.get('q_description')
        answer = request.POST.get('answer')

        data = ContactUs.objects.get(id=id)
        user_email = data.user_email

        Answer.objects.create(
            user_email=user_email,
            question=q_description,
            answer=answer
        )

        data.delete()
    return render(request, 'superuser/messages.html', context={'messages': messages})


@csrf_exempt
def response_message_description(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        data = ContactUs.objects.get(id=id)
        return JsonResponse({'id': data.id, 'description': data.description, 'q_type': data.about})



def blog_view(request):
    answer = Answer.objects.all().order_by('-on_date')
    return render(request, 'blog/blog.html', context={'answer': answer})


@csrf_exempt
def response_blog_id(request):
    id = request.POST.get('id')
    answer = Answer.objects.get(id=id)
    return JsonResponse({'q': answer.question, 'ans': answer.answer})
