import sublime
import sublime_plugin
import os
from datetime import datetime

class AutoSaveOnFocusLostListener(sublime_plugin.EventListener):
    def get_save_path(self):
        try:
            # Read the save path from the configuration file
            config_path = os.path.expanduser("~/darth_sublime_insync")
            with open(config_path, "r") as file:
                save_path = file.read().strip()
            return save_path
        except Exception as e:
            print(f"darth_auto_save: Error reading ~/darth_sublime_insync: {e}")
            return None

    def on_deactivated(self, view):
        auto_save_status = False
        project = 'longpaths'
        default_file_root = 'subl'

        # Check if auto save is going to be enabled or disabled
        try:
            save_path = self.get_save_path()
            if save_path != '':
                if os.path.expanduser(save_path):
                    project_path = os.path.expanduser(save_path + "/" + project)
                    os.makedirs(project_path, exist_ok=True)
                    auto_save_status = True
                else:
                    print('darth_auto_save:',project_path,': Invalid path')
            else:
                print('darth_auto_save: ~/darth_sublime_insync does not exist or does not contain a valid path. Auto-save not enabled.')
        except Exception as error:
            print("Error:", type(error).__name__, "–", error)

        if auto_save_status:
            # Check if the file has a path (i.e., it's saved)
            if not view.file_name():
                if view.is_dirty() and view.size() > 0:  # If the file has unsaved changes and it is not empty
                    now = datetime.now().strftime("%Y%m%d_%H%M%S")

                    file_name = default_file_root + '_' + now + '.txt'
                    full_path = os.path.join(project_path, file_name)
                    
                    # Retarget and save the file
                    view.retarget(full_path)
                    view.run_command("save")
                    print(f"darth_auto_save: Project {project}")
                    print(f"darth_auto_save: New file created: ./{file_name.replace(os.path.expanduser(project_path),'')}")
            else:
                if view.is_dirty():  # Save if changes are present
                    view.run_command("save")
                    print(f"darth_auto_save: Current project {project}")
                    if project_path in view.file_name():
                        print(f"darth_auto_save: Existing file saved: .{view.file_name().replace(os.path.expanduser(project_path),'')}")
                    else:
                        print(f"darth_auto_save: Existing file saved: ..{view.file_name().replace(os.path.expanduser(save_path),'')}")
