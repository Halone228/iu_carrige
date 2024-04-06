from sqlalchemy.orm import DeclarativeBase, declarative_base, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


Base: DeclarativeBase = declarative_base()


class Vein(Base):
    __tablename__ = "vein_table"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str]
    url: Mapped[str]


class Source(Base):
    __tablename__ = "source_table"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    vein_id: Mapped[int] = ForeignKey("vein_table.id")
    slug: Mapped[str]
    _metadata: Mapped[dict] = mapped_column(
        JSON(),
        name='metadata'
    )


class Mineral(Base):
    __tablename__ = "mineral_table"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    html_text: Mapped[str]
    created_at: Mapped[datetime]
    source_id: Mapped[int] = mapped_column(ForeignKey("source_table.id"))


class Tag(Base):
    __tablename__ = "tag_table"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    descriptor: Mapped[str] = mapped_column(unique=True)


class MineralTag(Base):
    __tablename__ = "mineral_tag_table"
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag_table.id"), primary_key=True)
    mineral_id: Mapped[int] = mapped_column(
        ForeignKey("mineral_table.id"), primary_key=True
    )


class MineralAttachment(Base):
    __tablename__ = "mineral_attachment_table"
    attachment_id: Mapped[int] = mapped_column(primary_key=True)
    mineral_id: Mapped[int] = mapped_column(
        ForeignKey("mineral_table.id"), primary_key=True
    )


__all__ = ["Mineral", "Tag", "Vein", "Source",
           "MineralAttachment", "MineralTag"]
