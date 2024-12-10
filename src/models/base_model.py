from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import Optional
import datetime

Base = declarative_base()
class AbstractModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class Person(AbstractModel):
    __abstract__ = True
    surname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str]
    phone_number: Mapped[str]


class UserModel(AbstractModel):
    __tablename__ = "users"
    login: Mapped[str]
    password: Mapped[str]
    # worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    # worker: Mapped["WorkerModel"] = relationship(back_populates="user")


class WorkerModel(Person):
    __tablename__ = "workers"
    position_at_work_id: Mapped[int | None] = mapped_column(ForeignKey("positions_at_work.id", ondelete="SET NULL"))
    position_at_work: Mapped["PositionAtWorkModel"] = relationship(back_populates="workers")
    # user: Mapped["UserModel"] = relationship(back_populates="worker")


class PositionAtWorkModel(AbstractModel):
    __tablename__ = "positions_at_work"
    position: Mapped[str]
    salary: Mapped[int]
    workers: Mapped[list["WorkerModel"]] = relationship(back_populates="position_at_work")
# Этажи
class FloorModel(AbstractModel):
    __tablename__ = "floors"
    number: Mapped[int]
    rooms: Mapped[list["RoomModel"]] = relationship(back_populates="floor")

# Комнаты
class RoomModel(AbstractModel):
    __tablename__ = "rooms"
    number: Mapped[int]
    floor_id: Mapped[int] = mapped_column(ForeignKey("floors.id", ondelete="CASCADE"))
    room_type_id: Mapped[int | None] = mapped_column(ForeignKey("room_types.id", ondelete="SET NULL"))
    room_type: Mapped["RoomTypeModel"] = relationship(back_populates="rooms")
    occupants: Mapped[list["OccupantModel"]] = relationship(back_populates="room")
    furniture: Mapped[list["FurnitureModel"]] = relationship(back_populates="room")
    floor: Mapped["FloorModel"] = relationship(back_populates="rooms")


class RoomTypeModel(AbstractModel):
    __tablename__ = "room_types"
    max_occupants: Mapped[int]
    area: Mapped[int]
    rooms: Mapped[list["RoomModel"]] = relationship(back_populates="room_type")
    cost_per_month: Mapped[list["CostPerMonthModel"]] = relationship(back_populates="room_type")


# Жильцы
class OccupantModel(Person):
    __tablename__ = "occupants"
    birth_date: Mapped[datetime.date]
    check_in_date: Mapped[datetime.date]
    room_id: Mapped[int | None] = mapped_column(ForeignKey("rooms.id", ondelete="SET NULL"))
    room: Mapped["RoomModel"] = relationship(back_populates="occupants")
    payments: Mapped[list["PaymentModel"]] = relationship(back_populates="occupant")


class FurnitureModel(AbstractModel):
    __tablename__ = "furniture"
    name: Mapped[str]
    description: Mapped[str]
    cost: Mapped[int]
    room_id: Mapped[int | None] = mapped_column(ForeignKey("rooms.id", ondelete="SET NULL"))
    room: Mapped[Optional["RoomModel"]] = relationship(back_populates="furniture")


class PaymentModel(AbstractModel):
    __tablename__ = "payments"
    payment_date: Mapped[datetime.date]
    number_of_month_paid: Mapped[int]
    cost_per_month_id: Mapped[int] = mapped_column(ForeignKey("cost_per_month.id", ondelete="CASCADE"))
    occupant_id: Mapped[int] = mapped_column(ForeignKey("occupants.id", ondelete="CASCADE"))
    cost_per_month: Mapped["CostPerMonthModel"] = relationship(back_populates="payments")
    occupant: Mapped["OccupantModel"] = relationship(back_populates="payments")



class CostPerMonthModel(AbstractModel):
    __tablename__ = "cost_per_month"
    price_date: Mapped[datetime.datetime]
    price: Mapped[int]
    room_type_id: Mapped[int | None] = mapped_column(ForeignKey("room_types.id", ondelete="SET NULL"))
    room_type: Mapped["RoomTypeModel"] = relationship(back_populates="cost_per_month")
    payments: Mapped[list["PaymentModel"]] = relationship(back_populates="cost_per_month")
