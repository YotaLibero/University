from __future__ import annotations
from abc import ABC, abstractmethod

class ClothesFactory(ABC):
    """
    Интерфейс Абстрактной Фабрики объявляет набор методов, которые возвращают
    различные абстрактные продукты. Эти продукты называются семейством и связаны
    темой или концепцией высокого уровня. Продукты одного семейства обычно могут
    взаимодействовать между собой. Семейство продуктов может иметь несколько
    вариаций, но продукты одной вариации несовместимы с продуктами другой.
    """
    @abstractmethod
    def create_product_MC(self) -> MaleComplect:
        pass

    @abstractmethod
    def create_product_FC(self) -> FemaleComplect:
        pass

    @abstractmethod
    def create_product_CC(self) -> CombineComplect:
        pass


class CotoFeyFactory(ClothesFactory):
    """
    Конкретная Фабрика производит семейство продуктов одной вариации. Фабрика
    гарантирует совместимость полученных продуктов. Обратите внимание, что
    сигнатуры методов Конкретной Фабрики возвращают абстрактный продукт, в то
    время как внутри метода создается экземпляр конкретного продукта.
    """
    def create_product_MC(self) -> MaleComplect:
        return CotoFeyMaleComplect()

    def create_product_FC(self) -> FemaleComplect:
        return CotoFeyFemaleComplect()

    def create_product_CC(self) -> CombineComplect:
        return CotoFeyCombineComplect()


class ProfessorFactory(ClothesFactory):
    """
    Каждая Конкретная Фабрика имеет соответствующую вариацию продукта.
    """
    def create_product_MC(self) -> MaleComplect:
        return ProfessorMaleComplect()

    def create_product_FC(self) -> FemaleComplect:
        return ProfessorFemaleComplect()

    def create_product_CC(self) -> CombineComplect:
        return ProfessorCombineComplect()


class MaleComplect(ABC):
    """
    Каждый отдельный продукт семейства продуктов должен иметь базовый интерфейс.
    Все вариации продукта должны реализовывать этот интерфейс.
    """
    @abstractmethod
    def useful_function_a(self) -> str:
        pass


"""
Конкретные продукты создаются соответствующими Конкретными Фабриками.
"""


class CotoFeyMaleComplect(MaleComplect):
    def useful_function_a(self) -> str:
        return "мужской комплект линейки \"Котофей\""

    def another_useful_function_a(self, collaborator: MaleComplect) -> str:
        result = "линейка \'Котофей\n'"
        return f"{result}"


class ProfessorMaleComplect(MaleComplect):
    def useful_function_a(self) -> str:
        return "мужской комплект линейки \"Кембриджский профессор\""

    def another_useful_function_b(self, collaborator: MaleComplect) -> str:
        result = "линейка \'Кембриджский профессор\n'"
        return f"{result}"


class FemaleComplect(ABC):
    """
    Базовый интерфейс другого продукта. Все продукты могут взаимодействовать
    друг с другом, но правильное взаимодействие возможно только между продуктами
    одной и той же конкретной вариации.
    """
    @abstractmethod
    def useful_function_b(self) -> None:
        """
        Продукт B способен работать самостоятельно...
        """
        pass

    @abstractmethod
    def another_useful_function_b(self, collaborator: MaleComplect) -> None:
        """
        ...а также взаимодействовать с Продуктами A той же вариации.

        Абстрактная Фабрика гарантирует, что все продукты, которые она создает,
        имеют одинаковую вариацию и, следовательно, совместимы.
        """
        pass


class CombineComplect(ABC):

    @abstractmethod
    def useful_function_c(self) -> None:
        """
        Продукт B способен работать самостоятельно...
        """
        pass


"""
Конкретные Продукты создаются соответствующими Конкретными Фабриками.
"""

class CotoFeyCombineComplect(CombineComplect):
    def useful_function_c(self) -> str:
        return "комбинированный комплект линейки \"Котофей\""

    """
    Продукт B1 может корректно работать только с Продуктом A1. Тем не менее, он
    принимает любой экземпляр Абстрактного Продукта А в качестве аргумента.
    """


class ProfessorCombineComplect(CombineComplect):
    def useful_function_c(self) -> str:
        return "комбинированный комплект линейки \"Кембриджский профессор\""



class CotoFeyFemaleComplect(FemaleComplect):
    def useful_function_b(self) -> str:
        return "женский комплект линейки \"Котофей\""

    """
    Продукт B1 может корректно работать только с Продуктом A1. Тем не менее, он
    принимает любой экземпляр Абстрактного Продукта А в качестве аргумента.
    """

    def another_useful_function_b(self, collaborator: MaleComplect) -> str:
        result = "линейка \'Котофей\n'"
        return f"{result}"


