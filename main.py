from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import engine, Base, get_db, init_db
from schemas import PlayerCreate
from models import Player
from crud import create_player, get_players, get_player_by_id, update_player_skill, delete_player
from crud import create_checkin, get_checkins
from crud import balance_teams

app = FastAPI()

# Criar as tabelas no banco ao iniciar o FastAPI
init_db()

# Criar um jogador
@app.post("/players/")
def add_player(player: PlayerCreate, db: Session = Depends(get_db)):
    if player.skill_level < 0 or player.skill_level > 5:
        raise HTTPException(status_code=400, detail="O nível de habilidade deve estar entre 0 e 5.")
    
    # Verificar se o jogador já existe
    existing_player = db.query(Player).filter(Player.name == player.name).first()
    if existing_player:
        raise HTTPException(status_code=400, detail="Já existe um jogador com esse nome.")

    return create_player(db, player.name, player.skill_level)

# Listar todos os jogadores
@app.get("/players/")
def list_players(db: Session = Depends(get_db)):
    return get_players(db)

# Buscar um jogador por ID
@app.get("/players/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = get_player_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return player

# Atualizar nível de habilidade de um jogador
@app.put("/players/{player_id}")
def update_skill(player_id: int, new_skill_level: float, db: Session = Depends(get_db)):
    if new_skill_level < 0 or new_skill_level > 5:
        raise HTTPException(status_code=400, detail="O nível de habilidade deve estar entre 0 e 5.")
    player = update_player_skill(db, player_id, new_skill_level)
    if not player:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return player

@app.delete("/players/{player_id}")
def remove_player(player_id: int, db: Session = Depends(get_db)):
    player = delete_player(db, player_id)

    if player is None:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    if isinstance(player, dict) and "error" in player:
        raise HTTPException(status_code=400, detail=player["error"])

    return {"message": "Jogador removido com sucesso"}


# Endpoint principal
@app.get("/")
def read_root():
    return {"message": "API do Vôlei Balance está rodando!"}

# ✅ Endpoint para um jogador fazer check-in
@app.post("/checkin/{player_id}")
def player_checkin(player_id: int, db: Session = Depends(get_db)):
    checkin = create_checkin(db, player_id)
    
    if checkin is None:
        raise HTTPException(status_code=400, detail="Jogador já fez check-in hoje.")
    
    if isinstance(checkin, dict) and "error" in checkin:
        raise HTTPException(status_code=404, detail=checkin["error"])

    return {"message": "Check-in realizado com sucesso"}


# ✅ Endpoint para listar todos os check-ins de hoje
@app.get("/checkins/")
def list_checkins(db: Session = Depends(get_db)):
    checkins = get_checkins(db)
    return checkins

@app.get("/balance-teams/")
def get_balanced_teams(db: Session = Depends(get_db)):
    teams = balance_teams(db)
    if "error" in teams:
        raise HTTPException(status_code=400, detail=teams["error"])
    return teams

# Endpoint para testar conexão com o banco de dados
@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Conexão com o banco de dados bem-sucedida!"}
    except Exception as e:
        return {"error": str(e)}


