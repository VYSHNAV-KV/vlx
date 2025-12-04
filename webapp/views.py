from django.dispatch import receiver
from django.shortcuts import render,redirect
from mainapp.models import categorydb,subcategorydb,productdb
from webapp.models import pendingdb,signupdb,myitemdb,Message,cartdb,contactdb
from django.http import JsonResponse
from mainapp.models import productdb,ApprovalMode
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from mainapp.models import productdb
from django.contrib import messages as django_messages
import ast
import razorpay
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.models import AdPending, AdApproved, DailyRate
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required



def home1(request):
    return render(request, 'home1.html')
def home2(request):
    images = AdApproved.objects.all()
    product=productdb.objects.all()
    cat = categorydb.objects.all()
    context = range(0, 4)  # Prepare the range in Python
    messages.success(request, 'Your Product Added successfully!.')

    return render(request, 'home2.html',{'cat':cat,'context':context,'product':product,'images':images})


def search_products(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')  # Minimum price from the form
    max_price = request.GET.get('max_price')  # Maximum price from the form

    # Start with all products
    products = productdb.objects.all()

    # Apply text-based search if query exists
    if query:
        products = products.filter(
            Q(Productname__icontains=query) |
            Q(Categoryname__icontains=query) |
            Q(Subcategoryname__icontains=query) |
            Q(Description__icontains=query)
        )

    # Apply price range filter if provided
    if min_price and max_price:
        products = products.filter(Price__gte=min_price, Price__lte=max_price)

    return render(request, 'search.html',
                  {'products': products, 'query': query, 'min_price': min_price, 'max_price': max_price})



def add_dataform(request):
    user = signupdb.objects.get(Name=request.session['Name'])
    user_name = user.Name
    categories = categorydb.objects.all()
    subcat = subcategorydb.objects.all()

    # Handle AJAX request for subcategories
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        category_name = request.GET.get('category')
        subcategories = subcategorydb.objects.filter(Categoryname=category_name).values('id', 'Subcategoryname')
        return JsonResponse(list(subcategories), safe=False)

    # Handle form rendering and POST request
    if request.method == 'POST':
        category_name = request.POST.get('Categoryname')
        return render(request, "add_dataform.html", {
            'categories': categories,
            'selected_category': category_name,
            'user_name': user_name
        })

    # Render the form for initial GET request
    return render(request, "add_dataform.html", {
        'categories': categories,
        'subcat': subcat,
        'user_name':user_name
    })

# def save_dataform(request):
#     if request.method == "POST":
#         a = request.POST.get('Categoryname')
#         b = request.POST.get('Subcategoryname')
#         c = request.POST.get('Productname')
#         d = request.POST.get('Ownername')
#         e = request.POST.get('Price')
#         f = request.POST.get('Mobile')
#         g = request.POST.get('Location')
#         h = request.POST.get('Description')
#         i = request.FILES['Vehicleimage1']
#         j = request.FILES['Vehicleimage2']
#         k = request.FILES['Vehicleimage3']
#         additional_data = {}
#
#         if a == "Cars":
#             additional_data['fuel_type'] = request.POST.get('fuel_type')
#             additional_data['mileage'] = request.POST.get('mileage')
#         elif a == "Bikes":
#             additional_data['engine_cc'] = request.POST.get('engine_cc')
#
#         product = pendingdb(
#             Categoryname=a,
#             Subcategoryname=b,
#             Productname=c,
#             Ownername=d,
#             Price=e,
#             Mobile=f,
#             Location=g,
#             Description=h,
#             Vehicleimage1=i,
#             Vehicleimage2=j,
#             Vehicleimage3=k,
#             AdditionalData=str(additional_data),
#         )
#         product.save()
#         return redirect(home2)


# def delete_subcategory(request,cat_id):
#     x=subcategorydb.objects.filter(id=cat_id)
#     x.delete()
#     return redirect(display_pending)


def save_dataform(request):
    if request.method == "POST":
        # Fetch form data
        a = request.POST.get('Categoryname')
        b = request.POST.get('Subcategoryname')
        c = request.POST.get('Productname')
        d = request.POST.get('Ownername')
        e = request.POST.get('Price')
        f = request.POST.get('Mobile')
        g = request.POST.get('Location')
        h = request.POST.get('Description')
        i = request.FILES.get('Vehicleimage1')
        j = request.FILES.get('Vehicleimage2')
        k = request.FILES.get('Vehicleimage3')
        l = request.POST.get('Username')

        # Collect additional data for specific categories
        # additional_data = {}

        additional_data = {}

        if a == "Cars":
            additional_data['fuel_type'] = request.POST.get('fuel_type')
            additional_data['mileage'] = request.POST.get('mileage')
            additional_data['transmission'] = request.POST.get('transmission')
            additional_data['engine_capacity'] = request.POST.get('engine_capacity')
            additional_data['number_of_owners'] = request.POST.get('number_of_owners')

        elif a == "Bikes":
            additional_data['engine_cc'] = request.POST.get('engine_cc')
            additional_data['mileage'] = request.POST.get('mileage')
            additional_data['fuel_type'] = request.POST.get('fuel_type')
            additional_data['number_of_owners'] = request.POST.get('number_of_owners')
            additional_data['brand'] = request.POST.get('brand')

        elif a == "Properties":
            additional_data['property_type'] = request.POST.get('property_type')
            additional_data['location'] = request.POST.get('location')
            additional_data['square_feet'] = request.POST.get('square_feet')
            additional_data['number_of_bedrooms'] = request.POST.get('number_of_bedrooms')
            additional_data['number_of_bathrooms'] = request.POST.get('number_of_bathrooms')

        elif a == "Mobiles":
            additional_data['brand'] = request.POST.get('brand')
            additional_data['model'] = request.POST.get('model')
            additional_data['storage_capacity'] = request.POST.get('storage_capacity')
            additional_data['ram'] = request.POST.get('ram')
            additional_data['condition'] = request.POST.get('condition')

        elif a == "Jobs":
            additional_data['job_title'] = request.POST.get('job_title')
            additional_data['company_name'] = request.POST.get('company_name')
            additional_data['location'] = request.POST.get('location')
            additional_data['experience_required'] = request.POST.get('experience_required')
            additional_data['salary'] = request.POST.get('salary')

        elif a == "Electronics and Appliances":
            additional_data['appliance_type'] = request.POST.get('appliance_type')
            additional_data['brand'] = request.POST.get('brand')
            additional_data['power_consumption'] = request.POST.get('power_consumption')
            additional_data['warranty'] = request.POST.get('warranty')
            additional_data['condition'] = request.POST.get('condition')

        elif a == "Vehicle Spare":
            additional_data['part_type'] = request.POST.get('part_type')
            additional_data['compatible_vehicle'] = request.POST.get('compatible_vehicle')
            additional_data['brand'] = request.POST.get('brand')
            additional_data['condition'] = request.POST.get('condition')
            additional_data['manufacture_date'] = request.POST.get('manufacture_date')

        elif a == "Furniture":
            additional_data['furniture_type'] = request.POST.get('furniture_type')
            additional_data['material'] = request.POST.get('material')
            additional_data['dimensions'] = request.POST.get('dimensions')
            additional_data['condition'] = request.POST.get('condition')
            additional_data['age'] = request.POST.get('age')

        elif a == "Fashion":
            additional_data['clothing_type'] = request.POST.get('clothing_type')
            additional_data['brand'] = request.POST.get('brand')
            additional_data['size'] = request.POST.get('size')
            additional_data['material'] = request.POST.get('material')
            additional_data['condition'] = request.POST.get('condition')

        elif a == "Pets":
            additional_data['pet_type'] = request.POST.get('pet_type')
            additional_data['breed'] = request.POST.get('breed')
            additional_data['age'] = request.POST.get('age')
            additional_data['vaccination_status'] = request.POST.get('vaccination_status')
            additional_data['gender'] = request.POST.get('gender')

        elif a == "Sports & Hobbies":
            additional_data['item_type'] = request.POST.get('item_type')
            additional_data['brand'] = request.POST.get('brand')
            additional_data['condition'] = request.POST.get('condition')
            additional_data['usage'] = request.POST.get('usage')
            additional_data['age_of_item'] = request.POST.get('age_of_item')

        elif a == "Services":
            additional_data['service_type'] = request.POST.get('service_type')
            additional_data['experience'] = request.POST.get('experience')
            additional_data['location'] = request.POST.get('location')
            additional_data['pricing'] = request.POST.get('pricing')
            additional_data['contact_info'] = request.POST.get('contact_info')
        # e.g., Weekdays, Weekends

        # Check the approval mode (auto or admin approval)
        approval_mode = ApprovalMode.objects.first()
        if approval_mode and approval_mode.auto_approve:
            # Save directly to productdb if auto approval is on
            product = productdb(
                Categoryname=a,
                Subcategoryname=b,
                Productname=c,
                Ownername=d,
                Price=e,
                Mobile=f,
                Location=g,
                Description=h,
                Vehicleimage1=i,
                Vehicleimage2=j,
                Vehicleimage3=k,
                Username=l,
                AdditionalData=str(additional_data),
            )
            product.save()
            # return JsonResponse({'message': 'Product auto-approved and added successfully!'})
            messages.success(request, 'Your Product Added successfully!.')
            return redirect('home2')
        else:
            # Save to pendingdb if admin approval is required
            pending_product = pendingdb(
                Categoryname=a,
                Subcategoryname=b,
                Productname=c,
                Ownername=d,
                Price=e,
                Mobile=f,
                Location=g,
                Description=h,
                Vehicleimage1=i,
                Vehicleimage2=j,
                Vehicleimage3=k,
                Username=l,
                AdditionalData=str(additional_data),
            )
            pending_product.save()
            # return JsonResponse({'message': 'Product added to pending approvals. Awaiting admin approval.'})
            messages.success(request, 'Product added to pending approvals. Awaiting admin approval.')
            return redirect('home2')
    else:
        # If not a POST request, redirect to home page
        return redirect(home2)
def edit_dataform(request,pro_id):
    product = get_object_or_404(productdb, id=pro_id)
    cat = categorydb.objects.all()
    subcat=subcategorydb.objects.all()
    pro = productdb.objects.get(id=pro_id)
    return render(request, 'edit_dataform.html', {'pro': pro, 'cat': cat,'subcat': subcat,'product':product})

def update_dataform(request,pro_id):
    if request.method=='POST':
        a = request.POST.get('Categoryname')
        b = request.POST.get('Subcategoryname')
        c = request.POST.get('Productname')
        d = request.POST.get('Ownername')
        e = request.POST.get('Price')
        f = request.POST.get('Mobile')
        g = request.POST.get('Location')
        h = request.POST.get('Description')
        try:
            img1=request.FILES['Vehicleimage1']
            fs=FileSystemStorage()
            file1=fs.save(img1.name,img1)
        except MultiValueDictKeyError:
            file1= productdb.objects.get(id=pro_id).Vehicleimage1

        try:
            img2=request.FILES['Vehicleimage2']
            fs=FileSystemStorage()
            file2=fs.save(img2.name,img2)
        except MultiValueDictKeyError:
            file2= productdb.objects.get(id=pro_id).Vehicleimage2

        try:
            img3 = request.FILES['Vehicleimage3']
            fs = FileSystemStorage()
            file3 = fs.save(img3.name, img3)
        except MultiValueDictKeyError:
            file3 = productdb.objects.get(id=pro_id).Vehicleimage3

        productdb.objects.filter(id=pro_id).update(Categoryname=a,Subcategoryname=b,Productname=c,Ownername=d,Price=e,Mobile=f,Location=g,Description=h,Vehicleimage1=file1,Vehicleimage2=file2,Vehicleimage3=file3)
        return redirect(myitem)
def delete_dataform(request,pro_id):
    pro=productdb.objects.filter(id=pro_id)
    pro.delete()
    return redirect(myitem)

def verthe(request):
    pro= productdb.objects.all()
    return render(request, "verthe.html",{'pro':pro})




def fetch_subcategories(request):
    category_name = request.GET.get('category')
    if category_name:
        subcategories = subcategorydb.objects.filter(category__name=category_name)
        subcategory_list = [{"Subcategoryname": sub.Subcategoryname} for sub in subcategories]
        return JsonResponse(subcategory_list, safe=False)
    return JsonResponse([], safe=False)

def signup_page(request):
    return render(request,'signup_page.html')
def signin_page(request):
    return render(request,'signin_page.html')

def save_signup(request):
    if request.method=="POST":
        a = request.POST.get('Name')
        b = request.POST.get('Mobile')
        c = request.POST.get('Email')
        d = request.POST.get('Password')
        e = request.POST.get('Re_password')
        data = signupdb(Name=a, Mobile=b, Email=c, Password=d,Re_password=e)
        if signupdb.objects.filter(Name=a):
            messages.warning(request,"User name already exist")
            return redirect(signin_page)
        elif signupdb.objects.filter(Email=c):
            messages.warning(request,"User name already exist")
            return redirect(signin_page)
        data.save()
        return redirect(signin_page)
def user_login(request):
    if request.method=='POST':
        un=request.POST.get('username')
        pswd=request.POST.get('password')
        if signupdb.objects.filter(Name=un,Password=pswd).exists():
            request.session['Name']=un
            request.session['Password']=pswd
            messages.success(request, "Login successfully...")
            return redirect(home2)

        else:
            messages.error(request, "Invalid")
            return redirect(signin_page)
    else:
        messages.error(request, "Invalid")
        return redirect(signin_page)
def user_logout(request):
    del request.session['Name']
    del request.session['Password']
    messages.success(request,"Logout")
    return redirect(home1)

def myitem(request):
    data=productdb.objects.filter(Username=request.session['Name'])
    data1 = pendingdb.objects.filter(Username=request.session['Name'])
    data2 = cartdb.objects.filter(Username=request.session['Name'])
    number =cartdb.objects.filter(Username=request.session['Name']).count()
    # m=(user_id.Productname)
    # Replace 'user_id' with your session key for user ID


    print(number)
    return render(request,'myitem.html',{'data':data,'data1':data1,'data2':data2,'number':number})


def home3(request):
    cat = categorydb.objects.all()
    context = range(0, 4)  # Prepare the range in Python
    messages.success(request, 'Your Product Added successfully!.')

    return render(request, 'home3.html',{'cat':cat,'context':context})


def subcategory(request, cat_name):
    # Query the subcategory database for the given category name
    data = subcategorydb.objects.filter(Categoryname=cat_name)

    paired_data = zip(data, range(1, len(data) + 1))
    pro=productdb.objects.filter(Categoryname=cat_name)
    return render(request, 'subcategory.html', {'data': data, 'paired_data': paired_data,'pro':pro})

def product_page(request,subcat_name):
    data1 = productdb.objects.filter(Subcategoryname=subcat_name)
    data2= subcat_name
    return render(request,'product_page.html',{'data1':data1,'data2':data2})
# def product_single(request,pro_id,product_id):
#     data=productdb.objects.get(id=pro_id)
#     product = get_object_or_404(productdb, id=product_id)
#     return render(request,"product_single.html",{'data':data,'product':product})
from django.shortcuts import render, get_object_or_404

def product_single(request, pro_id):
    # Cast `pro_id` to int to avoid type mismatches
    data = int(pro_id)

    # Fetch product IDs in the cart for the current user
    product_ids_in_cart = list(
        cartdb.objects.filter(Username=request.session['Name']).values_list('productdb_id', flat=True)
    )

    # Fetch product details
    product = get_object_or_404(productdb, id=pro_id)

    print(type(product.AdditionalData))
    print(product.AdditionalData)

    print("Product IDs in Cart:", product_ids_in_cart)
    a = ast.literal_eval(product.AdditionalData)
    context = a
    print(type(context))
    print(context)

    # Pass the product and cart info to the template
    return render(
        request,
        "product_single.html",
        {
            'context':context,
            'product': product,
            'data': data,
            'product_ids_in_cart': product_ids_in_cart
        }
    )

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import productdb, Message



def send_message(request, product_id):
    product = get_object_or_404(productdb, id=product_id)

    if request.method == 'POST':
        content = request.POST.get('content')  # The message content
        receiver = request.POST.get('receiver')  # Receiver's username from the form
        sender = request.session.get('Name')  # Logged-in user's name from the session
        # if receiver == None:


        # Validation to ensure all required fields are filled
        if not content or not receiver or not sender:
            return render(request, 'message_form.html', {
                'product': product,
                'error': 'All fields are required.',
                'receiver': receiver
            })

        # Create and save the message
        Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            product=product
        )

        # Redirect back to message view with selected sender
        return redirect('message_view', product_id=product.id)

    return render(request, 'message_form.html', {
        'product': product,
        'receiver': product.Username,
    })


