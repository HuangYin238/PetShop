import sqlite3 # SQL trong python
from PIL import Image, ImageTk # In ra hình ảnh
import time # Hiệu ứng loading
from tkinter import * # Sử dụng toàn bộ thư viện làm đồ hoạ
from tkinter.ttk import Progressbar # Lấy ra thành progressbar
from PIL import Image 
from tkinter import font # Điều chỉnh font chữ
from tkinter import Tk, Canvas, NW
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import shutil # Di chuyển hình ảnh được chọn vào thư mục background
import os # Làm việc với hệ điều hành, di chuyển file
import datetime # Lấy ra ngày hôm nay
import hashlib # Mã hoá 1 chiều MK
###########################
# kích thước của ứng dụng #
###########################
width = 1450
height = 880
var = ""
########################################
# hàm hiển thị thông báo đăng nhập sai #
########################################
def show_popup():
    messagebox.showinfo("WARNING", "WRONG ID OR PASSWORD")
###############
# hàm loading #
###############
def show_loading(message_label):
    ####################################
    # Xoá toàn bộ nội dung trên cửa sổ #
    ####################################
    for widget in root.winfo_children():
        widget.destroy()
    ###########
    # Tiêu đề #
    ########### 
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    loading_label = Label(root, text="Loading...",font=title_font)
    loading_label.grid(column=4,row=1,columnspan=2)
    progress_bar = Progressbar(root, length=200, mode='indeterminate')
    progress_bar.grid(column=4,row=2,columnspan=2)
    loading_time = 1
    progress_bar.start()
    root.update()
    #################
    # Thời gian chờ #
    #################
    time.sleep(loading_time)
    progress_bar.stop()
    for widget in root.winfo_children():
        widget.destroy()
###################
# Mã hoá mật khẩu #
###################
def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password
##############################################
# hàm bắt sự kiện đăng nhập và cơ sở dữ liệu #
##############################################
def login(username_entry, password_entry, message_label):
    ##############################
    # Nhận dữ liệu từ người dùng #
    ##############################
    UserName = username_entry.get()
    PassWord = password_entry.get()
    #########################
    # Kết nối cơ sở dữ liệu #
    #########################
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT UserName, Password FROM LoginManage")
    rows = cursor.fetchall()
    for row in rows:
        #########################################################
        # Mã hoá tên người dùng và mật khẩu đã nhập để kiểm tra #
        #########################################################
        hashed_username = hashlib.sha256(UserName.encode()).hexdigest()
        hashed_password = hashlib.sha256(PassWord.encode()).hexdigest()
        if hashed_username == row[0] and hashed_password == row[1] :
            if UserName == 'quanly123':
                message_label.config(text="Đăng nhập thành công")
                conn.close()
                return 1
            if UserName == 'ketoan123':
                conn.close()
                return 2
    message_label.config(text="Đăng nhập thất bại")
    show_popup()
    conn.close()
    return 0
###########################
# hàm xoá cửa sở hiện tại #
###########################
def clear_and_return():
    for widget in root.winfo_children():
        widget.destroy()
    canvas = Canvas(root, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.place(x=0, y=0)
    show_login_interface()
#################################
############Đăng nhập############
#################################
#hiển thị cửa sổ đăng nhập
def show_login_interface():
    ###################
    # Khởi tạo cửa sổ #
    ##################
    root.geometry("1450x880")
    root.title("LOGIN")
    ####################
    # Chia hàng và cột #
    ####################
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    ########################
    # Trang trí cho cửa sổ #
    ########################
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="PET SHOP", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)
    username_label = Label(frame, text="Username:",font=normal_font)
    username_label.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    username_entry = Entry(frame)
    username_entry.grid(column=1, row=0, padx=20, pady=10)
    password_label = Label(frame, text="Password:",font=normal_font)
    password_label.grid(column=0, row=2, padx=20, pady=20,sticky=W)
    password_entry = Entry(frame, show="*")
    password_entry.grid(column=1, row=2, padx=20, pady=20)
    message_label = Label(root, text="")
    login_button = Button(frame, text="Login",font=('Arial',16,'bold'),command=lambda: check_login(username_entry, password_entry, message_label))
    login_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)   
###################
# hàm check login #
###################
def check_login(username_entry, password_entry, message_label):
    ###############################################
    # Nếu là 1 thì là quản lý là 2 thì là kế toán #
    ###############################################
    if login(username_entry, password_entry, message_label) == 1:
        show_loading( message_label)
        Manage_Display()
    elif login(username_entry, password_entry, message_label) == 2:
        show_loading(message_label)
        AccountingDisplay()
#################################
########quản lý nhân viên########
#################################
def Manage_Display():
    ##############################
    # Xoá và khởi tạo lại cửa sổ #
    ##############################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Manage Display")
    root.geometry(f"{width}x{height}")
    canvas_frame = Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/background_manage.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    #############
    # Trang trí #
    #############
    title_font = font.Font(family="Arial",size=35,weight="bold")
    title = Label(root, text="MANAGE DISPLAY", font=title_font,fg="red")
    title.grid(column=2,row=0,pady=10)
    title.config(relief=RAISED,bd=5)
    normal_font = font.Font(family='Arial',size=20)
    add_button = Button(root,text="ADD EMPLOYEE",font=normal_font,fg="green",command=AddEmployee)
    add_button.config(relief=RAISED,bd=1,bg="green")
    add_button.grid(column=1,row=4,padx=10)
    back_button = Button(root, text="Back",font=normal_font,fg='green',command=clear_and_return,width=10)
    back_button.config(relief=RAISED,bd=1,bg="green")
    back_button.grid(column=2,row=4,padx=10)
    list_button = Button(root,text="EMPLOYEE LIST",font=normal_font,fg="green",command=EmployeeList)
    list_button.config(relief=RAISED,bd=1,bg="green")
    list_button.grid(column=3,row=4,padx=10)
    search_entry = Entry(root,font=title_font,width=50)
    search_entry.grid(column=2,row=1)
    search_button = Button(root,text="Search",font=normal_font,command=lambda:search(search_entry))
    search_button.grid(column=3,row=1)
    root.mainloop()
###########################
# hàm tiềm kiếm nhân viên #
###########################
def search(search_entry):
    ######################################################
    # Lấy dữ liệu từ người dùng và kết nối cơ sở dữ liệu #
    ######################################################
    ma_nhan_vien = search_entry.get()  
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee WHERE MANV=?", (ma_nhan_vien,))
    result = cursor.fetchone()  
    conn.close()
    result_label = Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    ##############################################
    # Tạo bảng nhỏ in ra thông tin các nhân viên #
    ##############################################
    treeview = ttk.Treeview(result_label, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")
    treeview.heading("col1", text="EMPLOYEE ID")
    treeview.heading("col2", text="EMPLOYEE NAME")
    treeview.heading("col3", text="EMPLOYEE DUTY")
    treeview.heading("col4", text="PHONE NUMBER")
    treeview.heading("col5", text="ADDRESS")
    treeview.heading("col6", text="ACCESS")
    result_frame = Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    ##############
    # Thanh cuộn #
    ##############
    scrollbar = Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    ##############################
    # đưa thông tin vào treeview #
    ##############################
    if result is not None:
        ten_nhan_vien = result[1]
        chuc_vu = result[2]
        so_dien_thoai = result[3]
        dia_chi = result[4]
        quyen_truy_cap = result[5]
        data = [(ma_nhan_vien,ten_nhan_vien,chuc_vu,so_dien_thoai,dia_chi,quyen_truy_cap)]
        for item in data:
            treeview.insert("", "end", values=item)
    else:
        result_label = Label(result_frame, text="NOT FOUND",fg='red',font=('Arial',25,'bold'))
        result_label.grid(row=1, column=0, padx=5, pady=5,sticky="w")
################################
# hiển thị thông tin nhân viên #
################################
def EmployeeList():
    #########################################
    # Xoá nội dung và kết nối cơ sở dữ liệu #
    #########################################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("EMPLOYEE LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/background_manage.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    result = cursor.fetchall()
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5, columnspan=9)
    title_label = Label(root, text="EMPLOYEE LIST",font=('Arial',35,'bold'),fg='red')
    title_label.config(relief=RAISED, bd=5)
    title_label.grid(column=5,row=0)
    back_button = Button(root,text="Back",command=Manage_Display,font=('Arial',25),width=10,fg='green')
    back_button.grid(column=2, row=3)
    replace_button = Button(root,text="Replace",font=('Arial',25),width=10,command=ReplaceDisplay,fg='green')
    replace_button.grid(column=5,row=3)
    delete_button = Button(root,text="Delete", font=('Arial',25),width=10,command=DeleteEmployee,fg='green')
    delete_button.grid(column=8,row=3)
    ###############################################
    # Tạo treeview và đưa thông tin nhân viên vào #
    ###############################################
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")
    treeview.heading("col1", text="EMPLOYEE ID")
    treeview.heading("col2", text="EMPLOYEE NAME")
    treeview.heading("col3", text="EMPLOYEE DUTY")
    treeview.heading("col4", text="PHONE NUMBER")
    treeview.heading("col5", text="ADDRESS")
    treeview.heading("col6", text="ACCESS")
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    for row in result:
        treeview.insert("", "end", values=row)
    conn.close()
    root.mainloop()
