# FlaskForApi

## 介绍
此框架以Flask为基础为实现RESTful api服务进行了拓展和改进.主要对Flask的一些常用插件进行了二次封装.如数据库orm插件sqlalchemy,
表单数据验证插件wtforms,Flask自带的json序列化类JSONEncoder进行改进等等

阅读文档前应对Flask有一定基础,并对blueprint,sqlalchemy,wtforms等Flask常用插件有一定了解 

## 安装

1. 安装pipenv包管理工具
2. 进入项目根目录执行命令:
    
    pipenv install  安装项目依赖
    
    pipenv shell    进入项目虚拟环境
3. 执行入口文件 python3 FlaskForApi.py
4. 
    
## 目录结构
Flask为web微型服务框架,目录结构原则上可自由设计,本项目提出了一种较为可行的结构可作为参考,若有有更好的设计可自行修改。

1. 项目入口文件 FlaskForApi.py:
    创建Flask对象app, 定义了全局异常捕获器framework_error,对所有异常标准化输出异常返回格式 
2. app/\_\_init\_\_.py
    
    初始化app ,并为app注册所需的Flask plugin, 包括blueprint注册
    
   app/app.py
   
    改写FLask的JSONEncoder序列化类,使得jsonify函数可对类变量,sqlalchemy模型变量等等自动序列化为json格式
   
3. app/api  视图模块
4. app/config   项目参数配置,公共参数配置在setting.py 私有参数配置在secure.py下 如数据库配置
5. app/libs  项目公共工具包
6. app/models  数据模型层
7. app/validators 表单验证层
8. app/view_models view_model层,对返回数据进行前端可读性转换


## 重要概念
### Redprint(app/libs/redprint.py)  

项目工程化的设计规范
   
   Flask的Blueprint插件是用于模块级别的拆分，Redprint用于实现比模块级别下更具体的视图函数的拆分，例如在用Flask制作REST API时版本号下根据不同业务对象的函数拆分
   
   Blueprint注册在Flask app上,那么Redprint则注册在Blueprint上
   
   使用示例:
   
   app/api/v1/\_\_init\_\_.py 中创建了一个v1版本的Blueprint对象bp_v1,url前缀为'v1'
   
   
   
       def create_blueprint_v1():
            bp_v1 = Blueprint('v1', __name__)
        
            user.api.register(bp_v1)
            client.api.register(bp_v1)
            token.api.register(bp_v1)
        
            return bp_v1
   
   app/api/v1/client.py 中实例化了一个RedPrint对象,url前缀为 'client',并在app/api/v1/\_\_init\_\_.py中注册在bp_v1上
   

        api = Redprint('client')
        
   
   那么client.py模块下所有的视图函数route都以 '/v1/client' 开头。
   
   如 app/api/v1/client.py 模块下的用户注册函数 create_client() 的 route 为 '/v1/client/register'
   
   
    @api.route('/register', methods=['POST'])
    def create_client():
        form = ClientForm().validate_for_api()
        promise = {
            ClientTypeEnum.USER_EMAIL: __register_user_by_email
        }
        promise[form.type.data]()
        return Success()
   
   同理 app/api/v1/user.py 模块下的修改密码函数 change_password() 的 route 为 '/v1/user/secure'
   
   这种设计为了更好的维护整个项目工程的路由结构,并增加API路由的可读性

### APIException (app/libs/error.py)   
继承并改写了werkzeug.exceptions的HTTPExcepton类，用于将所有HTTPException转化为json格式返回

如 app/libs/error_code.py (定义各种操作返回信息)
    
    class Success(APIException):
        code = 201
        msg = 'ok'
        error_code = 0
        
返回信息为:

    HTTP status = 200
    {
        "error_code": 0,
        "msg": "ok",
        "request": "POST /v1/user/secure"
    }

### jsonify()序列化sqlalchemy模型
Flask自带的jsonify()函数仅能序列化python的字典结构dict,那么经过app/app.py对原JSONEncoder类改写后可对sqlalchemy模型类进行自动序列化


例如视图函数 app/api/v1/user.py中 的 get_user()


    @api.route('', methods=['GET'])
    @auth.login_required
    def get_user():
        uid = g.user.uid
        user = User.query.filter_by(id=uid).first_or_404()
        return jsonify(user)
        
返回示例:
    
    
    {
        "id": 1,   
        "email": "123@gmail.com",
        "nickname": "稻草人"
    }

## 样例功能示例
### 建议自行运行框架,利用postman进行测试

1.注册 http://localhost:5000/v1/client/register 

    POST
    {
        "account": "123@gmail.com",
        "secret": "1234567",
        "nickname": "稻草人",
        "type": 100
    }
    
return:

    {
        "error_code": 0,
        "msg": "ok",
        "request": "POST /v1/client/register"
    }
    

2. 登陆 http://localhost:5000/v1/token 


    POST
    {
        "account": "123@gmail.com",
        "secret": "1234567",
        "type": 100
    }
    
        
return:


    {
        "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU1Njk2MDE5NiwiZXhwIjoxNTU5NTUyMTk2fQ.eyJ1aWQiOjEsInR5cGUiOjEwMCwic2NvcGUiOiJBZG1pblNjb3BlIn0.Kgn0DPMxhatd090tkDWB_FTX7Unc_mMkmkVz2LNQLgG9AYHt-SpM__QCFmr-ka2g97Pr7gIbtuiRb75HI6XrRw"
    }


3. 获取当前用户信息 HTTP header中携带该token信息 
    
    
    GET http://localhost:5000/v1/user
    
    
return:
    
    {
        "email": "123@gmail.com",
        "id": 1,
        "nickname": "稻草人"
    }
    
    
    
   
   

