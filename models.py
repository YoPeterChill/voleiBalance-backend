from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String, nullable=False, unique=True
    )  # Agora o String está corretamente importado
    skill_level = Column(Float, nullable=False, default=0.0)

    checkins = relationship("Checkin", back_populates="player")


class Checkin(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)

    player = relationship("Player", back_populates="checkins")
