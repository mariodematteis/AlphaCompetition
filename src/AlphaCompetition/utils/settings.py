from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_prefix='TWS_',
                                      env_file_encoding='UTF-8',
                                      extra='ignore')
    
    clientid: int = Field(default=0)
    username: str = Field(default='')
    password: str = Field(default='')
    ipaddress: str = Field(default='0.0.0.0')
    port: int = Field(default=0)

@lru_cache
def get_settings() -> EnvSettings:
    return EnvSettings()

@lru_cache
def get_client_id() -> int:
    return get_settings().clientid

@lru_cache
def get_username() -> str:
    return get_settings().username

@lru_cache
def get_password() -> str:
    return get_settings().password

@lru_cache
def get_ipaddress() -> str:
    return get_settings().ipaddress

@lru_cache
def get_port_address() -> int:
    return get_settings().port
