from rest_framework import serializers
from .models import Quiz, Option

# from .models import Article


# class AritcleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     author = serializers.CharField(max_length=100)
#     title = serializers.CharField(max_length=150)
#     content = serializers.CharField(Style = {'base_tamplate': 'textarea.html'})
#     date_created = serializers.DateTimeField()
#     is_public = serializers.BooleanField()

#     def create(self, validated_data):
#         return Article.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         instance.date_created = validated_data.get('date_created', instance.date_created)
#         instance.is_public = validated_data.get('is_public', instance.is_public)
#         return instance


# class Quiz(models.Model):
#     # topic = models.ForeignKey('Topic', related_name='quiz', on_delete=models.CASCADE,)
#     title = models.CharField(max_length=1000)
#     hints = models.CharField(max_length=3000, null=True ,blank=True)
#     is_approved = models.BooleanField(default=False)


#     def __str__(self):
#         return self.title



# class Option(models.Model):
#     quiz = models.ForeignKey('Quiz', related_name='option', on_delete=models.CASCADE,)
#     title = models.CharField(max_length=500)
#     is_correct = models.BooleanField(default=False)
    

#     def __str__(self):
#         return self.title



class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'title')


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'quiz', 'title', 'is_correct')