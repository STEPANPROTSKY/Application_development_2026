# Правка руками: генератор пропускал любой токен. Неизвестный токен -> None -> 401.
TOKENS = {"alice-token": "alice", "bob-token": "bob"}


def info_from_bearerAuth(token):
    user = TOKENS.get(token)
    return {"uid": user} if user else None
