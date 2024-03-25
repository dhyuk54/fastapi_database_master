import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

# 设置环境变量 ENV_STATE 为 "test",以确保使用测试配置
os.environ["ENV_STATE"] = "test"
from storeapi.database import database  # noqa: E402
from storeapi.main import app  # noqa: E402

"""
anyio_backend fixture:
这个 fixture 指定了使用 "asyncio" 作为 anyio 的后端。
anyio 是一个异步编程库,用于支持多个异步框架。
通过设置 scope="session",这个 fixture 在整个测试会话中只会被执行一次。
"""
# 定义一个 pytest fixture,指定使用 "asyncio" 作为 anyio 后端
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


"""
这个 fixture 创建了一个 TestClient 实例,用于测试 FastAPI 应用。
TestClient 是 FastAPI 提供的测试客户端,可以模拟发送 HTTP 请求到 FastAPI 应用。
通过 yield 语句返回 TestClient 实例,以便在测试函数中使用。
"""
# 定义一个 pytest fixture,创建一个 TestClient 实例,用于测试 FastAPI 应用
@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


"""
这个 fixture 用于管理数据库连接的建立和断开。
在每个测试函数运行之前,它会异步地建立数据库连接(await database.connect())。
在测试函数运行完毕后,它会异步地断开数据库连接(await database.disconnect())。
通过设置 autouse=True,这个 fixture 会自动应用于所有的测试函数,无需显式地将其作为参数传递。
"""
# 定义一个 pytest fixture,自动在每个测试函数运行前后建立和断开数据库连接
@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()

"""
这个 fixture 创建了一个异步的 TestClient 实例,用于测试异步端点。
它使用了 httpx 库提供的 AsyncClient 类,可以发送异步 HTTP 请求。
通过 async with 语句创建 AsyncClient 实例,并将 app 和 base_url 传递给它。
使用 yield 语句返回 AsyncClient 实例,以便在异步测试函数中使用。
"""
# 定义一个 pytest fixture,创建一个异步的 TestClient 实例,用于测试异步端点
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac