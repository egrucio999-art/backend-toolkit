"""Zip-based backup, restore and rotation manager."""
import os
import time
import zipfile


class BackupManager:
    def __init__(self, source_dir, backup_dir=None):
        self.source_dir = source_dir
        self.backup_dir = backup_dir or os.path.join(source_dir, 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self):
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}.zip'
        backup_path = os.path.join(self.backup_dir, backup_name)
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.source_dir):
                if 'backups' in dirs:
                    dirs.remove('backups')
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.source_dir)
                    zipf.write(file_path, arcname)
        return backup_path

    def restore_backup(self, backup_path):
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall(self.source_dir)
        return True

    def list_backups(self):
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.zip'):
                path = os.path.join(self.backup_dir, file)
                backups.append({
                    'name': file,
                    'path': path,
                    'size': os.path.getsize(path),
                    'created': os.path.getmtime(path),
                })
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups

    def delete_backup(self, backup_path):
        try:
            os.remove(backup_path)
            return True
        except OSError:
            return False
