# CRUD для базы данных пользователей
class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            users = User.objects.all()
            return Response({'users': UserSerializer(users, many=True).data})
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({'Error': "GET: not found USER"})
        return Response({'user': UserSerializer(user, many=False).data})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'user': serializer.data})
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'Error': "PUT: not found PK"})
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({'Error': "PUT: not found USER"})
        serializer = UserSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'user': serializer.data})
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'Error': "DELETE: not found PK"})
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({'Error': "DELETE: not found USER"})
        username = user.username
        user.delete()
        return Response({'user': "delete {}".format(username)})