##################
# thêm nhân viên #
##################
def AddEmployee():
    ###############################
    # Xoá và trang trí lại cửa sổ #
    ###############################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("EMPLOYEE LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/background_manage.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="ADD EMPLOYEE", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)  
    MANV_LABEL = Label(frame, text="EMPLOYEE ID:",font=normal_font)
    MANV_LABEL.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    MANV_ENTRY = Entry(frame,width=20)
    MANV_ENTRY.grid(column=1, row=0, padx=20, pady=10)
    TENNV_LABEL = Label(frame, text="EMPLOYEE NAME:",font=normal_font)
    TENNV_LABEL.grid(column=0, row=1, padx=20, pady=20,sticky=W)
    TENNV_ENTRY = Entry(frame,width=20)
    TENNV_ENTRY.grid(column=1, row=1, padx=20, pady=20)
    CV_LABEL = Label(frame, text="EMPLOYEE DUTY:", font=normal_font)
    CV_LABEL.grid(column=0,row=2,padx=20,pady=20,sticky=W)
    CV_ENTRY = Entry(frame,width=20)
    CV_ENTRY.grid(column=1,row=2,padx=20,pady=20)
    SDT_LABEL = Label(frame, text="PHONE NUMBER:", font=normal_font)
    SDT_LABEL.grid(column=0,row=3,padx=20,pady=20,sticky=W)
    SDT_ENTRY = Entry(frame,width=20)
    SDT_ENTRY.grid(column=1,row=3,padx=20,pady=20)
    DC_LABEL = Label(frame, text="ADDRESS:", font=normal_font)
    DC_LABEL.grid(column=0,row=4,padx=20,pady=20,sticky=W)
    DC_ENTRY = Entry(frame,width=20)
    DC_ENTRY.grid(column=1,row=4,padx=20,pady=20)
    A_LABEL = Label(frame, text="ACCESS:", font=normal_font)
    A_LABEL.grid(column=0,row=5,padx=20,pady=20,sticky=W)
    A_ENTRY = Entry(frame,width=20)
    A_ENTRY.grid(column=1,row=5,padx=20,pady=20)
    #############################
    # Bấm nút để thêm nhân viên #
    #############################
    add_button = Button(frame, text="ADD EMPLOYEE",font=('Arial',16,'bold'),command=lambda: Add(MANV_ENTRY,TENNV_ENTRY,CV_ENTRY,SDT_ENTRY,DC_ENTRY,A_ENTRY))
    add_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10,sticky=W)
    back_button = Button(frame, text="BACK",font=('Arial',16,'bold'),command=Manage_Display)
    back_button.grid(column=2, row=6, columnspan=2, padx=10, pady=10)
    root.mainloop()
############################
# chức năng thêm nhân viên #
############################
def Add(MANV,TENNV,CV,SDT,DC,A):
    ########################################################
    # Lấy thông tin từ người dùng và add vào cơ sở dữ liệu #
    ########################################################
    Ma = MANV.get()
    Ten = TENNV.get()
    cv = CV.get()
    sdt = SDT.get()
    dc = DC.get()
    a = A.get()
    connection = sqlite3.connect("Shop.db")
    cursor = connection.cursor()
    connection.execute(f"INSERT INTO Employee VALUES ('{Ma}','{Ten}','{cv}','{sdt}','{dc}','{a}')")
    connection.commit()
    connection.close()
    #################################################
    # Thông báo thành công và xoá nội dung vừa nhập #
    #################################################
    messagebox.showinfo("NOTICE", "ADD COMPLETED")
    MANV.delete(0, 'end')
    TENNV.delete(0, 'end') 
    CV.delete(0,'end')
    SDT.delete(0, 'end')
    DC.delete(0, 'end')
    A.delete(0, 'end')
#################
# xoá nhân viên #
#################
def DeleteEmployee():
    #################################
    # xoá nội dung và trang trí lại #
    #################################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("EMPLOYEE LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/background_manage.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="DELETE EMPLOYEE", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)   
    MANV_LABEL = Label(frame, text="EMPLOYEE ID:",font=normal_font)
    MANV_LABEL.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    MANV_ENTRY = Entry(frame,width=20)
    MANV_ENTRY.grid(column=1, row=0, padx=20, pady=10) 
    #####################
    # Nút xoá nhân viên #
    ##################### 
    delete_button = Button(frame, text="DELETE EMPLOYEE",font=('Arial',16,'bold'),command=lambda: Delete(MANV_ENTRY))
    delete_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10,sticky=W)
    back_button = Button(frame, text="BACK",font=('Arial',16,'bold'),command=Manage_Display)
    back_button.grid(column=2, row=6, columnspan=2, padx=10, pady=10)
    root.mainloop()
###########################
# chức năng xoá nhân viên #
###########################
def Delete(MANV):
    ######################################################
    # kết nối cơ sở dữ liệu tìm đúng mã nhân viên để xoá #
    ######################################################
    Ma = MANV.get()
    connection = sqlite3.connect("Shop.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Employee WHERE MANV=?", (Ma,))
    connection.commit()
    connection.close()
    MANV.delete(0, 'end')
#################################
# thay đổi thuộc tính nhân viên #
#################################
def ReplaceDisplay():
    #################################
    # xoá nội dung và trang trí lại #
    #################################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("EMPLOYEE LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/background_manage.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="REPLACE EMPLOYEE", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=2,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2) 
    search_Label = Label(root,font=normal_font,text="ENTER EMPLOYEE ID")
    search_Label.grid(column=1,row=1,padx=20)
    search_entry = Entry(root,font=title_font,width=30)
    search_entry.grid(column=2,row=1)
    ################################################
    # Tìm kiếm mã nhân viên cần thay thế thông tin #
    ################################################
    search_button = Button(root,text="SEARCH",font=normal_font,command=lambda:Replace(search_entry))
    search_button.grid(column=3,row=1)
    back_button = Button(root, text="BACK",font=normal_font,command=EmployeeList)
    back_button.grid(column=4,row=1)
    root.mainloop()