class ProfessorFemaleComplect(FemaleComplect):
    def useful_function_b(self) -> str:
        return "женский комплект линейки \"Кембриджский профессор\""

    def another_useful_function_b(self, collaborator: MaleComplect):
        """
        Продукт B2 может корректно работать только с Продуктом A2. Тем не менее,
        он принимает любой экземпляр Абстрактного Продукта А в качестве
        аргумента.
        """
        result = "линейка \'Кембриджский профессор\n'"
        return f"{result}"


def client_code(factory: ClothesFactory) -> None:
    """
    Клиентский код работает с фабриками и продуктами только через абстрактные
    типы: Абстрактная Фабрика и Абстрактный Продукт. Это позволяет передавать
    любой подкласс фабрики или продукта клиентскому коду, не нарушая его.
    """
    trigger = True
    while trigger:
        print("=========================================")
        print("Выберите один из доступных комплектов:")
        print("1. Мужской комплект: пиджак, рубашка, брюки")
        print("2. Женский комплект: пиджак, блузка, юбка")
        print("3. Комбинированный комплект: пиджак, брюки")
        print("4. Выход из программы")
        print("-----------------------------------------")
        number_2 = input("Введите число: ")

        if number_2.isdigit() == True:
            if int(number_2) == 1:
                tr = True
                product_a = factory.create_product_MC()
                print("Вы выбрали: " + f"{product_a.useful_function_a()}")
                while tr:
                    size = input("Введите размер партии: ")
                    if size.isdigit() == True:
                        print("\n")
                        print("=========================================")
                        print("----------БЫЛ ОСУЩЕСТВЛЁН ЗАКАЗ----------")
                        print("=========================================")
                        print("Вы выбрали: " + f"{product_a.useful_function_a()}")
                        print("Размер партии: " + size)
                        print("-----------------------------------------")
                        raise SystemExit(0)
                        #tr = False
                    elif size != int:
                        continue
                break


            if int(number_2) == 2:
                tr = True
                product_b = factory.create_product_FC()
                print("Вы выбрали: " + f"{product_b.useful_function_b()}")
                while tr:
                    size = input("Введите размер партии: ")
                    if size.isdigit() == True:
                        print("\n")
                        print("=========================================")
                        print("----------БЫЛ ОСУЩЕСТВЛЁН ЗАКАЗ----------")
                        print("=========================================")
                        print("Вы выбрали: " + f"{product_b.useful_function_b()}")
                        print("Размер партии: " + size)
                        print("-----------------------------------------")
                        raise SystemExit(0)
                        #tr = False
                    elif size != int:
                        continue
                break

            if int(number_2) == 3:
                tr = True
                product_c = factory.create_product_CC()
                print("Вы выбрали: " + f"{product_c.useful_function_c()}")
                while tr:
                    size = input("Введите размер партии: ")
                    if size.isdigit() == True:
                        print("\n")
                        print("=========================================")
                        print("----------БЫЛ ОСУЩЕСТВЛЁН ЗАКАЗ----------")
                        print("=========================================")
                        print("Вы выбрали: " + f"{product_c.useful_function_c()}")
                        print("Размер партии: " + size)
                        print("-----------------------------------------")
                        raise SystemExit(0)
                        #tr = False
                    elif size != int:
                        continue
                break


            # ВЫХОД
            if int(number_2) == 4:
                break

        elif number_2 != int:
            continue

    #product_a = factory.create_product_MC()
    #product_b = factory.create_product_FC()

    #print(f"{product_b.useful_function_b()}")
    #print(f"{product_b.another_useful_function_b(product_a)}", end="")


if __name__ == "__main__":
    """
    Клиентский код может работать с любым конкретным классом фабрики.
    """
    trigger = True
    while trigger:
        print("\n")
        print("=========================================")
        print("Реализация паттерна \'Абстрактная фабрика\'")
        print("=========================================")
        print("Выберите одну из доступных линейку одежды:")
        print("1. Котофей")
        print("2. Кембриджский профессор")
        print("3. Выход из программы")
        print("-----------------------------------------")
        number_1 = input("Введите число:")

        if number_1.isdigit() == True:
            if int(number_1) == 1:
                print("=========================================")
                print("Линейка \'Котофей\'")
                client_code(CotoFeyFactory())

            if int(number_1) == 2:
                print("=========================================")
                print("Линейка \'Кембриджский профессор\'")
                client_code(ProfessorFactory())

            # ВЫХОД
            if int(number_1) == 3:
                raise SystemExit(0)

        elif number_1 != int:
            continue