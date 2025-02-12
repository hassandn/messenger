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
        phone = request.data.get("phone")
        otp = request.data.get("otp")
        username = request.data.get("username", "")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        profile_picture = request.FILES.get("profile_picture", None)

        user = User.objects.filter(phone=phone).first() # get user by phone number

        if not user and otp == "1234": # check if user not exist and otp is correct
            user = User(
                phone=phone,
                username=username,
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture,
            )
            user.set_password("1") # set default password
            user.save()

            return Response(
                {
                    "message": "user created successfully",
                },
                status=200,# return 200 status code
            )
        return Response(status=400)# return 400 status code


class UserListView(APIView):
    """
    این API برای نمایش لیست کاربران استفاده می‌شود.

    نکات:
    1. دسترسی فقط برای کاربران احراز هویت شده ممکن است.
    2. قابلیت جستجو بر اساس `phone` و `username` وجود دارد.
    3. امکان مرتب‌سازی لیست بر اساس `phone` و `username` فراهم شده است.
    4. کاربران بر اساس `date_joined` به‌صورت پیش‌فرض به ترتیب نزولی مرتب می‌شوند.
    5. داده‌ها به‌صورت صفحه‌بندی شده برگردانده می‌شوند (هر صفحه شامل ۱۰ کاربر است).

    **نمونه درخواست (Query Parameters - Optional):**
    ```
    GET /api/users/?search=username_example
    GET /api/users/?ordering=phone
    GET /api/users/?ordering=-username
    ```
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["phone", "username"]
    ordering_fields = ["phone", "username"]
    ordering = ["-date_joined"]

    def get(self, request):
        users = User.objects.all()

        search_phone = request.GET.get("search", None)# get search_phone from query parameters
        search_username = request.GET.get("search", None)# get search_username from query parameters

        if search_username:# check if search_username is not None
            users = users.filter(username=search_username)

        if search_phone:# check if search_phone is not None
            users = users.filter(phone=search_phone)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = UserSerializer(paginated_users, many=True)
        return Response({"users": serializer.data}, status=200)


class UserDetailView(APIView):
    """
     این API برای دریافت جزئیات یک کاربر خاص بر اساس `id` استفاده می‌شود.

    نکات:
    1. دسترسی فقط برای کاربران احراز هویت شده ممکن است.
    2. مقدار `id` کاربر به‌عنوان پارامتر در URL ارسال می‌شود.
    3. در صورت یافت نشدن کاربر، پاسخ `404 Not Found` برگردانده می‌شود.

    **نمونه درخواست (Request):**
    ```
    GET /api/users/1/
    ```
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:# try to get user by id
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise FileNotFoundError(detail="user not found")

        seriliazer = UserSerializer(user)
        return Response({"user": seriliazer.data}, status=200)


class UserUpdateView(APIView):
    """
    بروزرسانی اطلاعات یک کاربر بر اساس شناسه (ID).

    نکات:
    1. تنها مالک حساب کاربری می‌تواند اطلاعات خود را تغییر دهد.
    2. در صورت عدم وجود کاربر، خطای 404 بازگردانده می‌شود.
    3. فیلدهای `username`، `first_name`، `last_name` و `profile_picture` قابل بروزرسانی هستند.

    نمونه درخواست:
    ```json
    {
        "username": "new_username",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "file"
    }
    ```
    """

    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise FileNotFoundError(detail="user not found")

        user.username = request.data.get("username", user.username)
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.profile_picture = request.FILES.get(
            "profile_picture", user.profile_picture
        )

        user.save()

        seriliazer = UserSerializer(user)
        return Response({"user": seriliazer.data}, status=200)
