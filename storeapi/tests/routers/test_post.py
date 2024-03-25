import pytest
from httpx import AsyncClient

# 定义一个异步函数 create_post,用于创建一个新的帖子
# 接受 body 参数作为帖子的内容,async_client 参数作为异步测试客户端
# 返回创建的帖子的 JSON 数据
async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    return response.json()

# 定义一个异步函数 create_comment,用于创建一个新的评论
# 接受 body 参数作为评论的内容,post_id 参数作为关联的帖子 ID,async_client 参数作为异步测试客户端
# 返回创建的评论的 JSON 数据
async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post(
        "/comment", json={"body": body, "post_id": post_id}
    )
    return response.json()

# 定义一个 pytest fixture created_post,用于在测试中创建一个帖子
# 使用 async_client fixture 发送请求创建帖子,返回创建的帖子数据
@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post", async_client)

# 定义一个 pytest fixture created_comment,用于在测试中创建一个评论
# 使用 async_client 和 created_post fixture 发送请求创建评论,返回创建的评论数据
@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Test Comment", created_post["id"], async_client)

# 使用 @pytest.mark.anyio 标记异步测试函数
# 测试创建帖子的端点
@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"

    response = await async_client.post("/post", json={"body": body})

    assert response.status_code == 201
    assert {"id": 1, "body": body}.items() <= response.json().items()

# 测试创建帖子时缺少必要数据的情况
@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post("/post", json={})

    assert response.status_code == 422

# 测试获取所有帖子的端点
@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")

    assert response.status_code == 200
    assert response.json() != [created_post]

# 测试创建评论的端点
@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Test Comment"

    response = await async_client.post(
        "/comment", json={"body": body, "post_id": created_post["id"]}
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "body": body,
        "post_id": created_post["id"],
    }.items() <= response.json().items()

# 测试获取指定帖子的评论的端点
@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == [created_comment]

# 测试获取指定帖子的评论,但该帖子没有评论的情况
@pytest.mark.anyio
async def test_get_comments_on_post_empty(
    async_client: AsyncClient, created_post: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200
    assert response.json() == []

# 测试获取指定帖子及其评论的端点
@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code == 200
    assert response.json() == {"post": created_post, "comments": [created_comment]}

# 测试获取不存在的帖子及其评论的情况
@pytest.mark.anyio
async def test_get_missing_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get("/post/2")
    assert response.status_code == 200