from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Details, GlobalConfig
from rest_framework import generics, filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
import datetime
import logging
from .serializers import UserSerializer
from django.db import connection
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
from rest_framework import views
from collections import defaultdict
import pytz
import py_compile
import re
import os
# logger settings
logger = logging.getLogger("api.users")


class AddUser(generics.ListCreateAPIView):
    """
        View to create and add a user
    """
    def post(self, request):
        """
            Parameters:
                {
                    "username": "username",
                    "password": "password",
                    "email": "emailid"
                }
        """
        self.username = request.DATA.get("username", None)
        self.password = request.DATA.get("password", None)
        self.email = request.DATA.get("email", None)

        if not self.username:
            return Response(dict(error=["username_empty"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            self.userObj = User.objects.get(username=self.username)
        except:
            self.userObj = None

        if self.userObj:
            return Response(dict(error=["username_already_exists"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.create_user(self.username, self.email, self.password)
            response_dict = dict(username=self.username)
            return Response(dict(error=[], data=response_dict), status=status.HTTP_200_OK)
        except:
            return Response(dict(error=["user_cant_not_be_added"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)


class AddDetails(generics.ListCreateAPIView):
    """
        View to add user details
    """
    def post(self, request):
        """
            Parameters:
            {
                "father_name": "father's name",
                "mother_name": "mother's name",
                "city": "city",
                "user": "username" 
            }
        """
        self.username = request.DATA.get("user", None)
        self.father = request.DATA.get("father_name", None)
        self.mother = request.DATA.get("mother_name", None)
        self.city = request.DATA.get("city", None)

        if not self.username:
            return Response(dict(error=["username_empty"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            self.userObj = User.objects.get(username=self.username)
        except:
            self.userObj = None

        if not self.userObj:
            return Response(dict(error=["user_does_not_exists"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            self.detailObj = Details.objects.create(father_name=self.father,
                                                    mother_name=self.mother,
                                                    city=self.city,
                                                    user=self.userObj)
            self.detailObj.save()
            response_dict = dict(father_name=self.father,
                                 mother_name=self.mother,
                                 city=self.city,
                                 user=self.username)
            return Response(dict(error=[], data=response_dict), status=status.HTTP_200_OK)
        except:
            return Response(dict(error=["details_cant_not_be_saved"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)


class UserDelete(generics.DestroyAPIView):
    """
        View to delete a user
    """
    def delete(self, request):
        """
            parameters:
            {
                "user": "username"
            }
        """
        self.username = request.DATA.get("user", None)

        if not self.username:
            return Response(dict(error=["username_empty"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            self.userObj = User.objects.get(username=self.username)
        except:
            self.userObj = None

        if not self.userObj:
            return Response(dict(error=["user_does_not_exists"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.filter(username=self.username).delete()
            return Response(dict(error=[], data=dict(), status=status.HTTP_200_OK))
        except:
            return Response(dict(error=["user_cant_not_be_deleted"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)


class ListAllUser(generics.ListAPIView):
    """
        List user(s) details
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        """
            get query set
        """
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        """
            send custom response using overriding the list method
        """
        
        response = generics.ListAPIView.list(self, request, *args, **kwargs).data
        return Response(dict(data=response, error=[]), status=status.HTTP_200_OK)


class ListUser(generics.ListAPIView):
    """
        List user details
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        """
            get query set
        """
        return [User.objects.get(id=self.kwargs.get("user_id"))]

    def list(self, request, *args, **kwargs):
        """
            send custom response using overriding the list method
        """
        try:
            response = generics.ListAPIView.list(self, request, *args, **kwargs).data
        except:
            return Response(dict(data=[], error=['user_not_found']), status=status.HTTP_400_BAD_REQUEST)
        return Response(dict(data=response, error=[]), status=status.HTTP_200_OK)


class EditUser(generics.ListCreateAPIView):
    """
        View to edit user
    """
    def post(self, request):
        """
            parameters:
            {
                "username": "<user>",
                "email": "<email id>"
            }
        """
        self.username = request.DATA.get("username", None)
        self.email = request.DATA.get("email", None)

        if not self.username:
            return Response(dict(error=["username_empty"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            self.userObj = User.objects.get(username=self.username)
        except:
            self.userObj = None

        if not self.userObj:
            return Response(dict(error=["user_does_not_exists"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            self.userObj.email = self.email
            self.userObj.save()
            response_dict = dict(username=self.username, email=self.email)
            return Response(dict(error=[], data=response_dict), status=status.HTTP_200_OK)
        except:
            return Response(dict(data=[], error=['can_not_edit_user']), status=status.HTTP_400_BAD_REQUEST)


class EditUserDetails(generics.ListCreateAPIView):
    """
        View to edit user details
    """
    def post(self, request):
        """
            parameters:
            {
                "username": "<user>",
                "city": "<city>"
            }
        """
        self.username = request.DATA.get("username", None)
        self.city = request.DATA.get("city", None)

        if not self.username:
            return Response(dict(error=["username_empty"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            self.userObj = User.objects.get(username=self.username)
        except:
            self.userObj = None

        if not self.userObj:
            return Response(dict(error=["user_does_not_exists"], data=dict()),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            self.detailObj = Details.objects.get(user=self.userObj)
        except:
            self.detailObj = None

        if not self.detailObj:
            return Response(dict(data=[], error=['details_not_found']), status=status.HTTP_400_BAD_REQUEST)

        try:
            self.detailObj.city = self.city
            self.detailObj.save()
            response_dict = dict(username=self.username, city=self.city)
            return Response(dict(error=[], data=response_dict), status=status.HTTP_200_OK)
        except:
            return Response(dict(data=[], error=['details_can_not_be_edit']), status=status.HTTP_400_BAD_REQUEST)


class AuthTokenUtils(object):

    def authenticate_user_token(self, userobj):
        """
            Generate a new token for each user and check the validity of the token.
            If the token has expired, generate a new token and return the new value.
        """

        try:
            time_period = int(GlobalConfig.objects.get(name="token_exp").value)
        except:
            time_period = 60

        # First time token generation
        token_obj, created = Token.objects.get_or_create(user=userobj)
        if token_obj and created:
            return token_obj

        # This is required for the time comparison
        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        # The token has expired, generate a new token and return the token
        # object
        if token_obj and token_obj.created < utc_now - timedelta(minutes=time_period):
            token_obj.delete()
            token_obj = Token.objects.create(user=userobj)
            return token_obj

        # No change, return the token as it is
        return token_obj


class AuthenticateUserView(views.APIView):

    """
        View to authenticate user
    """

    # Public access to login view
    permission_classes = (AllowAny,)

    def post(self, request):
        """
            Parameters:
                        {
                            "username": <username>,
                            "password": <password>,
                        }
        """

        # Get the POST parameters from the parsed JSON
        self.username = request.DATA.get("username")
        self.password = request.DATA.get("password")

        if not self.username or not self.password:
            logger.error("Empty username or password entered")
            return Response(dict(error=["username_password_empty"], data={}, status=status.HTTP_400_BAD_REQUEST))

        # User authentication against django database
        self.userobj = authenticate(username=self.username, password=self.password)

        authtokenutils = AuthTokenUtils()

        if self.userobj:
            # Check existing token and generate new token of existing token has expired
            user_auth_token = authtokenutils.authenticate_user_token(self.userobj)
            return Response(dict(error=[], data=dict(username=self.username, token=user_auth_token.key)),
                            status=status.HTTP_200_OK)
        else:
            return Response(dict(error=["unauthorized_access"], data={}), status=status.HTTP_401_UNAUTHORIZED)
