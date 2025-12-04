from django.shortcuts import render
from .models import CarList, ShowRoomList, Review
from django.http import JsonResponse
from .api_files.serializers import CarSerializer, ShowRoomSerializer, ReviewSerializer
from .api_files.permissions import AdminOrReadOnlyPermission, ReviewUserOrReadOnlyPermission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework import generics, mixins
from rest_framework import viewsets 
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from .api_files.throttling import ReviewDetailThrottle, ReviewListThrottle
from .api_files.pagination import ReviewListPagination 

# views are the funciton which are called by the urls when url matches the urls call these view functions and these functions have all the logic. 

# def car_list_view(request):
#     cars = Carlist.objects.all()
#     data = {
#         'cars':list(cars.values()),
#     }
#     data_json = json.dumps(data)
#     return HttpResponse(data_json, content_type='application/json')
#     # return JsonResponse(data)


# def car_detail_view(request,pk):
#     car = Carlist.objects.get(pk=pk)
#     data = {
#         'name':car.name,
#         'description':car.description,
#         'active':car.active
#     }
#     return JsonResponse(data)


# These are funciton based views. these are the special type of functions which are called the decorators.

@api_view(["GET","POST"])
def car_list_view(request):
    if request.method == "GET":
        cars = CarList.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CarSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors )

@api_view(["GET", "PUT", "DELETE"])
def car_detail_view(request,pk):
    try:
        car = CarList.objects.get(pk=pk)
    except:
        return Response({'Error':'Car not found.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
        serializer = CarSerializer(car)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = CarSerializer(car,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == "DELETE":
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Class based view, in these views you dont have to use decorators and does has to defines the type of method like POST and GET but instead inherit a class having functions abstract functions get and post and you can override them.

class showroom_view(APIView):
    # is you want same authentication and permission for all the classes then insted of writing this code in all the classes you need to apply authentication and permission in settings.py file.
    # authentication_classes = [SessionAuthentication]    # for session authentication you must make the auth path in project url file so that the login pop shows up in the browser.
    # permission_classes = [IsAuthenticated]  # in django permission is reffered to as the authorizatoin. now Is Authenticated is saying who ever is authenticated (signed in) should have all the right.
    # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    def get(self, request):
        showrooms = ShowRoomList.objects.all()
        serializer = ShowRoomSerializer(showrooms, many = True, context = {'request':request})
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = ShowRoomSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class showroomdetial_view(APIView):
    def get(self, request, pk):
        try:
            showroom = ShowRoomList.objects.get(pk = pk)
            serializer = ShowRoomSerializer(showroom, context = {'request':request})
            return Response(serializer.data)
        except showroom.DoesNotExist:
            return Response({'Error':"showroom does not exist"}, status = status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            showroom = ShowRoomList(pk = pk)
            serializer = ShowRoomSerializer(showroom, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except showroom.DoesNotExist:
            return Response({'Error':"showroom does not exist"}, status = status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            showroom = ShowRoomList.objects.get(pk = pk)
            showroom.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except showroom.DoesNotExist:
            return Response({'Error':"showroom does not exist"}, status = status.HTTP_404_NOT_FOUND)
        
# class ReviewDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):  # This is generic views in generic view you dont have to write the code for the get post put and delete methods generec views write code itself it will reduce code writting effort and save time.

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     authentication_classes = [SessionAuthentication]    # for session authentication you must make the auth path in project url file so that the login pop shows up in the browser.
#     permission_classes = [DjangoModelPermissionsOrAnonReadOnly] 

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# Concrete View class, concrete views are the modern form of generic view in which you dont have to even override the CRUD operations view class do it itself. In generic views you may overide the get post and returive funcions if you notices for every new class the get post delete and retrieve funcitons are same here the comes the concrete veiws in concrete even dont have to override the crud funciton just define the class and inherite the funciton class and done it will allow you to do CRUD in three lines of code.
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[ReviewUserOrReadOnlyPermission]
    # throttle_classes = [ReviewDetailThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle] # not needed only throttle_sceope got to be setted here like below if using default from setting.py otherwise both got to be used.
    throttle_scope = 'detail'
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminOrReadOnlyPermission]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle] #throtling means limiting the no of hit which a register and non registered user can make in the applied api. 
    pagination_class = ReviewListPagination 
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(car=pk)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        car = CarList.objects.get(pk=pk)
        useredit = self.request.user
        review_queryset = Review.objects.filter(car = car, apiuser = useredit)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this car.")
        serializer.save(car=car, apiuser = useredit)


# this is the ViewSets Viewset is the class with CRUD functions written in it and you have to override them, the View set are used with the defualt urls so that with only one class both list and reviews url can get combined.
class ReviewViewset(viewsets.ViewSet):

    def list(self, request):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        object = get_object_or_404(queryset, pk = pk)
        serializer = ReviewSerializer(object)
        return Response(serializer.data)
    
    def create(self, request):
        data = request.data
        serializer = ReviewSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def distroy(self, requst, pk):
        try:
            showroom = Review.objects.get(pk = pk)
            showroom.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except showroom.DoesNotExist:
            return Response({'Error':"showroom does not exist"}, status = status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk):
        try:
            showroom = Review(pk = pk)
            serializer = ReviewSerializer(showroom, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except showroom.DoesNotExist:
            return Response({'Error':"showroom does not exist"}, status = status.HTTP_404_NOT_FOUND)


# this is the model view set this is the advancement of view set  the concept is same the only feature is that it minimize your code and write itself you just have to give inherit the model view set class and retieve all objects and serializer class with model view set only with three lines of code you write all CRUD operaions.

class ReviewModelViewSet(viewsets.ModelViewSet): # there are tow varients ReadOnlyModelViewSet it will only give you the list and retireve function while model view set will give you all the CRUD operations.
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer