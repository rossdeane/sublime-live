import sublime
import sublime_plugin
import subprocess
import os
import stat

on = False


class ToggleLiveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global on
        if on:
            on = False
            sublime.active_window().run_command("hide_panel",
                                                {"panel": "output.textarea"})
        else:
            on = True


class ListenForModifyCommand(sublime_plugin.EventListener):
    def on_modified(self, view):
        if on:
            view.run_command("run_file")
        else:
            pass
        pass


class RunFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        window = self.view.window()
        contents = view.substr(sublime.Region(0, view.size()))

        f = open('tempfile', 'w')
        f.write(contents)
        f.close()
        st = os.stat('tempfile')
        os.chmod('tempfile', st.st_mode | stat.S_IEXEC)

        try:
            output = subprocess.check_output(["./tempfile"],
                                             stderr=subprocess.STDOUT)

            output_view = window.create_output_panel("textarea")
            window.run_command("show_panel", {"panel": "output.textarea"})

            region_all = sublime.Region(0, output_view.size())

            output_view.set_read_only(False)
            output_view.replace(edit, region_all, output.decode('utf-8'))
            output_view.set_read_only(True)
            sublime.Selection.clear(output_view)
            pass
        except subprocess.CalledProcessError as e:
            # print (e.output)
            pass
