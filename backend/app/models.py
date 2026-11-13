from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

SEGMENTS = ("B2G", "B2B")
ACTIVITY_STATUSES = ("NOT_VISITED", "VISITED")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    activities: Mapped[list["Activity"]] = relationship(back_populates="sales")


class Entity(Base):
    __tablename__ = "entities"
    __table_args__ = (
        CheckConstraint("segment IN ('B2G', 'B2B')", name="segment"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    type: Mapped[str] = mapped_column(String(60), nullable=False)
    segment: Mapped[str] = mapped_column(String(3), nullable=False)
    region: Mapped[str] = mapped_column(String(80), nullable=False)

    activities: Mapped[list["Activity"]] = relationship(back_populates="entity")


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("segment IN ('B2G', 'B2B')", name="segment"),
        CheckConstraint(
            "status IN ('NOT_VISITED', 'VISITED')", name="status"
        ),
        Index("ix_activities_visit_date", "visit_date"),
        Index("ix_activities_sales_id", "sales_id"),
        Index("ix_activities_segment", "segment"),
        Index("ix_activities_status", "status"),
    )

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    entity_id: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("entities.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Snapshot agar kunjungan lama tetap terbaca walau master berubah.
    entity_name: Mapped[str] = mapped_column(String(160), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(60), nullable=False)
    entity_region: Mapped[str] = mapped_column(String(80), nullable=False)
    segment: Mapped[str] = mapped_column(String(3), nullable=False)
    visit_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="NOT_VISITED"
    )
    sales_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    entity: Mapped[Entity | None] = relationship(back_populates="activities")
    sales: Mapped[User] = relationship(back_populates="activities")
