from django.shortcuts import render
from django.views import View

from search import forms
from search.services import search


class SearchView(View):
    def get(self, request):
        form = forms.SearchForm(self.request.GET)
        self.form = form
        if form.is_valid():
            query = form.cleaned_data.get('query')
            target_type = form.cleaned_data.get('target_type')
            sort = form.cleaned_data.get('sort')
            if query:
                search_result = search.get_content_for_search_query(query, target_type, sort=sort)
                template_name = search.get_template_name(target_type)
                return render(
                    request,
                    template_name,
                    context=dict(search_result=search_result, form=form)
                )
        return render(
            request,
            'search/base_search.html',
            context=dict(form=form)
        )
