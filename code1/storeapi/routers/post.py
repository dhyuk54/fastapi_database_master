from fastapi import APIRouter, HTTPException
from code1.storeapi.database import comment_table, database, post_table
from code1.storeapi.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

# 创建一个 APIRouter 实例,用于定义路由
router = APIRouter()


# 定义一个异步函数 find_post,用于查找指定 ID 的帖子
async def find_post(post_id: int):
    # 构建 SQL 查询,选择 post_table 中 id 等于 post_id 的行
    query = post_table.select().where(post_table.c.id == post_id)
    # 使用 database.fetch_one 方法执行查询,返回结果
    return await database.fetch_one(query)


# 定义一个路由,响应 POST 请求,用于创建帖子
@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    # 1. 创建帖子:
    #    - 客户端发送 POST 请求到 "/post" 端点,请求体包含帖子的内容(UserPostIn)。
    #    - 路由处理函数 `create_post` 接收请求,将 UserPostIn 实例转换为字典。
    data = post.model_dump()  # 之前使用 .dict()
    #    - 构建 SQL 插入语句,将帖子数据插入到 post_table 中。
    query = post_table.insert().values(data)
    #    - 使用 `database.execute` 方法执行插入操作,返回最后插入的记录的 ID。
    last_record_id = await database.execute(query)
    #    - 将插入的数据与 ID 组合成字典,并返回给客户端。
    return {**data, "id": last_record_id}


# 定义一个路由,响应 GET 请求,用于获取所有帖子
@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    # 2. 获取所有帖子:
    #    - 客户端发送 GET 请求到 "/post" 端点。
    #    - 路由处理函数 `get_all_posts` 接收请求。
    #    - 构建 SQL 查询,选择 post_table 中的所有行。
    query = post_table.select()
    #    - 使用 `database.fetch_all` 方法执行查询,返回所有帖子数据。
    #    - 将查询结果返回给客户端。
    return await database.fetch_all(query)


# 定义一个路由,响应 POST 请求,用于创建评论
@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    # 3. 创建评论:
    #    - 客户端发送 POST 请求到 "/comment" 端点,请求体包含评论的内容和关联的帖子 ID(CommentIn)。
    #    - 路由处理函数 `create_comment` 接收请求。
    #    - 使用 `find_post` 函数查找指定 ID 的帖子。
    post = await find_post(comment.post_id)
    #      - `find_post` 函数构建 SQL 查询,选择 post_table 中 id 等于指定值的行。
    #      - 使用 `database.fetch_one` 方法执行查询,返回结果。
    #    - 如果帖子不存在,抛出 HTTPException 异常,状态码为 404。
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    #    - 将 CommentIn 实例转换为字典。
    data = comment.model_dump()  # 之前使用 .dict()
    #    - 构建 SQL 插入语句,将评论数据插入到 comment_table 中。
    query = comment_table.insert().values(data)
    #    - 使用 `database.execute` 方法执行插入操作,返回最后插入的记录的 ID。
    last_record_id = await database.execute(query)
    #    - 将插入的数据与 ID 组合成字典,并返回给客户端。
    return {**data, "id": last_record_id}


# 定义一个路由,响应 GET 请求,用于获取指定帖子的评论
@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    # 4. 获取指定帖子的评论:
    #    - 客户端发送 GET 请求到 "/post/{post_id}/comment" 端点,其中 {post_id} 为要获取评论的帖子 ID。
    #    - 路由处理函数 `get_comments_on_post` 接收请求,获取 post_id 参数。
    #    - 构建 SQL 查询,选择 comment_table 中 post_id 等于指定值的行。
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    #    - 使用 `database.fetch_all` 方法执行查询,返回所有匹配的评论数据。
    #    - 将查询结果返回给客户端。
    return await database.fetch_all(query)


# 定义一个路由,响应 GET 请求,用于获取指定帖子及其评论
@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    # 5. 获取指定帖子及其评论:
    #    - 客户端发送 GET 请求到 "/post/{post_id}" 端点,其中 {post_id} 为要获取的帖子 ID。
    #    - 路由处理函数 `get_post_with_comments` 接收请求,获取 post_id 参数。
    #    - 使用 `find_post` 函数查找指定 ID 的帖子。
    post = await find_post(post_id)
    #      - `find_post` 函数构建 SQL 查询,选择 post_table 中 id 等于指定值的行。
    #      - 使用 `database.fetch_one` 方法执行查询,返回结果。
    #    - 如果帖子不存在,抛出 HTTPException 异常,状态码为 404。
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    #    - 调用 `get_comments_on_post` 函数获取该帖子的评论列表。
    #      - `get_comments_on_post` 函数构建 SQL 查询,选择 comment_table 中 post_id 等于指定值的行。
    #      - 使用 `database.fetch_all` 方法执行查询,返回所有匹配的评论数据。
    #    - 将帖子信息和评论列表组合成字典,并返回给客户端。
    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }