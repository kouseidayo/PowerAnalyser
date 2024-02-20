from rest_framework import serializers
from PIL import Image
from io import BytesIO

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
    kaiouken = serializers.IntegerField(min_value=1, max_value=100, required=False)

    def validate_image(self, value):
        # 画像データを読み込む
        image_data = value.read()
        
        # 画像として開けるかどうかを確認
        try:
            image = Image.open(BytesIO(image_data))
            image.verify()  # 画像の有効性を検証
        except Exception as e:
            raise serializers.ValidationError("無効な画像です。")

        return image_data  # バリデーションを通過した場合は、値を返す
    
    def validate_param(self, data):
        kaiouken = data.get('kaiouken')

        if kaiouken is not None:
            if kaiouken > 100 or kaiouken < 0:
                raise serializers.ValidationError("正しい倍率を指定してください")

        return data