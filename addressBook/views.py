from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import AddressBook
from django.http import JsonResponse
from django import forms
from guardian.shortcuts import assign_perm


class DashboardView(View):
    template_name = "dashboard.html"

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {'data': AddressBook.objects.filter(created_by=request.user)})

class EditForm(forms.Form):
    name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=80,required=False)
    email = forms.EmailField(required=False)
    qq = forms.CharField(max_length=11,required=False)


class EditView(View):
    template_name = "edit.html"

    @method_decorator(login_required)
    def get(self, request, pk=0):
        if pk:
            one_record = get_object_or_404(AddressBook,pk=pk)
            return render(request, self.template_name, {'oneRecord': one_record, 'pk': pk, 'title': "修改联系人"})
        return render(request, self.template_name, {'title': '添加联系人'})

    @method_decorator(login_required)
    def post(self, request, pk=0):
        f = EditForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data['name']
            phone = f.cleaned_data['phone']
            email = f.cleaned_data['email']
            qq = f.cleaned_data['qq']
            address = f.cleaned_data['address']
            if pk:
                item = AddressBook.objects.filter(pk=pk)
                if item is None:
                    return JsonResponse({'code': 'failed', 'errors': {'修改失败':'记录不存在'}})
                if (item[0].created_by != request.user) or (request.user.has_perm("change_addressbook",item[0])==False):
                    return JsonResponse({'code': 'failed', 'errors': {'修改失败':'没有权限'}})
                item.update(name=name,phone=phone,email=email,qq=qq,address=address)
                return JsonResponse({'code': 'success', 'info': '修改成功'})
            res = AddressBook.objects.create(name=name,phone=phone,email=email,qq=qq,address=address,created_by=request.user)
            assign_perm('delete_addressbook', request.user, res)
            assign_perm('change_addressbook', request.user, res)
            res.save()

            return JsonResponse({'code': 'success', 'info': '添加成功'})
        return JsonResponse({'code':'failure', 'errors':f.errors})

@login_required()
def Delete(request, pk,*args, **kwargs):
    if request.method == "POST":
        if pk:
            item = AddressBook.objects.filter(pk=pk)
            if item is None:
                return JsonResponse({'code':'failure', 'errors':{'删除失败':'记录不存在'}})
            if (item[0].created_by != request.user) or (request.user.has_perm("delete_addressbook",item[0])==False):
                return JsonResponse({'code': 'failed', 'errors': {'删除失败':'没有权限'}})
            item.delete()
            return JsonResponse({'code': 'success', 'info': '删除成功'})
    return JsonResponse({'code':'failure', 'errors':{'删除失败':'非法请求'}})
