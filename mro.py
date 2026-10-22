class Base:
    def action(self):
        print("Действие из Base")

class Left(Base):
    def action(self):
        super().action()

class Right(Base):
    def action(self):
        super().action()

class Child(Right, Left):
    pass

obj = Child()
obj.action()
