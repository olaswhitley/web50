import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django import forms


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    

def markdown_conversion(file):
    """
    Converts the content from the markdown file line by line
    into html.
    """
    file = open(file, 'r')
    content = ""
    unordered_list = False
    while True:
        line = file.readline()
        if not line:
            break
        
        # Find and convert link tags from the line
        link_tags = re.findall(r'\[(.+?)\]\((.+?)\)', line)
        for i in link_tags:
            line = re.sub('\[' + i[0] + '\]\(' +i[1] + '\)', '<a href="' + i[1] + '">' + i[0] + '</a>', line)

        # Find and convert strong tags from the line
        strong_tags = re.findall(r'\*{2}(.+?)\*{2}', line)
        for t in strong_tags:
            line = re.sub(r'\*{2}' + t + r'\*{2}', '<strong>' + t + '</strong>', line)

        # Determine if line is start or a continuation of an unordered list
        if re.search("^[*]{1}", line):
            linesplit = re.split("\s", line, 1)
            list_item = linesplit[1].strip()
            if unordered_list == False:
                content = content + "<ul>"
                content = content + "<li>" + list_item.strip() + "</li>"
                unordered_list = True
            else:
                content = content + "<li>" + list_item.strip() + "</li>"

        else:
            # Adds closing tag to unordered list
            if unordered_list == True:
                content = content + "</ul>"
                unordered_list = False

            # Determine if line is a heading
            if re.search("^#", line):
                linesplit = re.split("\s", line, 1)
                heading = linesplit[1].strip()
                heading_size = str(len(re.findall("#", linesplit[0])))
                content = content +"<h" + heading_size + ">" + heading + "</h" + heading_size + ">"

            # Adds paragraph tags to line
            elif not line == "\n":
                content = content + "<p>" + line.strip() + "</p>"

    file.close()

    return content.strip()


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput, label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditPageForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput, initial="class")
    content = forms.CharField(widget=forms.Textarea, label="Content", initial="class")