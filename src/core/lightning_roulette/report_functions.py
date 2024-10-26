from src.clients.mongodb_client import Mongo
from src.core.lightning_roulette.utils import resources

def create_report_win_lose_daily(client: Mongo, lang: str):
    wins, loses = client.obtain_win_lose_daily(db_name="RoobetDB")
    wins_percentage = 0 if wins == 0 else round((wins/(wins+loses))*100, 2)
    int_win_percentage = int(wins_percentage)
    decimal_win_percentage = int((wins_percentage - int_win_percentage) * 10)
    wins_percentage = int_win_percentage if decimal_win_percentage == 0 else f"{int_win_percentage}\\.{decimal_win_percentage}"
    messages = resources[lang]['default_messages']
    report = (f"{messages['report_wins_loses_daily_head']} 🟢 {wins} 🔴 {loses}\n" f"{messages['report_wins_loses_daily_body']} {wins_percentage}{messages['report_wins_loses_daily_foot']}")
    #print(f"Reporte diario generado en {lang}: {wins_percentage}")
    return report