################
# hàm thay đổi #
################
def Replace(search_entry):
    ###############################################
    # Nhận thông tin từ người dùng                #
    # Kết nối với cơ sở dữ liệu                   #
    # Tìm đúng mã nhân viên để tiến hành thay đổi #
    ###############################################
    ma_nhan_vien = search_entry.get() 
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee WHERE MANV=?", (ma_nhan_vien,))
    result = cursor.fetchone() 
    conn.close()
    result_label = ttk.Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    ####################################################
    # Tạo treeview hiển thị thông tin nhân viên đã tìm #
    ####################################################
    treeview = ttk.Treeview(result_label, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")
    treeview.heading("col1", text="EMPLOYEE ID")
    treeview.heading("col2", text="EMPLOYEE NAME")
    treeview.heading("col3", text="EMPLOYEE DUTY")
    treeview.heading("col4", text="PHONE NUMBER")
    treeview.heading("col5", text="ADDRESS")
    treeview.heading("col6", text="ACCESS")
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    scrollbar = ttk.Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    frame = Frame(root)
    frame.grid(column=1,row=3,padx=5,pady=5,columnspan=9)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    #####################################################################
    # Nếu đúng mã nhân viên sẽ hiển thị bảng để nhập thông tin muốn sửa #
    #####################################################################
    if result is not None:
        ten_nhan_vien = result[1]
        chuc_vu = result[2]
        so_dien_thoai = result[3]
        dia_chi = result[4]
        quyen_truy_cap = result[5] 
        data = [(ma_nhan_vien,ten_nhan_vien,chuc_vu,so_dien_thoai,dia_chi,quyen_truy_cap)]
        for item in data:
            treeview.insert("", "end", values=item)
        input_label = Label(frame, text="REPLACEMENT NEEED: ",font=('Arial',25))
        input_label.grid(column=0,row=3,sticky=W)
        input_entry = Entry(frame)
        input_entry.grid(column=1,row=3)
        fix_label = Label(frame,text="REPLACEMENT CONTENT: ",font=('Arial',25))
        fix_label.grid(column=0,row=4,sticky=W)
        fix_entry = Entry(frame)
        fix_entry.grid(column=1,row=4)
        ################
        # Nút thay thế #
        ################
        replace_button = Button(frame, text="REPLACED",command=lambda:REPLACE(ma_nhan_vien,fix_entry,input_entry))
        replace_button.grid(column=1,row=5)
        back_button = Button(frame,text="BACK",command=ReplaceDisplay)
        back_button.grid(column=0,row=5)     
    else:
        ##############################################
        # Không tìm thấy nhân viên thì báo not found #
        ##############################################
        result_label = ttk.Label(result_frame, text="NOT FOUND")
        result_label.grid(row=1, column=0, padx=5, pady=5,sticky="w")
################
# hàm thay đổi #
################
def REPLACE(MANV, fix_entry, input_entry):
    ##############################################
    # Nhận thông tin từ người dùng               #
    # Check xem giống với cái nào thì đổi cái đó #
    ##############################################
    FIX = fix_entry.get()
    input = input_entry.get()
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee WHERE MANV=?", (MANV,))
    result = cursor.fetchone()  
    if result is not None:
        print(result[0])
        print(input)
        print(FIX)
        if input == result[0]:
            conn.execute("UPDATE Employee SET MANV = ? WHERE MANV = ?", (FIX, input))
            conn.commit()
            messagebox.showinfo("NOTICE", "REPLACED SUCCESSFULLY")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[1]:
            conn.execute("UPDATE Employee SET TENNV = ? WHERE TENNV = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "REPLACED SUCCESSFULLY")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[2]:
            conn.execute("UPDATE Employee SET CV = ? WHERE CV = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "REPLACED SUCCESSFULLY")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[3]:
            conn.execute("UPDATE Employee SET SDT = ? WHERE SDT = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "REPLACED SUCCESSFULLY")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[4]:
            conn.execute("UPDATE Employee SET ADDRESS = ? WHERE ADDRESS = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "REPLACED SUCCESSFULLY")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[5]:
            conn.execute("UPDATE Employee SET ACCESS = ? WHERE ACCESS = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "REPLACED SUCCESSFULLY")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        else:
            print("Giá trị nhập không khớp với giá trị trong cơ sở dữ liệu.")
    conn.close()
#############################
###########kế toán###########  
############################# 
def AccountingDisplay():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("ACCOUNTING DISPLAY")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/accounting_background.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    title_label = Label(root,text="ACCOUNTING MANAGE",fg="red",font=('Arial',35,'bold'))
    title_label.config(relief=RAISED,bd=5)
    title_label.pack(pady=100)
    product_button = Button(root, text="PRODUCT MANAGEMENT",font=('Arial',25,'bold'),fg="green",width=30,command=ProductDisplay)
    product_button.pack(pady=20)
    product_button.config(relief=RAISED,bd=5)
    custumer_button = Button(root, text="CUSTOMER MANAGEMENT",font=('Arial',25,'bold'),fg="green",width=30,command=CustomerDisplay)
    custumer_button.pack(pady=20)
    custumer_button.config(relief=RAISED,bd=5)
    order_button = Button(root,text="ORDER MANAGEMENT",font=('Arial',25,'bold'),fg="green",width=30,command=OrderDisplay)
    order_button.pack(pady=20)
    order_button.config(relief=RAISED,bd=5)
    back_button = Button(root, text="BACK",font=('Arial',25,'bold'),fg='green',width=30,command=clear_and_return)
    back_button.pack(pady=20)
    root.mainloop()
#####################
# hiển thị sản phẩm #
#####################
def ProductDisplay():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("PRODUCT DISPLAY")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/accounting_background.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT")
    result = cursor.fetchall()
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5, columnspan=9)
    #################
    # Thanh tìm kím #
    #################
    search_frame = ttk.Frame(root)
    search_frame.grid(row=1, column=1, columnspan=9, padx=5, pady=5)
    search_entry = Entry(search_frame, font=('Arial', 25, 'bold'),width=80)
    search_entry.grid(column=0, row=0)
    search_button = Button(search_frame, text="SEARCH", font=('Arial', 25), width=10,command=lambda:searchproduct(search_entry))
    search_button.grid(column=1, row=0)
    title_label = Label(root, text="PRODUCT LIST", font=('Arial', 35, 'bold'), fg='red')
    title_label.config(relief=RAISED, bd=5)
    title_label.grid(column=3, row=0,sticky='nsew',pady=20)
    back_button = Button(root, text="BACK", command=lambda: AccountingDisplay(), font=('Arial', 25), width=10)
    back_button.grid(column=1, row=3,padx=20)
    replace_button = Button(root, text="LIST", font=('Arial', 25), width=10,command=ShowProduct)
    replace_button.grid(column=2, row=3,padx=20)
    add_button = Button(root, text="ADD", font=('Arial', 25), width=10, command=AddProduct)
    add_button.grid(column=4, row=3,padx=20)
    ana_button = Button(root, text="ANALYST",font=('Arial',25),width=10,command=ThongKe)
    ana_button.grid(column=5,row=3,padx=20)
    ########################################
    # Treeview hiển thị thông tin sản phẩm #
    ########################################
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"),
                            show="headings")
    treeview.heading("col1", text="PRODUCT ID")
    treeview.heading("col2", text="PRODUCT NAME")
    treeview.heading("col3", text="DESCRIBE")
    treeview.heading("col4", text="IMAGE")
    treeview.heading("col5", text="DIRECTORY")
    treeview.heading("col6", text="COST")
    treeview.heading("col7", text="STORAGE")
    ##############
    # Thanh cuộn #
    ##############
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=2, sticky="ns")
    #######################################
    # In thông tin nhân viên lên Treeview #
    #######################################
    for row in result:
        treeview.insert("", "end", values=row)
    ##################################
    # Kết nối chức năng cuộn tự động #
    ##################################
    treeview.yview_scroll(0, "units") 
    #########################################################################
    # Thiết lập chức năng cuộn tự động khi kích thước của Treeview thay đổi #
    #########################################################################
    treeview.bind("<Configure>", lambda e: treeview.yview_moveto(0.0))
    conn.close()
    root.mainloop()
####################
# Tìm kím sản phẩm #
####################
def searchproduct(search_entry):
    ############################################################
    # Lấy thông tin từ người dùng và kết nối với cơ sở dữ liệu #
    ############################################################
    search = search_entry.get() 
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    # conn.execute("CREATE TABLE Employee (MANV text, TENNV text, CV text, SDT INT, ADDRESS text, ACCESS text)")
    cursor.execute("SELECT * FROM PRODUCT WHERE MASP=?", (search,))
    result = cursor.fetchone()  
    conn.close()
    result_label = Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    result_frame = Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    ##############################
    # Treeview hiển thị sản phẩm #
    ##############################
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7"),
                            show="headings")
    treeview.heading("col1", text="PRODUCT ID")
    treeview.heading("col2", text="PRODUCT NAME")
    treeview.heading("col3", text="DESCRIBE")
    treeview.heading("col4", text="IMAGE")
    treeview.heading("col5", text="DIRECTORY")
    treeview.heading("col6", text="COST")
    treeview.heading("col7", text="STORAGE")
    scrollbar = Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    #############################
    # Đưa sản phẩm lên treeview #
    #############################
    if result is not None:
        ten_nhan_vien = result[1]
        chuc_vu = result[2]
        so_dien_thoai = result[3]
        dia_chi = result[4]
        quyen_truy_cap = result[5]
        tonkho = result[6]
        data = [(search,ten_nhan_vien,chuc_vu,so_dien_thoai,dia_chi,quyen_truy_cap,tonkho)]
        for item in data:
            treeview.insert("", "end", values=item)
    else:
        ################################
        # Không tìm thấy thì thông báo #
        ################################
        messagebox.showinfo("WARNING", "PRODUCT DOESNT EXITS")
        for widget in root.winfo_children():
            widget.destroy()
        ProductDisplay()
##############################
# Hiển thị hình ảnh sản phẩm #
##############################
def open_image():
    #########################
    # Sử dụng biến toàn cục #
    #########################
    global var
    ####################################################################################################
    # Nếu đúng file hình ảnh thì di chuyển hình ảnh được chọn vào folder để chứa hình ảnh cần hiển thị #
    ####################################################################################################
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = file_path.split("/")[-1]
        destination_folder = "product_picture/"
        shutil.move(file_path, os.path.join(destination_folder, file_name))
        var = file_name
#################
# Thêm sản phẩm #
#################
def AddProduct():
    global var
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("ADD PRODUCT")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/accounting_background.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="ADD PRODUCT", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)  
    MANV_LABEL = Label(frame, text="PRODUCT ID:",font=normal_font)
    MANV_LABEL.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    MANV_ENTRY = Entry(frame,width=20)
    MANV_ENTRY.grid(column=1, row=0, padx=20, pady=10)
    TENNV_LABEL = Label(frame, text="PRODUCT NAME:",font=normal_font)
    TENNV_LABEL.grid(column=0, row=1, padx=20, pady=20,sticky=W)
    TENNV_ENTRY = Entry(frame,width=20)
    TENNV_ENTRY.grid(column=1, row=1, padx=20, pady=20)
    CV_LABEL = Label(frame, text="DESCRIBE:", font=normal_font)
    CV_LABEL.grid(column=0,row=2,padx=20,pady=20,sticky=W)
    CV_ENTRY = Entry(frame,width=20)
    CV_ENTRY.grid(column=1,row=2,padx=20,pady=20)
    SDT_LABEL = Label(frame, text="IMAGE",font=normal_font)
    SDT_LABEL.grid(column=0,row=3,padx=20,pady=20,sticky=W)
    SDT_ENTRY = Button(frame, text="CHOOSE IMAGE", font=normal_font, command=lambda:open_image())
    SDT_ENTRY.grid(column=1,row=3,padx=20,pady=20)
    DC_LABEL = Label(frame, text="DIRECTORY:", font=normal_font)
    DC_LABEL.grid(column=0,row=4,padx=20,pady=20,sticky=W)
    DC_ENTRY = Entry(frame,width=20)
    DC_ENTRY.grid(column=1,row=4,padx=20,pady=20)
    A_LABEL = Label(frame, text="COST:", font=normal_font)
    A_LABEL.grid(column=0,row=5,padx=20,pady=20,sticky=W)
    A_ENTRY = Entry(frame,width=20)
    A_ENTRY.grid(column=1,row=5,padx=20,pady=20)
    T_LABEL = Label(frame, text="STORAGE:", font=normal_font)
    T_LABEL.grid(column=0,row=6,padx=20,pady=20,sticky=W)
    T_ENTRY = Entry(frame,width=20)
    T_ENTRY.grid(column=1,row=6,padx=20,pady=20)
    ##################
    # Chức năng thêm #
    ##################
    login_button = Button(frame, text="ADD",font=('Arial',16,'bold'),command=lambda: AddP(MANV_ENTRY,TENNV_ENTRY,CV_ENTRY,var,DC_ENTRY,A_ENTRY,T_ENTRY))
    login_button.grid(column=0, row=7, columnspan=2, padx=10, pady=10,sticky=W)
    back_button = Button(frame, text="BACK",font=('Arial',16,'bold'),command=ProductDisplay)
    back_button.grid(column=2, row=7, columnspan=2, padx=10, pady=10)
    root.mainloop()
##################
# Chức năng thêm #
##################
def AddP(MANV,TENNV,CV,SDT,DC,A,T):
    #########################################
    # Lấy thông tin từ người dùng           #
    # Kết nối với cơ sở dữ liệu             #
    # Đưa vào cơ sở dữ liệu                 #
    # Xoá nội dung đã nhập để tiếp tục nhập #
    #########################################
    Ma = MANV.get()
    Ten = TENNV.get()
    cv = CV.get()
    dc = DC.get()
    a = A.get()
    t = T.get()
    connection = sqlite3.connect("Shop.db")
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO PRODUCT VALUES ('{Ma}','{Ten}','{cv}','{SDT}','{dc}','{a}','{t}')")
    connection.commit()
    connection.close()
    messagebox.showinfo("NOTICE", "ADD SUCCESSFUL")
    MANV.delete(0, 'end')
    TENNV.delete(0, 'end') 
    CV.delete(0,'end')
    DC.delete(0, 'end')
    A.delete(0, 'end')
    T.delete(0,'end')
###############################
# Hiển thị sản phẩm hàng loạt #
###############################
def ShowProduct():
    ########################
    # xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    background_image = Image.open("background/accounting_background.png")  
    background_image = background_image.resize((1450, 880)) 
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #########################################################################################
    # Đảm bảo tham chiếu đến đối tượng PhotoImage để tránh bị thu hồi bởi garbage collector #
    #########################################################################################
    background_label.image = background_photo
    #########################
    # Kết nối cơ sở dữ liệu #
    #########################
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    title_label = Label(root, text="SHOW PRODUCT", font=('Arial', 35, 'bold'), fg='red')
    title_label.config(relief=RAISED, bd=5)
    title_label.pack(pady=50)
    scroll_frame = Frame(root)
    scroll_frame.pack()
    canvas = Canvas(scroll_frame, width=930,height=300)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    ######################
    # Tạo một thanh cuộn #
    ######################
    scrollbar = Scrollbar(scroll_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    table_frame = Frame(canvas)
    table_frame.config(relief=RAISED,bd=5)
    canvas.create_window((0, 0), window=table_frame, anchor=NW)
    MASP = Label(table_frame, text="PRODUCT ID")
    MASP.config(relief=RAISED, bd=1)
    MASP.grid(column=0, row=0)
    TENSP = Label(table_frame, text="PRODUCT NAME")
    TENSP.config(relief=RAISED, bd=1)
    TENSP.grid(column=1, row=0)
    MOTA = Label(table_frame, text="DESCRIBE")
    MOTA.config(relief=RAISED, bd=1)
    MOTA.grid(column=2, row=0)
    HA = Label(table_frame, text="IMAGE")
    HA.config(relief=RAISED, bd=1)
    HA.grid(column=3, row=0)
    DM = Label(table_frame, text="DIRECTORY")
    DM.config(relief=RAISED, bd=1)
    DM.grid(column=4, row=0)
    G = Label(table_frame, text="COST")
    G.config(relief=RAISED, bd=1)
    G.grid(column=5, row=0)
    T = Label(table_frame, text="STORAGE")
    T.config(relief=RAISED, bd=1)
    T.grid(column=6, row=0)
    back_button = Button(root, text="BACK", font=('Arial', 25), fg='green', width=30,command=ProductDisplay)
    back_button.pack(pady=30)
    replace_button = Button(root, text="REPLACE", font=('Arial', 25), fg='green', width=30,command=ReplaceDisplayD)
    replace_button.pack(pady=30)
    delete_button = Button(root, text="DELETE", font=('Arial', 25), fg='green', width=30,command=DeleteProduct)
    delete_button.pack(pady=30)
    ################################
    # Lấy dữ liệu từ cơ sở dữ liệu #
    ################################
    cursor.execute("SELECT * FROM PRODUCT")
    rows = cursor.fetchall()
    #############################################
    # Nếu là cột hình ảnh thì hiển thị hình ảnh #
    # Còn lại đưa chữ lên bảng                  #
    #############################################
    for row_index, row in enumerate(rows):
        for col_index, value in enumerate(row):
            if col_index == 3:
                image = Image.open('product_picture/' + value) 
                ##################################
                # Điều chỉnh kích thước hình ảnh #
                # Hiển thị hình ảnh              #
                ##################################
                image.thumbnail((100, 100))  
                photo = ImageTk.PhotoImage(image)
                image_label = Label(table_frame, image=photo, padx=10, pady=10)
                image_label.grid(row=row_index + 1, column=col_index)
                image_label.image = photo
                ######################################################
                # Đưa hình ảnh vào thư mực product_image             #
                # Tạo đường dẫn kết hợp với tiền tố "product_image/" #
                ######################################################
                image_path = 'product_image/' + value
            else:
                text_label = Label(table_frame, text=value, padx=40)
                text_label.grid(row=row_index + 1, column=col_index)
    table_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    root.mainloop()
    conn.close()
################
# Xoá sản phẩm #
################
def DeleteProduct():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("PRODUCT LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/accounting_background.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="DELETE PRODUCT", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)   
    MANV_LABEL = Label(frame, text="PRODUCT ID:",font=normal_font)
    MANV_LABEL.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    MANV_ENTRY = Entry(frame,width=20)
    MANV_ENTRY.grid(column=1, row=0, padx=20, pady=10)  
    #################
    # Chức năng xoá #
    #################
    login_button = Button(frame, text="DELETE PRODUCT",font=('Arial',16,'bold'),command=lambda: DeleteP(MANV_ENTRY))
    login_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10,sticky=W)
    back_button = Button(frame, text="BACK",font=('Arial',16,'bold'),command=ShowProduct)
    back_button.grid(column=2, row=6, columnspan=2, padx=10, pady=10)
    root.mainloop()
#################
# Chức năng xoá #
#################
def DeleteP(MANV):
    #####################################################################
    # Nhận thông tin và kiểm tra đúng tiến hành xoá trong cơ sở dữ liệu #
    #####################################################################
    Ma = MANV.get()
    connection = sqlite3.connect("Shop.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM PRODUCT WHERE MASP=?", (Ma,))
    connection.commit()
    connection.close()
    messagebox.showinfo('NOTICE', 'DELETED SUCCESSFULLY')
    MANV.delete(0, 'end')
###################################
# Hàm thay thế thông tin sản phẩm #
###################################
def ReplaceDisplayD():
    ########################
    # Xóa và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("PRODUCT LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/accounting_background.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="REPLACE PRODUCT", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=2,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2) 
    search_Label = Label(root,font=normal_font,text="PRODUCT ID")
    search_Label.grid(column=1,row=1,padx=20)
    search_entry = Entry(root,font=title_font,width=30)
    search_entry.grid(column=2,row=1)
    ######################
    # Chức năng thay đổi #
    ######################
    search_button = Button(root,text="SEARCH",font=normal_font,command=lambda:ReplaceD(search_entry))
    search_button.grid(column=3,row=1)
    back_button = Button(root,text="BACK",font=normal_font,command=ShowProduct)
    back_button.grid(column=4,row=1)
    root.mainloop()
###############################
# Thay đổi thông tin sản phẩm #
###############################
def ReplaceD(search_entry):
    ############################################################################
    # Lấy thông tin từ người dùng                                              #
    # Kiểm tra nếu đúng thông tin thì sẽ mở bảng để nhập thông tin cần sửa đổi #
    # Nếu sai thông tin thì hiển thị notfound                                  #
    ############################################################################
    ma_nhan_vien = search_entry.get()  
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE MASP=?", (ma_nhan_vien,))
    result = cursor.fetchone()  
    conn.close()
    result_label = ttk.Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    treeview = ttk.Treeview(result_label, columns=("col1", "col2", "col3", "col4", "col5", "col6","col7"), show="headings")
    treeview.heading("col1", text="PRODUCT ID")
    treeview.heading("col2", text="PRODUCT NAME")
    treeview.heading("col3", text="DESCRIBE")
    treeview.heading("col4", text="IMAGE")
    treeview.heading("col5", text="DIRECTORY")
    treeview.heading("col6", text="COST")
    treeview.heading("col7", text="STORAGE")
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    scrollbar = ttk.Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    frame = Frame(root)
    frame.grid(column=1,row=3,padx=5,pady=5,columnspan=9)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    if result is not None:
        ten_nhan_vien = result[1]
        chuc_vu = result[2]
        so_dien_thoai = result[3]
        dia_chi = result[4]
        quyen_truy_cap = result[5]
        ton_kho = result[6]
        data = [
        (ma_nhan_vien,ten_nhan_vien,chuc_vu,so_dien_thoai,dia_chi,quyen_truy_cap,ton_kho)
    ]
        for item in data:
            treeview.insert("", "end", values=item)
        input_label = Label(frame, text="REPLACE NEEDED: ",font=('Arial',25))
        input_label.grid(column=0,row=3,sticky=W)
        input_entry = Entry(frame)
        input_entry.grid(column=1,row=3)
        fix_label = Label(frame,text="REPLACE CONTENT: ",font=('Arial',25))
        fix_label.grid(column=0,row=4,sticky=W)
        fix_entry = Entry(frame)
        fix_entry.grid(column=1,row=4)
        ############
        # Thay thế #
        ############
        replace_button = Button(frame, text="REPLACE",command=lambda:REPLACED(ma_nhan_vien,fix_entry,input_entry))
        replace_button.grid(column=1,row=5)
        back_button = Button(frame,text="BACK",command=ReplaceDisplayD)
        back_button.grid(column=0,row=5)
    else:
        result_label = ttk.Label(result_frame, text="NOT FOUND")
        result_label.grid(row=1, column=0, padx=5, pady=5,sticky="w")
############
# Thay thế #
############
def REPLACED(MANV, fix_entry, input_entry):
    ##############################################################
    # Kiểm tra dữ liệu cần thay có khớp với dữ liệu có sẵn không #
    # Nếu có thì thay cái mới vào                                #
    ##############################################################
    FIX = fix_entry.get()
    input = input_entry.get()
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE MASP=?", (MANV,))
    result = cursor.fetchone()  
    if result is not None:
        ten_nhan_vien = result[1]
        chuc_vu = result[2]
        so_dien_thoai = result[3]
        dia_chi = result[4]
        quyen_truy_cap = result[5]
        tonkho = result[6]
        print(result[0])
        print(input)
        print(FIX)
        if input == result[0]:
            conn.execute("UPDATE PRODUCT SET MASP = ? WHERE MASP = ?", (FIX, input))
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == ten_nhan_vien:
            conn.execute("UPDATE PRODUCT SET TENSP = ? WHERE TENSP = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == chuc_vu:
            conn.execute("UPDATE PRODUCT SET MOTA = ? WHERE MOTA = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == so_dien_thoai:
            conn.execute("UPDATE PRODUCT SET HINHANH = ? WHERE HINHANH = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == dia_chi:
            conn.execute("UPDATE PRODUCT SET DM = ? WHERE DM = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif int(input) == quyen_truy_cap:
            conn.execute("UPDATE PRODUCT SET GIA = ? WHERE GIA = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif int(input) == tonkho:
            conn.execute("UPDATE PRODUCT SET TONKHO = ? WHERE TONKHO = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        else:
            print("Giá trị nhập không khớp với giá trị trong cơ sở dữ liệu.")
    conn.close()
#################
# Thống kê tiền #
#################
def ThongKe():
    ########################
    # Xoá và trang trí lại #
    #######################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Login Display")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/accounting_background.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    #########################
    # Kết nối cơ sở dữ liệu #
    #########################
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT")
    result = cursor.fetchall()
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5, columnspan=9)
    search_frame = ttk.Frame(root)
    search_frame.grid(row=1, column=1, columnspan=9, padx=5, pady=5)
    search_entry = Entry(search_frame, font=('Arial', 25, 'bold'),width=80)
    search_entry.grid(column=0, row=0)
    ###############################
    # thống kê tiền của ngày khác #
    ###############################
    search_button = Button(search_frame, text="SEARCH", font=('Arial', 25), width=10,command=lambda:searchTien(search_entry))
    search_button.grid(column=1, row=0)
    title_label = Label(root, text="PRODUCT LIST", font=('Arial', 35, 'bold'), fg='red')
    title_label.config(relief=RAISED, bd=5)
    title_label.grid(column=3, row=0,sticky='nsew',pady=20)
    back_button = Button(root, text="BACK", command=lambda: ProductDisplay(), font=('Arial', 25), width=10)
    back_button.grid(column=1, row=3,padx=20)
    #############################
    # Kiểm tra thu nhập hôm nay #
    #############################
    thongke_button = Button(root, text="REVENUE", font=('Arial', 25), width=10,command=TienHomNay)
    thongke_button.grid(column=2,row=3,padx=20)
    root.mainloop()
##########################
# Tìm thống kê theo ngày #
##########################
def searchTien(search_entry):
    ###############################
    # Nếu có thu nhập thì in ra   #
    # Không thì không có thu nhập #
    ###############################
    search = search_entry.get()
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(TONGGIATRI) FROM ORDERS WHERE NGAYTAO=?",(search,))
    result = cursor.fetchone()[0]
    if result == None:
        messagebox.showinfo("NOTICE","DONT HAVE ANY ORDER TODAY")
    else:
        messagebox.showinfo("NOTICE",f"TODAY'S REVENUE IS {result}đ")
    print(result)
##########################
# In ra thu nhập hôm nay #
##########################
def TienHomNay():
    ##############################################
    # Lấy ngày hiện tại                          #
    # Chuyển format đúng dịnh dạng cơ sở dữ liệu #
    # Tìm kiếm ngày trong cơ sở dữ liệu          #
    # Không có thì hiển thị không có             #
    ##############################################
    today = datetime.date.today()
    formatted_date = today.strftime("%d/%m/%Y")
    print(formatted_date)
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(TONGGIATRI) FROM ORDERS WHERE NGAYTAO=?",(formatted_date,))
    result = cursor.fetchone()[0]
    if result == None:
        messagebox.showinfo("NOTICE","DONT HAVE ANY ORDER TODAY")
    else:
        messagebox.showinfo("NOTICE",f"TODAY'S REVENUE IS {result}đ")
    print(result)    
###################################
########Quản lý  khách hàng######## 
###################################  
def CustomerDisplay():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Customer Display")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/Customer.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER")
    result = cursor.fetchall()
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5, columnspan=9)
    search_frame = ttk.Frame(root)
    search_frame.grid(row=1, column=1, columnspan=9, padx=5, pady=5)
    search_entry = Entry(search_frame, font=('Arial', 25, 'bold'),width=80)
    search_entry.grid(column=0, row=0)
    search_button = Button(search_frame, text="SEARCH", font=('Arial', 25), width=10,command=lambda:searchCustomer(search_entry))
    search_button.grid(column=1, row=0)
    title_label = Label(root, text="CUSTOMER LIST", font=('Arial', 35, 'bold'), fg='red')
    title_label.config(relief=RAISED, bd=5)
    title_label.grid(column=3, row=0,sticky='nsew',pady=20)
    back_button = Button(root, text="BACK", command=lambda: AccountingDisplay(), font=('Arial', 25), width=10)
    back_button.grid(column=1, row=3,padx=20)
    replace_button = Button(root, text="LIST", font=('Arial', 25), width=10,command=ShowCustomer)
    replace_button.grid(column=2, row=3,padx=20)
    ana_button = Button(root, text="HISTORY",font=('Arial',25),width=10,command=lambda:History(search_entry))
    ana_button.grid(column=5,row=3,padx=20)
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5"),
                            show="headings")
    treeview.heading("col1", text="CUSTOMER ID")
    treeview.heading("col2", text="CUSTOMER NAME")
    treeview.heading("col3", text="PHONE NUMBER")
    treeview.heading("col4", text="ADDRESS")
    treeview.heading("col5", text="PURCHASE")
    ######################
    # Tạo thanh cuộn dọc #
    ######################
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=2, sticky="ns")
    for row in result:
        treeview.insert("", "end", values=row)
    treeview.yview_scroll(0, "units") 
    treeview.bind("<Configure>", lambda e: treeview.yview_moveto(0.0))
    conn.close()
    root.mainloop()
#######################
# Tìm kiếm khách hàng #
#######################
def searchCustomer(search_entry):
    ################################################
    # Nhận thông tin từ người dùng                 #
    # Nếu có trong cơ sở dữ liệu sẽ in ra treeview #
    ################################################
    search = search_entry.get()  
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER WHERE MAKH=?", (search,))
    result = cursor.fetchone()
    conn.close()
    result_label = Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    result_frame = Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5"),
                            show="headings")
    treeview.heading("col1", text="CUSTOMER ID")
    treeview.heading("col2", text="CUSTOMER NAME")
    treeview.heading("col3", text="PHONE NUMBER")
    treeview.heading("col4", text="ADDRESS")
    treeview.heading("col5", text="PURCHASE")
    scrollbar = Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    if result is not None:
        ten_nhan_vien = result[1]
        chuc_vu = result[2]
        so_dien_thoai = result[3]
        dia_chi = result[4]
        data = [(search,ten_nhan_vien,chuc_vu,so_dien_thoai,dia_chi)]
        for item in data:
            treeview.insert("", "end", values=item)
    else:
        messagebox.showinfo("NOTICE", "NOT FOUND")
        for widget in root.winfo_children():
            widget.destroy()
        CustomerDisplay()
#######################
# Thông tin khác hàng #
#######################
def ShowCustomer():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Customer Display")
    root.geometry()
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/Customer.png"
    background_image = Image.open(background_image_path)
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    #############################
    # Kết nối với cơ sở dữ liệu #
    #############################
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER")
    result = cursor.fetchone() 
    conn.close()
    result_label = Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    title = Label(root,text="HISTORY",font=('Arial',35,'bold'),fg='red')
    title.config(relief=RAISED,bd=5)
    title.grid(column=5,row=0)
    result_frame = Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5"),
                            show="headings")
    treeview.heading("col1", text="CUSTOMER ID")
    treeview.heading("col2", text="CUSTOMER NAME")
    treeview.heading("col3", text="PHONE NUMBER")
    treeview.heading("col4", text="ADDRESS")
    treeview.heading("col5", text="PURCHASE")
    scrollbar = Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=1, column=1, sticky="w")
    scrollbar.grid(row=1, column=2, sticky="ns")
    if result is not None:
        ten_nhan_vien = result[0]
        chuc_vu = result[1]
        so_dien_thoai = result[2]
        dia_chi = result[3]
        giatri = result[4]
        data = [(ten_nhan_vien,chuc_vu,so_dien_thoai,dia_chi,giatri)]
        for item in data:
            treeview.insert("", "end", values=item)
    ###############
    # Nút quay về #
    ###############
    backbutton = Button(root,text="BACK",command=CustomerDisplay,font=('Arial',25),fg="green",width=10)
    backbutton.config(relief=RAISED,bd=5)
    backbutton.grid(column=5,row=5,pady=20)
    ###########################
    # Sửa thông tin nhân viên #
    ###########################
    replacebutton = Button(root,text="REPLACE",command=replaceC,font=('Arial',25),fg="green",width=10)
    replacebutton.config(relief=RAISED,bd=5)
    replacebutton.grid(column=5,row=6,pady=20)
    ##################
    # Xoá khách hàng #
    ##################
    deletebutton = Button(root,text="DELETE",command=deleteC,font=('Arial',25),fg="green",width=10)
    deletebutton.config(relief=RAISED,bd=5)
    deletebutton.grid(column=5 ,row=7,pady=20)
    root.mainloop()
