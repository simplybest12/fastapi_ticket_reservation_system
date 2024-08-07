from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_name: str = "Reservation_System"
    project_version: str = "1.0.0"
    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: str  # default postgres port is 5432
    postgres_db: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()
