# test_*.py or *_test.py

from main import * # function
from models import * # class
from fixtures import sqlite_session_fixture
from sqlalchemy.orm import Session
from fastapi import Request
from prints import printstd,  printout
import schemas
import pytest
import random, string

use_fixtures = [sqlite_session_fixture]

# sqlite_session from @pytest.fixture(name='sqlite_session') in fixtures.py
def test_supp_(sqlite_session: Session):
    supplier = schemas.SupplierCreate(name="test", taxid=12345678)
    result: Supplier = create_supp(supplier=supplier, request=Request, db=sqlite_session)

    # printstd(result.__dict__) #'終端機'頁
    printout(result.__dict__) #'輸出'頁
    assert (result.name == supplier.name)
    assert (result.taxid == supplier.taxid)
    assert (result.id != None )
    assert (result.products == [] )

def test_supp_2(sqlite_session: Session):
    name = "test12"
    taxid = 12
    input = schemas.SupplierCreate(name=name, taxid=taxid)
    result: Supplier = create_supp(input, Request, sqlite_session)
    assert (result.name == input.name)
    assert (result.taxid == input.taxid)
    assert (result.id != None)

def test_supp_3(sqlite_session: Session):
    name = "supplier"
    taxid = 34
    result: Supplier = create_supp(schemas.SupplierCreate(name=name, taxid=taxid), Request, sqlite_session)
    assert (result.name == name)
    assert (result.taxid == taxid)
    assert (result.id != None)

@pytest.mark.skip()
def test_skip():
    assert 1 + 1 == 3

import sys
@pytest.mark.skipif(condition=sys.platform == "win32", reason="測試跳過指定條件範例")
def test_skip_test_case_by_condition():
    assert 1 + 1 == 4

# -----------------------------------------------------------------------------
# 查詢DB執行SQL之前要先被阻擋 所以不用傳sqlite_session
def test_supp_name_null():
    with pytest.raises(HTTPException) as exc:
        supplier = schemas.SupplierCreate(name="", taxid=12345678)
        create_supp(supplier, Request, Session)
    assert isinstance(exc.value, HTTPException)
    assert exc.value.status_code == 422
    assert exc.value.detail == "Name can not be null"

def test_supp_taxid_0():
    with pytest.raises(HTTPException) as exc:
        supplier = schemas.SupplierCreate(name="name", taxid=0)
        create_supp(supplier, Request, Session)
    assert isinstance(exc.value, HTTPException)
    assert exc.value.status_code == 422

def test_supp_taxid_negative():
    with pytest.raises(HTTPException) as exc:
        supplier = schemas.SupplierCreate(name="name", taxid=-123)
        create_supp(supplier, Request, Session)
    assert isinstance(exc.value, HTTPException)
    assert exc.value.status_code == 422

def test_supp_taxid_exist(sqlite_session: Session):
    with pytest.raises(HTTPException) as exc:
        name = "supplier"
        taxid = 34
        result: Supplier = create_supp(schemas.SupplierCreate(name=name, taxid=taxid), Request, sqlite_session)
        assert (result.name == name)
        assert (result.taxid == taxid)
        assert (result.id != None)

        create_supp(schemas.SupplierCreate(name=name, taxid=taxid), Request, sqlite_session)
    assert isinstance(exc.value, HTTPException)
    assert exc.value.status_code == 422

# -----------------------------------------------------------------------------
# 隨機產生內容
def test_supp_x(sqlite_session: Session):
    # 大小寫字母
    name = ''.join(random.choice(string.ascii_letters) for x in range(10))
    taxid = random.randint(1, 99999999)
    input = schemas.SupplierCreate(name=name, taxid=taxid)
    result: Supplier = create_supp(input, Request, sqlite_session)
    assert (result.name == name)
    assert (result.taxid == taxid)
    assert (result.id != None)

def test_supp_x100(sqlite_session: Session):
    for i in range(100):
        test_supp_x(sqlite_session)

