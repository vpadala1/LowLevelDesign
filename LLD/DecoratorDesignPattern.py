from abc import ABC, abstractmethod

# Component Interface
class Pizza(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def cost(self):
        pass

# Concrete Component
class MargheritaPizza(Pizza):
    def get_description(self):
        return "Margherita Pizza"

    def cost(self):
        return 5.0  # base price of Margherita Pizza

# Decorator Base Class
class PizzaDecorator(Pizza):
    def __init__(self, pizza):
        self._pizza = pizza

    def get_description(self):
        return self._pizza.get_description()

    def cost(self):
        return self._pizza.cost()

# Concrete Decorators
class Cheese(PizzaDecorator):
    def get_description(self):
        return self._pizza.get_description() + ", Cheese"

    def cost(self):
        return self._pizza.cost() + 1.5  # cost of cheese

class Pepperoni(PizzaDecorator):
    def get_description(self):
        return self._pizza.get_description() + ", Pepperoni"

    def cost(self):
        return self._pizza.cost() + 2.0  # cost of pepperoni

class Olives(PizzaDecorator):
    def get_description(self):
        return self._pizza.get_description() + ", Olives"

    def cost(self):
        return self._pizza.cost() + 1.0  # cost of olives

# Usage
basic_pizza = MargheritaPizza()
print(basic_pizza.get_description())  # Output: Margherita Pizza
print(basic_pizza.cost())             # Output: 5.0

# Adding Cheese
pizza_with_cheese = Cheese(basic_pizza)
print(pizza_with_cheese.get_description())  # Output: Margherita Pizza, Cheese
print(pizza_with_cheese.cost())             # Output: 6.5

# Adding Cheese and Pepperoni
pizza_with_cheese_pepperoni = Pepperoni(pizza_with_cheese)
print(pizza_with_cheese_pepperoni.get_description())  # Output: Margherita Pizza, Cheese, Pepperoni
print(pizza_with_cheese_pepperoni.cost())             # Output: 8.5

# Adding Cheese, Pepperoni, and Olives
pizza_with_all_toppings = Olives(pizza_with_cheese_pepperoni)
print(pizza_with_all_toppings.get_description())  # Output: Margherita Pizza, Cheese, Pepperoni, Olives
print(pizza_with_all_toppings.cost())             # Output: 9.5
