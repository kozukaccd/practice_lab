from django.shortcuts import get_object_or_404, render # render関数は request,テンプレートパスを渡すとそのテンプレートを使用したレンダリング結果をHttpRsponceとして返す
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # """Return the last five published questions."""
        # return Question.objects.order_by("-pub_date")[:5]
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

"""
これらのviewは汎用Viewに置き換えられる

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    return render(request, "polls/index.html",{
        "latest_question_list": latest_question_list,
    })
    #template = loader.get_template("polls/index.html")
    # context = {
    #     "latest_question_list": latest_question_list
    # }
    # return HttpResponse(template.render(context, request))
# Leave the rest of the views (detail, results, vote) unchanged

def detail(request, question_id):
    # return HttpResponse("You're looking at question {0}.".format(question_id))
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
"""
"""
    Memo: Views.py 内に必要な各種処理を書く
    参照: https://docs.djangoproject.com/ja/2.0/intro/tutorial03/
    index関数でrenderを使った際に参照したサイト https://qiita.com/maisuto/items/eece9d880d94fd241a0d
"""
