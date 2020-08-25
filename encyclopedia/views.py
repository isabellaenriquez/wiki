from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    markdowner = Markdown()
    raw_content = util.get_entry(title)
    if (raw_content):
        html_content = markdowner.convert(raw_content)
        return render(request, "encyclopedia/entry_page.html", {
            "title": title,
            "content": html_content
        })
    else: # error
        return render(request, "encyclopedia/error.html", {
            "error_type": "Page Not Found",
            "message": "Your request for\"" + title + "\"does not exist in our database. Please check your query and try again."
        })

def search(request): 
    query = request.GET.get('q')
    # TODO: what if user doesn't enter anything
    result = util.get_entry(query)
    if (result): # query is the name of the exact entry
        return HttpResponseRedirect(reverse("entry_page", args=(query,)))
    else:
        # return list of results that have query as substring

        entries = util.list_entries()
        print(str(entries))
        results = []
        for entry in entries:
            if query in entry:
                results.append(entry)
        return render(request, "encyclopedia/results.html", {
            "results": results,
            "query": query
        })

def create(request):
    if request.method == "POST": # pressed save
        title = request.POST['title']
        if title in util.list_entries():
            # already exists
            return render(request, "encyclopedia/error.html", {
                "error_type": "Page Rewrite Attempt",
                "message": "The page \"" + title + "\" already exists!"
            })
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry_page", args=(title,))) # redirect to new page
    else:
        return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST": # pressed save
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry_page", args=(title,))) # redirect to newly edited page
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": util.get_entry(title)
        })

def random_page(request):
    entries = util.list_entries()
    num = random.randint(0, len(entries) - 1) # choose random number
    chosen_entry = entries[num]
    return HttpResponseRedirect(reverse("entry_page", args=(chosen_entry,))) # redirect to random page