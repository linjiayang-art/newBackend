from flask_httpauth import HTTPTokenAuth
from sqlalchemy import select
from ..models.system import UserInfo, SysUserRole,SysRole
from ..core.extensions import db
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous import  BadSignature, SignatureExpired
from flask import current_app,g

auth=HTTPTokenAuth(scheme='Bearer',header='Authorization')

#创建token
def generate_token(user):
    expiration=3600
    s=Serializer(current_app.config['SECRET_KEY'])
    #验证修改为字典传输
    data={'id':user.id}
    token=s.dumps(data,'sfa%$#^&*')
    #token=s.dumps({'id':user.Userid}).decode('ascii')
    return(token,expiration)




@auth.verify_token
def verify_token(token):#验证token 可以返回一个USER
    s=Serializer(current_app.config['SECRET_KEY'])
    try:
        data=s.loads(token,36000,False,'sfa%$#^&*')
    except (BadSignature,SignatureExpired):
        return False
    user=db.session.get(UserInfo,data['id'])
    if user is None:
        return False
    return user

@auth.get_user_roles
def get_user_roles(user:UserInfo):
    id=user.id
    #查询用户角色
    #查询用户角色
    roles=db.session.query(SysRole).join(SysUserRole,SysUserRole.role_id==SysRole.id).filter(SysUserRole.user_id==id).all()
    if roles is None:
        return []
    return [role.code for role in roles]