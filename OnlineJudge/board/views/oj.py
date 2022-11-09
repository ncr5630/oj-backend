import logging
import traceback
from utils.api import APIView, validate_serializer

from board.models import Board
from board.serializers import (BoardSerializer, CreateBoardSerializer, EditBoardSerializer)
from account.decorators import login_required


class BoardListAPI(APIView):
    @login_required
    def get(self, request):
        boards = Board.objects.select_related("created_by").filter(visible=True)
        return self.success(self.paginate_data(request, boards, BoardSerializer))


class BoardViewCountAPI(APIView):
    @login_required
    def put(self, request):
        """
        update board view count
        """
        board_id = request.GET.get("id")
        view_count = request.data.get("view_count")
        if board_id:
            try:
                Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return self.error("Board does not exist")
        try:
            Board.objects.filter(id=board_id).update(view_count=view_count)
            return self.success("Succeeded")
        except Exception as Error:
            Error_data = "Can't update Board views.%s %s" % (Error, traceback.format_exc())
            logging.DEBUG(Error_data)
            return self.error("Can't update Board views.")

class BoardAPI(APIView):
    @validate_serializer(CreateBoardSerializer)
    @login_required
    def post(self, request):
        """
        publish Board
        """
        data = request.data
        board = Board.objects.create(title=data["title"], content=data["content"], created_by=request.user, visible=data["visible"])
        return self.success(BoardSerializer(board).data)

    @validate_serializer(EditBoardSerializer)
    @login_required
    def put(self, request):
        """
        edit Board
        """
        data = request.data
        try:
            board = Board.objects.get(id=data.pop("id"), created_by=request.user)
        except Board.DoesNotExist:
            return self.error("Board  does not exist")
        for k, v in data.items():
            setattr(board, k, v)
        board.save()
        return self.success(BoardSerializer(board).data)

    @login_required
    def get(self, request):
        """
        get Board list / get one Board
        """
        board_id = request.GET.get("id")
        if board_id:
            try:
                board = Board.objects.get(id=board_id)
                return self.success(BoardSerializer(board).data)
            except Board.DoesNotExist:
                return self.error("Board does not exist")
        board_data = Board.objects.all().order_by("-create_time")

        return self.success(self.paginate_data(request, board_data, BoardSerializer))

    @login_required
    def delete(self, request):
        board_id = request.GET.get("id")
        if board_id:
            try:
                Board.objects.get(id=board_id, created_by=request.user)
            except Board.DoesNotExist:
                return self.error("Board  does not exist or you don't have permission")
            Board.objects.filter(id=request.GET["id"]).delete()
        return self.success()
