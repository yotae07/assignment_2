from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from apps.products.models import Menu, Item, Tag
from .serializers import MenuSerializer, ItemSerializer, TagSerializer
from rest_framework import permissions
from api.permissions import CustomAuthenticated
from api.pagination import CustomPagination


# CRUD 모든 행동들이 각 mixin에 적혀있고 그것들을 상속받아 사용하게됩니다.
class ProductViewSet(CreateModelMixin,
                     ListModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):

    # 하나의 viewset에서 사용한 queryset입니다.
    queryset = Menu.objects.all()
    # 하나의 viewset에서 사용한 serializer입니다.
    serializer_class = MenuSerializer
    # view에서 사용될 권한을 설정할 수 있습니다.
    # IsAuthenticated 로그인된 유저인지 확인합니다.
    # CustomAuthenticated 제가 직접 만든 권한이며 로그인한 유저가 ADMIN인지 확인합니다.
    permission_classes = [permissions.IsAuthenticated, CustomAuthenticated]
    # 선언할시 pagination이 자동으로 설정됩니다.
    pagination_class = CustomPagination

    # 조건중 admin권한만 가능한 액션들이 있기때문에 특정 액션(읽기)을 할시 로그인한 유저로 권한을 낮췄습니다.
    def get_permissions(self):
        # self.action할시 CRUD중 어떤 액션인지 알 수 있습니다.
        # retrieve 상세보기입니다.
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated]

        return super().get_permissions()


class ItemViewSet(CreateModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [CustomAuthenticated]

    # 모델에 menu가 연결되어있기때문에 url에 있는 menu의 pk를 입력받은 데이터에 추가해주는 작업입니다.
    # 이 작업이 있어야 Item object를 생성할떄 menu와 Foreignkey로 연결된 상태로 생성가능합니다.
    # 이때 id만 있어도 되는 이유는 DB에서 PK로 연결되기 때문에 장고에서도 내부적으로 ID값으로도 연결가능하게 처리합니다.
    def create(self, request, *args, **kwargs):
        request.data.setdefault('menu', kwargs['product_pk'])
        return super().create(request, *args, **kwargs)


class TagViewSet(CreateModelMixin,
                 UpdateModelMixin,
                 DestroyModelMixin,
                 GenericViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [CustomAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data.setdefault('menu', kwargs['product_pk'])
        return super().create(request, *args, **kwargs)

    # queryset
    # def get_queryset(self):
    #     """
    #     Get the list of items for this view.
    #     This must be an iterable, and may be a queryset.
    #     Defaults to using `self.queryset`.
    #
    #     This method should always be used rather than accessing `self.queryset`
    #     directly, as `self.queryset` gets evaluated only once, and those results
    #     are cached for all subsequent requests.
    #
    #     You may want to override this if you need to provide different
    #     querysets depending on the incoming request.
    #
    #     (Eg. return a list of items that is specific to the user)
    #     """
    #     assert self.queryset is not None, (
    #         "'%s' should either include a `queryset` attribute, "
    #         "or override the `get_queryset()` method."
    #         % self.__class__.__name__
    #     )
    #
    #     queryset = self.queryset
    #     if isinstance(queryset, QuerySet):
    #         # Ensure queryset is re-evaluated on each request.
    #         queryset = queryset.all()
    #     return queryset

    # serializer_class
    # def get_serializer(self, *args, **kwargs):
    #     """
    #     Return the serializer instance that should be used for validating and
    #     deserializing input, and for serializing output.
    #     """
    #     serializer_class = self.get_serializer_class()
    #     kwargs.setdefault('context', self.get_serializer_context())
    #     return serializer_class(*args, **kwargs)

    # def get_serializer_class(self):
    #     """
    #     Return the class to use for the serializer.
    #     Defaults to using `self.serializer_class`.
    #
    #     You may want to override this if you need to provide different
    #     serializations depending on the incoming request.
    #
    #     (Eg. admins get full serialization, others get basic serialization)
    #     """
    #     assert self.serializer_class is not None, (
    #         "'%s' should either include a `serializer_class` attribute, "
    #         "or override the `get_serializer_class()` method."
    #         % self.__class__.__name__
    #     )
    #
    #     return self.serializer_class

    # get_object
    # def get_object(self):
    #     """
    #     Returns the object the view is displaying.
    #
    #     You may want to override this if you need to provide non-standard
    #     queryset lookups.  Eg if objects are referenced using multiple
    #     keyword arguments in the url conf.
    #     """
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     # Perform the lookup filtering.
    #     lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
    #
    #     assert lookup_url_kwarg in self.kwargs, (
    #         'Expected view %s to be called with a URL keyword argument '
    #         'named "%s". Fix your URL conf, or set the `.lookup_field` '
    #         'attribute on the view correctly.' %
    #         (self.__class__.__name__, lookup_url_kwarg)
    #     )
    #
    #     filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
    #     obj = get_object_or_404(queryset, **filter_kwargs)
    #
    #     # May raise a permission denied
    #     self.check_object_permissions(self.request, obj)
    #
    #     return obj

    # permission_class
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     return [permission() for permission in self.permission_classes]

    # pagination_class
    # @property
    # def paginator(self):
    #     """
    #     The paginator instance associated with the view, or `None`.
    #     """
    #     if not hasattr(self, '_paginator'):
    #         if self.pagination_class is None:
    #             self._paginator = None
    #         else:
    #             self._paginator = self.pagination_class()
    #     return self._paginator
    #
    # def paginate_queryset(self, queryset):
    #     """
    #     Return a single page of results, or `None` if pagination is disabled.
    #     """
    #     if self.paginator is None:
    #         return None
    #     return self.paginator.paginate_queryset(queryset, self.request, view=self)
    #
    # def get_paginated_response(self, data):
    #     """
    #     Return a paginated style `Response` object for the given output data.
    #     """
    #     assert self.paginator is not None
    #     return self.paginator.get_paginated_response(data)

    # CreateModelMixin
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def perform_create(self, serializer):
    #     serializer.save()

    # ListModelMixin
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # RetrieveModelMixin
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # UpdateModelMixin
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)
    #
    # def perform_update(self, serializer):
    #     serializer.save()
    #
    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    # DestroyModelMixin
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # def perform_destroy(self, instance):
    #     instance.delete()
