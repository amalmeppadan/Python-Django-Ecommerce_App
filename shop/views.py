from django.http import  JsonResponse
from django.shortcuts import redirect, render
from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

def index(request):
     products=Products.objects.filter(trending=1)
     return render(request,'shop/index.html',{'products':products})


   
def delete_fav(request,fid):
    favitem=Favour.objects.get(id=fid)
    favitem.delete()
    return redirect('favviewpage')


def delete_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('cart')



def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',{'cart':cart})

    else:
        return redirect('index')
    


def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favour.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("index")


def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Products.objects.get(id=product_id)
      if product_status:
         if Favour.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favour.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
    





def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
         
              data = json.loads(request.body)
              product_qty=(data['product_qty'])
              product_id=(data['pid'])
             # print(request.user.id)
              product_status=Products.objects.get(id=product_id)
              if product_status:
                  if Cart.objects.filter(user=request.user.id,product_id=product_id):
                       return JsonResponse({'status': 'Product already in cart'}, status=200)
                  else:
                      if product_status.quantity>=product_qty:
                          Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                          return JsonResponse({'status': 'Product added to cart'}, status=200)
                      else:
                          return JsonResponse({'status': 'Product stock not available'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
            
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
        

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully..")
        return redirect('/')
    

def login_page(request):
  if request.user.is_authenticated:
      return redirect('index')
  else:
    if request.method =='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      print(f"username:{name}")
      print(f"password: {pwd}")

                                        
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("index")
      else:
        messages.error(request,"Invalid User Name or Password")                                                
        return redirect("login")
      
    return render(request,"shop/login.html")
  

def register(request):
    form=CustomUserForm()
    if request.method == 'POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1') 
            print(f"username:{username}")
            print(f"password1:{password1}")
            form.save()
            messages.success(request,"registration success,now you can Login!!")
            return redirect('login')

        else:
            messages.warning(request,'error found')

    
    return render(request,'shop/register.html',{'form':form})

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,'shop/collections.html',{'catagory':catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(status=0,name=name)):
        products=Products.objects.filter(category__name=name)
        return render(request,'shop/product/collectionsview.html',{'products':products,'category_name':name})
    else:
        messages.warning(request,"No such catagory found!!")
        return redirect('collection')
        
def product_details(request,cname,pname):
    if Catagory.objects.filter(name=cname,status=0):
        if Products.objects.filter(name=pname,status=0):
            products=Products.objects.filter(name=pname,status=0).first()
            return render(request,'shop/product/product_details.html',{'products':products})

        else:
          messages.warning('No such product Found')
          return redirect('collections')
    else:
         messages.warning('No such Catagory Found')
         return redirect('collections') 

     
      