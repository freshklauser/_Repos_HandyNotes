
### 1. 传参
```buildoutcfg
test
```

### 2. 切入点函数 (接入点函数)
 `tornado.web.RequestHandler`子类继承，切入点函数
- `initialize` 

  初始化继承类，`__init__`不能被重写，需要的话重写 `initialize`
  
  `directly and subclasses should not override ``__init__`` (override ~RequestHandler.initialize instead).`
  
  该方法被子类重写，实现了RequestHandler子类实现的初始化过程。可以为该函数传递参数（参数来源于配置URL映射的定义）,如下所示：

```buildoutcfg
initialize = _initialize  # type: Callable[..., None]
    """Hook for subclass initialization. Called for each request.

    A dictionary passed as the third argument of a ``URLSpec`` will be
    supplied as keyword arguments to ``initialize()``.

    Example::

        class ProfileHandler(RequestHandler):
            def initialize(self, database):
                self.database = database

            def get(self, username):
                ...

        app = Application([
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
            ])
    """
```

- `prepare`

  `Called at the beginning of a request before  `get`/`post`/etc.`, 在`http`行为方法之前会被调用
  
  `prepare()`方法用于调用请求处理（`get、post`等）方法之前的初始化处理，通常用来做资源初始化操作

```buildoutcfg
Override this method to perform common initialization regardless
        of the request method.

        Asynchronous support: Use ``async def`` or decorate this method with
        `.gen.coroutine` to make it asynchronous.
        If this method returns an  ``Awaitable`` execution will not proceed
        until the ``Awaitable`` is done.
```

- `on-finish`

  `on_finish()`方法用于请求处理结束后的一些清理工作，通常用来清理对象占用的内存或者关闭数据库连接等工作。

```buildoutcfg
test
```