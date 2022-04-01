from django.shortcuts import render, redirect

from customer.models import Carts
from owner.models import Books
from django.views.generic import View,CreateView,ListView
from customer.forms import UserRegistrationForm, LoginForm,PasswordResetForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from customer.decorators import Signin_required
from django.utils.decorators import method_decorator

@method_decorator(Signin_required,name="dispatch")
# Create your views here.
class CustomerIndex(ListView):
    model = Books
    template_name = "custhome.html"
    context_object_name = "books"
   # def get(self, request, *args, **kwargs):
    #    qs = Books.objects.all()
    #    return render(request, "custhome.html", {"books": qs})


class SignUp(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("signin")
    #def get(self, request, *args, **kwargs):
    #    form = UserRegistrationForm()
     #   return render(request, "signup.html", {"form": form})

    #def post(self, request, *args, **kwargs):
      #  form = UserRegistrationForm(request.POST)
      #  if form.is_valid():
        #    form.save()
         #   return redirect("signin")
       # else:
         #   return render(request, 'signup.html', {'form': form})


class SignIn(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "signin.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
              print("login success")
              login(request,user)
              return redirect("custhome")
            else:
              print("login failed")
              return render(request,"signin.html",{"form":form})
@Signin_required

def Signout(request,*arg,**kwargs):
    logout(request)
    return redirect("signin")



@method_decorator(Signin_required,name="dispatch")

class PasswordReset(View):
    def get(self,request):
        form=PasswordResetForm()
        return render(request,'password_reset.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("oldpassword")
            newpassword=form.cleaned_data.get("newpassword")
            user=authenticate(request,username=request.user,password=oldpassword)
            if user:
                user.set_password(newpassword)
                user.save()
                return  redirect("signin")
            else:
                return render(request, 'password_reset.html', {'form': form})
        else:
            return render(request, 'password_reset.html', {'form': form})

@Signin_required

def  Add_to_cart(request,*args,**kwargs):
    book=Books.objects.get(id=kwargs["id"])
    user=request.user
    cart=Carts(product=book,user=user)
    cart.save()
    return redirect("custhome")
@method_decorator(Signin_required,name="dispatch")

class MyCart(ListView):
    model=Carts
    template_name = "mycart.html"
    context_object_name = "carts"

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)





def remove_from_cart(request,*args,**kwargs):
    cart=Carts.objects.get(id=kwargs["id"])
    cart.status="cancelled"
    cart.save()
    return  redirect("custhome")
