###########################
# Chức năng sửa thông tin #
###########################
def replaceC():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("CUSTOMER LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/Customer.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="REPLACE CUSTOMER", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=2,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2) 
    search_Label = Label(root,font=normal_font,text="CUSTOMER ID")
    search_Label.grid(column=1,row=1,padx=20)
    search_entry = Entry(root,font=title_font,width=30)
    search_entry.grid(column=2,row=1)
    ######################
    # Chức năng thay thế #
    ######################
    search_button = Button(root,text="SEARCH",font=normal_font,command=lambda:Replacec(search_entry))
    search_button.grid(column=3,row=1)
    back_button = Button(root, text="BACK",font=normal_font,command=ShowCustomer)
    back_button.grid(column=4,row=1)
    root.mainloop()
######################
# Chức năng thay thế #
######################
def Replacec(search_entry):
    ######################################
    # Lấy thông tin từ người dùng        #
    # Kết nối với cơ sở dữ liệu          #
    # in thông tin tìm được lên treeview #
    # Tạo bảng để nhập thông tin cần sửa #
    ######################################
    ma_nhan_vien = search_entry.get() 
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER WHERE MAKH=?", (ma_nhan_vien,))
    result = cursor.fetchone() 
    conn.close()
    result_label = ttk.Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    treeview = ttk.Treeview(result_label, columns=("col1", "col2", "col3", "col4", "col5"), show="headings")
    treeview.heading("col1", text="CUSTOMER ID")
    treeview.heading("col2", text="CUSTOMER NAME")
    treeview.heading("col3", text="PHONE NUMBER")
    treeview.heading("col4", text="ADDRESS")
    treeview.heading("col5", text="PURCHASE")
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    scrollbar = ttk.Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    frame = Frame(root)
    frame.grid(column=1,row=3,padx=5,pady=5,columnspan=9)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    if result is not None:
        ten_nhan_vien = result[1]
        chuc_vu = result[2]
        so_dien_thoai = result[3]
        dia_chi = result[4] 
        data = [(ma_nhan_vien,ten_nhan_vien,chuc_vu,so_dien_thoai,dia_chi)]
        for item in data:
            treeview.insert("", "end", values=item)
        input_label = Label(frame, text="REPLACE NEEDED",font=('Arial',25))
        input_label.grid(column=0,row=3,sticky=W)
        input_entry = Entry(frame)
        input_entry.grid(column=1,row=3)
        fix_label = Label(frame,text="REPLACE CONTENT: ",font=('Arial',25))
        fix_label.grid(column=0,row=4,sticky=W)
        fix_entry = Entry(frame)
        fix_entry.grid(column=1,row=4)
        ############
        # Thay thế #
        ############
        replace_button = Button(frame, text="REPLACE",command=lambda:REPLACEC(ma_nhan_vien,fix_entry,input_entry))
        replace_button.grid(column=1,row=5)
        back_button = Button(frame,text="BACK",command=replaceC)
        back_button.grid(column=0,row=5)     
    else:
        result_label = ttk.Label(result_frame, text="NOT FOUND")
        result_label.grid(row=1, column=0, padx=5, pady=5,sticky="w")
############
# Thay thế #
############
def REPLACEC(MANV, fix_entry, input_entry):
    #####################################
    # Lấy thông tin từ người dùng       #
    # Check đúng thì tiến hành thay thế #
    #####################################
    FIX = fix_entry.get()
    input = input_entry.get()
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CUSTOMER WHERE MAKH=?", (MANV,))
    result = cursor.fetchone()  
    if result is not None:
        print(result[0])
        print(input)
        print(FIX)
        if input == result[0]:
            conn.execute("UPDATE CUSTOMER SET MAKH = ? WHERE MAKH = ?", (FIX, input))
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[1]:
            conn.execute("UPDATE CUSTOMER SET TENKH = ? WHERE TENKH = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[2]:
            conn.execute("UPDATE CUSTOMER SET SDT = ? WHERE SDT = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[3]:
            conn.execute("UPDATE CUSTOMER SET DIACHI = ? WHERE DIACHI = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        elif input == result[4]:
            conn.execute("UPDATE CUSTOMER SET LS = ? WHERE LS = ?", (FIX, input)) 
            conn.commit()
            messagebox.showinfo("NOTICE", "SUCCESSFUL")
            input_entry.delete(0,'end')
            fix_entry.delete(0,'end')
        else:
            print("Giá trị nhập không khớp với giá trị trong cơ sở dữ liệu.")
    conn.close()
##################
# Xoá khách hàng #
##################
def deleteC():
    ####################
    # Xoá và trang trí #
    ####################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("CUSTOMER LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/Customer.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="DELETE CUSTOMER", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)   
    MANV_LABEL = Label(frame, text="CUSTOMER ID:",font=normal_font)
    MANV_LABEL.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    MANV_ENTRY = Entry(frame,width=20)
    MANV_ENTRY.grid(column=1, row=0, padx=20, pady=10)  
    #################
    # Chức năng xoá #
    #################
    login_button = Button(frame, text="DELETE",font=('Arial',16,'bold'),command=lambda: DeleteC(MANV_ENTRY))
    login_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10,sticky=W)
    back_button = Button(frame, text="BACK",font=('Arial',16,'bold'),command=ShowCustomer)
    back_button.grid(column=2, row=6, columnspan=2, padx=10, pady=10)
    root.mainloop()
#################
# Chức năng xoá #
#################
def DeleteC(MANV):
    Ma = MANV.get()
    connection = sqlite3.connect("Shop.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM CUSTOMER WHERE MAKH=?", (Ma,))
    cursor.execute("DELETE FROM ORDERS WHERE MAKH=?",(Ma,))
    connection.commit()
    messagebox.showinfo("NOTICE","SUCCESSFULLY")
    connection.close()
    MANV.delete(0, 'end')
####################
# Lịch sử mua hàng #
####################  
def History(search_entry):
    ##########################################################
    # Xoá và hiển thị lại toàn bộ lần khách hàng đã mua hàng #
    ##########################################################
    search = search_entry.get()
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Customer Display")
    root.geometry()
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/Customer.png"
    background_image = Image.open(background_image_path)
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    if search == None:
        messagebox.showinfo("NOTICE","NOT FOUND")
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    a = cursor.execute("SELECT * FROM ORDERS WHERE MAKH=?", (search,))
    result_label = Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    title = Label(root,text="HISTORY",font=('Arial',35,'bold'),fg='red')
    title.config(relief=RAISED,bd=5)
    title.grid(column=4,row=0)
    result_frame = Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5","col6"),
                            show="headings")
    treeview.heading("col1", text="ORDER ID")
    treeview.heading("col2", text="DATE")
    treeview.heading("col3", text="CUSTOMER ID")
    treeview.heading("col4", text="PRODUCT ID")
    treeview.heading("col5", text="AMOUNT")
    treeview.heading("col6",text="VALUE")
    scrollbar = Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=1, column=1, sticky="w")
    scrollbar.grid(row=1, column=2, sticky="ns")
    for row in a:
        MADH = row[0]
        ten_nhan_vien = row[1]
        chuc_vu = row[2]
        so_dien_thoai = row[3]
        dia_chi = row[4]
        giatri = row[5]
        data = (MADH, ten_nhan_vien, chuc_vu, so_dien_thoai, dia_chi, giatri)
        treeview.insert("", "end", values=data)
    backbutton = Button(root,text="BACK",command=CustomerDisplay,font=('Arial',25),fg="green",width=10)
    backbutton.config(relief=RAISED,bd=5)
    backbutton.grid(column=4,row=5)
    conn.close()
    root.mainloop()
####################################
##########Quản lý đơn hàng##########
####################################
def OrderDisplay():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Order Display")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/order.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ORDERS")
    result = cursor.fetchall()
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5, columnspan=9)
    search_frame = ttk.Frame(root)
    search_frame.grid(row=1, column=1, columnspan=9, padx=5, pady=5)
    search_entry = Entry(search_frame, font=('Arial', 25, 'bold'),width=80)
    search_entry.grid(column=0, row=0)
    ###########
    # tìm kím #
    search_button = Button(search_frame, text="SEARCH", font=('Arial', 25), width=10,command=lambda:searchorder(search_entry))
    search_button.grid(column=1, row=0)
    title_label = Label(root, text="ORDER LIST", font=('Arial', 35, 'bold'), fg='red')
    title_label.config(relief=RAISED, bd=5)
    title_label.grid(column=3, row=0,sticky='nsew',pady=20)
    ###########
    # Quay về #
    ###########
    back_button = Button(root, text="BACK", command=lambda: AccountingDisplay(), font=('Arial', 25), width=10)
    back_button.grid(column=1, row=3,padx=20)
    ####################
    # Hiển thị đơn mua #
    ####################
    replace_button = Button(root, text="LIST", font=('Arial', 25), width=10,command=ShowOrder)
    replace_button.grid(column=2, row=3,padx=20)
    #################
    # Thêm đơn hàng #
    #################
    add_button = Button(root, text="ADD", font=('Arial', 25), width=10, command=Addorder)
    add_button.grid(column=4, row=3,padx=20)
    ################
    # Xuất hoá đơn #
    ################
    ana_button = Button(root, text="EXPORT",font=('Arial',25),width=10,command=SHOWHOADONDISPLAY)
    ana_button.grid(column=5,row=3,padx=20)
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5","col6"),
                            show="headings")
    treeview.heading("col1", text="ORDER ID")
    treeview.heading("col2", text="DATE")
    treeview.heading("col3", text="CUSTOMER ID")
    treeview.heading("col4", text="PRODUCT ID")
    treeview.heading("col5", text="AMOUNT")
    treeview.heading("col6", text="VALUE")
    ######################
    # Tạo thanh cuộn dọc #
    ######################
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=2, sticky="ns")
    for row in result:
        treeview.insert("", "end", values=row)
    treeview.yview_scroll(0, "units")  
    treeview.bind("<Configure>", lambda e: treeview.yview_moveto(0.0))
    conn.close()
    root.mainloop()