# def send_message(request, product_id):
#     if request.method == "POST":
#         product = get_object_or_404(productdb, id=product_id)
#         sender = request.session.get('Name')  # Logged-in user's username
#         receiver = request.POST.get('receiver')  # Receiver's username from the form
#         content = request.POST.get('content')
#
#         # Validate fields
#         if not sender or not receiver or not content:
#             messages.error(request, "All fields are required.")
#             return redirect('message_view', product_id=product_id)
#
#         # Ensure receiver is valid
#         if receiver is None:
#             receiver = product.Username  # Default to the product owner's username
#
#         # Create the message
#         Message.objects.create(
#             sender=sender,
#             receiver=receiver,
#             content=content,
#             product=product,
#         )
#         messages.success(request, "Message sent successfully!")
#         return redirect('message_view', product_id=product_id)
#
#     return redirect(message_view)  # Redirect to product list if the request is not POST









from django.db.models import Q

def message_view(request, product_id):

    product = get_object_or_404(productdb, id=product_id)

    username = request.session.get('Name')  # Logged-in user's username

    # Get all senders for this product
    distinct_senders = Message.objects.filter(product=product).values_list('sender', flat=True).distinct()

    # Filter messages if a specific sender is selected
    selected_sender = request.GET.get('sender')  # Get sender from query params
    if selected_sender:
        messages = Message.objects.filter(
            Q(product=product) &
            (Q(sender=selected_sender, receiver=username) | Q(sender=username, receiver=selected_sender))
        ).order_by('timestamp')
    else:
        messages = None  # No sender selected yet

    return render(request, 'message_view.html', {
        'product': product,
        'messages': messages,
        'senders': distinct_senders,
        'selected_sender': selected_sender,
        'username': username,

    })


