from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permissions import IsAdmin, IsAuthorOrModeratorOrAdmin

CATEGORIE_METHOD_PERMISSIONS = {
    'GET': (AllowAny,),
    'POST': (IsAdmin,),
    'DELETE': (IsAdmin,),
}

GENRE_METHOD_PERMISSIONS = {
    'GET': (AllowAny,),
    'POST': (IsAdmin,),
    'DELETE': (IsAdmin,),
}

TITLE_METHOD_PERMISSIONS = {
    'GET': (AllowAny,),
    'POST': (IsAdmin,),
    'PATCH': (IsAdmin,),
    'DELETE': (IsAdmin,),
}

REVIEW_METHOD_PERMISSIONS = {
    'GET': (AllowAny,),
    'POST': (IsAuthenticated,),
    'PATCH': (IsAuthorOrModeratorOrAdmin,),
    'DELETE': (IsAuthorOrModeratorOrAdmin,),
}

COMMENT_METHOD_PERMISSIONS = {
    'GET': (AllowAny,),
    'POST': (IsAuthenticated,),
    'PATCH': (IsAuthorOrModeratorOrAdmin,),
    'DELETE': (IsAuthorOrModeratorOrAdmin,),
}
