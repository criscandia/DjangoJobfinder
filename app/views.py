from django.shortcuts import render, redirect
from .forms import JobSearchForm, RssFeedForm
from .models import Job, RSSFeed
import feedparser
from dateutil import parser
from django.utils.timezone import make_aware  # Import make_aware function from django.utils.timezone
# Create your views here.

def index(request):
    return render(request, 'index.html')

def job_search(request):
    form = JobSearchForm(request.GET)
    jobs = Job.objects.all()
    
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        company = form.cleaned_data.get('company')
        location = form.cleaned_data.get('location')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
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
                
        return render(request, 'job-search.html', {'jobs': jobs, 'form': form})
    
def new_feed(request):
    if request.method == 'POST':
        form = RssFeedForm(request.POST)
        
        if form.is_valid():
            # Guardar el objeto RSSFeed con los datos del formulario
            rss_feed = form.save()
            
            # Llamar a la función para parsear el RSS
            parse_rss(rss_feed)
            
            return redirect('index')
    else:
        form = RssFeedForm()
    
    return render(request, 'new_feed.html', {'form': form})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

def parse_rss(rss_feed):
    # Aquí, 'rss_feed' debería ser una instancia de RSSFeed que contiene la URL del feed RSS
    parsed_entries = []
    
    # Acceder a la URL del feed RSS desde el objeto rss_feed
    rss_feed_url = rss_feed.url
    
    # Parsear el feed RSS usando feedparser
    parser_feed = feedparser.parse(rss_feed_url)
    
    # Iterar sobre las entradas del feed
    for entry in parser_feed.entries:
        title = entry.get('title', '')
        link = entry.get('link', '')
        description = entry.get('description', '')
        pub_date = parser.parse(entry.get('published', '')) if entry.get('published') else None
        
        # Crear o actualizar el objeto Job basado en las entradas del feed
        job, created = Job.objects.update_or_create(
            title=title,
            company=rss_feed.site_name,  # Usar el nombre del sitio del RSSFeed como la empresa por ahora
            location='',  # Puedes agregar la ubicación si está disponible en el feed
            description=description,
            pub_date=pub_date,
            link=link,
            rss_feed=rss_feed  # Asociar este Job con el RSSFeed correspondiente
        )
        
        parsed_entries.append(job)
    
    return parsed_entries