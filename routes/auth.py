from sanic import response,Blueprint
from tortoise.exceptions import IntegrityError as IE
from models.user import User
from core.auth import get_token,protected

auth_blueprint = Blueprint("Auth","/auth")

@auth_blueprint.route("/signup",methods=["POST"])
async def signup(request):
    name = request.json.get("name",None)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    try:
        user = await User.create(email=email,name=name)
    except IE:
        return response.json({"message":"Already Signed up"},status=200)
    user.set_password(password)
    await user.save()
    return response.json({"message":"Signed In successfully"},status=201)
        


@auth_blueprint.route("/login",methods=["POST"])
async def login(request):
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    user = await User.authenticate(email,password)
    
    if user is None:
        return response.json({"message":"Invalid creds"},status=400)
    token = get_token(request,user)
    return response.json({"message":"Logged in succesfully","access":token},status=200)


@auth_blueprint.route("/change_password",methods=["POST"])
@protected
async def change_password(request,*args, **kwargs):
    if "password" not in request.json:
        return response.json({"message":"Please provide new password"},status=400)
    user = kwargs.get("user")
    user.set_password(request.json.get("password"))
    await user.save()
    return response.json({"message":"Password changed succesfully"},status=200)
    
    
    