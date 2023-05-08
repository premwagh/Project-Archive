from rest_framework import status
from rest_framework.viewsets import (
    ModelViewSet,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

# from core.swagger.schema import auto_schema_from_dict
from ..models import (
    User,
)
from .permissions import UserPermission
from .serializers import (
    UserSerializer,
    UserMeSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
    VerifyTokenSerializer,
    ResetPasswordSerializer,
)
from .utils import (
    send_email_verification,
    send_password_reset,
)
# from .views_auto_schema import user_viewset_auto_schema


class UserViewSet(ModelViewSet):
    """
    get: List all the users.
    post: Create a new user.
    """

    ordering = ('created_on',)

    queryset = User.objects.get_queryset()
    permission_classes = (UserPermission,)
    serializer_class = UserSerializer

    @property
    def is_user_me(self):
        if self.action == "me":
            return True
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return lookup_url_kwarg in self.kwargs and self.kwargs[lookup_url_kwarg] == "me"

    def get_object(self):
        if self.is_user_me:
            return self.request.user
        return super().get_object()

    def perform_create(self, serializer):
        instance = serializer.save()
        send_email_verification(instance)

    @action(
        detail=False,
        methods=["get", "patch"],
        name="User Me view",
        url_name="me",
        url_path="me",
        serializer_class=UserMeSerializer,
        permission_classes=(IsAuthenticated,),
        filter_backends=(),
        pagination_class=None,
    )
    def me(self, request, *args, **kwargs):
        """
        Action for current logged in user.
        """
        action = {"get": self.retrieve, "patch": self.partial_update,}.get(request.method.lower())
        return action(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post"],
        name="User Password Change",
        url_name="change-password",
        url_path="change-password",
        serializer_class=ChangePasswordSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def change_password(self, request, *args, **kwargs):
        """
        Action for user password change.
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data.get("new_password"))
        user.save()
        return Response({"Password Changed Successfully!"}, status=200)

    @action(
        detail=False,
        methods=["post"],
        name="send Forgot Password Email",
        url_name="forgot-password",
        url_path="forgot-password",
        serializer_class=EmailSerializer,
        permission_classes=(AllowAny,),
    )
    def send_forgot_password_email(self, request, *args, **kwargs):
        """
        send forgot password link email to the user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data.get("email"))
        except User.DoesNotExist:
            return Response({"detail": "Email address not found."}, status=400)
        else:
            send_password_reset(user)
            return Response({"message": "Password reset link sent!"}, status=200)

    @action(
        detail=False,
        methods=["post"],
        name="Check forgot password token",
        url_name="forgot-password-token-check",
        url_path="forgot-password-token-check",
        serializer_class=VerifyTokenSerializer,
        permission_classes=(AllowAny,),
    )
    def forgot_password_token_check(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get("token")
        User.get_object_from_password_reset_token(token)
        return Response({"message": "OK"}, status=200)

    @action(
        detail=False,
        methods=["post"],
        name="Forgotten Password Reset",
        url_name="forgot-password-reset",
        url_path="forgot-password-reset",
        serializer_class=ResetPasswordSerializer,
        permission_classes=(AllowAny,),
    )
    def forgot_password_reset(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get("token")
        new_password = serializer.validated_data.get("new_password")
        user = User.get_object_from_password_reset_token(token)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully!"}, status=200)

    @action(
        detail=False,
        methods=["post"],
        name="Send User Email Verification",
        url_name="send-email-verification",
        url_path="send-email-verification",
        serializer_class=EmailSerializer,
        permission_classes=(AllowAny,),
    )
    def send_email_verification(self, request, *args, **kwargs):
        """
        Send email verification action.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data.get("email"))
        except User.DoesNotExist:
            return Response({"detail": "Email address not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if user.is_email_verified:
                return Response({"detail": "Already verified!"}, status=status.HTTP_400_BAD_REQUEST)
            send_email_verification(user)
            return Response({"message": "Verification link sent!"}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        name="Verify User Email",
        url_name="verify-email",
        url_path="verify-email",
        serializer_class=VerifyTokenSerializer,
        permission_classes=(AllowAny,),
    )
    def verify_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get("token")
        user = User.get_object_from_email_verification_token(token)
        user.is_email_verified = True
        user.save()
        return Response({"message": "Verified successfully!"}, status=200)