# def cart(request):
#     data = cartdb.objects.filter(Username=request.session['Name'])
#     subtotal = 0
#     shipping_amount = 0
#     discount=0
#     total = 0
#     for i in data:
#         subtotal = subtotal + i.Price
#         if subtotal > 50000:
#             shipping_amount = 1000
#         else:
#             shipping_amount = 250
#         discount = int(subtotal * 3 / 100)
#         total = int(shipping_amount + subtotal-discount)
#
#     return render(request,' myitem.html',
#                   {'data': data, 'subtotal': subtotal, 'shipping_amount': shipping_amount, 'total': total,'discount':discount})

def save_cart(request):
    if request.method=="POST":
        a = request.POST.get('Username')
        b = request.POST.get('Productname')
        d = request.POST.get('Price')
        e=request.POST.get('productdb_id')
        data = cartdb(Username=a, Productname=b,Price=d,productdb_id=e)
        data.save()
        return redirect('home2')

def delete_cart(request,cart_id):
    x=cartdb.objects.filter(id=cart_id)
    x.delete()
    return redirect(myitem)








def submit_ad(request):
    if request.method == 'POST':
        username=request.POST['username']
        title = request.POST['title']
        description = request.POST['description']
        duration = int(request.POST['duration'])
        transaction_id = request.POST['transaction_id']
        link=request.POST['link']
        content=request.FILES['content']
        payment_screenshot = request.FILES['payment_screenshot']

        # Fetch the current rate per day
        rate = DailyRate.objects.first().rate_per_day

        amount = rate * duration

        ad = AdPending(
            username=username,
            title=title,
            description=description,
            duration=duration,
            amount=amount,
            transaction_id=transaction_id,
            content= content,
            payment_screenshot=payment_screenshot,
            link=link
        )
        ad.save()
        messages.success(request, "Your ad has been submitted for review.")
        return redirect('home2')

    rate = DailyRate.objects.first().rate_per_day

    return render(request, 'submit_ad.html', {'rate': rate})

