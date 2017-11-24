学习Django的时候知道,在Django请求的生命周期中,请求经过WSGI和中间件到达路由,不管是FBV还是CBV都会先执行View视图函数中的dispatch方法

`REST framework`是基于Django的API框架,REST framework采用的是CBV的请求模式.

所以在一个项目中,使用了REST framework的时候,

请求到达`REST framework`后,也先执行`REST framework`中的`dispatch`方法

先来看看`dispatch`方法的源码

    def dispatch(self, request, *args, **kwargs):

        self.args = args			# 函数传递过来的参数
        self.kwargs = kwargs        # 函数传递过来的参数
		
		# 封装request
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

查看`initialize_request`方法,可以知道这个方法接收客户端的request请求,再重新封装成新的request

    def initialize_request(self, request, *args, **kwargs):

        parser_context = self.get_parser_context(request)

        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )

再查看Request方法的源码

可以知道这个`Request`类是`rest framework`中定义的一个类

	class Request(object):

		def __init__(self, request, parsers=None, authenticators=None,
					 negotiator=None, parser_context=None):
			self._request = request
			self.parsers = parsers or ()
			self.authenticators = authenticators or ()
			self.negotiator = negotiator or self._default_negotiator()
			self.parser_context = parser_context
			self._data = Empty
			self._files = Empty
			self._full_data = Empty
			self._content_type = Empty
			self._stream = Empty

			if self.parser_context is None:
				self.parser_context = {}
			self.parser_context['request'] = self
			self.parser_context['encoding'] = request.encoding or settings.DEFAULT_CHARSET

			force_user = getattr(request, '_force_auth_user', None)
			force_token = getattr(request, '_force_auth_token', None)
			if force_user is not None or force_token is not None:
				forced_auth = ForcedAuthentication(force_user, force_token)
				self.authenticators = (forced_auth,)

先不看这个`Request`到底执行了什么操作

但是已经知道经过Request处理过的request已经不再是客户端发送过来的那个request了

在`initialize_request`方法中,有一个方法处理过request,来看看`get_parser_context`方法的源码

    def get_parser_context(self, http_request):

        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {})
        }

在这里,view的值是self,代指的是`UsersView`这个对象,所以`get_parser_context`方法把UsersView这个类封装进来然后返回

所以`get_parser_context`方法最后返回的当前对象以及当前对象所传的参数

经过`initialize_request`函数处理之后的request,现在就变成了

    Request(
        request,
        parsers=self.get_parsers(),
        authenticators=self.get_authenticators(),
        negotiator=self.get_content_negotiator(),
        parser_context=parser_context
    )

现在再来看看Request的其他参数代指的是什么

	get_parsers					根据字面意思,是解析get请求的意思
	get_authenticators			认证相关
	get_content_negotiator		选择相关
	parser_context				封闭self和self的参数

    def get_parsers(self):

        return [parser() for parser in self.parser_classes]

    def get_authenticators(self):

        return [auth() for auth in self.authentication_classes]

    def get_permissions(self):
  
        return [permission() for permission in self.permission_classes]

    def get_throttles(self):
   
        return [throttle() for throttle in self.throttle_classes]

    def get_content_negotiator(self):

        if not getattr(self, '_negotiator', None):
            self._negotiator = self.content_negotiation_class()
        return self._negotiator

再来看看`UsersView`这个类中的get方法和post方法

    def get(self,request,*args,**kwargs):
        pass

    def post(self,request,*args,**kwargs):
        pass

可以看到get方法的参数中有一个request,通过前面可以知道这个request已经不是最开始时到达服务端的request了

这个request方法中已经被`REST framework`封装了解析,认证和选择等相关的方法

    def dispatch(self, request, *args, **kwargs):

        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

`default_response_headers`这个方法从它的注释可以看出已经被丢弃了.

再来看`initial`这个方法

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)

先执行`get_format_suffix`来获取客户端所发送的url的后缀

然后执行`perform_content_negotiation`方法,从它的注释可以知道这个方法的主要作用是执行内容选择,并把服务端接收到的信息保存在request中

然后再执行`determine_version`方法

    def determine_version(self, request, *args, **kwargs):
        """
        If versioning is being used, then determine any API version for the
        incoming request. Returns a two-tuple of (version, versioning_scheme)
        """
        if self.versioning_class is None:
            return (None, None)
        scheme = self.versioning_class()
        return (scheme.determine_version(request, *args, **kwargs), scheme)

