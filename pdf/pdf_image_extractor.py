import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText # ScrolledTextをインポート
import fitz  # PyMuPDFライブラリ
import os
import threading

# --- コア機能 ---

def extract_images_from_pdf(pdf_path, output_dir, progress_var, status_label, window):
    """
    PDFから画像を抽出するメインの処理。
    時間がかかる可能性があるため、別スレッドで実行される。
    """
    try:
        # ステータスを更新
        status_label.config(text="処理中: PDFファイルを開いています...")
        
        doc = fitz.open(pdf_path)
        total_images = 0
        
        # まずPDF全体の画像数を数える（プログレスバーのため）
        for page in doc:
            total_images += len(page.get_images(full=True))

        if total_images == 0:
            status_label.config(text="完了: 画像は見つかりませんでした。")
            messagebox.showinfo("完了", "このPDFには抽出可能な画像が含まれていませんでした。")
            window.after(100, lambda: progress_var.set(0)) # 処理後にプログレスバーをリセット
            return

        progress_var.set(0) # プログレスバーをリセット
        extracted_count = 0

        # 各ページから画像を抽出
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images(full=True)
            
            if not image_list:
                continue

            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]  # 画像の参照番号
                
                # 画像データを抽出
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # 画像をファイルとして保存
                image_filename = f"image_p{page_num + 1}_{image_index}.{image_ext}"
                image_path = os.path.join(output_dir, image_filename)
                
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                
                extracted_count += 1
                
                # プログレスバーとステータスを更新
                progress_value = (extracted_count / total_images) * 100
                status_text = f"処理中: {extracted_count}/{total_images} 個の画像を抽出中..."
                
                # GUIの更新はメインスレッドで行う
                window.after(0, lambda p=progress_value, s=status_text: (progress_var.set(p), status_label.config(text=s)))

        doc.close()
        
        # 完了メッセージ
        final_message = f"完了: {extracted_count} 個の画像を '{output_dir}' に保存しました。"
        status_label.config(text=final_message)
        messagebox.showinfo("抽出完了", final_message)

    except Exception as e:
        error_message = f"エラーが発生しました: {e}"
        status_label.config(text="エラー")
        messagebox.showerror("エラー", error_message)
    finally:
        # 処理完了後、ボタンを再度有効化する（チェックボックスがONの場合のみ）
        window.after(10, toggle_button_state)


# --- GUI関連の関数 ---

def start_extraction_thread():
    """
    抽出処理を別スレッドで開始するためのラッパー関数。
    """
    pdf_path = pdf_path_entry.get()
    output_dir = output_path_entry.get()

    # 入力チェック
    if not pdf_path or not os.path.exists(pdf_path):
        messagebox.showerror("エラー", "有効なPDFファイルを選択してください。")
        return
    if not output_dir or not os.path.isdir(output_dir):
        messagebox.showerror("エラー", "有効な保存先フォルダを選択してください。")
        return

    # 処理中はボタンを無効化
    extract_button.config(state="disabled")

    # スレッドを作成して処理を開始
    thread = threading.Thread(
        target=extract_images_from_pdf,
        args=(pdf_path, output_dir, progress, status_label, app),
        daemon=True
    )
    thread.start()


def select_pdf_file():
    """PDFファイル選択ダイアログを開く"""
    file_path = filedialog.askopenfilename(
        title="PDFファイルを選択",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if file_path:
        pdf_path_entry.delete(0, tk.END)
        pdf_path_entry.insert(0, file_path)

def select_output_dir():
    """保存先フォルダ選択ダイアログを開く"""
    dir_path = filedialog.askdirectory(title="保存先フォルダを選択")
    if dir_path:
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, dir_path)

def toggle_button_state():
    """チェックボックスの状態に応じてボタンの有効/無効を切り替える"""
    if agree_var.get():
        extract_button.config(state="normal")
    else:
        extract_button.config(state="disabled")

# --- GUIのセットアップ ---

# メインウィンドウ
app = ttk.Window(themename="litera")
app.title("PDF画像抽出ツール")
app.geometry("600x600") # ウィンドウの高さを調整

main_frame = ttk.Frame(app, padding=20)
main_frame.pack(fill=BOTH, expand=YES)

