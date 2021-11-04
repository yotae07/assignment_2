from rest_framework import serializers
from apps.products.models import Menu, Item, Tag


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    size = serializers.CharField(max_length=10)
    price = serializers.IntegerField(default=0)
    isSold = serializers.BooleanField(default=False)

    class Meta:
        model = Item
        fields = ['id', 'menu', 'name', 'size', 'price', 'isSold']

    def validate_size(self, value):
        if value not in [Item.L, Item.M, Item.S]:
            raise

        return value

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'menuId': instance.menu_id,
            'name': instance.name,
            'size': instance.size,
            'price': instance.price,
            'isSold': instance.isSold,
        }


class TagSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Tag
        fields = ['id', 'type', 'name', 'menu']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'menuId': instance.menu_id,
            'type': instance.type,
            'name': instance.name,
        }


class MenuSerializer(serializers.ModelSerializer):
    category = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    isSold = serializers.BooleanField(default=False)
    badge = serializers.CharField(max_length=8)
    items = ItemSerializer(required=False, many=True)
    tags = TagSerializer(required=False, many=True)

    class Meta:
        model = Menu
        fields = ['id', 'category', 'name', 'description', 'isSold', 'badge', 'items', 'tags']

    def validate_category(self, value):
        if value not in [Menu.SALAD, Menu.MILK, Menu.EGG]:
            raise

        return value

    def validate_badget(self, value):
        if value not in [Menu.NEW, Menu.OLD]:
            raise

        return value

    def create(self, validated_data):
        items = validated_data.pop('items', None)
        tags = validated_data.pop('tags', None)
        instance = super().create(validated_data)
        if items:
            items_instance = []
            for item_dict in items:
                items_instance.append(
                    Item(
                        name=item_dict.get('name'),
                        size=item_dict.get('size'),
                        price=item_dict.get('price', 0),
                        isSold=item_dict.get('isSold', False),
                        menu=instance
                    )
                )
            Item.objects.bulk_create(items_instance, batch_size=10)
        if tags:
            tags_instance = []
            for tag_dict in tags:
                tags_instance.append(
                    Tag(
                        name=tag_dict.get('name'),
                        type=tag_dict.get('type'),
                        menu=instance
                    )
                )
            Tag.objects.bulk_create(tags_instance, batch_size=10)
        return instance

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'category': instance.category,
            'name': instance.name,
            'description': instance.description,
            'isSold': instance.isSold,
            'badge': instance.badge,
            'items': ItemSerializer(instance.item_set.all(), many=True).data,
            'tags': TagSerializer(instance.tag_set.all(), many=True).data,
        }

    # def create(self, validated_data):
    #     """
    #     We have a bit of extra checking around this in order to provide
    #     descriptive messages when something goes wrong, but this method is
    #     essentially just:
    #
    #         return ExampleModel.objects.create(**validated_data)
    #
    #     If there are many to many fields present on the instance then they
    #     cannot be set until the model is instantiated, in which case the
    #     implementation is like so:
    #
    #         example_relationship = validated_data.pop('example_relationship')
    #         instance = ExampleModel.objects.create(**validated_data)
    #         instance.example_relationship = example_relationship
    #         return instance
    #
    #     The default implementation also does not handle nested relationships.
    #     If you want to support writable nested relationships you'll need
    #     to write an explicit `.create()` method.
    #     """
    #     raise_errors_on_nested_writes('create', self, validated_data)
    #
    #     ModelClass = self.Meta.model
    #
    #     # Remove many-to-many relationships from validated_data.
    #     # They are not valid arguments to the default `.create()` method,
    #     # as they require that the instance has already been saved.
    #     info = model_meta.get_field_info(ModelClass)
    #     many_to_many = {}
    #     for field_name, relation_info in info.relations.items():
    #         if relation_info.to_many and (field_name in validated_data):
    #             many_to_many[field_name] = validated_data.pop(field_name)
    #
    #     try:
    #         instance = ModelClass._default_manager.create(**validated_data)
    #     except TypeError:
    #         tb = traceback.format_exc()
    #         msg = (
    #             'Got a `TypeError` when calling `%s.%s.create()`. '
    #             'This may be because you have a writable field on the '
    #             'serializer class that is not a valid argument to '
    #             '`%s.%s.create()`. You may need to make the field '
    #             'read-only, or override the %s.create() method to handle '
    #             'this correctly.\nOriginal exception was:\n %s' %
    #             (
    #                 ModelClass.__name__,
    #                 ModelClass._default_manager.name,
    #                 ModelClass.__name__,
    #                 ModelClass._default_manager.name,
    #                 self.__class__.__name__,
    #                 tb
    #             )
    #         )
    #         raise TypeError(msg)
    #
    #     # Save many-to-many relationships after the instance is created.
    #     if many_to_many:
    #         for field_name, value in many_to_many.items():
    #             field = getattr(instance, field_name)
    #             field.set(value)
    #
    #     return instance

    # def update(self, instance, validated_data):
    #     raise_errors_on_nested_writes('update', self, validated_data)
    #     info = model_meta.get_field_info(instance)
    #
    #     # Simply set each attribute on the instance, and then save it.
    #     # Note that unlike `.create()` we don't need to treat many-to-many
    #     # relationships as being a special case. During updates we already
    #     # have an instance pk for the relationships to be associated with.
    #     m2m_fields = []
    #     for attr, value in validated_data.items():
    #         if attr in info.relations and info.relations[attr].to_many:
    #             m2m_fields.append((attr, value))
    #         else:
    #             setattr(instance, attr, value)
    #
    #     instance.save()
    #
    #     # Note that many-to-many fields are set after updating instance.
    #     # Setting m2m fields triggers signals which could potentially change
    #     # updated instance and we do not want it to collide with .update()
    #     for attr, value in m2m_fields:
    #         field = getattr(instance, attr)
    #         field.set(value)
    #
    #     return instance
