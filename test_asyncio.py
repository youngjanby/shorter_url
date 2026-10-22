import asyncio

async def fetch_user(user_id: str):
    print(f"Начинаю скачивать данные для пользователя {user_id}")

    await asyncio.sleep(2)

    print(f"Данные пользователя {user_id} успешно скачаны")

    return {"id": user_id, "status": "active"}

async def main():
    results = await asyncio.gather(
        fetch_user("1b34"),
        fetch_user("2b35"),
        fetch_user("3b35")
    )

    print("Результаты: ", results)

asyncio.run(main())