###########
# Tìm kím # 
###########
def searchorder(search_entry):
    search = search_entry.get()  
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ORDERS WHERE MADH=?", (search,))
    result = cursor.fetchone()  
    conn.close()
    result_label = Frame(root)
    result_label.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    result_frame = Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5,columnspan=9)
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5","col6"),
                            show="headings")
    treeview.heading("col1", text="ORDER ID")
    treeview.heading("col2", text="DATE")
    treeview.heading("col3", text="CUSTOMER ID")
    treeview.heading("col4", text="PRODUCT ID")
    treeview.heading("col5", text="AMOUNT")
    treeview.heading("col6", text="VALUE")
    scrollbar = Scrollbar(result_label, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    if result is not None:
        ten_nhan_vien = result[1]
        chuc_vu = result[2]
        so_dien_thoai = result[3]
        dia_chi = result[4]
        tong = result[5]
        data = [(search,ten_nhan_vien,chuc_vu,so_dien_thoai,dia_chi,tong)]
        for item in data:
            treeview.insert("", "end", values=item)
    else:
        messagebox.showinfo("NOTICE", "NOT FOUND")
        for widget in root.winfo_children():
            widget.destroy()
        OrderDisplay()
###############################
# Hiển thị thông tin đơn hàng #
###############################
def ShowOrder():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("ORDER LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/order.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ORDERS")
    result = cursor.fetchall()
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5, columnspan=9)
    title_label = Label(root, text="ORDER LIST",font=('Arial',35,'bold'),fg='red')
    title_label.config(relief=RAISED, bd=5)
    title_label.grid(column=5,row=0)
    back_button = Button(root,text="BACK",command=OrderDisplay,font=('Arial',25),width=10)
    back_button.grid(column=2, row=3)
    delete_button = Button(root,text="DELETE", font=('Arial',25),width=10,command=DeleteOrder)
    delete_button.grid(column=8,row=3)
    treeview = ttk.Treeview(result_frame, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")
    treeview.heading("col1", text="ORDER ID")
    treeview.heading("col2", text="DATE")
    treeview.heading("col3", text="CUSTOMER ID")
    treeview.heading("col4", text="PRODUCT")
    treeview.heading("col5", text="AMOUNT")
    treeview.heading("col6", text="VALUE")
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scrollbar.set)
    treeview.grid(row=0, column=0, sticky="w")
    scrollbar.grid(row=0, column=1, sticky="ns")
    for row in result:
        treeview.insert("", "end", values=row)
    conn.close()
    root.mainloop()
    conn.close()
