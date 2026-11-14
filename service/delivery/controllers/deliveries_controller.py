# Написано руками: генератор оставил заглушки `return 'do some magic!'`.
# `user` подставляет connexion из security_controller, тело запроса приходит в `body`.

# Хранилище в памяти. owner, courier_id и cost — внутренние поля, наружу не отдаются.
DELIVERIES = {
    1: {"owner": "alice", "status": "created", "address": "г. Екатеринбург, ул. Ленина, 1",
        "recipientName": "Алиса", "weightKg": 1.0, "comment": None, "price": 350.0,
        "courier_id": None, "cost": 200.0},
    2: {"owner": "bob", "status": "in_transit", "address": "г. Москва, ул. Тверская, 7",
        "recipientName": "Боб", "weightKg": 3.0, "comment": None, "price": 450.0,
        "courier_id": 17, "cost": 260.0},
    3: {"owner": "alice", "status": "in_transit", "address": "г. Казань, ул. Баумана, 3",
        "recipientName": "Алиса", "weightKg": 0.5, "comment": None, "price": 325.0,
        "courier_id": 4, "cost": 180.0},
}
PUBLIC = ("status", "address", "recipientName", "weightKg", "comment", "price")


def _dto(delivery_id):
    d = DELIVERIES[delivery_id]
    return {"id": delivery_id, **{k: d[k] for k in PUBLIC if d[k] is not None}}


def _error(code, message):
    return {"code": code, "message": message}, code


def _check(delivery_id, user, need_created=False):
    """404 — нет; 403 — чужая; 409 — уже отправлена/закрыта, менять нельзя."""
    d = DELIVERIES.get(delivery_id)
    if d is None:
        return _error(404, "Доставка не найдена")
    if d["owner"] != user:
        return _error(403, "Это доставка другого клиента")
    if need_created and d["status"] != "created":
        return _error(409, f"Нельзя изменить доставку в статусе {d['status']}")
    return None


def list_deliveries(user, status=None):  # noqa: E501
    """Получить список доставок текущего клиента"""
    return [_dto(i) for i, d in DELIVERIES.items()
            if d["owner"] == user and (status is None or d["status"] == status)]


def create_delivery(body, user):  # noqa: E501
    """Оформить новую доставку. Цена: 300 ₽ + 50 ₽ за кг."""
    new_id = max(DELIVERIES) + 1
    DELIVERIES[new_id] = {
        "owner": user, "status": "created", "address": body["address"],
        "recipientName": body["recipientName"], "weightKg": body["weightKg"],
        "comment": body.get("comment"), "price": round(300 + 50 * body["weightKg"], 2),
        "courier_id": None, "cost": None,
    }
    return _dto(new_id), 201


def get_delivery(delivery_id, user):  # noqa: E501
    """Получить одну доставку и её текущий статус"""
    return _check(delivery_id, user) or _dto(delivery_id)


def update_delivery(delivery_id, body, user):  # noqa: E501
    """Изменить адрес или комментарий, пока доставка не отправлена"""
    err = _check(delivery_id, user, need_created=True)
    if err:
        return err
    for key in ("address", "comment"):
        if key in body:
            DELIVERIES[delivery_id][key] = body[key]
    return _dto(delivery_id)


def cancel_delivery(delivery_id, user):  # noqa: E501
    """Отменить доставку, пока она не отправлена"""
    err = _check(delivery_id, user, need_created=True)
    if err:
        return err
    DELIVERIES[delivery_id]["status"] = "cancelled"
    return None, 204
