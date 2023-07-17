from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, renderers, status, viewsets
from rest_framework import permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.core import ApiResponse
from app.core.Throttle import BurstRateThrottle, RandomRateThrottle, SustainedRateThrottle
from app.utils import Util
from demo.middlewares import MyMiddleware, my_middleware

from demo.models import Demo
from demo.permissions import IsOwnerOrReadOnly
from demo.serializers import DemoSerializer, UserSerializer

# Create your views here.
@csrf_exempt
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def demo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Demo.objects.all()
        serializer = DemoSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DemoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def demo_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        demo = Demo.objects.get(pk=pk)
    except Demo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DemoSerializer(demo)
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DemoSerializer(demo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        demo.delete()
        return HttpResponse(status=204)

# Function-based view (Restful Api)
@api_view(['GET', 'POST'])
@my_middleware
@MyMiddleware
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def demo_list_api_view(request):
    """
    List all code demos, or create a new demo.
    """
    if request.method == 'GET':
        demos = Demo.objects.all()
        serializer = DemoSerializer(demos, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Relationship
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

##################################### ONLY SHUOLD USE FOR SINGLE TABLE WITH ONE PRIMARY KEY #####################################
# Class-based view (APIs: list & create) => using generics
class DemoListBasedViewClass(generics.ListCreateAPIView):
    queryset = Demo.objects.all()
    serializer_class = DemoSerializer

# Class-based view (detail, update & delete)
class DemoDetailBasedViewClass(generics.RetrieveUpdateDestroyAPIView):
    queryset = Demo.objects.all()
    serializer_class = DemoSerializer


# Class-based view (APIs: list & create) => using APIView class
class DemoCreateListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request: HttpRequest, format=None):
        print(Util.parse_request(request))
        snippets = Demo.objects.all()
        serializer = DemoSerializer(snippets, many=True)
        return ApiResponse.success(serializer.data)

    def post(self, request, format=None):
        serializer = DemoSerializer(data=request.data)
        print(Util.parse_request(request))
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return ApiResponse.success(serializer.data, status=status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors)

class DemoDetailUpdateDeleteAPIView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Demo.objects.get(pk=pk)
        except Demo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """Get demo list

        Args:
            request Request: Request
            pk int: Identity
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            Response: _description_
        """
        snippet = self.get_object(pk)
        serializer = DemoSerializer(snippet)
        return ApiResponse.success(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DemoSerializer(snippet, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return ApiResponse.success(status=status.HTTP_204_NO_CONTENT)
#==============================================================#
class DemoListAPIView(generics.RetrieveAPIView):
    """ List all records """

    # authentication_classes = []
    permission_classes = [IsAuthenticated]
    # throttle_classes = [BurstRateThrottle, SustainedRateThrottle, RandomRateThrottle]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    # throttle_scope = 'list-demo' # only applied for ScopedRateThrottle throttle

    def get(self, request: HttpRequest) -> ApiResponse:
        print(Util.parse_request(request))
        snippets = Demo.objects.all()
        serializer = DemoSerializer(snippets, many=True)
        return ApiResponse.success(serializer.data)

class DemoCreateAPIView(generics.CreateAPIView):
    """ Create record """

    def post(self, request: HttpRequest, *args, **kwargs) -> ApiResponse:
        """ Create new record

        Args:
            request (HttpRequest): Http Request

        Returns:
            ApiResponse: Api Response
        """
        serializer = DemoSerializer(data=request.data)
        print(Util.parse_request(request))
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return ApiResponse.success(serializer.data, status=status.HTTP_201_CREATED)
        return ApiResponse.error(serializer.errors)

class DemoDetailAPIView(generics.RetrieveAPIView):
    """ Get record detail """

    def get_object(self, pk):
        try:
            return Demo.objects.get(pk=pk)
        except Demo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None) -> ApiResponse:
        """Get demo list

        Args:
            request Request: Request
            pk int: Identity
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            Response: _description_
        """
        snippet = self.get_object(pk)
        serializer = DemoSerializer(snippet)
        return ApiResponse.success(serializer.data)

class DemoUpdateAPIView(generics.UpdateAPIView):
    """ Update record """
    def get_object(self, pk):
        try:
            return Demo.objects.get(pk=pk)
        except Demo.DoesNotExist:
            raise Http404

    def put(self, request, pk, *args, **kwargs) -> ApiResponse:
        snippet = self.get_object(pk)
        serializer = DemoSerializer(snippet, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors)

    def patch(self, request, pk, *args, **kwargs) -> ApiResponse:
        snippet = self.get_object(pk)
        serializer = DemoSerializer(snippet, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data)
        return ApiResponse.error(serializer.errors)

class DemoDeleteAPIView(generics.DestroyAPIView):
    """ Delete record """
    def get_object(self, pk):
        try:
            return Demo.objects.get(pk=pk)
        except Demo.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None) -> ApiResponse:
        snippet = self.get_object(pk)
        snippet.delete()
        return ApiResponse.success(status=status.HTTP_204_NO_CONTENT)

################################## END - ONLY SHUOLD USE FOR SINGLE TABLE WITH ONE PRIMARY KEY ##################################
