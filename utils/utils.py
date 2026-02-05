import traceback
from datetime import datetime

# used evrywhere: don't delete them
from pydantic import Field as PydanticField
from sqlmodel import Field as SQLModelField
# ----- 


def log(e: Exception):
  exc = traceback.format_exc()
  print(
    "\n***************************************\n", 
    "Error:", exc, "\nDate:", datetime.now(),
    "\n\nDetails:", "\n--------\n", exc,
    "\n***************************************\n"
  )

