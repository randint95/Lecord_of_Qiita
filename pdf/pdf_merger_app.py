import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from pypdf import PdfWriter

# --- メインウィンドウ ---
root = tk.Tk()
root.title("PDF結合アプリ")
root.geometry("600x600")

# 同意常体の保持
agreement_var = tk.BooleanVar()
agreement_var.set(False) # 初期状態はオフ

# --- 説明ラベル ---
description_text = "本アプリは作者本人による使用のみを想定したPDFを結合するだけのwindows11専用のアプリです。\n本アプリは配布を想定していないため、作者は本アプリの想定された挙動を保証・保障できません。\nデバッグ等も行っていません。\n本アプリの使用により生じたいかなる損害・結果について、作者は一切の責任を負いません。\n以上を十分に理解し、本アプリの使用により生じたいかなる損害・結果について、\n自身で一切の責任を負う方のみ本アプリを使用してください。\n\n技術情報-本アプリは以下のオープンソース・ソフトウェアを利用して作成されました。\nPython (https://www.python.org/)\npypdf (https://pypdf.readthedocs.io/)\nPyInstaller (https://www.pyinstaller.org/)\n※URLは本アプリ作成時にアクセスできるURLです。\n\n使用方法\n1. [PDFを追加]でファイルを選択\n2. [▲▼]で順番を調整\n3. [すべてを結合]で名前を設定して保存"
description_label = tk.Label(root, text=description_text, justify="left")
description_label.pack(pady=10, padx=10, anchor="w")

# --- GUIのフレーム設定 ---
top_frame = tk.Frame(root)
top_frame.pack(pady=5, padx=10, fill="both", expand=True)
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

# --- ウィジェットの作成 ---
listbox = Listbox(top_frame, selectmode=tk.SINGLE)
listbox.pack(side="left", fill="both", expand=True)
scrollbar = tk.Scrollbar(top_frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)

# --- 関数の定義 ---
def add_files():
    filepaths = filedialog.askopenfilenames(filetypes=[("PDFファイル", "*.pdf")])
    for path in filepaths:
        listbox.insert(tk.END, path)

def remove_selected():
    selected_indices = listbox.curselection()
    if not selected_indices: return
    for i in reversed(selected_indices):
        listbox.delete(i)

def move_up():
    selected_indices = listbox.curselection()
    if not selected_indices: return
    idx = selected_indices[0]
    if idx > 0:
        text = listbox.get(idx)
        listbox.delete(idx)
        listbox.insert(idx - 1, text)
        listbox.selection_set(idx - 1)

def move_down():
    selected_indices = listbox.curselection()
    if not selected_indices: return
    idx = selected_indices[0]
    if idx < listbox.size() - 1:
        text = listbox.get(idx)
        listbox.delete(idx)
        listbox.insert(idx + 1, text)
        listbox.selection_set(idx + 1)
        
def merge_all():
    # 同意チェックを確認するロジック
    if not agreement_var.get():
        messagebox.showwarning("同意が必要です", "免責事項に同意の上、チェックボックスにチェックを入れてください。")
        return # 同意されていなければ処理を中断

    pdf_list = listbox.get(0, tk.END)
    if not pdf_list:
        messagebox.showwarning("注意", "結合するPDFがありません。")
        return
        
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDFファイル", "*.pdf")])
    if not save_path:
        return

    try:
        merger = PdfWriter()
        for pdf_path in pdf_list:
            merger.append(pdf_path)
        merger.write(save_path)
        merger.close()
        messagebox.showinfo("成功", f"PDFの結合が完了しました。\n{save_path} に保存されました。")
    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")

# --- ボタンの作成と配置 ---
add_btn = tk.Button(bottom_frame, text="PDFを追加", command=add_files)
add_btn.grid(row=0, column=0, padx=5, pady=5)

remove_btn = tk.Button(bottom_frame, text="選択を削除", command=remove_selected)
remove_btn.grid(row=0, column=1, padx=5, pady=5)

up_btn = tk.Button(bottom_frame, text="▲ 上へ", command=move_up)
up_btn.grid(row=0, column=2, padx=5, pady=5)

down_btn = tk.Button(bottom_frame, text="▼ 下へ", command=move_down)
down_btn.grid(row=0, column=3, padx=5, pady=5)

# 免責事項とチェックボックスを配置
disclaimer_label = tk.Label(bottom_frame, text="本アプリの使用により生じたいかなる損害についても、作者は一切の責任を負いません。", fg="red")
disclaimer_label.grid(row=1, column=0, columnspan=4, padx=5, pady=(10, 0))

agreement_check = tk.Checkbutton(bottom_frame, text="上記に同意する", variable=agreement_var)
agreement_check.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

# 結合ボタンの配置行を変更
merge_btn = tk.Button(bottom_frame, text="すべてを結合", command=merge_all, bg="lightblue")
merge_btn.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

# --- GUIループを開始 ---
root.mainloop()
