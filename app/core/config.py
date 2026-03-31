from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # ---------- DB ----------
    db_host: str = "host.docker.internal"
    db_port: int = 5432
    db_name: str = "traceledger"
    db_user: str = "postgres"
    db_password: str = ""

    # ---------- Redis ----------
    redis_host: str = "localhost"
    redis_port: int = 6379

    # ---------- RabbitMQ ----------
    rabbitmq_host: str = "localhost"

    # ---------- Elasticsearch ----------
    elastic_search_host: str = "http://localhost:9200"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()