from drf_yasg import openapi


put_post_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'first_name', 'last_name', 'birthdate'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'birthdate': openapi.Schema(type=openapi.TYPE_STRING)
            },
        )

patch_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'birthdate': openapi.Schema(type=openapi.TYPE_STRING)
            },
        )