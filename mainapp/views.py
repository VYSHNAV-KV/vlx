import datetime
from mainapp.models import categorydb,productdb,subcategorydb,ApprovalMode
from webapp.models import pendingdb,signupdb,contactdb
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ApprovalMode
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.models import AdPending, AdApproved, DailyRate
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone




def index(request):
    x = categorydb.objects.count()
    y = productdb.objects.count()
    z= subcategorydb.objects.count()
    date=datetime.datetime.now()
    return render(request,'index.html',{'x':x,'y':y,'z':z,'date':date})

def add_category(request):
    return render(request,'add_category.html')
# def save_category(request):
#     if request.method=="POST":
#         a=request.POST.get('Categoryname')
#         b=request.POST.get('Description')
#         c=request.FILES['Categoryimage']
#         obj=categorydb(Categoryname=a,Description=b,Categoryimage=c)
#         obj.save()
#         return redirect(add_category)
def save_category(request):
    if request.method == "POST":
        try:
            a = request.POST.get('Categoryname')
            b = request.POST.get('Description')
            c = request.FILES['Categoryimage']
            obj = categorydb(Categoryname=a, Description=b, Categoryimage=c)
            obj.save()
            messages.success(request, "Category added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding category: {e}")
        return redirect(add_category)
def display_category(request):
    cat=categorydb.objects.all()
    return render(request,'display_category.html',{'cat':cat})
def edit_category(request,cat_id):
    cat=categorydb.objects.get(id=cat_id)
    return render(request,'edit_category.html',{'cat':cat})
def update_category(request,cat_id):
    if request.method=='POST':
        a=request.POST.get('Categoryname')
        b=request.POST.get('Description')
        try:
            img=request.FILES['Categoryimage']
            fs=FileSystemStorage()
            file=fs.save(img.name,img)
        except MultiValueDictKeyError:
            file= categorydb.objects.get(id=cat_id).Categoryimage
        categorydb.objects.filter(id=cat_id).update(Categoryname=a,Description=b,Categoryimage=file)
        return redirect(display_category)
def delete_category(request,cat_id):
    x=categorydb.objects.filter(id=cat_id)
    x.delete()
    return redirect(display_category)
# Create your views here.

def add_product(request):
    # user = signupdb.objects.get(Name=request.session['Name'])
    user_name = request.user.username
    categories = categorydb.objects.all()
    subcat = subcategorydb.objects.all()
    print(user_name)

    # Handle AJAX request for subcategories
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        category_name = request.GET.get('category')
        subcategories = subcategorydb.objects.filter(Categoryname=category_name).values('id', 'Subcategoryname')
        return JsonResponse(list(subcategories), safe=False)

    # Handle form rendering and POST request
    if request.method == 'POST':
        category_name = request.POST.get('Categoryname')
        return render(request, "add_product.html", {
            'categories': categories,
            'selected_category': category_name,
            'user_name': user_name
        })

    # Render the form for initial GET request
    return render(request, "add_product.html", {
        'categories': categories,
        'subcat': subcat,
        'user_name': user_name
    })

def edit_product(request,pro_id):
    cat=categorydb.objects.all()
    pro=productdb.objects.get(id=pro_id)
    return render(request,'edit_product.html',{'pro':pro,'cat':cat})
    # selected_category = product.Categoryname


# def add_product(request):
#     pro=categorydb.objects.all()
#     return render(request,"add_product.html",{'pro':pro})
# def save_product(request):
#     if request.method=="POST":
#         a=request.POST.get('Categoryname')
#         b=request.POST.get('Vehiclename')
#         c = request.POST.get('Model')
#         d = request.POST.get('Price')
#         e = request.POST.get('Specification')
#         f = request.POST.get('Registration')
#         g = request.POST.get('Company')
#         h = request.FILES['Vehicleimage1']
#         i = request.FILES['Vehicleimage2']
#         j = request.FILES['Vehicleimage3']
#         obj=productdb(Categoryname=a,Vehiclename=b,Model=c,Price=d,Specification=e,Registration=f,Company=g,Vehicleimage1=h,Vehicleimage2=i,Vehicleimage3=j)
#         obj.save()
#         return redirect(add_product)
def save_product(request):
    if request.method == "POST":
        a = request.POST.get('Categoryname')
        b = request.POST.get('Subcategoryname')
        c = request.POST.get('Productname')
        d = request.POST.get('Ownername')
        e = request.POST.get('Price')
        f = request.POST.get('Mobile')
        g = request.POST.get('Location')
        h = request.POST.get('Description')
        i = request.FILES['Vehicleimage1']
        j = request.FILES['Vehicleimage2']
        k = request.FILES['Vehicleimage3']
        additional_data = {}

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
            AdditionalData=str(additional_data),
        )
        product.save()
        return redirect(add_product)


