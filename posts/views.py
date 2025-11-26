# posts/views.py - ULTRA SIMPLE WORKING VERSION
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from django.http import JsonResponse
from django.core.management import call_command

# Create Post - SIMPLIFIED
@api_view(['POST'])
def create_post(request):
    try:
        print("📝 CREATE POST - Received data:", request.data)
        
        # Create data with defaults
        data = {
            'title': request.data.get('title', '').strip(),
            'description': request.data.get('description', '').strip(),
            'due_date': request.data.get('due_date') or None,
            'priority': request.data.get('priority', 'medium'),
            'status': request.data.get('status', 'pending'),
        }
        
        print("📝 Processed data:", data)
        
        serializer = PostSerializer(data=data)
        
        if serializer.is_valid():
            print("✅ Data is valid")
            instance = serializer.save()
            print(f"✅ Saved instance ID: {instance.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("❌ Validation errors:", serializer.errors)
            return Response(
                {"error": "Validation failed", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        print("💥 CREATE POST ERROR:", str(e))
        import traceback
        print("Traceback:", traceback.format_exc())
        return Response(
            {"error": "Internal server error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# List all Posts - SIMPLIFIED
@api_view(['GET'])
def list_posts(request):    
    try:
        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Update Post
@api_view(['GET', 'PUT'])
def update_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        
        if request.method == 'GET':
            serializer = PostSerializer(post)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete Post
@api_view(['DELETE'])
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({"message": "Post deleted successfully"})
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Run Migrations
@api_view(['GET'])
def run_migrations(request):
    try:
        call_command('makemigrations', 'posts', '--noinput')
        call_command('migrate', 'posts', '--noinput')
        call_command('migrate', '--noinput')
        return JsonResponse({"message": "Migrations completed successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)