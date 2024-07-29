from sanic import response, Blueprint

from managers import UserManager
from decorators.auth import protected

auth_blueprint = Blueprint("Auth", "/auth")


@auth_blueprint.route("/signup", methods=["POST"])
async def signup(request):
    await UserManager.signup_user(request.json)
    return response.json({"message": "Signed up successfully"}, status=201)


@auth_blueprint.route("/login", methods=["POST"])
async def login(request):
    token = await UserManager.login_user(request.json)
    return response.json(
        {"message": "Logged in succesfully", "access": token}, status=200
    )


@auth_blueprint.route("/change_password", methods=["POST"])
@protected
async def change_password(request, static_id, *args, **kwargs):
    await UserManager.change_password(request.json)
    return response.json({"message": "Password changed succesfully"}, status=200)
