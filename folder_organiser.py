#! /usr/bin/env python
# @author github.com/j-000
import os
import datetime
import shutil
import sys

from prettytable import PrettyTable


today = datetime.datetime.now()


class FolderOrganiser:

    new_folders = dict()
    deleted_folders = dict()

    def __init__(self, main_folder):
        self.main_folder = main_folder
        self.log_filename = os.path.join(self.main_folder,
                                         f'organiser_log_{today.date()}.txt')
        self.organise_folder()
        self.create_new_folders_and_move_files()
        self.delete_empty_folders()
        self.create_tables_and_log_file()
        _total_files = sum([len(i) for i in self.new_folders.values()])

        print(f'Folder organised! {len(self.new_folders)} new folders '
              f'created, {len(self.deleted_folders)} folders deleted and '
              f'{_total_files} moved.\n'
              f'Log is at >> {self.log_filename}')

    def path_is_safe(self, path):
        """
        A path is deemed safe if main_folder is
        a substring within path and not itself. Otherwise it is not safe.
        """
        return self.main_folder in path and path != self.main_folder

    def create_new_folders_and_move_files(self):
        """
        Create new folders based on the new_folders object and
        move files accordingly
        """
        for new_folder, file_objects in self.new_folders.items():
            try:
                os.mkdir(os.path.join(self.main_folder, new_folder))
            except FileExistsError:
                pass
            for file in file_objects:
                shutil.move(file.get('old_path'), file.get('new_path'))

    def delete_empty_folders(self):
        """
        Delete empty folders if there are no files and if it is safe to do so.
        """
        for root, _, files in os.walk(self.main_folder, topdown=False):
            if len(files) == 0 and self.path_is_safe(root):
                # Update dict of deleted folders to write log later
                self.deleted_folders.update({root: 'DELETED'})
                os.rmdir(root)

    def create_tables_and_log_file(self):
        """
        Create all data tables to write in the log file.
        """
        # Create first table (Files table)
        files_table = PrettyTable(field_names=['File', 'Old path', 'New path'])
        # Align each column to the left
        for field in files_table.field_names:
            files_table.align[field] = 'l'
        # Append each row of data to the table
        # main_folder string is removed from the file paths
        # to shorten the text and remove duplicate text.
        for files in self.new_folders.values():
            for file in files:
                files_table.add_row(
                  [i.replace(self.main_folder, '') for i in file.values()]
                )
        # Create second table - (Folders table)
        folders_table = PrettyTable(field_names=['Folder', 'Action'])
        # Align headers to the left
        for field in folders_table.field_names:
            folders_table.align[field] = 'l'
        # Append each row of data to the table
        # main_folder string is removed from the file paths
        # to shorten the text and remove duplicate text.
        for (folder, action) in self.deleted_folders.items():
            folders_table.add_row(
                [folder.replace(self.main_folder, ''), action])
        self.write_log(files_table=files_table, folders_table=folders_table)

    def write_log(self, **table_objects):
        """
        Write log. A table with the filename, old file path and new file path
        of all files moved. Also includes a table of all directories deleted.
        """
        files_table = table_objects.get('files_table')
        folders_table = table_objects.get('folders_table')
        with open(self.log_filename, 'w', encoding='utf-8') as log:
            info = f'Folder organiser by github.com/j-000\n'
            info += f'Generated: {today}\n\n'
            info += f'MAIN_FOLDER = {self.main_folder}\n'
            info += f'All paths in the tables are relative to the main folder.'
            info += '\n\n'
            log.write(info)
            log.write(str(files_table))
            log.write('\n\n')
            log.write(str(folders_table))

    def organise_folder(self):
        """
        Walk directory, get file names and construct new_folders object
        """
        for root, _, files in os.walk(self.main_folder):
            for file in files:
                old_path = os.path.join(root, file)
                file_created_date = str(datetime.datetime.fromtimestamp(
                  os.path.getmtime(old_path)).date())
                new_path = os.path.join(self.main_folder,
                                        file_created_date, file)
                if file_created_date in self.new_folders:
                    self.new_folders.get(file_created_date).append(
                      {'filename': file, 'old_path': old_path,
                       'new_path': new_path})
                else:
                    self.new_folders.update(
                      {file_created_date: [{'filename': file,
                                            'old_path': old_path,
                                            'new_path': new_path}]})


if __name__ == '__main__':
    try:
        FolderOrganiser(main_folder=sys.argv[1])
    except IndexError:
        print('You need provide a path as the first argument.\n'
              'Eg: python folder_organiser.py /home/user/Downloads/')
