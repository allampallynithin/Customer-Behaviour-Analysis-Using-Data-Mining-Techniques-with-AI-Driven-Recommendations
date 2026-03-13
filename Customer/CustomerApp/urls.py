from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
		     path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),
		     path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
	             path("UserLogin.html", views.UserLogin, name="UserLogin"),
		     path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
		     path("Signup.html", views.Signup, name="Signup"),
		     path("SignupAction", views.SignupAction, name="SignupAction"),
		     path("ViewUsers", views.ViewUsers, name="ViewUsers"),
		     path("LoadDataset", views.LoadDataset, name="LoadDataset"),
		     path("Visualization", views.Visualization, name="Visualization"),
		     path("VisualizationAction", views.VisualizationAction, name="VisualizationAction"),
		     path("Suggestion", views.Suggestion, name="Suggestion"),
		     path("SuggestionAction", views.SuggestionAction, name="SuggestionAction"),		     
		    ]