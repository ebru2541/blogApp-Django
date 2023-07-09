from rest_framework import serializers
from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = []

#? bu haliyle olursa user ve category nin sadece id si olur
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         exclude = []

#! nested serializer
class PostSerializer(serializers.ModelSerializer):
    #? user ın str ve id si yazar
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField()

    #? category ın str ve id si yazar
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()

    class Meta:
        model = Post
        exclude = [
            # 'created_date',
            # 'updated_date',
        ]