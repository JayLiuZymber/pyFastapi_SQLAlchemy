# test_xxx.py

from crud import *
from models import *
from fixtures import sqlite_session_fixture
from sqlalchemy.orm import Session
from datetime import datetime
import schemas

use_fixtures = [sqlite_session_fixture]

def test_create_supp(sqlite_session: Session):
    data = schemas.SupplierCreate(name="test_user", taxid=12345678)

    result: Supplier = create_supp(supp=data, db=sqlite_session)
    print(result.__dict__)

    assert (result.name == data.name) & (result.taxid == data.taxid)