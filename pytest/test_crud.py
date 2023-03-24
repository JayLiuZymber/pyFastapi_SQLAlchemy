# test_xxx.py

from crud import * # function
from models import * # class
from fixtures import sqlite_session_fixture
from sqlalchemy.orm import Session
import schemas
import pytest

use_fixtures = [sqlite_session_fixture]

# sqlite_session from @pytest.fixture(name='sqlite_session') in fixtures.py
def test_create_supp_(sqlite_session: Session):
    data = schemas.SupplierCreate(name="test_user", taxid=12345678)
    result: Supplier = create_supp(supp=data, db=sqlite_session)
    print(result.__dict__)

    assert (result.name == data.name)
    assert (result.taxid == data.taxid)
    
def test_create_supp_2(sqlite_session: Session):
    input = schemas.SupplierCreate(name="", taxid=12)
    result: Supplier = create_supp(supp=input, db=sqlite_session)
    assert (result.name == input.name)
    assert (result.taxid == input.taxid)

def test_create_supp_3(sqlite_session: Session):
    name = "test"
    taxid = 34
    input = schemas.SupplierCreate(name=name, taxid=taxid)
    result: Supplier = create_supp(sqlite_session, input)
    assert (result.name == name)
    assert (result.taxid == taxid)
    