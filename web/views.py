from django.shortcuts import render
from django.views import View
from .utils import *
import pandas as pd
from api.models import *


class MainView(View):
    def get(self, request):
        
        datas = Data.objects.all()
        json = []
        for data in datas:
            
            json.append({
                "question_1": data.course.name,
                "is_relevant": data.is_relevant,
                "object": data.object,
                "is_positive": data.is_positive,
            })
        df = pd.DataFrame(json)

        plot_feedback_distribution_data = plot_feedback_distribution(df)
        distribution_relevant_reviews_data = distribution_relevant_reviews(df)
        plot_relevant_reviews_data = plot_relevant_reviews(df)
        distribution_positivity_feedback_data = distribution_positivity_feedback(df)
        plot_positivity_feedback_data = plot_positivity_feedback(df)
        distribution_object_feedback_data = distribution_object_feedback(df)
        plot_object_feedback_data = plot_object_feedback(df)
        plot_positivity_feedback_facilities_data = plot_positivity_feedback_facilities(df)

        context = {
            "graphs": [
                plot_feedback_distribution_data.to_html(full_html=False, default_height=500, default_width=700), # type: ignore
                distribution_relevant_reviews_data.to_html(full_html=False, default_height=500, default_width=700),
                plot_relevant_reviews_data.to_html(full_html=False, default_height=500, default_width=700),
                distribution_positivity_feedback_data.to_html(full_html=False, default_height=500, default_width=700),
                plot_positivity_feedback_data.to_html(full_html=False, default_height=500, default_width=700),
                distribution_object_feedback_data.to_html(full_html=False, default_height=500, default_width=700),
                plot_object_feedback_data.to_html(full_html=False, default_height=500, default_width=700),
                plot_positivity_feedback_facilities_data.to_html(full_html=False, default_height=500, default_width=700),
            ]
        }

        return render(request, 'index.html', context)
    