################
# Xoá đơn hàng #
################
def DeleteOrder():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("ORDER LIST")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/order.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="DELETE ORDER", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)   
    MANV_LABEL = Label(frame, text="ORDER ID:",font=normal_font)
    MANV_LABEL.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    MANV_ENTRY = Entry(frame,width=20)
    MANV_ENTRY.grid(column=1, row=0, padx=20, pady=10)  
    #################
    # Chức năng xoá #
    #################
    login_button = Button(frame, text="DELETE",font=('Arial',16,'bold'),command=lambda: DeleteO(MANV_ENTRY))
    login_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10,sticky=W)
    back_button = Button(frame, text="BACK",font=('Arial',16,'bold'),command=ShowOrder)
    back_button.grid(column=2, row=6, columnspan=2, padx=10, pady=10)
    root.mainloop()
#################
# Chức năng xoá #
#################
def DeleteO(MANV):
    Ma = MANV.get()
    connection = sqlite3.connect("Shop.db")
    cursor = connection.cursor()
    MAKH=""
    LS=""
    messagebox.showinfo("NOTICE","SUCCESSFULLY")
    makh = cursor.execute("SELECT * FROM ORDERS WHERE MADH=?",(Ma,))
    for i in makh:
        MAKH = i[2]
    ls = cursor.execute("SELECT * FROM CUSTOMER WHERE MAKH=?",(MAKH,))
    for i in ls:
        LS = i[4]
    new = int(LS) -1
    cursor.execute("UPDATE CUSTOMER SET LS = ? WHERE MAKH = ?", (new, MAKH))
    cursor.execute("DELETE FROM ORDERS WHERE MADH=?", (Ma,))
    connection.commit()
    connection.close()
    MANV.delete(0, 'end')
