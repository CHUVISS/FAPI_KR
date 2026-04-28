from app.database import SessionLocal, engine
from app.models import Product, Base

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Product).count()
        if existing == 0:
            p1 = Product(title="Ноутбук", price=59990.0, count=10)
            p2 = Product(title="Мышь", price=1500.0, count=50)
            db.add_all([p1, p2])
            db.commit()
            print("Добавлены 2 тестовые записи.")
        
        products = db.query(Product).all()
        print(f"\nВ таблице 'products' {len(products)} записей:")
        for p in products:
            desc = getattr(p, "description", "Поле отсутствует")
            print(f"  ID:{p.id} | {p.title} | {p.price}₽ | шт:{p.count} | desc:{desc}")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    run()