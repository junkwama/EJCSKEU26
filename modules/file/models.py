from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import (
    Column, ForeignKey, Index, Integer, 
    UniqueConstraint, text
)

class File(SQLModel, table=True):

    __tablename__ = "file"

    id: int | None = Field(default=None, primary_key=True)
    original_name: str | None = Field(default=None, nullable=True, max_length=255)
    file_name: str = Field(..., max_length=255, unique=True)
    mimetype: str = Field(..., max_length=255)
    size: int = Field(...)

    signed_url: str | None = Field(default=None, nullable=True, max_length=1000)
    signed_url_expiration_date: datetime | None = Field(default=None, nullable=True, max_length=1000)
    
    est_supprimee: bool = Field(
        default=False,
        nullable=False,
        sa_column_kwargs={"server_default": text("0")},
        description="Est supprimée (soft delete)",
    )
    date_suppression: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Date de suppression logique",
    )
    date_creation: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        description="Date de création",
    )
    date_modification: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "server_onupdate": text("CURRENT_TIMESTAMP"),
        },
        description="Date de modification",
    )

    id_document_type: int = Field(
		sa_column=Column(
			Integer,
			ForeignKey("document_type.id", ondelete="RESTRICT"),
			nullable=False,
		)
	)
    id_document: int = Field(...)

    __table_args__ = (
		UniqueConstraint("file_name", name="uq_files_file_name"),
		Index("idx_files_document", "id_document_type", "id_document"),
		Index("idx_files_est_supprimee", "est_supprimee"),
	)

    class Config:
        from_attributes = True


class FileProjFlat(BaseModel):
	id: int
	original_name: str | None
	file_name: str
	mimetype: str
	size: int
	signed_url: str | None
	signed_url_expiration_date: datetime | None
	id_document_type: int
	id_document: int
	est_supprimee: bool
	date_suppression: datetime | None
	date_creation: datetime
	date_modification: datetime

	class Config:
		from_attributes = True
