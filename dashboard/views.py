from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            note = Notes(user=request.user,title=request.POST['title'],discription=request.POST['discription'])
            note.save()
        messages.success(request,f"Notes added from {request.user} successfully")
    else:
        form  = NotesForm()
    notes = Notes.objects.filter(user = request.user)
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_notes(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class notes_detail(generic.DetailView):
    model=Notes

@login_required
def homework(request):
    if request.method == "POST":
        forms= HomeworkForm(request.POST)
        if forms.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished = False
            except:
                finished = False
            homeworks=Homework(
                user = request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f"Homework added from {request.user.username} successfully")
    else:
        forms = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks)==0:
        homeworks_com=True
    else:
        homeworks_com = False
    context = {'homeworks':homeworks,'homeworks_com':homeworks_com,'forms':forms}
    return render(request,'dashboard/homework.html',context)

@login_required
def homework_update(request,pk=None):
    homeworks = Homework.objects.get(id = pk)
    if homeworks.is_finished ==True:
        homeworks.is_finished = False
    else:
        homeworks.is_finished = True
    homeworks.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def youtube(request):
    if request.method =="POST":
        form = DashboradForm()
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashboradForm()
    context = {'form':form}
    return render(request,'dashboard/youtube.html',context)

@login_required
def todo(request):
    if request.method == "POST":
        form= TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished = False
            except:
                finished = False
            todos=Todo(
                user = request.user,
                title=request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"Todo added from {request.user.username} successfully")
    else:
        form  = TodoForm()
    todos = Todo.objects.filter(user = request.user)
    if len(todos)==0:
        todo_done = True
    else:
        todo_done =False
    context = {
        'todos':todos,
        'form':form,
        'todo_done':todo_done
        }
    return render(request,"dashboard/todo.html",context)

@login_required
def todo_update(request,pk=None):
    todos = Todo.objects.get(id = pk)
    if todos.is_finished ==True:
        todos.is_finished = False
    else:
        todos.is_finished = True
    todos.save()
    return redirect('todo')

@login_required
def todo_delete(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def books(request):
    if request.method =="POST":
        form = DashboradForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                # 'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                #'thumbnail': answer.get('imageLinks', {}).get('thumbnail', 'N/A'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    else:
        form = DashboradForm()
    context = {'form':form}
    return render(request,'dashboard/books.html',context)


def dictionary(request):
    if request.method == "POST":
        form = DashboradForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
            try:
                r = requests.get(url, timeout=5)
                r.raise_for_status()  # Raise an HTTPError for bad responses
                answer = r.json()

                # Extract data from the JSON response
                phonetics = answer[0].get('phonetics', [{}])[0].get('text', 'N/A')
                audio = answer[0].get('phonetics', [{}])[0].get('audio', '')
                definition = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', 'N/A')
                example = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('example', 'N/A')
                synonyms = answer[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('synonyms', [])

                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms,
                }
            except requests.exceptions.RequestException as e:
                context = {
                    'form': form,
                    'input': '',
                    'error': 'There was a problem connecting to the dictionary service. Please try again later.'
                }
            except (IndexError, KeyError) as e:
                context = {
                    'form': form,
                    'input': text,
                    'error': 'The word was not found in the dictionary. Please try another word.'
                }
        else:
            context = {'form': form}
    else:
        form = DashboradForm()
        context = {'form': form}
    
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == "POST":
        form = DashboradForm(request.POST)
        text = request.POST['text']
        
        try:
            # Try to fetch the Wikipedia page
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary
            }
        except DisambiguationError as e:
            # Handle disambiguation error
            context = {
                'form': form,
                'error': f'The term "{text}" is ambiguous. It may refer to:',
                'options': e.options,  # List of options to present to the user
            }
        except PageError:
            # Handle page not found error
            context = {
                'form': form,
                'error': f'No page found for "{text}". Please try another query.',
            }
        except Exception as e:
            # Handle any other possible exceptions
            context = {
                'form': form,
                'error': f'An error occurred: {str(e)}',
            }

        return render(request, "dashboard/wiki.html", context)
    else:
        form = DashboradForm()
        context = {
            'form': form,
        }

    return render(request, "dashboard/wiki.html", context)

def conversion(request):
    if request.method =="POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] =='length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer =''
                if input and int(input) >= 0:
                    if first == 'yard' and second=='foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'yard' and second=='yard':
                        answer = f'{input} yard = {input} yard'
                    if first == 'foot' and second=='yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                    if first == 'foot' and second=='foot':
                        answer = f'{input} foot = {input} foot'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        if request.POST['measurement'] =='mess':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer =''
                if input and int(input) >= 0:
                    if first == 'pound' and second=='kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'pound' and second=='pound':
                        answer = f'{input} pound = {input} pound'
                    if first == 'kilogram' and second=='pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                    if first == 'kilogram' and second=='kilogram':
                        answer = f'{input} kilogram = {input} kilogram'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }

    else:
        form = ConversionForm()
        context = {
            'form':form
        }
    return render(request,'dashboard/conversion.html',context)

def register(request):
    if request.method =="POST":
        form = UserRegistrationFrom(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username} successfully !!")
            return redirect('login')
    else:
        form = UserRegistrationFrom()
    context = {
        'form':form
    }
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished =False,user = request.user)
    todos = Todo.objects.filter(is_finished =False,user = request.user)
    if len(homeworks)==0:
        homework_done = True
    else:
        homework_done = False
    if len(todos)==0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todo_done':todo_done
    }
    return render(request,'dashboard/profile.html',context)

def about(request):
    return render(request, 'dashboard/about.html')