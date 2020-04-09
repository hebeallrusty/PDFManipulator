#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.5 on Thu Apr  9 19:42:14 2020
#

import wx
from PDFManipulator import *
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


PROGRAM_VERSION = '20200403'
FILE_WILDCARD = "PDF Files (*.pdf)|*.pdf;*.PDF;*Pdf;*PDf;*pDf;*pdF"



class Frame_PDFManipulator(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Frame_PDFManipulator.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((640, 480))
        
        # Menu Bar
        self.Menu = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "&About", "")
        self.Bind(wx.EVT_MENU, self.Menu_About, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "&Quit", "")
        self.Bind(wx.EVT_MENU, self.Menu_Quit, id=item.GetId())
        self.Menu.Append(wxglade_tmp_menu, "&Menu")
        self.SetMenuBar(self.Menu)
        # Menu Bar end
        self.Panel_PDFManipulator = wx.Panel(self, wx.ID_ANY)
        self.Notebook_Panel = wx.Notebook(self.Panel_PDFManipulator, wx.ID_ANY)
        self.Notebook_Split = wx.Panel(self.Notebook_Panel, wx.ID_ANY)
        self.Text_Split_InputFile = wx.TextCtrl(self.Notebook_Split, wx.ID_ANY, "", style=wx.TE_AUTO_URL | wx.TE_READONLY)
        self.Button_Split_InputFile = wx.Button(self.Notebook_Split, wx.ID_ANY, "...")
        self.Text_Split_StartPage = wx.TextCtrl(self.Notebook_Split, wx.ID_ANY, "")
        self.Text_Split_EndPage = wx.TextCtrl(self.Notebook_Split, wx.ID_ANY, "")
        self.Radiobox_Split_OutputOptions = wx.RadioBox(self.Notebook_Split, wx.ID_ANY, "Output Option", choices=["Single file containing all pages", "Multiple files containing one page each"], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.Notebook_Join = wx.Panel(self.Notebook_Panel, wx.ID_ANY)
        self.Button_Join_SelectFile = wx.Button(self.Notebook_Join, wx.ID_ANY, "Select File(s)")
        self.Button_Join_SelectFolder = wx.Button(self.Notebook_Join, wx.ID_ANY, "Select Folder")
        self.Listbox_Join_Files = wx.ListBox(self.Notebook_Join, wx.ID_ANY, choices=[], style=wx.LB_EXTENDED | wx.LB_HSCROLL | wx.LB_NEEDED_SB)
        self.Button_Join_Up = wx.Button(self.Notebook_Join, wx.ID_ANY, u"↑")
        self.Button_Join_Down = wx.Button(self.Notebook_Join, wx.ID_ANY, u"↓")
        self.Button_Join_Remove = wx.Button(self.Notebook_Join, wx.ID_ANY, "Remove")
        self.Notebook_Encrypt = wx.Panel(self.Notebook_Panel, wx.ID_ANY)
        self.Text_Encrypt_InputFile = wx.TextCtrl(self.Notebook_Encrypt, wx.ID_ANY, "", style=wx.TE_AUTO_URL | wx.TE_READONLY)
        self.Button_Encrypt_InputFile = wx.Button(self.Notebook_Encrypt, wx.ID_ANY, "...")
        self.Text_Encrypt_Password1 = wx.TextCtrl(self.Notebook_Encrypt, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.Text_Encrypt_Password2 = wx.TextCtrl(self.Notebook_Encrypt, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.Radiobox_Encrypt_Options = wx.RadioBox(self.Notebook_Encrypt, wx.ID_ANY, "Encryption Options", choices=["Strength 1 (Recommended)", "Strength 2", "Strength 3", "Strength 4 (Weakest)"], majorDimension=4, style=wx.RA_SPECIFY_ROWS)
        self.Text_Panel_SelectOutputFile = wx.TextCtrl(self.Panel_PDFManipulator, wx.ID_ANY, "", style=wx.TE_AUTO_URL | wx.TE_READONLY)
        self.Button_Panel_OutputFile = wx.Button(self.Panel_PDFManipulator, wx.ID_ANY, "...")
        self.Button_Panel_Go = wx.Button(self.Panel_PDFManipulator, wx.ID_ANY, "Go")
        # Added as wxglade does not do it
        self.Label_Split_Info = wx.StaticText(self.Notebook_Split, wx.ID_ANY, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.Event_Button_Split_InputFile, self.Button_Split_InputFile)
        self.Bind(wx.EVT_BUTTON, self.Event_Button_Join_SelectFile, self.Button_Join_SelectFile)
        self.Bind(wx.EVT_BUTTON, self.Event_Button_Join_SelectFolder, self.Button_Join_SelectFolder)
        self.Bind(wx.EVT_LISTBOX, self.Event_Listbox_Join_Files, self.Listbox_Join_Files)
        self.Bind(wx.EVT_BUTTON, self.Event_Button_Join_Up, self.Button_Join_Up)
        self.Bind(wx.EVT_BUTTON, self.Event_Button_Join_Down, self.Button_Join_Down)
        self.Bind(wx.EVT_BUTTON, self.Event_Button_Join_Remove, self.Button_Join_Remove)
        self.Bind(wx.EVT_BUTTON, self.Event_Button_Encrypt_InputFile, self.Button_Encrypt_InputFile)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.Event_Notebook_Page_Changed, self.Notebook_Panel)
        self.Bind(wx.EVT_BUTTON, self.Event_Button_Panel_OutputFile, self.Button_Panel_OutputFile)
        self.Bind(wx.EVT_BUTTON, self.Event_Button_Panel_Go, self.Button_Panel_Go)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Frame_PDFManipulator.__set_properties
        self.SetTitle("PDFManipulator")
        self.Text_Split_StartPage.SetMinSize((50, -1))
        self.Text_Split_StartPage.SetToolTip("Leave this blank if you want the start page to be the first page in the PDF")
        self.Text_Split_EndPage.SetMinSize((50, -1))
        self.Text_Split_EndPage.SetToolTip("Leave this blank if you want the last page to be the last page in the PDF")
        self.Radiobox_Split_OutputOptions.SetSelection(0)
        self.Listbox_Join_Files.SetMinSize((-1, 150))
        self.Radiobox_Encrypt_Options.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Frame_PDFManipulator.__do_layout
        Sizer_Application = wx.BoxSizer(wx.VERTICAL)
        Sizer_Panel = wx.BoxSizer(wx.VERTICAL)
        Sizer_Panel_Go = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Panel_OutputFile = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Encrypt = wx.BoxSizer(wx.VERTICAL)
        Sizer_Encrypt_Password = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Encrypt_InputFile = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Join = wx.BoxSizer(wx.VERTICAL)
        Sizer_Join_ArrangeFiles = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Join_Listbox_Controls = wx.BoxSizer(wx.VERTICAL)
        Sizer_Join_SelectFiles = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Split = wx.BoxSizer(wx.VERTICAL)
        Sizer_Split_OutputOptions = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Split_Pages = wx.BoxSizer(wx.VERTICAL)
        Sizer_Split_Pages_OutputOptions = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Split_Pages_Selection = wx.BoxSizer(wx.HORIZONTAL)
        Sizer_Split_InputFile = wx.BoxSizer(wx.HORIZONTAL)
        Label_Split_InputFile = wx.StaticText(self.Notebook_Split, wx.ID_ANY, "Select File:")
        Sizer_Split_InputFile.Add(Label_Split_InputFile, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        Sizer_Split_InputFile.Add(self.Text_Split_InputFile, 10, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 0)
        Sizer_Split_InputFile.Add(self.Button_Split_InputFile, 0, wx.ALIGN_CENTER, 0)
        Sizer_Split.Add(Sizer_Split_InputFile, 1, wx.EXPAND, 0)
        Label_Split_StartPage = wx.StaticText(self.Notebook_Split, wx.ID_ANY, "First Page:")
        Label_Split_StartPage.SetMinSize((73, -1))
        Sizer_Split_Pages_Selection.Add(Label_Split_StartPage, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        Sizer_Split_Pages_Selection.Add(self.Text_Split_StartPage, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        Label_Split_EndPage = wx.StaticText(self.Notebook_Split, wx.ID_ANY, "Last Page:")
        Label_Split_EndPage.SetMinSize((73, -1))
        Sizer_Split_Pages_Selection.Add(Label_Split_EndPage, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        Sizer_Split_Pages_Selection.Add(self.Text_Split_EndPage, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        #Label_Split_Info = wx.StaticText(self.Notebook_Split, wx.ID_ANY, "There are x number of pages in this PDF")
        Sizer_Split_Pages_Selection.Add(self.Label_Split_Info, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        Sizer_Split_Pages.Add(Sizer_Split_Pages_Selection, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        Sizer_Split_Pages_OutputOptions.Add(self.Radiobox_Split_OutputOptions, 2, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, 5)
        Sizer_Split_Pages.Add(Sizer_Split_Pages_OutputOptions, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        Sizer_Split_OutputOptions.Add(Sizer_Split_Pages, 1, wx.EXPAND, 0)
        Sizer_Split.Add(Sizer_Split_OutputOptions, 3, wx.EXPAND, 0)
        self.Notebook_Split.SetSizer(Sizer_Split)
        Label_Join_Add = wx.StaticText(self.Notebook_Join, wx.ID_ANY, "Add:")
        Sizer_Join_SelectFiles.Add(Label_Join_Add, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        Sizer_Join_SelectFiles.Add(self.Button_Join_SelectFile, 2, wx.ALIGN_CENTER, 0)
        Sizer_Join_SelectFiles.Add(self.Button_Join_SelectFolder, 2, wx.ALIGN_CENTER, 0)
        Sizer_Join.Add(Sizer_Join_SelectFiles, 1, wx.EXPAND, 0)
        Sizer_Join_ArrangeFiles.Add(self.Listbox_Join_Files, 10, wx.EXPAND, 5)
        Sizer_Join_Listbox_Controls.Add(self.Button_Join_Up, 1, 0, 0)
        Sizer_Join_Listbox_Controls.Add(self.Button_Join_Down, 1, 0, 0)
        Sizer_Join_Listbox_Controls.Add(self.Button_Join_Remove, 1, 0, 0)
        Sizer_Join_ArrangeFiles.Add(Sizer_Join_Listbox_Controls, 1, wx.EXPAND, 0)
        Sizer_Join.Add(Sizer_Join_ArrangeFiles, 3, wx.EXPAND, 0)
        self.Notebook_Join.SetSizer(Sizer_Join)
        Label_Encrypt_InputFile = wx.StaticText(self.Notebook_Encrypt, wx.ID_ANY, "Select File:")
        Sizer_Encrypt_InputFile.Add(Label_Encrypt_InputFile, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        Sizer_Encrypt_InputFile.Add(self.Text_Encrypt_InputFile, 10, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 0)
        Sizer_Encrypt_InputFile.Add(self.Button_Encrypt_InputFile, 0, wx.ALIGN_CENTER, 0)
        Sizer_Encrypt.Add(Sizer_Encrypt_InputFile, 1, wx.EXPAND, 0)
        Label_Encrypt_Password1 = wx.StaticText(self.Notebook_Encrypt, wx.ID_ANY, "Password:")
        Sizer_Encrypt_Password.Add(Label_Encrypt_Password1, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP, 5)
        Sizer_Encrypt_Password.Add(self.Text_Encrypt_Password1, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        Label_Encrypt_Password2 = wx.StaticText(self.Notebook_Encrypt, wx.ID_ANY, "Re-enter Password:")
        Sizer_Encrypt_Password.Add(Label_Encrypt_Password2, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP, 5)
        Sizer_Encrypt_Password.Add(self.Text_Encrypt_Password2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        Sizer_Encrypt.Add(Sizer_Encrypt_Password, 1, wx.EXPAND, 0)
        Sizer_Encrypt.Add(self.Radiobox_Encrypt_Options, 0, wx.LEFT, 5)
        self.Notebook_Encrypt.SetSizer(Sizer_Encrypt)
        self.Notebook_Panel.AddPage(self.Notebook_Split, "Split")
        self.Notebook_Panel.AddPage(self.Notebook_Join, "Join")
        self.Notebook_Panel.AddPage(self.Notebook_Encrypt, "Encrypt")
        Sizer_Panel.Add(self.Notebook_Panel, 2, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
        Label_Panel_SelectOutputFile = wx.StaticText(self.Panel_PDFManipulator, wx.ID_ANY, "Save File:")
        Sizer_Panel_OutputFile.Add(Label_Panel_SelectOutputFile, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        Sizer_Panel_OutputFile.Add(self.Text_Panel_SelectOutputFile, 10, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 0)
        Sizer_Panel_OutputFile.Add(self.Button_Panel_OutputFile, 0, wx.ALIGN_CENTER, 0)
        Sizer_Panel.Add(Sizer_Panel_OutputFile, 0, wx.BOTTOM | wx.EXPAND | wx.RIGHT | wx.TOP, 5)
        Sizer_Panel_Go.Add(self.Button_Panel_Go, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 0)
        Sizer_Panel.Add(Sizer_Panel_Go, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT | wx.TOP, 5)
        self.Panel_PDFManipulator.SetSizer(Sizer_Panel)
        Sizer_Application.Add(self.Panel_PDFManipulator, 1, wx.EXPAND, 0)
        self.SetSizer(Sizer_Application)
        self.Layout()
        # end wxGlade

    def Menu_About(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        dialog = wx.MessageDialog(self,f'PDFManipulator Version: {PROGRAM_VERSION} \n\nCreated By: Ashley Butler \nLicenced under GNU General Public License v3.0',caption = "About...",style = wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        event.Skip()

    def Menu_Quit(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        self.Destroy()
        event.Skip()

    def Event_Button_Split_InputFile(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        # show file selection, then put file path and name into Text_Split_InputFile
        with wx.FileDialog(self,"Open PDF File", wildcard = FILE_WILDCARD, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        	# if the cancel button was pressed - do nothing and return
        	if fileDialog.ShowModal() == wx.ID_CANCEL:
        		return
        	
        	# put the file path into the text control
        	pathname = fileDialog.GetPath()
        	self.Text_Split_InputFile.SetValue(pathname)
        	# get the number of pages an update the label
        	pages = get_pages(pathname)
        	self.Label_Split_Info.SetLabel(f'There are {pages} pages in this PDF')
        	#print(dir(self))
        	
        
        event.Skip()

    def Event_Button_Join_SelectFile(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        print("Event handler 'Event_Button_Join_SelectFile' not implemented!")
        event.Skip()

    def Event_Button_Join_SelectFolder(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        print("Event handler 'Event_Button_Join_SelectFolder' not implemented!")
        event.Skip()

    def Event_Listbox_Join_Files(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        print("Event handler 'Event_Listbox_Join_Files' not implemented!")
        event.Skip()

    def Event_Button_Join_Up(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        print("Event handler 'Event_Button_Join_Up' not implemented!")
        event.Skip()

    def Event_Button_Join_Down(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        print("Event handler 'Event_Button_Join_Down' not implemented!")
        event.Skip()

    def Event_Button_Join_Remove(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        print("Event handler 'Event_Button_Join_Remove' not implemented!")
        event.Skip()

    def Event_Button_Encrypt_InputFile(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        print("Event handler 'Event_Button_Encrypt_InputFile' not implemented!")
        event.Skip()

    def Event_Notebook_Page_Changed(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        #NOTEBOOK_FOCUS = self.Notebook_Panel.GetPageText(event.GetSelection())
        #print(NOTEBOOK_FOCUS)
        event.Skip()

    def Event_Button_Panel_OutputFile(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
        with wx.FileDialog(self, "Save PDF File", wildcard = FILE_WILDCARD, style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
        	if fileDialog.ShowModal() == wx.ID_CANCEL:
        		return
        	# enter file name into output text box
        	pathname = fileDialog.GetPath()
        	
        	#print(pathname.lower())
        	# filename might not have .pdf in filename, so add it in if it's missing - PDF function adds ",pdf" automatically
        	#if pathname.lower()[-4:] != ".pdf":
        	#	pathname = ''.join([pathname,".pdf"])
        	self.Text_Panel_SelectOutputFile.SetValue(pathname)
        	
        event.Skip()
        
    def Event_Button_Panel_Go(self, event):  # wxGlade: Frame_PDFManipulator.<event_handler>
    	# get which page currently has focus so that we can split execution into the relevant sections
        NotebookPage = self.Notebook_Panel.GetPageText(self.Notebook_Panel.GetSelection())
        print(self.Text_Split_InputFile.GetValue())
        if NotebookPage == "Split":
        	# pick up the values of each relevant section
        	InputFile = self.Text_Split_InputFile.GetValue()
        	OutputFile = self.Text_Panel_SelectOutputFile.GetValue()
        	Pages = [self.Text_Split_StartPage.GetValue(),self.Text_Split_EndPage.GetValue()]
        	OutputFileChoice = self.Radiobox_Split_OutputOptions.GetSelection()
        	
        	# need to do some validation and processing
        	# a file is missing so halt
        	if InputFile == "" or OutputFile == "":
        		dialog = wx.MessageDialog(self,f'Plese select a file to split, or a file to save the split file to',caption = "File Error",style = wx.OK | wx.ICON_ERROR)
        		dialog.ShowModal()
        		return
        		
        	maxpages = get_pages(InputFile)	
        	# adjust Pages as can allow blank selections
        	if Pages[0] == "":
        		Pages[0] = 1
        		
        	if Pages[1] == "":
        		Pages[1] = maxpages
        		
        	# check pages to ensure they are sane
        	try:
        		Pages = [int(Pages[0]),int(Pages[1])]
        	except:
        		dialog = wx.MessageDialog(self,f'Page Numbers are not numeric',caption = "Page Number Error",style = wx.OK | wx.ICON_ERROR)
        		dialog.ShowModal()
        		return
        	# check page number boundaries don't exceed pdf boundaries
        	if (Pages[0] < 1) or (Pages[1] > maxpages) or (Pages[0] > maxpages) or (Pages[1] < 1):
        		dialog = wx.MessageDialog(self,f'Page number selection should be between 1 and {maxpages}',caption = "Page Selection Error",style = wx.OK | wx.ICON_ERROR)
        		dialog.ShowModal()
        		return
        	
        	# validation passed	
        	split(InputFile,OutputFile,Pages,dismantle = OutputFileChoice)
        	
        event.Skip()

# end of class Frame_PDFManipulator

class MyApp(wx.App):
    def OnInit(self):
        self.frame = Frame_PDFManipulator(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