#################
# Thêm đơn hàng #
#################
def Addorder():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("ADD ORDER")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/order.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="ADD ORDER", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)  
    MANV_LABEL = Label(frame, text="ORDER ID:",font=normal_font)
    MANV_LABEL.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    MANV_ENTRY = Entry(frame,width=20)
    MANV_ENTRY.grid(column=1, row=0, padx=20, pady=10)
    TENNV_LABEL = Label(frame, text="DATE:",font=normal_font)
    TENNV_LABEL.grid(column=0, row=1, padx=20, pady=20,sticky=W)
    TENNV_ENTRY = Entry(frame,width=20)
    TENNV_ENTRY.grid(column=1, row=1, padx=20, pady=20)
    CV_LABEL = Label(frame, text="CUSTOMER ID:", font=normal_font)
    CV_LABEL.grid(column=0,row=2,padx=20,pady=20,sticky=W)
    CV_ENTRY = Entry(frame,width=20)
    CV_ENTRY.grid(column=1,row=2,padx=20,pady=20)
    A_LABEL = Label(frame, text="PRODUCT ID:", font=normal_font)
    A_LABEL.grid(column=0,row=5,padx=20,pady=20,sticky=W)
    A_ENTRY = Entry(frame,width=20)
    A_ENTRY.grid(column=1,row=5,padx=20,pady=20)
    T_LABEL = Label(frame, text="AMOUNT:", font=normal_font)
    T_LABEL.grid(column=0,row=6,padx=20,pady=20,sticky=W)
    T_ENTRY = Entry(frame,width=20)
    T_ENTRY.grid(column=1,row=6,padx=20,pady=20,sticky=W)
    ##################
    # Chức năng thêm #
    ##################
    login_button = Button(frame, text="ADD",font=('Arial',16,'bold'),command=lambda: AddO(MANV_ENTRY,TENNV_ENTRY,CV_ENTRY,A_ENTRY,T_ENTRY))
    login_button.grid(column=0, row=8, columnspan=2, padx=10, pady=10,sticky=W)
    back_button = Button(frame, text="BACK",font=('Arial',16,'bold'),command=OrderDisplay)
    back_button.grid(column=2, row=8, columnspan=2, padx=10, pady=10)
    root.mainloop()
##################
# Chức năng thêm #
##################
def AddO(MANV,TENNV,CV,A,T):
    Ma = MANV.get()
    Ten = TENNV.get()
    cv = CV.get()
    a = A.get()
    t = T.get()
    t = int(t)
    connection = sqlite3.connect("Shop.db")
    cursor = connection.cursor()
    cursor.execute("SELECT GIA FROM PRODUCT WHERE MASP=?",(a,))
    g = cursor.fetchone()[0]
    gia = g*t
    cursor.execute(f"INSERT INTO ORDERS VALUES ('{Ma}','{Ten}','{cv}','{a}','{t}','{gia}')")
    connection.commit()
    #mở ra khách hàng
    conn = sqlite3.connect("Shop.db")
    cur = conn.cursor()
    cur.execute("SELECT MAKH FROM CUSTOMER WHERE MAKH=?", (cv,))
    makh = existing_customer = cur.fetchall()
    b=""
    sl=""
    for i in makh:
        b = i[0]
    ##########################################################################
    # Nếu như là khách hàng cũ thì tiến hành thêm vào hoá đơn sản phẩm thứ 1 #
    # xử lý vấn đề 1 mã đơn hàng chỉ tồn tại 1 mã sản phẩm                   # 
    ##########################################################################
    if b == cv:
        
        messagebox.showinfo("NOTICE", "CUSTOMER ALREADY EXITS")
        test = cur.execute("SELECT * FROM CUSTOMER WHERE MAKH=?",(cv,))
        for i in test:
            sl = i[4]
        new_count = int(sl) + 1
        cur.execute("UPDATE CUSTOMER SET LS=? WHERE MAKH=?", (new_count, cv))
        conn.commit()
        cur.execute("SELECT TONKHO FROM PRODUCT WHERE MASP=?",(a,))
        tonkho = cur.fetchall()
        new = int(tonkho[0][0]) - int(t)
        cur.execute("UPDATE PRODUCT SET TONKHO=? WHERE MASP=?",(new,a))
        conn.commit()
        HOADONDISPLAY() 
    else:
        #############################
        # Nếu như là khách hàng mới #
        # Thêm vào hoá đơn trước    #
        # Thêm khách hàng mới luôn  #
        #############################
        
        messagebox.showinfo("NOTICE", "CREATE CUSTOMER")
        test = cur.execute("SELECT * FROM CUSTOMER WHERE MAKH=?",(cv,))
        cur.execute("UPDATE CUSTOMER SET LS=? WHERE MAKH=?", (1, cv))
        conn.commit()
        cur.execute("SELECT TONKHO FROM PRODUCT WHERE MASP=?",(a,))
        tonkho = cur.fetchall()
        new = int(tonkho[0][0]) - int(t)
        cur.execute("UPDATE PRODUCT SET TONKHO=? WHERE MASP=?",(new,a))
        conn.commit()
        HOADONDISPLAY()
        AddCustomer()
    messagebox.showinfo("NOTICE", "SUCCESSFULLY")
    MANV.delete(0, 'end')
    TENNV.delete(0, 'end') 
    CV.delete(0,'end')
    A.delete(0, 'end')
    T.delete(0,'end')
    cursor.execute("SELECT MADH FROM ORDERS")
    connection.close()
###########
# Hoá đơn #
###########
def HOADONDISPLAY():
    ###############################################
    # Tạo một cửa sổ mới giống việc in tờ hoá đơn #
    ###############################################
    window = Tk()
    MAKH_Label = Label(window, text="CUSTOMER ID: ")
    MAKH_Label.grid(column=0,row=0)
    MAKH_Entry = Entry(window)
    MAKH_Entry.grid(column=1,row=0)
    MADH_Label = Label(window, text="ORDER ID: ")
    MADH_Label.grid(column=0,row=1)
    MADH_Entry = Entry(window)
    MADH_Entry.grid(column=1,row=1)
    MASP_Label = Label(window, text="PRODUCT ID: ")
    MASP_Label.grid(column=0,row=2)
    MASP_Entry = Entry(window)
    MASP_Entry.grid(column=1,row=2)
    SL_Label = Label(window, text="AMOUNT: ")
    SL_Label.grid(column=0,row=3)
    SL_Entry = Entry(window)
    SL_Entry.grid(column=1,row=3)
    ADD = Button(window,text="ADD", command=lambda:ADDHOADON(MAKH_Entry,MADH_Entry,MASP_Entry,SL_Entry))
    ADD.grid(column=0,row=4,columnspan=2)
    conn = sqlite3.connect('Shop.db')
    cursor = conn.cursor()
    conn.commit()
    conn.close()
    window.mainloop()
