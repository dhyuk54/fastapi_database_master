# 从functools模块导入lru_cache装饰器,用于缓存函数的返回值
from functools import lru_cache
# 从typing模块导入Optional类型注释,用于指定可选的类型
from typing import Optional

# 从pydantic_settings模块导入BaseSettings和SettingsConfigDict类,用于配置管理
from pydantic_settings import BaseSettings, SettingsConfigDict


# 定义基础配置类BaseConfig,继承自BaseSettings
class BaseConfig(BaseSettings):
    # 定义ENV_STATE属性,类型为可选的字符串,默认值为None
    ENV_STATE: Optional[str] = None
    # 打印ENV_STATE的值
    """
    加载.env文件。包含此代码是为了让pydantic加载.env文件。
    """
    # 定义model_config属性,使用SettingsConfigDict加载.env文件,忽略额外的环境变量
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


# 定义全局配置类GlobalConfig,继承自BaseConfig
class GlobalConfig(BaseConfig):
    # 定义DATABASE_URL属性,类型为可选的字符串,默认值为None
    DATABASE_URL: Optional[str] = None
    # 定义DB_FORCE_ROLL_BACK属性,类型为布尔值,默认值为False
    DB_FORCE_ROLL_BACK: bool = False


# 定义开发环境配置类DevConfig,继承自GlobalConfig
class DevConfig(GlobalConfig):
    # 定义model_config属性,使用SettingsConfigDict加载以"DEV_"为前缀的环境变量
    model_config = SettingsConfigDict(env_prefix="DEV_")
    # 打印model_config的值


# 定义生产环境配置类ProdConfig,继承自GlobalConfig
class ProdConfig(GlobalConfig):
    # 定义model_config属性,使用SettingsConfigDict加载以"PROD_"为前缀的环境变量
    model_config = SettingsConfigDict(env_prefix="PROD_")


# 定义测试环境配置类TestConfig,继承自GlobalConfig
class TestConfig(GlobalConfig):
    # 定义DATABASE_URL属性,类型为字符串,默认值为"sqlite:///test.db"
    DATABASE_URL: str = "sqlite:///test.db"
    # DB_FORCE_ROLL_BACK属性被注释掉,不会生效
    # DB_FORCE_ROLL_BACK: bool = True

    # 定义model_config属性,使用SettingsConfigDict加载以"TEST_"为前缀的环境变量
    model_config = SettingsConfigDict(env_prefix="TEST_")


# 定义get_config函数,使用lru_cache装饰器进行缓存
@lru_cache()
def get_config(env_state: str):
    """
    根据环境状态实例化配置对象。
    """
    # 定义configs字典,将环境状态映射到对应的配置类
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    # 根据env_state获取对应的配置类,并实例化返回
    return configs[env_state]()


# 获取BaseConfig的ENV_STATE值,并将其传递给get_config函数,获取对应的配置对象
config = get_config(BaseConfig().ENV_STATE)
# 打印获取到的配置对象
