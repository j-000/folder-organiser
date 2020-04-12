# Folder Organiser

### About
This script allows you to organise a given folder based on the created date of all the files. 

### Dependencies
- [PrettyTable](https://pypi.org/project/PrettyTable/) 

### Installation
```python
git clone https://github.com/j-000/folder-organiser.git
cd folder-organiser
pip install 'prettytable>=0.7.2'
```

### Usage
```python
python folder-organiser.py /path/to/the/folder/to/organise
```
Concrete examples:
```python
python folder-organiser.py /home/user/Pictures
```

### Results
```text
            BEFORE                                   AFTER
/Pictures                        | /Pictures
    |__pic1.png                  |     /2020-04-07/
    |__pic2.png                  |         |__pic1.png
    |__pic3.png                  |         |__pic2.png
    /FolderA                     |         |__pic3.png
    /FolderB                     |     /2020-04-12/
    /FolderC                     |         |__test.txt
        |__test.txt              |     organiser_log_2020-04-12.txt
```
The log file text looks like:
```text

Folder organiser by github.com/j-000
Generated: 2020-04-12 15:09:28.787896

MAIN_FOLDER = /home/joao/Pictures
All paths in the tables are relative to the main folder.

+----------+----------------------------+----------------------+
| File     | Old path                   | New path             |
+----------+----------------------------+----------------------+
| pic3.png | /pic3.png                  | /2020-04-07/pic3.png |
| pic2.png | /pic2.png                  | /2020-04-07/pic2.png |
| pic1.png | /pic1.png                  | /2020-04-07/pic1.png |
| test.txt | /FolderB/FolderC/test.txt  | /2020-04-12/test.txt |
+----------+----------------------------+----------------------+

+-------------------+---------+
| Folder            | Action  |
+-------------------+---------+
| /FolderB/FolderC  | DELETED |
| /FolderB          | DELETED |
| /FolderA          | DELETED |
+-------------------+---------+
```
### New feature ideas
- [ ] Different date format for folder names
- [ ] Alternative method of organisation (modified date, last accessed, etc.)
 

### Contribute
Pull requests accepted
