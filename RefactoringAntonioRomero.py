"""Payroll management CLI application.

This module provides a small command-line payroll system that allows
adding employees by department, calculating net salary with department-
specific tax rates and a fixed cafeteria discount, and printing a report.

Refactoring highlights:
- Introduces descriptive names and clear separation of concerns.
- Uses type hints and dataclasses for strong structure and readability.
- Adds input validation helpers and centralized business rules.
- Provides docstrings and constants for maintainability.

Behavior is preserved relative to the original script:
- Departments: Ventas (Sales), IT, RRHH (HR)
- Tax rates: 15% for Ventas and IT, 16% for RRHH
- Cafeteria discount: 50 (applied after tax); net salary cannot be negative
- Interactive menu with options to add employees and view a report
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Department(Enum):
    """Supported departments in the payroll system."""

    SALES = "Ventas"
    IT = "IT"
    HR = "RRHH"

    @staticmethod
    def from_menu_option(option: str) -> Optional["Department"]:
        """Map a numeric menu option to a Department.

        Args:
            option: String representing the user's menu choice.

        Returns:
            The corresponding Department, or None if the option is invalid.
        """
        mapping = {"1": Department.SALES, "2": Department.IT, "3": Department.HR}
        return mapping.get(option)


@dataclass(slots=True)
class Employee:
    """Employee record with basic payroll fields.

    Attributes:
        name: Employee full name.
        department: Department the employee belongs to.
        gross_salary: Gross salary value provided by the user.
        net_salary: Calculated net salary after taxes and discounts.
    """

    name: str
    department: Department
    gross_salary: float
    net_salary: float


class PayrollCalculator:
    """Encapsulates payroll business rules and calculations."""

    # Business rules
    TAX_RATES = {Department.SALES: 0.15, Department.IT: 0.15, Department.HR: 0.16}
    CAFETERIA_DISCOUNT = 50.0

    @classmethod
    def calculate_net_salary(cls, gross_salary: float, department: Department) -> float:
        """Calculate the net salary for the given gross salary and department.

        Net = gross_salary - (gross_salary * tax_rate) - CAFETERIA_DISCOUNT
        The result is floored to zero if negative.

        Args:
            gross_salary: Gross salary value.
            department: Employee department used to determine tax rate.

        Returns:
            Net salary as a non-negative float.
        """
        tax_rate = cls.TAX_RATES[department]
        tax_amount = gross_salary * tax_rate
        net = gross_salary - tax_amount - cls.CAFETERIA_DISCOUNT
        return max(net, 0.0)


class PayrollSystem:
    """High-level facade for managing employees and reporting."""

    def __init__(self) -> None:
        self._employees: List[Employee] = []

    def add_employee(self, name: str, department: Department, gross_salary: float) -> Employee:
        """Create and store a new employee with computed net salary.

        Args:
            name: Employee full name.
            department: Department in which the employee works.
            gross_salary: Gross salary value.

        Returns:
            The created Employee instance.
        """
        net_salary = PayrollCalculator.calculate_net_salary(gross_salary, department)
        employee = Employee(name=name, department=department, gross_salary=gross_salary, net_salary=net_salary)
        self._employees.append(employee)
        return employee

    def has_employees(self) -> bool:
        """Check whether any employees have been registered."""
        return len(self._employees) > 0

    def iter_employees(self):
        """Iterate over registered employees in insertion order."""
        return iter(self._employees)


# ==========================
# I/O helper functions
# ==========================

def prompt_non_empty_string(prompt_text: str) -> str:
    """Prompt until a non-empty string is entered.

    Args:
        prompt_text: The input prompt message.

    Returns:
        A non-empty string provided by the user.
    """
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Entrada vacía. Intente nuevamente.")


def prompt_float(prompt_text: str) -> float:
    """Prompt until a valid float is entered.

    Args:
        prompt_text: The input prompt message.

    Returns:
        A float parsed from user input.
    """
    while True:
        raw = input(prompt_text).strip()
        try:
            return float(raw)
        except ValueError:
            print("Entrada inválida. Ingrese un número válido.")


def print_header() -> None:
    """Print the application header/banner."""
    print("********************************")
    print("SISTEMA DE NOMINAS V2.3 FINAL_REAL_AHORA_SI")
    print("********************************")


def print_menu() -> None:
    """Display the main menu options."""
    print("")
    print("1. Agregar empleado Ventas")
    print("2. Agregar empleado IT")
    print("3. Agregar empleado RRHH")
    print("4. Ver reporte")
    print("5. Salir")
    print("")


def handle_add_employee(system: PayrollSystem, department: Department) -> None:
    """Handle the flow to add a new employee for the selected department.

    Args:
        system: The payroll system to add the employee to.
        department: Department chosen by the user.
    """
    name = prompt_non_empty_string("Nombre: ")
    gross_salary = prompt_float("Sueldo Bruto: ")
    employee = system.add_employee(name=name, department=department, gross_salary=gross_salary)
    print(f"Guardado {employee.department.value}.")


def print_report(system: PayrollSystem) -> None:
    """Print a simple report of all registered employees."""
    if not system.has_employees():
        print("No hay nadie")
        return

    for employee in system.iter_employees():
        print(f"Emp: {employee.name}")
        print(f"Depto: {employee.department.value}")
        print(f"Pago Final: {employee.net_salary}")
        print("----------------")


def main() -> None:
    """Run the interactive payroll CLI loop."""
    system = PayrollSystem()

    print_header()

    while True:
        print_menu()
        option = input("Seleccione opcion: ").strip()

        if option in {"1", "2", "3"}:
            department = Department.from_menu_option(option)
            assert department is not None  # for type checkers; guarded by option set above
            handle_add_employee(system, department)
        elif option == "4":
            print_report(system)
        elif option == "5":
            break
        else:
            print("Error")


if __name__ == "__main__":
    main()
