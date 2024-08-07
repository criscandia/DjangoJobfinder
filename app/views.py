from django.shortcuts import render, redirect
import requests
from .forms import JobSearchForm, RssFeedForm
from .models import Job, RSSFeed
from dateutil import parser as date_parser
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime
import feedparser
from bs4 import BeautifulSoup
import re
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Crear tus vistas aquí


# Esta vista es la página de inicio
def index(request):
    return render(request, "index.html")


# Esta vista es para buscar trabajos
def job_search(request):
    form = JobSearchForm(request.GET)
    jobs = Job.objects.all()

    if form.is_valid():
        return filter_jobs(form, jobs, request)
    return render(request, "job-search.html", {"jobs": jobs, "form": form})


# Función para filtrar trabajos según criterios de búsqueda
def filter_jobs(form, jobs, request):
    keyword = form.cleaned_data.get("keyword")
    company = form.cleaned_data.get("company")
    location = form.cleaned_data.get("location")
    start_date = form.cleaned_data.get("start_date")
    end_date = form.cleaned_data.get("end_date")

    if keyword:
        jobs = jobs.filter(title__icontains=keyword)
    if company:
        jobs = jobs.filter(company__icontains=company)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if start_date:
        jobs = jobs.filter(pub_date__gte=start_date)
    if end_date:
        jobs = jobs.filter(pub_date__lte=end_date)

    return render(request, "job-search.html", {"jobs": jobs, "form": form})


# Esta vista es para analizar el feed RSS y almacenar los trabajos en la base de datos
def parse_rss(rss_feed):
    parsed_entries = []

    rss_feed_url = rss_feed.url
    parser_feed = feedparser.parse(rss_feed_url)

    for entry in parser_feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        description = entry.get("description", "")
        pub_date = None
        if pub_date_str := entry.get("published"):
            pub_date = date_parser.parse(pub_date_str)
            if timezone.is_naive(pub_date):
                pub_date = timezone.make_aware(pub_date)

            # Limpiar la descripción HTML usando BeautifulSoup
            soup = BeautifulSoup(description, "html.parser")

            # Eliminar las etiquetas específicas como <img>, <a>, <script>, <style>, etc.
            for tag in soup(
                ["img", "a", "script", "style", "br", "li", "ul", "strong", "div", "p"]
            ):
                tag.decompose()

            # Obtener solo el texto limpio eliminando etiquetas restantes y espacios innecesarios
            description_text = soup.get_text(separator=" ").strip()
            description_text = re.sub(r"\s+", " ", description_text)

            # Crear o actualizar el objeto Job basado en las entradas del feed
            job, created = Job.objects.update_or_create(
                title=title,
                company=rss_feed.site_name,
                location="",
                defaults={
                    "description": description_text,
                    "pub_date": pub_date,
                    "link": link,
                    "rss_feed": rss_feed,
                },
            )

            parsed_entries.append(job)

    return parsed_entries


# Esta vista es para mostrar la lista de trabajos
def job_list(request):
    jobs = Job.objects.all()
    return render(request, "job_list.html", {"jobs": jobs})


# Esta vista es para agregar un nuevo feed RSS
def new_feed(request):
    if request.method == "POST":
        form = RssFeedForm(request.POST)
        if form.is_valid():
            rss_feed = form.save()
            parse_rss(rss_feed)
            return redirect("job_list")
    else:
        form = RssFeedForm()
    return render(request, "new_feed.html", {"form": form})


def schedule_task(request):
    # Crear un nuevo intervalo de 24 horas
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    # Crear una nueva tarea periódica para analizar los feeds RSS
    task = PeriodicTask.objects.create(
        interval=schedule,
        name="Actualizar feeds RSS",
        task="app.cron.update_rss_feeds",
    )

    return render(request, "schedule_task.html", {"task": task})
