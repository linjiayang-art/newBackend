from flask import Blueprint,request,jsonify,current_app,make_response,send_file
from  src.core.extensions import db
from src.models.file_model  import FileInfo
import os
import uuid
import time
import urllib.parse
file_bp=Blueprint('file',__name__,url_prefix='/file')

@file_bp.route('/')
def index():
    return 'fileserver' 

def random_filename(filename):
    ext=os.path.splitext(filename)[1]
    new_filename=uuid.uuid4().hex+ext
    return new_filename



@file_bp.route('/upload',methods=['POST','GET'])
def upload():
    if request.method!='POST':
        return jsonify({'code':400,'msg':'bad request'})
    #暂时未添加表单验证,后续添加
    file=request.files.get('file',None)
    if file is None:
        return jsonify({'code':201,'msg':'http heads has no file'})
    file_name=file.filename
    new_file_name=random_filename(file_name)
    #获取当前年+月
    year_month=time.strftime("%Y\%m", time.localtime())
    file_path=os.path.join(current_app.config['UPLOAD_PATH'],year_month)
    #没有就创建一个
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file.save(os.path.join(file_path,new_file_name))
    fileinfo=FileInfo(orginname=file_name,localname=new_file_name,file_path=year_month)
    db.session.add(fileinfo)
    db.session.commit()
    results={
            'name':new_file_name}
    return jsonify(code='200', message="文件保存成功",data=results)


@file_bp.route('/download/<local_file>',methods=['GET'])
def download(local_file):
    #local_file='5f946ca7ce7e47638f8d972a0e52017d.md'
    fileinfo=FileInfo(orginname=local_file,localname=local_file,file_path='2023/12')
    db.session.add(fileinfo)
    db.session.commit()

    fileinfo=FileInfo.query.filter_by(localname=local_file).first()
    if fileinfo is None:
        return jsonify({'code':201,'msg':'file not found'})
    file_name=fileinfo.orginname
    filename_encoded = urllib.parse.quote(file_name.encode('utf-8'))
    file_path = os.path.join(current_app.config['UPLOAD_PATH'], fileinfo.file_path, local_file)
    #判断文件是否存在
    if not os.path.exists(file_path):
        return jsonify({'code':201,'msg':'file not found'})
    response = make_response(send_file(file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
    response.headers['Content-Disposition'] = f'attachment; filename="{filename_encoded}"'
    return response