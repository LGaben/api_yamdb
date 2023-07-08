"""В api во views.py просто замени мой код этим""" 

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id, title=title_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)


"""В reviews В models.py удали blank и null строку """


"""В пермишах замени и потом поправь permission_classes во views.py"""
class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'Изменить контент может только автор.'

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or request.user == obj.author


class IsAdminOrModerator(permissions.BasePermission):
    message = 'Изменить контент может только админ или модератор.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_moderator)
    

"""Убери из IsAdminOrReadOnly и сделай в IsAdmin(Не уверен, что сам правильно понял его коммент)"""
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )
    

"""Также в models.py, который в reviews замени"""

ordering = ['-pub_date']