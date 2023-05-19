from aiodal.oqm import query, filters, dbentity
from aiodal import dal
import sqlalchemy as sa
from typing import Any, Optional
import dataclasses
import pytest

pytestmark = pytest.mark.anyio


async def test_dbentity_delete_stmt(transaction):
    # setup
    author = transaction.get_table("author")
    book = transaction.get_table("book")

    stmt = sa.insert(author).values(**{"name": "author1"}).returning(author)
    result = await transaction.execute(stmt)
    author1 = result.one()

    stmt = (
        sa.insert(book)
        .values(**{"name": "book1", "author_id": author1.id})
        .returning(book)
    )
    result = await transaction.execute(stmt)
    book1 = result.one()

    # actual testing
    # params = BookQueryParams(name="book1")
    # l = BookListQ(where=params)
    # res = await l.list(transaction)
    # assert len(res) == 1

    # book1_exp = res.pop()
    # assert book1_exp.id == book1.id
    # assert book1_exp.name == book1.name
    # assert book1_exp.author_id == book1.author_id

    # params = BookQueryParams(author_name_contains="author")
    # l = BookListQ(where=params)
    # res = await l.list(transaction)
    # assert len(res) == 1

    # id_params = query.IdFilter(id_=book1.id, tablename="book")
    # dq = BookDetailQ(where=id_params)
    # res = await dq.detail(transaction)

    # assert res.id == book1.id
    # assert res.name == book1.name
    # assert res.author_id == book1.author_id

    await transaction.rollback()