import os
import emailer
from RPA.Excel.Files import Files
from RPA.Tables import Tables

EMPLOYEES_EXCEL_PATH = os.environ["EMPLOYEES_EXCEL_PATH"]
TRAININGS_EXCEL_PATH = os.environ["TRAININGS_EXCEL_PATH"]
excel = Files()
tables = Tables()


def send_training_reminders():
    employees = get_active_employees(EMPLOYEES_EXCEL_PATH)
    trainings = read_excel_as_table(TRAININGS_EXCEL_PATH)
    send_reminders(employees, trainings)


def get_active_employees(excel_path):
    employees = read_excel_as_table(excel_path)
    tables.filter_table_by_column(employees, "Status", "==", "Active")
    tables.filter_table_by_column(employees, "Category", "==", "Employee")
    return employees


def read_excel_as_table(excel_path):
    try:
        excel.open_workbook(excel_path)
        return excel.read_worksheet_as_table(header=True)
    finally:
        excel.close_workbook()


def send_reminders(employees, trainings):
    for employee in employees:
        not_completed_trainings = get_not_completed_trainings(
            employee, trainings)
        if not_completed_trainings:
            send_reminder(employee, not_completed_trainings)


def get_not_completed_trainings(employee, trainings):
    trainings_copy = tables.copy_table(trainings)
    training_names = set(tables.get_table_column(
        trainings_copy, "Training name"))
    tables.filter_table_by_column(
        trainings_copy, "Person ID", "==", employee["Person ID"])
    completed_trainings = set(tables.get_table_column(
        trainings_copy, "Training name"))
    not_completed_trainings = training_names.difference(completed_trainings)
    return not_completed_trainings


def send_reminder(employee, not_completed_trainings):
    name = f"{employee['First name']} {employee['Last name']}"
    recipient = employee["Email"]
    subject = "Remember to complete your training!"
    body = (
        f"Hi, {name}! "
        f"Remember to complete these trainings: {not_completed_trainings}."
    )
    emailer.send_email(recipient, subject, body)


if __name__ == "__main__":
    send_training_reminders()
