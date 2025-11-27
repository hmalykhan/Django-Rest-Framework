from rest_framework import serializers
from ..models import CarList, ShowRoomList, Review
#             raise ValidationError("Only alphanumeric characters are allowed.")

# These are the normal serializers, serializers atutomatically converts the data in the json format which you can send through api.

# class CarSerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField(read_only = True)
#     chassisnumber = serializers.CharField(validators = [alphanumeric])
#     price = serializers.DecimalField(max_digits=9, decimal_places=2)

#     def create(self, validation_data):
#         return Carlist.objects.create(**validation_data)

#     def update(self, instance, validation_data):
#         instance.name = validation_data.get('name',instance.name)
#         instance.description = validation_data.get('description',instance.description)
#         instance.active = validation_data.get('active',instance.active)
#         instance.chassisnumber = validation_data.get('chassisnumber',instance.chassisnumber)
#         instance.price = validation_data.get('price', instance.price)
#         instance.save()
#         return instance

# These are model serializers, these serializers extends the funciton of normal serializer but extra feature is yout dont have to define each field but instead it will do itself map the fields from the model class
# abd automatically defines them.

class ReviewSerializer(serializers.ModelSerializer):
    apiuser = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('car',)
        # fields = "__all__"

class CarSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    Reviews = ReviewSerializer(many=True, read_only = True) # this is the nested serialization in nested serializaiton the name must be the same which has been set while creating the model and defining the relation (ForiegnKeyField) in related_name = "Reviews".
    class Meta:
        model = CarList
        fields = "__all__"  # take all fields.
        # fields = ['name', 'description', 'chassisnumber']   # take these fields.
        # exclude = ['name', 'price', 'description']  # take the rest of all feilds but exclude these ones.
    
    def get_discounted_price(self, object):
        if object.price != None:
            object.price = object.price - 5000
        return object.price

    def validate_price(self, value):
        if value <= 20000.00:
            raise serializers.ValidationError("price must be greator than 20000.00")
        return value
    
    def validate(self, data):
        if data['name']  == data['description']:
            raise serializers.ValidationError("Name and description must be different.")
        return data

class ShowRoomSerializer(serializers.ModelSerializer):
    # Showrooms = CarSerializer(many = True, read_only = True)  # this is the nested serializer basically this is the relation which says showroom can have multiple objects of carlist in readonly mode.
    # Showrooms = serializers.StringRelatedField(many=True)   # this is string related field it will print exactly what you have overirdes the string __str__ funciton in carlist insteald of whole object of carlist.
    # Showrooms = serializers.PrimaryKeyRelatedField(many = True, read_only = True)   # this is the primary related field it will print the id's if each carlist object instead of whole object.
    Showrooms = serializers.HyperlinkedRelatedField(many = True, read_only = True, view_name="car_detail")
    class Meta:
        model = ShowRoomList
        fields = "__all__"

