from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import render
from django.http import JsonResponse

# Create Post.

@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all Posts.
@api_view(['GET'])
def list_posts(request):    
    posts = Post.objects.all().order_by('-id')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


# Update Post.
@api_view(['PUT'])
def update_post(request, pk):       # pk is primary key(id) of the post to be updated.
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete Post.
@api_view(['DELETE'])
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    post.delete()
    return Response({"message": "Post deleted successfully"})


# def detail_post(request, pk):
#     try:
#         post = Post.objects.get(id=pk)
#         data = {
#             "id": post.id,
#             "title": post.title,
#             "description": post.description,
#             "due_date": post.due_date,
#             "priority": post.priority,
#             "status": post.status,
#         }
#         return JsonResponse(data, safe=False)
#     except Post.DoesNotExist:
#         return JsonResponse({"error": "Task not found"}, status=404)
