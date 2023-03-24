# test_xxx.py

from main import * # function
from models import * # class
from fixtures import sqlite_session_fixture
from sqlalchemy.orm import Session
from fastapi import Request
import schemas
import pytest

use_fixtures = [sqlite_session_fixture]

# sqlite_session from @pytest.fixture(name='sqlite_session') in fixtures.py
def test_supp_(sqlite_session: Session):
    supplier = schemas.SupplierCreate(name="test", taxid=12345678)
    result: Supplier = create_supp(supplier=supplier, request=Request, db=sqlite_session)

    # print(result.__dict__)
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
