from django import template 
register = template.Library() 
@register.filter
def to_image(i): 
    ans="images/"+str(i)+".jpg"
    return ans