####################
# Thêm vào hoá đơn #
####################
def ADDHOADON(MAKH_Entry, MADH_Entry, MASP_Entry, SL_Entry):
    #######################################################################
    # Nhận thông tin từ người dùng                                        #
    # gồm có Mã đơn hàng, mã khách hàng, mã sản phẩm và số lượng sản phẩm #
    #######################################################################
    MAKH = MAKH_Entry.get()
    MADH = MADH_Entry.get()
    MASP = MASP_Entry.get()
    SL = SL_Entry.get()
    a = int(SL)
    connect = sqlite3.connect("Shop.db")
    cursor = connect.cursor()
    cursor.execute("SELECT COUNT(*) FROM CUSTOMER WHERE MAKH = ?", (MAKH,))
    result = cursor.fetchone()[0]
    if result == 0:
        ######################################
        # Khách hàng mới thì thêm khách hàng #
        ######################################
        AddCustomer()
    else:
        ##############################################################
        # khoá chính sẽ là MãKH và sử lý bằng cách thêm số lượng vào #
        # ví dụ khách hàng 1 có 3 món                                #
        # thì sẽ là KH001_1, KH001_2, KH001_3                        #
        # sẽ lưu được cùng 1 mã đơn hàng và 3 món sản phẩm           #
        ##############################################################
        messagebox.showinfo("NOTICE", "SUCCESSFUL")
        cursor.execute("SELECT GIA FROM PRODUCT WHERE MASP=?", (MASP,))
        gia = cursor.fetchone()[0]
        ###############################################
        # Tiền sẽ là số sản phẩm * với giá 1 sản phẩm #
        ###############################################
        gia_new = gia * a
        cursor.execute("SELECT COUNT(*) FROM HOADON WHERE MAKH LIKE ?", (f"{MAKH}_%",))
        count = cursor.fetchone()[0] + 1
        new_MAKH = f"{MAKH}_{count}"
        cursor.execute("INSERT INTO HOADON (MAKH, MADH, MASP, SL, GIA) VALUES (?, ?, ?, ?, ?)", (new_MAKH, MADH, MASP, SL, gia_new))
        connect.commit()
        MAKH.delete(0, 'end')
        MADH.delete(0, 'end')
        MASP.delete(0, 'end')
        SL.delete(0, 'end')
####################
# Hiển thị hoá đơn #
####################
def SHOWHOADONDISPLAY():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Order Display")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/order.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="SHOW BILL", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=3)
    conn = sqlite3.connect("Shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ORDERS")
    result = cursor.fetchall()
    result_frame = ttk.Frame(root)
    result_frame.grid(row=2, column=1, padx=5, pady=5, columnspan=9)
    search_frame = ttk.Frame(root)
    search_frame.grid(row=1, column=1, columnspan=9, padx=5, pady=5)
    search_entry = Entry(search_frame, font=('Arial', 25, 'bold'),width=60)
    search_entry.grid(column=0, row=0)
    ###########
    # In Bill #
    ###########
    search_button = Button(search_frame, text="SEARCH", font=('Arial', 25), width=10,command=lambda:BILL(search_entry))
    search_button.grid(column=1, row=0)
    back_button = Button(search_frame,text="BACK",font=('Arial', 25), width=10,command=OrderDisplay)
    back_button.grid(column=2,row=0)
    conn.close()
    root.mainloop()
###########
# In Bill #
###########
def BILL(search_entry):
    #######################################################################
    # Kết nối với cơ sở dữ liệu với mã đơn hàng                           #
    # Nếu đúng thì sẽ tiến hàng xem coi còn hàng nào có mã đơn hàng không #
    # in ra 1 lượt                                                        #
    #######################################################################
    TEN = search_entry.get()
    conn = sqlite3.connect("Shop.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM HOADON WHERE MADH=?", (TEN,))
    results = cur.fetchall()
    gia_dict = {}
    cur.execute("SELECT MAKH FROM ORDERS WHERE MADH=?", (TEN,))
    a = cur.fetchone()[0]
    for i in results:
        MADH = i[1]
        MASP = i[2]
        SL = int(i[3])
        GIA = int(i[4])
        ####################################################
        # Tạo khóa duy nhất bằng cách kết hợp MADH và MASP #
        ####################################################
        key = MADH + "-" + MASP
        ##########################################################
        # Cộng giá vào tổng giá cho khóa tương ứng trong từ điển #
        ##########################################################
        if key in gia_dict:
            gia_dict[key] += GIA
        else:
            gia_dict[key] = GIA
    ######################
    # Tạo giao diện bill #
    ######################
    bill_window = Toplevel()
    bill_window.title("Bill")
    order_label = Label(bill_window, text="Order: " + TEN)
    order_label.pack()
    customer_label = Label(bill_window, text="Customer: " + a)
    customer_label.pack()
    #################################
    # Lưu trữ MASP đã được hiển thị #
    #################################
    displayed_masp = set()
    for i in results:
        MADH = i[1]
        MASP = i[2]
        SL = int(i[3])
        GIA = int(i[4])
        ###############################################
        # Kiểm tra xem MASP đã được hiển thị hay chưa #
        ###############################################
        if MASP not in displayed_masp:
            price_label = Label(bill_window, text="Price: " + str(gia_dict[MADH + "-" + MASP]))
            price_label.pack()
            displayed_masp.add(MASP)
        quantity_label = Label(bill_window, text="Quantity for MASP " + MASP + ": " + str(SL))
        quantity_label.pack()
    conn.close()
###################
# Thêm khách hàng #
###################
def AddCustomer():
    ########################
    # Xoá và trang trí lại #
    ########################
    for widget in root.winfo_children():
        widget.destroy()
    root.title("ADD CUSTOMER")
    root.geometry(f"{width}x{height}")
    canvas_frame = ttk.Frame(root)
    canvas_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    background_image_path = "background/Customer.png"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((width, height))
    photo = ImageTk.PhotoImage(background_image)
    canvas = Canvas(canvas_frame, width=width, height=height)
    canvas.create_image(0, 0, image=photo, anchor=NW)
    canvas.pack()
    for i in range(10):
        root.grid_columnconfigure(i, weight=1)
    for i in range(7):
        root.grid_rowconfigure(i, weight=1)
    title_font = font.Font(family="Tahoma", size=35, weight="bold")
    Name_Label = Label(root, text="ADD PRODUCT", font=title_font, fg="red")
    Name_Label.config(relief=RAISED, bd=5)
    Name_Label.grid(column=4,row=0,columnspan=2)
    normal_font = font.Font(family="Arial", size=20, weight="bold")
    frame = Frame(root, relief=RAISED, bd=3)
    frame.grid(column=3, row=2, columnspan=4, padx=10, pady=50, rowspan=2)  
    MANV_LABEL = Label(frame, text="CUSTOMER ID:",font=normal_font)
    MANV_LABEL.grid(column=0, row=0, padx=20, pady=10,sticky=W)
    MANV_ENTRY = Entry(frame,width=20)
    MANV_ENTRY.grid(column=1, row=0, padx=20, pady=10)
    TENNV_LABEL = Label(frame, text="CUSTOMER NAME:",font=normal_font)
    TENNV_LABEL.grid(column=0, row=1, padx=20, pady=20,sticky=W)
    TENNV_ENTRY = Entry(frame,width=20)
    TENNV_ENTRY.grid(column=1, row=1, padx=20, pady=20)
    CV_LABEL = Label(frame, text="PHONE NUMBER:", font=normal_font)
    CV_LABEL.grid(column=0,row=2,padx=20,pady=20,sticky=W)
    CV_ENTRY = Entry(frame,width=20)
    CV_ENTRY.grid(column=1,row=2,padx=20,pady=20)
    A_LABEL = Label(frame, text="ADDRESS:", font=normal_font)
    A_LABEL.grid(column=0,row=5,padx=20,pady=20,sticky=W)
    A_ENTRY = Entry(frame,width=20)
    A_ENTRY.grid(column=1,row=5,padx=20,pady=20)
    T_LABEL = Label(frame, text="PURCHASE:", font=normal_font)
    T_LABEL.grid(column=0,row=6,padx=20,pady=20,sticky=W)
    T_ENTRY = Entry(frame,width=20)
    T_ENTRY.grid(column=1,row=6,padx=20,pady=20)
    ##################
    # Chức năng thêm #
    ##################
    login_button = Button(frame, text="ADD",font=('Arial',16,'bold'),command=lambda: AddC(MANV_ENTRY,TENNV_ENTRY,CV_ENTRY,A_ENTRY,T_ENTRY))
    login_button.grid(column=0, row=7, columnspan=2, padx=10, pady=10,sticky=W)
    back_button = Button(frame, text="BACK",font=('Arial',16,'bold'),command=OrderDisplay)
    back_button.grid(column=2, row=7, columnspan=2, padx=10, pady=10)
    root.mainloop()
##################
# Chức năng thêm #
##################
def AddC(MANV,TENNV,CV,A,T):
    Ma = MANV.get()
    Ten = TENNV.get()
    cv = CV.get()
    a = A.get()
    t = T.get()
    connection = sqlite3.connect("Shop.db")
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO CUSTOMER VALUES ('{Ma}','{Ten}','{cv}','{a}','{t}')")
    connection.commit()
    connection.close()
    messagebox.showinfo("NOTICE", "SUCCESSFULLY")
    MANV.delete(0, 'end')
    TENNV.delete(0, 'end') 
    CV.delete(0,'end')
    A.delete(0, 'end')
    T.delete(0,'end')
###################################
#############main##################
###################################
root = Tk()
canvas = Canvas( width=width, height=height)
image = Image.open("background/pet.png")
resize_image = image.resize((width,height))
photo = ImageTk.PhotoImage(resize_image)
canvas.create_image(0, 0, image=photo, anchor=NW)
canvas.place(x=0, y=0)
show_login_interface()
root.mainloop()