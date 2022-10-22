from fastapi import APIRouter

routes = APIRouter()


@routes.get('/')
async def admin_create_user():
    return {
        'admin': 'administrator',
        'message': 'os testes testam',
        'number': 934,
        'pi': 3.141516,
        'user': 'dalmo',
        'emails': ['dalmo@email.com', 'felipe@email.com'],
        'password': '123123'
    }
