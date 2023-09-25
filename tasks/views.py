# parsing data from the client
from rest_framework.parsers import JSONParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
# API definition for task
from .serializers import TaskSerializer
# Task model
from .models import Info
from .admin import InfoResource
from django.db.models import Q

import calendar, time, json, hashlib, openpyxl, tablib, pandas

from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.conf import settings

import shutil

class ImportView(APIView):
    # import data from data.xlsx
    # authentication_classes = [TokenAuthentication,SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    @csrf_exempt
    def post(self,request):
        info_resource = InfoResource()
        df = pandas.read_excel('data.xlsx',sheet_name='北同医生数据')
        ds = tablib.Dataset()
        data_import = ds.load(df[3:])
        res = info_resource.import_data(data_import, dry_run=True, raise_errors=True)
        if not res.has_errors():
            info_resource.import_data(data_import, dry_run=False)
        else:
            return HttpResponse(status=500)
        print(Info.objects.all())
        return HttpResponse(status=201)

class ExportView(APIView):
    # authentication_classes = [TokenAuthentication,SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    @csrf_exempt
    def post(self,request):
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        book_resource = InfoResource()
        ds = book_resource.export()

        # old df
        df = pandas.read_excel('data.xlsx','北同医生数据') 
        df = df.drop(index=[i for i in range(3,len(df))])

        # new df
        df2 = ds.export('df')
        df2 = df2[list(df2)[1:]]

        df=pandas.concat([df,df2],ignore_index=True)
        print(df)

        shutil.copy2('./data.xlsx','./data.'+str(time_stamp)+'.xlsx')
        from openpyxl import load_workbook

        with pandas.ExcelWriter('./data.xlsx', engine = 'openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer,sheet_name='北同医生数据', index=False)

        return HttpResponse(status=201)
        

@csrf_exempt
def info_detail(request, pk):
    print(pk)
    try:
        # obtain the task with the passed id.
        task = Info.objects.get(pk=pk)
    except:
        # respond with a 404 error message
        return HttpResponse(status=404)  
    if(request.method == 'GET'):
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data, status=201)

def inner_query(request, status):
    keys = request.POST.get('keywords').split(' ')
    q = Q(**{'status': status})

    for k in keys:
        print(k)
        kwa = {
            'name__icontains': k,
            'professionalType__icontains': k,
            'attitudeType__icontains': k,
            'hospital__icontains': k,
            'position__icontains': k,
            'province__icontains': k,
            'city__icontains': k,
            'address__icontains': k,
        }
        dq = Q()
        for k,v in kwa.items():
            dq = dq | Q(**{k:v})
        q = q & dq
    print(q)
    ret = Info.objects.filter(q).values()
    ret_list = []
    for item in ret:
        ret_list.append(item)
    return ret_list

@csrf_exempt
def query(request):
    if(request.method == 'POST'):
        page = request.POST.get('page')
        pages = Paginator(inner_query(request,'active'),10).get_page(page)
        # serialize the task data
        serializer = TaskSerializer(pages, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def item_count(request):
    if(request.method=='POST'):
        return JsonResponse(len(inner_query(request,'active')), safe=False)

@csrf_exempt
def pending_query(request):
    if(request.method=='POST'):
        page = request.POST.get('page')
        pages = Paginator(inner_query(request,'pending'),10).get_page(page)
        serializer = TaskSerializer(pages, many=True)
        return JsonResponse(serializer.data, safe=False)


class AdminSuggestView(APIView):
    # import data from data.xlsx
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    @csrf_exempt
    def suggest(request):
        if(request.method=='POST'):
            di = {
                'name': request.POST.get('name'),
                "hospital": request.POST.get('hospital'),
                "professionalType": '、'.join(request.POST.getlist('professionalType[]')),
                "attitudeType": '、'.join(request.POST.getlist('attitudeType[]')),
                "experience": request.POST.get('experience'),
                "position": request.POST.get('jobQualification'),
                "city": request.POST.get('city'),
                "province": request.POST.get('province'),
                "address": request.POST.get('address'),
                "info": request.POST.get('info'),
                "nickname": request.POST.get('nickname'),
                "contact": request.POST.get('contact'),
                "status": 'active',
            }
            info = Info(**di)
            info.save()
            return JsonResponse({},status=201)


class CustomAuthToken(ObtainAuthToken):
    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })