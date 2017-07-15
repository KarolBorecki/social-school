from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'social_school/index.html'