def display_product(request):
    pro=productdb.objects.all()
    return render(request,'display_product.html',{'pro':pro})
# def edit_product(request,pro_id):
#     cat=categorydb.objects.all()
#     pro=productdb.objects.get(id=pro_id)
#     return render(request,'edit_product.html',{'pro':pro,'cat':cat})
def update_product(request,pro_id):
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
        return redirect(display_product)
def delete_product(request,pro_id):
    pro=productdb.objects.filter(id=pro_id)
    pro.delete()
    return redirect(display_product)

def add_subcategory(request):
    subcat=categorydb.objects.all()
    return render(request,'add_subcategory.html',{'subcat':subcat})
def save_subcategory(request):
    if request.method=="POST":
        a=request.POST.get('Categoryname')
        b = request.POST.get('Subcategoryname')
        c=request.POST.get('Description')
        obj=subcategorydb(Categoryname=a,Subcategoryname=b,Description=c)
        obj.save()
        return redirect(add_subcategory)
def display_subcategory(request):
    cat=subcategorydb.objects.all()
    return render(request,'display_subcategory.html',{'cat':cat})
def edit_subcategory(request,cat_id):
    subcat=categorydb.objects.all()
    cat=subcategorydb.objects.get(id=cat_id)
    return render(request,'edit_subcategory.html',{'cat':cat,'subcat':subcat})
def update_subcategory(request,cat_id):
    if request.method=='POST':
        a=request.POST.get('Categoryname')
        b = request.POST.get('Subcategoryname')
        c=request.POST.get('Description')
        # try:
        #     img=request.FILES['Categoryimage']
        #     fs=FileSystemStorage()
        #     file=fs.save(img.name,img)
        # except MultiValueDictKeyError:
        #     file= categorydb.objects.get(id=cat_id).Categoryimage
        subcategorydb.objects.filter(id=cat_id).update(Categoryname=a,Subcategoryname=b,Description=c)
        return redirect(display_subcategory)
def delete_subcategory(request,cat_id):
    x=subcategorydb.objects.filter(id=cat_id)
    x.delete()
    return redirect(display_subcategory)
def login_page(request):
    return render(request,"login.html")
def admin_login(request):
    if request.method=='POST':
        un=request.POST.get('username')
        pswd=request.POST.get('password')
        if User.objects.filter(username__contains=un).exists():
            user=authenticate(username=un,password=pswd)
            if user is not None:
                login(request,user)
                request.session['username']=un
                request.session['password'] = pswd
                return redirect(index)
            else:
                return redirect(login_page)
        else:
            return redirect(login_page)
def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(login_page)
# def user_data(request):
#     data=contactdb.objects.all()
#     return render(request,'user_data.html',{'data':data})
# def delete_data(request,user_id):
#     data=contactdb.objects.filter(id=user_id)
#     data.delete()
#     return redirect(user_data)


def display_pending(request):
    pro=pendingdb.objects.all()
    return render(request,'display_pending.html',{'pro':pro})

def delete_pending(request,cat_id):
    x=pendingdb.objects.filter(id=cat_id)
    x.delete()
    return redirect(display_pending)

# def approve_pending(request, pk):
#     pending_product = get_object_or_404(pendingdb, pk=pk)
#     # Move to productdb
#     productdb.objects.create(
#         Categoryname=pending_product.Categoryname,
#         Subcategoryname=pending_product.Subcategoryname,
#         Productname=pending_product.Productname,
#         Ownername=pending_product.Ownername,
#         Price=pending_product.Price,
#         Mobile=pending_product.Mobile,
#         Location=pending_product.Location,
#         Description=pending_product.Description,
#         Vehicleimage1=pending_product.Vehicleimage1,
#         Vehicleimage2=pending_product.Vehicleimage2,
#         Vehicleimage3=pending_product.Vehicleimage3,
#         AdditionalData=pending_product.AdditionalData,
#     )
#     # Delete from PendingProduct
#     pending_product.delete()
#     return redirect(display_pending)
def approve_pending(request, pk):
    pending_product = get_object_or_404(pendingdb, pk=pk)
    productdb.objects.create(
        Username=pending_product.Username,
        Categoryname=pending_product.Categoryname,
        Subcategoryname=pending_product.Subcategoryname,
        Productname=pending_product.Productname,
        Ownername=pending_product.Ownername,
        Price=pending_product.Price,
        Mobile=pending_product.Mobile,
        Location=pending_product.Location,
        Description=pending_product.Description,
        Vehicleimage1=pending_product.Vehicleimage1,
        Vehicleimage2=pending_product.Vehicleimage2,
        Vehicleimage3=pending_product.Vehicleimage3,
        AdditionalData=pending_product.AdditionalData,
    )
    pending_product.delete()
    return redirect(display_pending)


