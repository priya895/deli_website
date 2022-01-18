from django import forms
 
class create(forms.Form):
    title = forms.CharField(label='title', max_length= 64)
    description =forms.CharField(label= 'description', max_length=64)
    img= forms.URLField(label="Image Url")
    bid= forms.IntegerField(label= "Starting bid")
    

class comments(forms.Form):
    comment= forms.CharField(label= "comment",max_length= 1000)


"""from django import forms

# Create your models here.

class QuestionPostForm(forms.Form):
    question = forms.CharField(label='Question text', max_length=1000)
    tag = forms.CharField(label='Tags', max_length=200)
    pub_date = forms.DateTimeField(label='Date published')


class AnswerPostForm(forms.Form):
    answer_text = forms.CharField(label='Answer Text', max_length=1000)
    answer_rate = forms.IntegerField(label='Rate')///"""