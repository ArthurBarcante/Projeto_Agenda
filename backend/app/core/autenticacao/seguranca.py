from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha_texto_plano: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_texto_plano, senha_hash)
