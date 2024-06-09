from django.shortcuts import render, redirect
from . import util
import re
import os
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, url_name):
    read_path = './entries'
    file = os.path.join(read_path, url_name + ".md")
    html = util.markdown_conversion(file)
    return render(request, "encyclopedia/entry.html",{
        "content": html,
        "name": url_name
    })

def search(request):
    search_entry = request.GET['q']
    entries = util.list_entries()
    results = []

    if len(search_entry) > 0:
        for entry in entries:

            # if search entry has match, go to that path
            if search_entry.lower() == entry.lower():
                return redirect('/wiki/' + entry)
            
            # create list of possible links for search entry
            if re.findall(search_entry.lower(), entry.lower()):
                results.append(entry)
        
    return render(request, "encyclopedia/search.html", {
        "results": results
    })
        
def create_new_page(request):

    if request.method == "POST":
        form = util.NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            save_path = './entries'
            complete_name = os.path.join(save_path, title + ".md")
            
            try:
                file = open(complete_name, "x")
            except FileExistsError:
                return render(request, "encyclopedia/create_new_page.html", {
                    "pageExists": True
                })
            file.write(content)
            file.close()

            return redirect('/wiki/' + title)
            
    return render(request, "encyclopedia/create_new_page.html", {
        "form": util.NewPageForm()
    })

def edit_page(request, url_name):

    if request.method == "POST":
        form = util.NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            save_path = './entries'
            complete_name = os.path.join(save_path, title + ".md")
            file = open(complete_name, "w")
            file.write(content)
            file.close()

            return redirect('/wiki/' + title)

    return render(request, "encyclopedia/edit_page.html", {
        "form": util.EditPageForm(initial={"title": url_name, "content": util.get_entry(url_name)}, auto_id=False),
        "name": url_name
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)

    return redirect('/wiki/' + title)
