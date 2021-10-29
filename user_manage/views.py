from django.shortcuts import redirect, render

from django.http import HttpResponseRedirect
from .forms import fileUploaded,RegisterForm
from django.contrib.auth.models import User,auth
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout
from .models import fileUpload,comment,uploadExcel
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse,reverse_lazy
import pandas as pd
from .resources import uploadExcelResources
from tablib import Dataset
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')


# submitted = False
#    if request.method == 'POST':
#         user_data = request.POST

#         form = userForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/register?submitted=True')
#     else:
#         form = userForm
#         if 'submitted' in request.GET:
#             submitted = True
def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')

def registerUser(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        c_password = request.POST['c_password']
        passwordRegex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$'
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        pat = re.compile(password)
        # searching regex
        mat = re.search(pat, password)
        regularExpression = "^[A-Za-z][A-Za-z0-9_]{7,29}$"
        # validating conditions
        if mat:
            if re.fullmatch(regularExpression, username):
                if password == c_password:
                    if not User.objects.filter(username=username):
                        user = User.objects.create_user(username = username, email = email, first_name = first_name, last_name = last_name, password = password)
                        user.save()
                        
                        result = 'SignUp Successful'
                    else:
                        result = 'Username Exists'
                else:
                    result = 'Password Not Matching'
            else:
                result = 'Username incorrect'
        else:
            result = 'Invalid Password Type'
    else:
        return render(request, 'register.html')

                

        

    return render(request, 'register.html',{'result':result})



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect(dashboard)
        else:
            return render(request, 'login.html',{'result':'Invalid Credentials'})

    else:
        return render(request,'login.html')


@login_required(login_url='/login/')
def dashboard(request):
    current_user = request.user
   
    done = False
    result = {'result': 'Upload a file'}
    print('In dashboard')
    context = {}
    context['form'] = fileUploaded
    print(context)
    
    
    if 'done' in request.GET:
        result = {'result': 'File uploaded successfully'}
    
    data = uploadExcel.objects.all().order_by('id')
    for i in data.reverse():
        print(i.id)
    
    context['data'] = data
    return render(request, "dashboard.html", context)
    



def user_logout(request):
    logout(request)
    return redirect(login)
  

def uploadFile(request):
    current_user = request.user
    user_id = User.objects.get(username=current_user.username)
    user_id.is_superuser = True
    user_id.is_staff = True
    print(user_id.is_staff,user_id.is_superuser)
    doc = request.FILES  # returns a dict-like object
    data = fileUpload(user=user_id,file = doc['file'])
    data.save()
    result = ''
    print(type(user_id),doc['file'])
    return HttpResponseRedirect('/dashboard?done=True')



def user_create(request):
    print('inside usercreate')
    result = False
    context = {}
    if request.method == 'POST':
        print('inside now post')
        user_form  = RegisterForm(request.POST)
        errors = user_form.errors
        print(errors)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect('/user_create?done=True')
        else:
            context['error'] = user_form.errors
            for i in context['error']:
                print(context['error'][i])
            print("not  really correct")
    else:
        user_form = RegisterForm()
        if 'done' in request.GET:
            result = 'Sign Up Succesful'
        context = {'form': user_form, 'result': result}
    
    return render(request, 'registernew.html', context)


def likepost(request,id):
    file_obj = fileUpload.objects.get(id=id)
    file_obj.file_like.add(request.user)
    file_obj.save()
    return HttpResponseRedirect(reverse('dashboard'))

def addcomment(request,id):
    current_user = request.user
    user_id = User.objects.get(username=current_user.username)
    file_obj = fileUpload.objects.get(id=id)
    if request.method == 'POST':
        body = request.POST['comment']
        comment_data = comment(from_user=user_id,body=body,file=file_obj)
        comment_data.save()

    return HttpResponseRedirect(reverse('dashboard'))

def uploadExcelFile(request):
    if request.method == 'POST':
        doc = request.FILES  # returns a dict-like object
        file = doc['file']
        file_resource = uploadExcelResources()
        dataset = Dataset()
        imported_data = dataset.load(file.read(),format='xlsx')
        if uploadExcel.objects.all():
            df_data = pd.DataFrame(list(uploadExcel.objects.all().values()))
            df_new =  pd.read_excel(file)
            # print(df_data.drop([df_data.columns[0]],axis=1) == df_new.drop([df_new.columns[0]],axis=1))
            # print('columns:',df_new.columns,df_data.columns)
            d1 = df_data.drop([df_data.columns[0]],axis=1)
            d2 = df_new.drop([df_new.columns[0]],axis=1)
            if d1.columns.equals(d2.columns):
                
                if (d1.equals(d2)):
                    print(True)
                else:
                    df_check = d1 == d2
                    print(df_check)
                    listOfPos = list()
                    # Get bool dataframe with True at positions where the given value exists
                    result = df_check.isin([False])
                    # Get list of columns that contains the value
                    seriesObj = result.any()
                    columnNames = list(seriesObj[seriesObj == True].index)
                    # Iterate over list of columns and fetch the rows indexes where value exists
                    for col in columnNames:
                        rows = list(result[col][result[col] == True].index)
                        for row in rows:
                            listOfPos.append((row, col))
                    print(listOfPos)
                    # for i in listOfPos:
                    #     col = i[1] 
                    #     print(d2.loc[i[0],i[1]])
                    #     uploadExcel.objects.filter(id=i[0]).update('{0}'.format(col) = d2.loc[i[0],i[1]] )
                    for data in imported_data:
                        value = uploadExcel(id=data[0],field_a=data[1], field_b=data[2], field_c=data[3],field_d=data[4])
                        value.save()     
        else:
            for data in imported_data:
                value = uploadExcel(id=data[0],field_a=data[1], field_b=data[2], field_c=data[3],field_d=data[4])
                value.save()   
    
    return HttpResponseRedirect('/dashboard?done=True')


@api_view(['GET', 'POST'])
def upload_file(request):

    if request.method == 'POST':
        file = request.data.get('file')
        dataset = Dataset()

        imported_data = dataset.load(file.read(),format='xlsx')

        df_data = pd.DataFrame(list(uploadExcel.objects.all().values()))
        df_new =  pd.read_excel(request.data.get('file'))

        
        d1 = df_data.drop([df_data.columns[0]],axis=1)
        d2 = df_new.drop([df_new.columns[0]],axis=1)

        if d1.columns.equals(d2.columns):
            if (d1.equals(d2)):
                print(True)
                message='nothing to update in data'
            else:
                df_check = d1 == d2
                print(df_check)
                listOfPos = list()
                # Get bool dataframe with True at positions where the given value exists
                result = df_check.isin([False])
                # Get list of columns that contains the value
                seriesObj = result.any()
                columnNames = list(seriesObj[seriesObj == True].index)
                # Iterate over list of columns and fetch the rows indexes where value exists
                for col in columnNames:
                    rows = list(result[col][result[col] == True].index)
                    for row in rows:
                        listOfPos.append((row, col))
                print(listOfPos)

                # for i in listOfPos:
                #     col = i[1] 
                #     print(d2.loc[i[0],i[1]])
                #     uploadExcel.objects.filter(id=i[0]).update('{0}'.format(col) = d2.loc[i[0],i[1]] )
                
                for data in imported_data:
                    value = uploadExcel(id=data[0],field_a=data[1], field_b=data[2], field_c=data[3],field_d=data[4])
                    value.save()     
                message='data updated'
        else:
            for data in imported_data:
                value = uploadExcel(id=data[0],field_a=data[1], field_b=data[2], field_c=data[3],field_d=data[4])
                value.save()  
                message='data added'
        
        #exporting
        data_resource = uploadExcelResources()
        dataset = data_resource.export()
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="persons.xls"'

        return response

        