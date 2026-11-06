import shutil
import shutil
import os
from tkinter import filedialog, messagebox
from datetime import datetime

DB_PATH = "data/academy.db"
BACKUP_FOLDER = "backup"

def backup_database():
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_file = os.path.join(
        BACKUP_FOLDER,
        f"academy_backup_{timestamp}.db"
    )

    shutil.copy(DB_PATH, backup_file)

    return backup_file

def cleanup_old_backups():
    files= sorted(os.listdir(BACKUP_FOLDER))

    if len(files) > 10:
        for f in files[:-10]:
            os.remove(os.path.join(BACKUP_FOLDER, f))


def restore_database():
    file_path = filedialog.askopenfilename(
        title="Select Backup File",
        filetypes=[("Database Files", "*.db")]
    )

    if not file_path:
        return

    confirm = messagebox.askyesno(
        "Confirm Restore",
        "This will overwrite current data. Continue?"
    )

    if not confirm:
        return

    try:
        shutil.copy(file_path, DB_PATH)
        messagebox.showinfo("Success", "Database restored successfully!\nRestart app.")
    except Exception as e:
        messagebox.showerror("Error", str(e))