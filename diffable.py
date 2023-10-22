from sublime import View, Region, load_settings, version
from sublime_plugin import WindowCommand
import os
import subprocess

class Diffable(WindowCommand):

    def __get_view__(self, number: int) -> View:
        if int(version()) >= 4000:  # ST4
            ## TODO: Validate that there's just 2 groups or tabs somehow.
            return self.window.selected_sheets()[number].view() if len(self.window.selected_sheets()) == 2 else self.window.active_view_in_group(number)
        else:  # ST3
            return self.window.active_view_in_group(number)

    def is_enabled(self):
        return True if self.__get_view__(0) and self.__get_view__(1) else False

    def get_entire_content(self, view):
        selection = Region(0, view.size())
        content = view.substr(selection)
        return content

    def run(self, **kwargs):
        self.settings = load_settings("Diffable.sublime-settings")

        action = kwargs.get('action', None)

        view_1 = self.__get_view__(0)
        view_2 = self.__get_view__(1)

        if action == 'clear':
            if view_1: view_1.reset_reference_document()
            if view_2: view_2.reset_reference_document()

        if view_1 and view_2:
            text_left = self.get_entire_content(view_1)
            text_right = self.get_entire_content(view_2)

            if action == 'inline':
                if self.settings.get("two_panes_mode"):
                    view_2.set_reference_document(text_left)
                    view_1.set_reference_document(text_right)
                else:
                    view_2.set_reference_document(text_left) if self.settings.get("left_to_right") else view_1.set_reference_document(text_right)
                ## this approach requires to select each diff hunk and toggle it manualy
                # if self.settings.get("expand_all_diffs"):
                #     view_1.run_command('select_all')
                #     view_1.run_command('toggle_inline_diff')
                #     view_2.run_command('select_all')
                #     view_2.run_command('toggle_inline_diff')

            elif action == 'kaleidoscope':
                self.write_in_pipe(text_left, text_right)

    def write_in_pipe(self, left_text, right_test):
        lhs_read_fd, lhs_write_fd = os.pipe()
        rhs_read_fd, rhs_write_fd = os.pipe()

        lhs_bytes = bytes(left_text, encoding='utf-8')
        rhs_bytes = bytes(right_test, encoding='utf-8')

        lhs_path = "/dev/fd/" + str(lhs_read_fd)
        rhs_path = "/dev/fd/" + str(rhs_read_fd)

        ksdiff_path = self.settings.get("kaleidoscope_path")

        ksdiff = subprocess.Popen([ksdiff_path, "-l", "Sublime Text", lhs_path, rhs_path], pass_fds=[lhs_read_fd, rhs_read_fd], close_fds=True)

        os.write(lhs_write_fd, lhs_bytes)
        os.close(lhs_write_fd)

        os.write(rhs_write_fd, rhs_bytes)
        os.close(rhs_write_fd)

        _, _ = ksdiff.communicate()