在`determine_version`方法的官方注释中可以知道,`determine_version`方法的主要作用是

    如果url中有版本信息,就获取发送到服务端的版本,返回一个元组

执行完上面的方法,再执行`perform_authentication`方法来进行认证操作

来看下`perform_authentication`方法的源码

    def perform_authentication(self, request):
        """
        Perform authentication on the incoming request.

        Note that if you override this and simply 'pass', then authentication
        will instead be performed lazily, the first time either
        `request.user` or `request.auth` is accessed.
        """
        request.user

从上面有代码及注释中可以看出,`perform_authentication`方法的作用就是

    执行认证功能,确认进行后续操作的用户是被允许的.
    perform_authentication方法返回经过认证的用户对象
	
执行完`perform_authentication`方法,就会执行`check_permissions`方法	
		
    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )
                
`check_permissions`方法的作用是

    如果用户通过认证,检查用户是否有权限访问url中所传的路径.
    如用用户访问的是没有没有权限的路径,则会抛出异常.

`check_permissions`方法执行完成后,就会执行`check_throttles`方法

`check_throttles`方法的作用是检查用户是否被限制了访问主机的次数
如果用户访问服务器的次数超出设定值,则会抛出一个异常

例如,如果想限制一个ip地址每秒钟只能访问几次,一个小时之内最多可以访问多少次,就可以在`settings.py`文件中进行配置

    def check_throttles(self, request):
        """
        Check if request should be throttled.
        Raises an appropriate exception if the request is throttled.
        """
        for throttle in self.get_throttles():
            if not throttle.allow_request(request, self):
                self.throttled(request, throttle.wait())

`initial`这个方法执行完成后,`request.method.lower`把请求的方法转换成小写

    # Get the appropriate handler method
    if request.method.lower() in self.http_method_names:
        handler = getattr(self, request.method.lower(),
                          self.http_method_not_allowed)
    else:
        handler = self.http_method_not_allowed

    response = handler(request, *args, **kwargs)



再通过通过反射的方式来执行`UsersView`类中的get或post等自定义方法		

需要注意的是,在执行`initial`方法之前,使用了`try/except`方法来进行异常处理
		
如果执行`initial`方法的时候出现错误,就调用`handle_exception`来处理`initial`方法抛出的异常,返回正确的响应信息
		
    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        return response

在前面,如果`initial`方法执行完成没有抛出异常,则根据反射执行自定义的请求方法,然后返回响应信息

如果`initial`方法抛出异常则执行`handle_exception`方法处理抛出的异常,也返回响应信息

等到上面的过程执行完成后,再执行`finalize_response`方法把最终的响应信息返回给客户端的浏览器

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Returns the final response object.
        """
        # Make the error obvious if a proper response is not returned
        assert isinstance(response, HttpResponseBase), (
            'Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` '
            'to be returned from the view, but received a `%s`'
            % type(response)
        )

        if isinstance(response, Response):
            if not getattr(request, 'accepted_renderer', None):
                neg = self.perform_content_negotiation(request, force=True)
                request.accepted_renderer, request.accepted_media_type = neg

            response.accepted_renderer = request.accepted_renderer
            response.accepted_media_type = request.accepted_media_type
            response.renderer_context = self.get_renderer_context()

        # Add new vary headers to the response instead of overwriting.
        vary_headers = self.headers.pop('Vary', None)
        if vary_headers is not None:
            patch_vary_headers(response, cc_delim_re.split(vary_headers))

        for key, value in self.headers.items():
            response[key] = value

        return response
 
所以总结:

`REST framework`请求的生命周期为:

    1.请求到达服务端,经过WSGI和中间件到达路由系统
    2.路由系统执行配置的CBV或者FBV中的dispatch方法
    3.在dispatch方法中,request方法被封装添加了解析器,认证方法及选择器等方法
    4.然后执行initial方法
    5.再获取版本,进行认证操作,权限操作和节流操作
    6.最后执行自定义的get,post,push,delete等自定义方法
    7.在执行initial方法之前,通过try来捕获可能出现的异常
    8.如果出现异常,就执行handle_exception方法来处理捕获到的异常
    9.不管是否出现异常,最后的返回值都通过finalize_response方法来处理响应的内容