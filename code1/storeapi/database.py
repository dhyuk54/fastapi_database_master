# 导入必要的库
import databases  # 导入databases库,用于异步数据库操作
import sqlalchemy  # 导入sqlalchemy库,用于定义数据库表结构和执行数据库操作

from code1.storeapi.config import config  # 从storeapi.config模块导入config对象,用于获取配置信息

metadata = sqlalchemy.MetaData()  # 创建一个MetaData对象,用于存储数据库表的元数据信息

# 定义posts表的结构
post_table = sqlalchemy.Table(
    "posts",  # 表名为"posts"
    metadata,  # 关联到metadata对象
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),  # 定义id列,类型为Integer,是主键
    sqlalchemy.Column("body", sqlalchemy.String)  # 定义body列,类型为String
)

# 定义comments表的结构
comment_table = sqlalchemy.Table(
    "comments",  # 表名为"comments"
    metadata,  # 关联到metadata对象
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),  # 定义id列,类型为Integer,是主键
    sqlalchemy.Column("body", sqlalchemy.String),  # 定义body列,类型为String
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False)  # 定义post_id列,类型为ForeignKey,关联到posts表的id列,不允许为空
)

# 创建数据库引擎
engine = sqlalchemy.create_engine(
    config.DATABASE_URL,  # 从配置对象获取数据库连接的URL
    connect_args={"check_same_thread": False}  # 设置连接参数,禁用对线程安全的检查(仅适用于SQLite)
)

metadata.create_all(engine)  # 使用数据库引擎创建所有定义的表结构

# 创建异步数据库连接
database = databases.Database(
    config.DATABASE_URL,  # 从配置对象获取数据库连接的URL
    force_rollback=config.DB_FORCE_ROLL_BACK  # 从配置对象获取是否强制回滚的设置
)