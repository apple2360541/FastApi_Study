from fastapi import APIRouter

app = APIRouter()


def fun():
    try:
        print('1')
        db = 'SessinLocal()'
        yield db
    finally:
        print('3')


for i in fun():
    print(i)
    print('2')
# <generator object fun at 0x000001A87F9AB200>
print(fun())
