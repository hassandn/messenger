from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .custompermission import IsOwner


class OTPSignView(APIView):
    """
    برای ثبت نام کاربران است
    نکات:
    1.otp باید برابر با 1234 باشد
    2.اگر کاربر وجود نداشته باشد کاربر ساخته میشود
    3.پسورد پیش فرض برای همه کاربران 1 است
    4.ورودی های مورد نیاز برای ثبت نام به صورت زیر است:
    +احباری
    -phone
    -otp
    +اختیاری
    -username
    -first_name
    -last_name
    -profile_picture
    5.خروجی ها:
    - 201 : در صورت ساخته با موفقیت ساخته شدن کاربر
    - 400 : در صورت وجود کاربر یا ارسال otp اشتباه یا خطاهای دیگر
    
    
        **نمونه درخواست (JSON Input):**
    json
    {
        "phone": "09123456789",
        "otp": "1234",
        "username": "hassan_dn",
        "first_name": "Hassan",
        "last_name": "Dehghan",
        "profile_picture": "profile.jpg"
    }
    """
    
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')
        username = request.data.get('username','')
        first_name = request.data.get('first_name','')
        last_name = request.data.get('last_name','')
        profile_picture = request.FILES.get('profile_picture',None)
        
        user = User.objects.filter(phone=phone).first()
        
        if not user and otp == '1234':
            user = User(phone=phone,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        profile_picture=profile_picture
            )
            user.set_password("1")
            user.save()
            
        
            return Response(
                {'message': 'user created successfully',
                },status=200
            )
        return Response(status=
            400
        )
               
class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['phone','username']
    ordering_fields = ['phone','username']
    ordering = ['-date_joined']
        
    def get(self, request):
        users = User.objects.all()
        
        search_phone =request.GET.get('search', None)
        search_username = request.GET.get('search', None)
        
        if search_username:
            users = users.filter(username=search_username)
        
        if search_phone:
            users = users.filter(phone=search_phone)
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_users = paginator.paginate_queryset(users, request)
        
        serializer = UserSerializer(paginated_users, many=True)
        return Response(
            {'users': serializer.data},
            status=200
        )    
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @csrf_exempt
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise FileNotFoundError(detail = 'user not found')
        
        
        seriliazer = UserSerializer(user)
        return Response(
            {'user': seriliazer.data},
            status=200
        )
  
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated,IsOwner]
    
    @csrf_exempt
    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise FileNotFoundError(detail = 'user not found')
        
        user.username = request.data.get('username', user.username)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.profile_picture = request.FILES.get('profile_picture', user.profile_picture)
        
        user.save()
        
        seriliazer = UserSerializer(user)
        return Response(
            {'user': seriliazer.data},
            status=200
        )
      