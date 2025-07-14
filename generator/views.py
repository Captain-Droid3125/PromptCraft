from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from generator.langgraph_flow import build_graph
import traceback


class ImageGenerationView(APIView):
    def post(self, request):
        # print("Received request to generate image", request.data)
        prompt = request.data.get("prompt")

        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            flow = build_graph()
            # print("Flow built successfully")
            result  = flow.invoke({"prompt":prompt})
            # print("Flow execution result:", result)
            # return Response(result["output"], status=status.HTTP_200_OK)
            image_bytes = result["output"].get("image_bytes")
            response=HttpResponse(image_bytes, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="generated_image.png"'
            return response
        
        except Exception as e:
            # print("Error during image generation:", str(e))
            traceback.print_exc() 
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
def index(request):
    return render(request, 'index.html')