# mainapp/views.py



# View to render the toggle approval page
# def toggle_approval_mode(request):
#     # Check if the ApprovalMode instance exists
#     mode = ApprovalMode.objects.first()
#     if not mode:
#         # If no ApprovalMode record exists, create a default one
#         mode = ApprovalMode.objects.create(auto_approve=False)
#
#     # Render the toggle.html template and pass the current auto_approve value
#     return render(request, 'toggle.html', {'auto_approve': mode.auto_approve})

# View to handle the POST request when toggling the auto_approve setting

from django.utils import timezone

def toggle_approval_mode(request):
    # Check if the ApprovalMode instance exists
    mode = ApprovalMode.objects.first()
    if not mode:
        # If no ApprovalMode record exists, create a default one
        mode = ApprovalMode.objects.create(auto_approve=False)

    # Handle the POST request when toggling the checkbox
    if request.method == 'POST':
        data = json.loads(request.body)
        auto_approve = data.get('auto_approve', False)

        # Update the auto_approve value and the timestamp
        mode.auto_approve = auto_approve
        mode.save()

        # Convert the time to the local timezone
        updated_at_local = timezone.localtime(mode.updated_at)

        # Return the updated state and last updated timestamp in the correct timezone
        return JsonResponse({
            'message': 'State updated successfully',
            'auto_approve': mode.auto_approve,
            'updated_at': updated_at_local.strftime('%Y-%m-%d %H:%M:%S'),
        })

    # Convert the time to the local timezone for rendering in the template
    last_updated_local = timezone.localtime(mode.updated_at)

    # Render the toggle page with the current approval mode and last updated time
    return render(request, 'toggle.html', {
        'auto_approve': mode.auto_approve,
        'last_updated': last_updated_local.strftime('%Y-%m-%d %H:%M:%S')
    })


def toggle_auto_approval(request):
    if request.method == 'POST':
        # Load the incoming request data
        data = json.loads(request.body)
        auto_approve = data.get('auto_approve', False)

        # Get the first ApprovalMode instance
        mode = ApprovalMode.objects.first()

        if mode:
            # Update the auto_approve field and save the record
            mode.auto_approve = auto_approve
            mode.save()
            return JsonResponse({'message': 'State updated successfully', 'auto_approve': mode.auto_approve})

        return JsonResponse({'message': 'ApprovalMode instance not found.'}, status=400)

    # If not a POST request, just return the current state of auto_approve
    mode = ApprovalMode.objects.first()
    return JsonResponse({'auto_approve': mode.auto_approve})





@staff_member_required
def pending_ads(request):
    ads = AdPending.objects.all()
    return render(request, 'pending_ads.html', {'ads': ads})



@staff_member_required
def approve_ad(request, ad_id):
    ad = get_object_or_404(AdPending, id=ad_id)

    if request.method == 'POST':
        # Move the ad to the approved database
        approved_ad = AdApproved.objects.create(
            username=ad.username,
            title=ad.title,
            description=ad.description,
            duration=ad.duration,
            amount=ad.amount,
            link=ad.link,
            approved_date=date.today(),
            content=ad.content
        )
        approved_ad.save()

        # Delete the pending ad
        ad.delete()

        messages.success(request, "Ad approved successfully!")
        return redirect('admin_pending_ads')

    return render(request, 'approve_ad.html', {'ad': ad})


@staff_member_required
def update_rate(request):
    rate_instance = DailyRate.objects.first()
    if request.method == 'POST':
        new_rate = float(request.POST['rate_per_day'])
        if rate_instance:
            rate_instance.rate_per_day = new_rate
            rate_instance.save()
        else:
            DailyRate.objects.create(rate_per_day=new_rate)
        messages.success(request, "Daily rate updated successfully.")
        return redirect('index')

    return render(request, 'update_rate.html', {'rate': rate_instance.rate_per_day if rate_instance else 10.00})

def user_data(request):
    data=contactdb.objects.all()
    return render(request,'user_data.html',{'data':data})

def delete_data(request,user_id):
    data=contactdb.objects.filter(id=user_id)
    data.delete()
    return redirect(user_data)

