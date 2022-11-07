from datetime import date

from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import CommentForm, AdForm
from .models import Category, Ad


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'board/index.html'


class AdsList(ListView):
    model = Ad  # указываем модель, объекты которой будем выводить
    template_name = 'board/ads.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о
    # том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'ads'  # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-id']  # сортировка по полю id по убыванию
    paginate_by = 10  # поставим постраничный вывод

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # переменная списка категорий
        context['ads_limit'] = Ad.objects.order_by('-id')[:3]  # первые три свежих поста для карусели
        p = {}
        for r in Ad.objects.annotate(Count('comment')):
            p[r.title] = r.comment__count
        sorted_p = dict(sorted(p.items(), key=lambda item: -item[1]))
        context['ad_comment'] = sorted_p  # Словарь: title объявления и количество комментов в нем
        # context['num_comments'] = Ad.objects.all().annotate(cnt=Count('comment_set')).order_by('cnt')
        print('ad_comment', context['ad_comment'])
        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'board/ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['ads_limit'] = Ad.objects.order_by('-id')[:3]  # первые три свежих поста для карусели
        return context


class AddComment(View):

    def ad(self, request, pk):
        print(request.POST)
        form = CommentForm(request.POST)
        ad = Ad.objects.get(id=pk)
        if form.is_valid():
            print('form is valid')

            form = form.save(commit=False)
            form.post_id = pk
            form.save()
        else:
            print('form is NOT valid')
        print(form.errors)
        return redirect(ad.get_absolute_url())


class AdCreateView(CreateView):  # позже добавим эти группы:
    # LoginRequiredMixin - для идентификации и авторизации
    # PermissionRequiredMixin - для организции прав доступа
    model = Ad
    template_name = 'board/ad_create.html'
    form_class = AdForm

    # permission_required = ('board.add_ad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        return context

    def form_valid(self, AdForm):
        self.object = AdForm.save(commit=False)
        new_author, created = User.objects.get_or_create(
            author_user=self.request.user
        )
        self.object.id_author = new_author
        if Ad.objects.filter(date_created__date=date.today(), id_author__username=self.request.user).count() < 3:
            self.object = AdForm.save()
            return super().form_valid(AdForm)
        else:
            return HttpResponseRedirect('/')


# Для примера формы
def AdCreate(request):
    if request.method == 'POST':
        pass
    else:
        form = AdForm()
    return render(request, 'board/ad_create.html', {'form': form})


def Add(request):
    if request.method == 'POST':
        pass
    else:
        form = AdForm()
    return render(request, 'board/add.html', {'form': form})
