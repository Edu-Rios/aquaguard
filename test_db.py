from sqlalchemy import text
from app.db.session import SessionLocal

def test_connection():
    print("Intentando conectar a Supabase...")
    try:
        # Intenta abrir la sesión usando la URL de tu .env
        db = SessionLocal()
        
        # Ejecuta una consulta súper básica (pedirle a Postgres que devuelva un 1)
        result = db.execute(text("SELECT 1")).scalar()
        
        if result == 1:
            print("✅ ¡Éxito! La conexión a Supabase está funcionando perfectamente.")
        
        # Cerramos la sesión por buenas prácticas
        db.close()
        
    except Exception as e:
        print("❌ Error al conectar con la base de datos. Revisa tu archivo .env:")
        print(e)

if __name__ == "__main__":
    test_connection()