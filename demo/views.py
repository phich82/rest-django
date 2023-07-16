from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, renderers, status, viewsets
from rest_framework import permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
class DemoListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Demo.objects.all()
        serializer = DemoSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DemoDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Demo.objects.get(pk=pk)
        except Demo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DemoSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DemoSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
################################## END - ONLY SHUOLD USE FOR SINGLE TABLE WITH ONE PRIMARY KEY ##################################


class DemoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Demo.objects.all()
    serializer_class = DemoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    #@action(url_path='/highlight', detail=True, renderer_classes=[renderers.StaticHTMLRenderer], methods=['GET'])
    @action(url_path='highlight', url_name='highlight', detail=False, methods=['GET'])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        print(snippet)
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)