from rest_framework import serializers
from django.contrib.auth.models import User
class RegisterSerializer(serializers.ModelSerializer):
    confirmation_password = serializers.CharField(style={"input_type":'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmation_password']
        extra_kwargs = {"password":{"write_only":True}}

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['confirmation_password']
        
        if password != password2:
            raise serializers.ValidationError({'error':'passwords are not same.'})
        if User.objects.filter(username = self.validated_data['username']).exists():
            raise serializers.ValidationError({'error':'username already exists.'})
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'email already exists.'})
        account = User(username = self.validated_data['username'], email = self.validated_data['email'])
        account.set_password(password)
        account.save()
        return account