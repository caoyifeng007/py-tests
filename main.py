import os
import cmd


class SplitShell(cmd.Cmd):
    intro = 'Welcome to the split shell.   Type help or ? to list commands.\n'
    prompt = '>>>'

    def do_snap(self, arg):
        """    specify single file: snap path/to/file.csv
    specify a folder   : snap -d path/to/folder"""
        os.system(f'python splitToDetail_snap.py {arg}')
        print("script executed.")

    def do_day(self, arg):
        """    specify single file: day path/to/file.csv
    specify a folder   : day -d path/to/folder"""
        os.system(f'python splitToDetail_day.py {arg}')
        print("script executed.")

    def do_exit(self, _):
        """exit"""
        exit(0)


if __name__ == '__main__':
    SplitShell().cmdloop()
