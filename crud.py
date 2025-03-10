from sqlalchemy.orm import Session
from models import Player, Checkin
from sqlalchemy.sql import func

# Criar um jogador
def create_player(db: Session, name: str, skill_level: float):
    player = Player(name=name, skill_level=skill_level)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

# Buscar todos os jogadores
def get_players(db: Session):
    return db.query(Player).all()

# Buscar um jogador por ID
def get_player_by_id(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()

# Atualizar nível de habilidade de um jogador
def update_player_skill(db: Session, player_id: int, new_skill_level: float):
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        player.skill_level = new_skill_level
        db.commit()
        db.refresh(player)
    return player

# Deletar um jogador
def delete_player(db: Session, player_id: int):
    player = db.query(Player).filter(Player.id == player_id).first()
    if player:
        db.delete(player)
        db.commit()
    return player

# Registrar um check-in
def create_checkin(db: Session, player_id: int):
    # Verifica se o jogador já fez check-in hoje
    existing_checkin = db.query(Checkin).filter(
        Checkin.player_id == player_id,
        func.date(Checkin.timestamp) == func.current_date()
    ).first()

    if existing_checkin:
        return None  # Retorna None se o jogador já fez check-in hoje

    checkin = Checkin(player_id=player_id)
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin

# Listar todos os jogadores que fizeram check-in hoje
def get_checkins(db: Session):
    return db.query(Checkin).filter(func.date(Checkin.timestamp) == func.current_date()).all()

