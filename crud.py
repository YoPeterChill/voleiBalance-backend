from sqlalchemy.orm import Session
from models import Player, Checkin
from sqlalchemy.sql import func
import random

# Definir o número mínimo de jogadores para formar dois times
MIN_PLAYERS = 12
MAX_PLAYERS_PER_TEAM = 6


def balance_teams(db: Session):
    # Obter jogadores que fizeram check-in
    checkins = db.query(Checkin).all()
    if len(checkins) < MIN_PLAYERS:
        return {"error": "Jogadores insuficientes para formar dois times."}

    # Recuperar os jogadores a partir dos check-ins
    players = [
        db.query(Player).filter(Player.id == checkin.player_id).first()
        for checkin in checkins
    ]

    # Embaralhar os jogadores aleatoriamente
    random.shuffle(players)

    # Dividir jogadores aleatoriamente em dois times
    team_a, team_b = [], []
    for i, player in enumerate(players):
        (team_a if i % 2 == 0 else team_b).append(player)

    # Ajustar os times até que fiquem equilibrados
    def team_weight(team):
        return sum(player.skill_level for player in team)

    while abs(team_weight(team_a) - team_weight(team_b)) > 1.0:
        # Trocar jogadores aleatórios para balancear
        if team_weight(team_a) > team_weight(team_b):
            stronger_team, weaker_team = team_a, team_b
        else:
            stronger_team, weaker_team = team_b, team_a

        player_to_swap = random.choice(stronger_team)
        stronger_team.remove(player_to_swap)
        weaker_team.append(player_to_swap)

    # Lidar com jogadores extras
    extra_players = len(players) - (MAX_PLAYERS_PER_TEAM * 2)
    reserves = []
    third_team = []

    if extra_players > 0:
        if extra_players <= 6:
            # Selecionar reservas aleatoriamente
            reserves = random.sample(players, extra_players)
        else:
            # Criar um terceiro time
            third_team = players[-extra_players:]

    return {
        "team_a": [
            {"id": p.id, "name": p.name, "skill": p.skill_level} for p in team_a
        ],
        "team_b": [
            {"id": p.id, "name": p.name, "skill": p.skill_level} for p in team_b
        ],
        "reserves": (
            [{"id": p.id, "name": p.name, "skill": p.skill_level} for p in reserves]
            if reserves
            else None
        ),
        "third_team": (
            [{"id": p.id, "name": p.name, "skill": p.skill_level} for p in third_team]
            if third_team
            else None
        ),
    }


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
    # Verificar se o jogador tem check-ins registrados
    has_checkins = db.query(Checkin).filter(Checkin.player_id == player_id).first()
    if has_checkins:
        return {
            "error": "Não é possível excluir o jogador, pois ele tem check-ins registrados."
        }

    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        return None  # Retorna None se o jogador não existir

    db.delete(player)
    db.commit()
    return player


# Registrar um check-in
def create_checkin(db: Session, player_id: int):
    # Verificar se o jogador existe antes de criar o check-in
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        return {"error": "Jogador não encontrado"}

    # Verifica se o jogador já fez check-in hoje
    existing_checkin = (
        db.query(Checkin)
        .filter(
            Checkin.player_id == player_id,
            func.date(Checkin.timestamp) == func.current_date(),
        )
        .first()
    )

    if existing_checkin:
        return None  # Retorna None se o jogador já fez check-in hoje

    # Criar check-in garantindo que o player_id seja válido
    checkin = Checkin(player_id=player_id)
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin


# Listar todos os jogadores que fizeram check-in hoje
def get_checkins(db: Session):
    return (
        db.query(Checkin)
        .filter(func.date(Checkin.timestamp) == func.current_date())
        .all()
    )
