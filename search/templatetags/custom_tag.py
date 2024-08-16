from django import template
register = template.Library()

@register.simple_tag()
def tag_checked(request, tag_id):
    
    tags = request.GET.getlist("tag")

    if str(tag_id) in tags:
        return "checked"