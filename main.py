from database import create_students_table
from gui.dashboard import launch_dashboard

if __name__ == "__main__":

    print("1. Starting main.py")

    create_students_table()

    print("2. Database setup complete")

    launch_dashboard()

    print("3. Dashboard closed")