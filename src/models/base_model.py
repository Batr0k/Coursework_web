from sqlalchemy.orm import declarative_base, mapped_column, Mapped

Base = declarative_base()
class AbstractModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)


