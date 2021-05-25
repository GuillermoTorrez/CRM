import random

from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.views import generic 
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin

# https://github.com/justdjango/getting-started-with-django/
# Create your views here.
class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
      template_name = "agents/agent_list.html"
      # queryset = agents.objects.all()
      def get_queryset(self):
          request_user_organisation = self.request.user.userprofile
          # return Agent.objects.all()
          return Agent.objects.filter(organisation=request_user_organisation)

      context_object_name = "agent"

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user  = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 10000000000)}")
        user.save()
        Agent.objects.create(user=user, organisation=self.request.user.userprofile)
        #send_mail(
            #subject="You are invited to be a agent",
            #message="You were added as am agent on DJ-CRM, Please login to start working",
            #from_email="admin@test.com",
            #recipient_list=[user.email]
        #)
        #agent.organisation = self.request.user.userprofile
        #agent.save()
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    # queryset = agents.objects.all()
    def get_queryset(self):
        organisation = self.request.user.userprofile
        # return Agent.objects.all()
        return Agent.objects.filter(organisation=organisation)

    context_object_name = "agent"


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
        
    def get_queryset(self):
        organisation = self.request.user.userprofile
        # return Agent.objects.all()
        return Agent.objects.filter(organisation=organisation)

class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"
    # queryset = agents.objects.all()
    def get_queryset(self):
        organisation = self.request.user.userprofile
        # return Agent.objects.all()
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse("agents:agent-list")
