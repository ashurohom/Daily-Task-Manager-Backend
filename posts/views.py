# posts/views.py 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from django.http import JsonResponse
from django.core.management import call_command
import traceback

# Create Post
# posts/views.py - ENHANCED ERROR LOGGING
@api_view(['POST'])
def create_post(request):
    try:
        print("📝 CREATE POST - Received data:", request.data)
        print("📝 Data types:", {k: type(v) for k, v in request.data.items()})
        
        # Validate required fields
        if not request.data.get('title'):
            return Response(
                {"error": "Title is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            print("✅ Data is valid, saving...")
            instance = serializer.save()
            print(f"✅ Saved instance ID: {instance.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("❌ Validation errors:", serializer.errors)
            return Response(
                {
                    "error": "Validation failed",
                    "details": serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        print("💥 CREATE POST ERROR:", str(e))
        print("Traceback:", traceback.format_exc())
        return Response(
            {
                "error": "Internal server error",
                "message": str(e)
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# List all Posts
@api_view(['GET'])
def list_posts(request):    
    try:
        print("📋 LIST POSTS - Fetching all posts")
        posts = Post.objects.all().order_by('-id')
        print(f"✅ Found {len(posts)} posts")
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        print("💥 LIST POSTS ERROR:", str(e))
        print("Traceback:", traceback.format_exc())
        return Response(
            {"error": str(e), "detail": "Internal server error in list_posts"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Update Post - GET for fetching, PUT for updating
@api_view(['GET', 'PUT'])
def update_post(request, pk):
    try:
        print(f"🔄 UPDATE POST - ID: {pk}, Method: {request.method}")
        post = Post.objects.get(pk=pk)
        
        if request.method == 'GET':
            # Return task data for editing
            serializer = PostSerializer(post)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            # Update task data
            print("📝 PUT - Received data:", request.data)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Post.DoesNotExist:
        print(f"❌ UPDATE POST - Post {pk} not found")
        return Response(
            {"error": f"Post with id {pk} not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print("💥 UPDATE POST ERROR:", str(e))
        print("Traceback:", traceback.format_exc())
        return Response(
            {"error": str(e), "detail": "Internal server error in update_post"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Delete Post
@api_view(['DELETE'])
def delete_post(request, pk):
    try:
        print(f"🗑️ DELETE POST - ID: {pk}")
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({"message": "Post deleted successfully"})
        
    except Post.DoesNotExist:
        print(f"❌ DELETE POST - Post {pk} not found")
        return Response(
            {"error": f"Post with id {pk} not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print("💥 DELETE POST ERROR:", str(e))
        print("Traceback:", traceback.format_exc())
        return Response(
            {"error": str(e), "detail": "Internal server error in delete_post"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Run Migrations
@api_view(['GET'])
def run_migrations(request):
    try:
        print("🔄 Running migrations...")
        call_command('makemigrations', 'posts', '--noinput')
        call_command('migrate', 'posts', '--noinput')
        call_command('migrate', '--noinput')
        return JsonResponse({"message": "Migrations completed successfully!"})
    except Exception as e:
        print("💥 MIGRATION ERROR:", str(e))
        return JsonResponse({"error": str(e)}, status=500)