# --- 入力フィールド ---
# PDFファイル選択
pdf_frame = ttk.Frame(main_frame)
pdf_frame.pack(fill=X, pady=5)

pdf_label = ttk.Label(pdf_frame, text="PDFファイル:", width=12)
pdf_label.pack(side=LEFT, padx=(0, 10))

pdf_path_entry = ttk.Entry(pdf_frame)
pdf_path_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))

pdf_button = ttk.Button(pdf_frame, text="選択...", command=select_pdf_file, bootstyle=SECONDARY)
pdf_button.pack(side=LEFT)

# 保存先フォルダ選択
output_frame = ttk.Frame(main_frame)
output_frame.pack(fill=X, pady=5)

output_label = ttk.Label(output_frame, text="保存先フォルダ:", width=12)
output_label.pack(side=LEFT, padx=(0, 10))

output_path_entry = ttk.Entry(output_frame)
output_path_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))

output_button = ttk.Button(output_frame, text="選択...", command=select_output_dir, bootstyle=SECONDARY)
output_button.pack(side=LEFT)

# --- 免責事項と同意チェック ---
separator = ttk.Separator(main_frame, orient=HORIZONTAL)
separator.pack(fill=X, pady=15)

# スクロール可能なテキストエリアで免責事項を表示
disclaimer_text_content = """免責事項や使用時の注意点が記載されているため、スクロールして最後までお読みください。
【免責事項・利用規約】
本アプリは作者本人による使用のみを想定した、PDFから画像を抽出するWindows11専用のアプリです。
本アプリは配布を想定していないため、作者は本アプリの想定された挙動を保証・保障できません。
デバッグ等も行っていません。
本アプリの使用により生じたいかなる損害・結果について、作者は一切の責任を負いません。
以上を十分に理解し、本アプリの使用により生じたいかなる損害・結果について、自身で一切の責任を負う方のみ本アプリを使用してください。

【技術情報】
本アプリは以下のオープンソース・ソフトウェアを利用して作成されました。
- Python (https://www.python.org/)
- PyMuPDF (https://pymupdf.readthedocs.io/)
- ttkbootstrap (https://ttkbootstrap.readthedocs.io/)
- PyInstaller (https://www.pyinstaller.org/)
※URLは本アプリ作成時にアクセスできるものです。

【使用方法】
1. [選択...] ボタンで画像を取り出したいPDFファイルを選択します。
2. [選択...] ボタンで抽出した画像の保存先フォルダを選択します。
3. 下のチェックボックスにチェックを入れ、規約に同意します。
4. [画像抽出を開始] ボタンを押して処理を実行します。

【使用時の注意点】
1. 抽出できない画像があります。（場合によってはPDF内から1つも抽出されません。）
2. 選択したPDF内の抽出可能なすべての画像を抽出します。（空き容量や出力場所に注意してください。）
"""
disclaimer_text = ScrolledText(main_frame, height=10, padding=5, autohide=True)
disclaimer_text.insert(tk.END, disclaimer_text_content)
# ScrolledTextウィジェット内のTextウィジェットに直接アクセスしてstateを変更します
disclaimer_text.text.config(state="disabled") 
disclaimer_text.pack(fill=X, expand=NO, pady=(0, 10))

# 同意チェックボックス
agree_var = tk.BooleanVar()
agree_check = ttk.Checkbutton(
    main_frame,
    variable=agree_var,
    text="上記の内容をすべて理解し、同意します。",
    bootstyle="primary",
    command=toggle_button_state
)
agree_check.pack(anchor='w', pady=(0, 15))


# --- 実行ボタンとステータス表示 ---
# 抽出実行ボタン
extract_button = ttk.Button(
    main_frame,
    text="画像抽出を開始",
    command=start_extraction_thread,
    bootstyle=(PRIMARY, OUTLINE),
    state="disabled" # 初期状態は無効
)
extract_button.pack(pady=(0, 10), fill=X)

# プログレスバー
progress = tk.DoubleVar()
progress_bar = ttk.Progressbar(main_frame, variable=progress, maximum=100)
progress_bar.pack(fill=X, pady=5)

# ステータスラベル
status_label = ttk.Label(main_frame, text="免責事項に同意してください。")
status_label.pack(fill=X, pady=(5, 0))


# アプリケーションの実行
if __name__ == "__main__":
    app.mainloop()
