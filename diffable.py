import sublime, sublime_plugin
import os
import subprocess

class Diffable(sublime_plugin.TextCommand):
    def get_entire_content(self, view):
        selection = sublime.Region(0, view.size())
        content = view.substr(selection)
        return content

    def run(self, edit, **kwargs):
        window = self.view.window()

        action = kwargs.get('action', None)

        view_1 = window.selected_sheets()[0].view() if len(window.selected_sheets()) >= 2 else window.active_view_in_group(0)
        view_2 = window.selected_sheets()[1].view() if len(window.selected_sheets()) >= 2 else window.active_view_in_group(1)

        if action == 'clear':
            if view_1: view_1.reset_reference_document()
            if view_2: view_2.reset_reference_document()

        if view_1 and view_2:
            text_left = self.get_entire_content(view_1)
            text_right = self.get_entire_content(view_2)

            if action == 'inline':
                    # view_1.set_reference_document(text_right)
                    view_2.set_reference_document(text_left)

            elif action == 'kaleidoscope':
                self.write_in_pipe(text_left, text_right)

    def write_in_pipe(self, left_text, right_test):
        lhs_read_fd, lhs_write_fd = os.pipe()
        rhs_read_fd, rhs_write_fd = os.pipe()

        lhs_bytes = bytes(left_text, encoding='utf-8')
        rhs_bytes = bytes(right_test, encoding='utf-8')

        lhs_path = "/dev/fd/" + str(lhs_read_fd)
        rhs_path = "/dev/fd/" + str(rhs_read_fd)

        ksdiff = subprocess.Popen(["/usr/local/bin/ksdiff", "-l", "Sublime", lhs_path, rhs_path], pass_fds=[lhs_read_fd, rhs_read_fd], close_fds=True)

        os.write(lhs_write_fd, lhs_bytes)
        os.close(lhs_write_fd)

        os.write(rhs_write_fd, rhs_bytes)
        os.close(rhs_write_fd)

        _, _ = ksdiff.communicate()
