from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ImageUploadSerializer
from django.http import JsonResponse
from .MyLib import main as predict

from django.shortcuts import render

class AjaxAPI(APIView):
    def post(self, request):

        def is_ajax():#ajaxかどうか
            return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        #ペイロードのバリデーション
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid() and is_ajax():#バリデーション通過かつajaxである

            byte_image_data = serializer.validated_data['image']
            kaiouken = serializer.validated_data['kaiouken']

            if kaiouken == None:
                kaiouken = 1

            #予測
            score = predict.Predict(byte_image_data) * kaiouken
            #漢数字追加
            score = predict.number_to_japanese(score)
            #表示する画像作成
            img_str = predict.ImageEncoding(byte_image_data)

            # レスポンスデータの準備
            response_data = {
                'result': 'success',
                'image': img_str,  # Base64エンコードされた画像データ
                'score': score  # 他のデータ
            }
            return JsonResponse(response_data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)#バリデーションが通過できなかった


def main_page(request):

    return render(request, 'main.html', {'IsKaiouken':False})

def main_page_kaiouken(request):

    return render(request, 'main.html', {'IsKaiouken':True})

def reason_page(request):

    return render(request, 'reason.html')