def contact(request):
    return render(request,'contact.html')

def save_page(request):
    if request.method=="POST":
        a=request.POST.get('Name')
        b=request.POST.get('Mobile')
        c=request.POST.get('Email')
        d=request.POST.get('Message')
        data=contactdb(Name=a,Mobile=b,Email=c,Message=d)
        data.save()
        return redirect(contact)
def about(request):
    return render(request,'about.html')

def shop(request):
    products = productdb.objects.all()
    liked_products = request.session.get('liked_products', [])
    return render(request, 'shop.html', {'pro': products, 'liked_products': liked_products})

# def save_ad(request):
#     if request.method == "POST":
#         a = request.POST.get('Name')
#         b = request.POST.get('Email')
#         c = request.POST.get('Place')
#         d = request.POST.get('Address')
#         e = request.POST.get('Mobile')
#         f = request.POST.get('Message')
#         g = request.POST.get('Totalprice')
#         data = AdPending(Name=a, Email=b, Place=c, Address=d, Mobile=e, Message=f, Totalprice=g)
#         data.save()
#         return redirect(payment)




# def payment(request):
#     # retrieve the data from orderdb with the specified ID
#     customer=AdPending.objects.order_by('-id').first()
#     # get the payment amount of the specified customer
#     payy=customer.amount
#     # convert the amount into paisa (smallest currency unit)
#     amount= int(payy*100)  # assuming the payment amount in rupees
#     payy_str= str(amount)
#
#     for i in payy_str:
#         print(i)
#     if request.method=="POST":
#         order_currency='INR'
#         client= razorpay.Client(auth=('rzp_test_fis20GTuy931b9','LIVeo1oNh8POcRHvgqT2YGRI'))
#         paymen=client.order.create({'amount':amount,'currency':order_currency})
#     return render(request,"payment.html",{'customer':customer,'payy_str':payy_str })



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
 # Replace with your actual product model

def like_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(productdb, id=product_id)
        user_likes = request.session.get('liked_products', [])

        if product_id in user_likes:
            user_likes.remove(product_id)  # Unlike the product
            liked = False
        else:
            user_likes.append(product_id)  # Like the product
            liked = True

        request.session['liked_products'] = user_likes
        request.session.modified = True  # Ensure session updates
        print(user_likes)
        print(request.session['Name'])

        return JsonResponse({'liked': liked, 'likes_count': len(user_likes)})

    return JsonResponse({'error': 'Invalid request'}, status=400)





