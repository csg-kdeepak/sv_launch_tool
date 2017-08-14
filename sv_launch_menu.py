"""
Sample application for creating a GUI window
"""
import wx
from read_ini import get_login_data
from pywinauto import Application, application

APP_ICON = "launch.png"

class WindowClass(wx.Frame):
    """
    This is the class which will be used for creating the frames
    """
    menu_names = {}  # Member variable
    sv_app = ''

    def __init__(self, menu_name, sv, *args, **kwargs):
        super(WindowClass, self).__init__(*args, **kwargs)
        self.menu_names = menu_name
        self.sv_app = sv
        self.basic_gui()

    def basic_gui(self):
        menu_bar = wx.MenuBar()  # init MenuBar item
        file_menu = wx.Menu()    # init file Button to be added to menu bar

        """
        Loop through the menu_names and add each button
        """
        x = 1
        for names in self.menu_names.keys():
            file_menu.Append(x, names, 'status entry')
            self.Bind(wx.EVT_MENU_RANGE, self.init_sv_login, id=1, id2=len(self.menu_names.keys()))
            x += 1

        menu_bar.Append(file_menu, '&Select Env')  # add the file_menu on the menu bar
        self.SetMenuBar(menu_bar)  # turn on the menu bar for WindowClass which is inherits Frame class
        self.SetTitle('SV Launch Tool')
        self.SetSize(200, 80)
        self.SetWindowStyle(style=wx.SYSTEM_MENU | wx.RESIZE_BORDER | wx.CAPTION | wx.CLOSE_BOX)
        app_icon = wx.EmptyIcon()
        app_icon.CopyFromBitmap(wx.Bitmap(APP_ICON, wx.BITMAP_TYPE_PNG))
        self.SetIcon(app_icon)
        self.Show()

    def quit(self, e):
        self.Close()

    def init_sv_login(self, event):
        """
        function to get the label that is clicked
        and launch the sv application
        """
        # Launch the application
        evt_id = event.GetId() - 1

        try:
            app = Application(backend='uia').start(self.sv_app)

        except application.AppStartError as err:
            show_msg_box("Singview Application Start Failure : {}".format(err))

        # get the Dialogue Handler
        dlg = app.window(title_re='Singleview Convergent Billing.*')

        db_pane = dlg.child_window(title="Database", control_type="Pane")

        # set variables from the clicked menu
        keys_list = list(self.menu_names.keys())
        db = self.menu_names[keys_list[evt_id]][0]
        uname = self.menu_names[keys_list[evt_id]][1]
        passwd = self.menu_names[keys_list[evt_id]][2]
        # set database name
        db_edit = db_pane.Edit0
        db_edit.set_text(db)

        # set user name
        uname_edit = db_pane.Edit3
        uname_edit.set_text(uname)

        # set password name
        pass_edit = db_pane.Edit2
        pass_edit.set_text(passwd)

        dlg.Ok.click()


def show_msg_box(msg):
    wx.MessageBox(msg, 'ERROR:', wx.OK | wx.ICON_ERROR)


def main():

    app = wx.App()
    try:
        (env_list, sv_app) = get_login_data()

        env_dict = {}
        # have environment list as dict.
        for entry in env_list:
            env_dict[entry[0]] = entry[1:]

    except IOError as err:
        print("OS error: {0}".format(err))
        show_msg_box("OS error: {0}".format(err))
    WindowClass(env_dict, sv_app, None)
    app.MainLoop()

"""
Main program starts here
"""

if __name__ == '__main__':
    main()
