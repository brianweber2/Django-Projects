from rest_framework import serializers

from postings.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
  '''
  Converts to JSON.
  Validations for data passed.
  '''
  url = serializers.SerializerMethodField(read_only=True)

  class Meta:
    model = BlogPost
    fields = [
      # 'pk',
      'id',
      'user',
      'title',
      'content',
      'timestamp',
      'url'
    ]
    read_only_fields = ['id', 'user']

  def get_url(self, obj):
    # Request
    request = self.context.get('request')
    return obj.get_api_url(request=request)

  def validate_title(self, value):
    qs = BlogPost.objects.filter(title__iexact=value) # including isntance
    if self.instance:
      qs = qs.exclude(pk=self.instance.pk)
    if qs.exists():
      raise serializers.ValidationError('This title has already been used')
    return value
