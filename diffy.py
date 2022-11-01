import sublime, sublime_plugin
import sys
import os
import subprocess


if sys.version_info >= (3, 0):
    from .diffy_lib import diffier
else:
    from diffy_lib import diffier

class DiffyCommand(sublime_plugin.TextCommand):
    def get_entire_content(self, view):
        selection = sublime.Region(0, view.size())
        content = view.substr(selection)
        return content

    """
    return the marked lines
    """
    def draw_difference(self, view, diffs):
        self.clear(view)

        lines = [d.get_region(view) for d in diffs]

        view.add_regions(
            'highlighted_lines',
            lines,
            'keyword',
            'dot',
            sublime.DRAW_OUTLINED
        )

        return lines


    def set_view_point(self, view, lines):
        if len(lines) > 0:
            view.show(lines[0])

    def run(self, edit, **kwargs):
        diffy = diffier.Diffy()
        window = self.view.window()

        action = kwargs.get('action', None)

        view_1 = window.selected_sheets()[0].view() if len(window.selected_sheets()) >= 2 else window.active_view_in_group(0)
        view_2 = window.selected_sheets()[1].view() if len(window.selected_sheets()) >= 2 else window.active_view_in_group(1)

        if action == 'clear':
            if view_1: self.clear(view_1)
            if view_2: self.clear(view_2)
        else:
            #make sure there are 2 columns side by side
            if view_1 and view_2:
                text_left = self.get_entire_content(view_1)
                text_right = self.get_entire_content(view_2)

                lhs_text = bytes(text_left, encoding='utf-8')
                rhs_Text = bytes(text_right, encoding='utf-8')

                if len(text_left) > 0 and len(text_right) > 0:
                    lhs_read_fd, lhs_write_fd = os.pipe()
                    rhs_read_fd, rhs_write_fd = os.pipe()
                    print("this")

                    lhs_bytes = bytes(text_left,'utf-8')
                    rhs_bytes = bytes(text_right,'utf-8')

                    lhs_path = "/dev/fd/" + str(lhs_bytes)
                    rhs_path = "/dev/fd/" + str(rhs_bytes)

                    self.write_in_pipe(text_left, text_right)

    def write_in_pipe(self, left_text, right_test):
        lhs_read_fd, lhs_write_fd = os.pipe()
        rhs_read_fd, rhs_write_fd = os.pipe()

        lhs_text = bytes(left_text, encoding='utf-8')
        rhs_Text = bytes(right_test, encoding='utf-8')

        lhs_path = "/dev/fd/" + str(lhs_read_fd)
        rhs_path = "/dev/fd/" + str(rhs_read_fd)

        ksdiff = subprocess.Popen(["/usr/local/bin/ksdiff", lhs_path, rhs_path], pass_fds=[lhs_read_fd, rhs_read_fd], close_fds=True)

        os.write(lhs_write_fd, lhs_text)
        os.close(lhs_write_fd)

        os.write(rhs_write_fd, rhs_Text)
        os.close(rhs_write_fd)

        stdout, stderr = ksdiff.communicate()
