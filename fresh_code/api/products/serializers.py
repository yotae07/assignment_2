from rest_framework import serializers
from apps.products.models import Menu, Item, Tag


class ItemSerializer(serializers.ModelSerializer):
    # 이런 형태로 필드를 선언하면 마치 models에 필드 제약을 설정하는것처럼 설정할 수 있습니다.
    # models에 선언하는것과 차이는 models에 선언할시 DB에 제약을 반영되어야만 제약이 설정가능하지만
    # serializer에 선언시 코드단에서 제약을 바로 걸거나 해제할 수 있습니다.
    name = serializers.CharField(max_length=50)
    size = serializers.CharField(max_length=10)
    price = serializers.IntegerField(default=0)
    isSold = serializers.BooleanField(default=False)

    class Meta:
        model = Item
        # fields 목록에 models에 있는 필드 이름보다 더 선언해도 되고 안해도 됩니다. 몇가지 필드들을 제외하곤 명시되어야만 평가됩니다.
        fields = ['id', 'menu', 'name', 'size', 'price', 'isSold']

    # validate_필드명 형태로 하면 특정 필드에 대해서만 validate 체크가 가능합니다.
    def validate_size(self, value):
        if value not in [Item.L, Item.M, Item.S]:
            raise

        return value

    # 이렇게 작성해놓을시 Item object들을 호출할시 밑에 명시된 형태로 나가게 됩니다.
    # 만약 사용하지 않을시 Meta클래스에 fields에 정의된 값들만 serializer 혹은 model에 적힌 형태로 나가게됩니다.
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
            # 대량생성을위해 bulk를 사용했습니다.
            # 기존의 create사용시 단일생성만 되지만 bulk 사용시 여러개를 생성할 수 있습니다.
            # batch_size 옵션시 명시된 갯수만큼 끊어서 생성하는 작업을 하게됩니다. ex) 100개 생성시 10개씩*10번
            # batch_size가 존재하는 이유는 DB의 트랜잭션이 장시간 걸릴 경우 성능의 문제가 있기 때문입니다.
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
    #
    # def save(self, **kwargs):
    #     assert hasattr(self, '_errors'), (
    #         'You must call `.is_valid()` before calling `.save()`.'
    #     )
    #
    #     assert not self.errors, (
    #         'You cannot call `.save()` on a serializer with invalid data.'
    #     )
    #
    #     # Guard against incorrect use of `serializer.save(commit=False)`
    #     assert 'commit' not in kwargs, (
    #         "'commit' is not a valid keyword argument to the 'save()' method. "
    #         "If you need to access data before committing to the database then "
    #         "inspect 'serializer.validated_data' instead. "
    #         "You can also pass additional keyword arguments to 'save()' if you "
    #         "need to set extra attributes on the saved model instance. "
    #         "For example: 'serializer.save(owner=request.user)'.'"
    #     )
    #
    #     assert not hasattr(self, '_data'), (
    #         "You cannot call `.save()` after accessing `serializer.data`."
    #         "If you need to access data before committing to the database then "
    #         "inspect 'serializer.validated_data' instead. "
    #     )
    #
    #     validated_data = {**self.validated_data, **kwargs}
    #
    #     if self.instance is not None:
    #         self.instance = self.update(self.instance, validated_data)
    #         assert self.instance is not None, (
    #             '`update()` did not return an object instance.'
    #         )
    #     else:
    #         self.instance = self.create(validated_data)
    #         assert self.instance is not None, (
    #             '`create()` did not return an object instance.'
    #         )
    #
    #     return self.instance
    #
    # def is_valid(self, raise_exception=False):
    #     assert hasattr(self, 'initial_data'), (
    #         'Cannot call `.is_valid()` as no `data=` keyword argument was '
    #         'passed when instantiating the serializer instance.'
    #     )
    #
    #     if not hasattr(self, '_validated_data'):
    #         try:
    #             self._validated_data = self.run_validation(self.initial_data)
    #         except ValidationError as exc:
    #             self._validated_data = {}
    #             self._errors = exc.detail
    #         else:
    #             self._errors = {}
    #
    #     if self._errors and raise_exception:
    #         raise ValidationError(self.errors)
    #
    #     return not bool(self._errors)
    #
    # @property
    # def data(self):
    #     if hasattr(self, 'initial_data') and not hasattr(self, '_validated_data'):
    #         msg = (
    #             'When a serializer is passed a `data` keyword argument you '
    #             'must call `.is_valid()` before attempting to access the '
    #             'serialized `.data` representation.\n'
    #             'You should either call `.is_valid()` first, '
    #             'or access `.initial_data` instead.'
    #         )
    #         raise AssertionError(msg)
    #
    #     if not hasattr(self, '_data'):
    #         if self.instance is not None and not getattr(self, '_errors', None):
    #             self._data = self.to_representation(self.instance)
    #         elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
    #             self._data = self.to_representation(self.validated_data)
    #         else:
    #             self._data = self.get_initial()
    #     return self._data
    #
    # def to_internal_value(self, data):
    #     """
    #     Dict of native values <- Dict of primitive datatypes.
    #     """
    #     if not isinstance(data, Mapping):
    #         message = self.error_messages['invalid'].format(
    #             datatype=type(data).__name__
    #         )
    #         raise ValidationError({
    #             api_settings.NON_FIELD_ERRORS_KEY: [message]
    #         }, code='invalid')
    #
    #     ret = OrderedDict()
    #     errors = OrderedDict()
    #     fields = self._writable_fields
    #
    #     for field in fields:
    #         validate_method = getattr(self, 'validate_' + field.field_name, None)
    #         primitive_value = field.get_value(data)
    #         try:
    #             validated_value = field.run_validation(primitive_value)
    #             if validate_method is not None:
    #                 validated_value = validate_method(validated_value)
    #         except ValidationError as exc:
    #             errors[field.field_name] = exc.detail
    #         except DjangoValidationError as exc:
    #             errors[field.field_name] = get_error_detail(exc)
    #         except SkipField:
    #             pass
    #         else:
    #             set_value(ret, field.source_attrs, validated_value)
    #
    #     if errors:
    #         raise ValidationError(errors)
    #
    #     return ret
    #
    # def to_representation(self, instance):
    #     """
    #     Object instance -> Dict of primitive datatypes.
    #     """
    #     ret = OrderedDict()
    #     fields = self._readable_fields
    #
    #     for field in fields:
    #         try:
    #             attribute = field.get_attribute(instance)
    #         except SkipField:
    #             continue
    #
    #         # We skip `to_representation` for `None` values so that fields do
    #         # not have to explicitly deal with that case.
    #         #
    #         # For related fields with `use_pk_only_optimization` we need to
    #         # resolve the pk value.
    #         check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
    #         if check_for_none is None:
    #             ret[field.field_name] = None
    #         else:
    #             ret[field.field_name] = field.to_representation(attribute)
    #
    #     return ret
    #
    # def validate(self, attrs):
    #     return attrs
