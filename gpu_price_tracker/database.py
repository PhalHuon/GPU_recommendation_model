# gpu_price_tracker/database.py

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import json

Base = declarative_base()

class GPU(Base):
    __tablename__ = 'gpus'
    
    id = Column(Integer, primary_key=True)
    brand = Column(String(50))
    model = Column(String(50))
    name = Column(String(255))
    manufacturer = Column(String(100))
    price = Column(Float)
    currency = Column(String(10))
    original_price = Column(Float)
    retailer = Column(String(50))
    url = Column(String(1000))
    availability = Column(String(100))
    shipping_cost = Column(String(100))
    rating = Column(Float)
    num_reviews = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    specifications = Column(Text)  # JSON string
    
    def __repr__(self):
        return f"<GPU(name='{self.name}', price={self.price}, retailer='{self.retailer}')>"

class Database:
    def __init__(self, connection_string=None):
        if connection_string is None:
            # Default to a local MySQL connection
            connection_string = "mysql+pymysql://root:password@localhost/gpu_tracker"
        
        self.engine = create_engine(connection_string)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        
        # Create a session factory
        self.Session = sessionmaker(bind=self.engine)
    
    def store_gpu(self, item):
        """Store a GPU item in the database"""
        session = self.Session()
        
        # Convert specifications dict to JSON string if needed
        specs = item.get('specifications')
        if specs and isinstance(specs, dict):
            specs_json = json.dumps(specs)
        else:
            specs_json = None
            
        gpu = GPU(
            brand=item.get('brand'),
            model=item.get('model'),
            name=item.get('name'),
            manufacturer=item.get('manufacturer'),
            price=item.get('price'),
            currency=item.get('currency', 'USD'),
            original_price=item.get('original_price'),
            retailer=item.get('retailer'),
            url=item.get('url'),
            availability=item.get('availability'),
            shipping_cost=item.get('shipping_cost'),
            rating=item.get('rating'),
            num_reviews=item.get('num_reviews'),
            specifications=specs_json
        )
        
        try:
            session.add(gpu)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error storing GPU: {e}")
            return False
        finally:
            session.close()
    
    def get_all_gpus(self):
        """Retrieve all GPUs from the database"""
        session = self.Session()
        gpus = session.query(GPU).all()
        session.close()
        return gpus
    
    def get_gpus_by_brand_model(self, brand, model):
        """Retrieve GPUs by brand and model"""
        session = self.Session()
        gpus = session.query(GPU).filter_by(brand=brand, model=model).all()
        session.close()
        return gpus
    
    def get_cheapest_gpus(self, limit=5):
        """Get the cheapest GPUs in the database"""
        session = self.Session()
        gpus = session.query(GPU).filter(GPU.price.isnot(None)).order_by(GPU.price.asc()).limit(limit).all()
        session.close()
        return gpus