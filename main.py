import streamlit as st
from PIL import Image
import io
import base64


def convert_heic_to_jpeg(heic_bytes):
    try:
        with Image.open(io.BytesIO(heic_bytes)) as img:
            if img.format == "HEIF":
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # サイズを半分にする
                width, height = img.size
                new_width = width // 2
                new_height = height // 2
                img = img.resize((new_width, new_height))

                # Exif情報を取得
                exif_data = img.info.get('exif')
                jpeg_bytes = io.BytesIO()
                img.save(jpeg_bytes, format='JPEG', exif=exif_data)
                return jpeg_bytes.getvalue()
            else:
                st.error("Uploaded file is not in HEIC format.")
                return None
    except Exception as e:
        st.error("Error occurred while processing the image:"+str(e))
        return None


def main():
    st.title("HEIC to JPEG Converter")

    # HEICファイルをアップロード
    st.header("Upload HEIC Images")
    heic_files = st.file_uploader(
        "Choose multiple HEIC images", type="heic", accept_multiple_files=True)

    # if heic_files is not None:
    if len(heic_files) != 0:
        for idx, heic_file in enumerate(heic_files):
            # 変換ボタン
            if st.button(f"Convert {heic_file.name} to JPEG", key=f"convert_button_{idx}"):
                jpeg_bytes = convert_heic_to_jpeg(heic_file.read())
                # jpeg_bytes = convert_heic_to_jpeg(str(f'{heic_file.name}'))

                # JPEG画像の表示
                st.image(jpeg_bytes, use_column_width=True,
                         output_format='JPEG'
                         )

                # JPEG画像のダウンロードリンク
                st.markdown(get_binary_file_downloader_html(
                    jpeg_bytes, heic_file.name.split(".")[0] + ".jpg"), unsafe_allow_html=True)


def get_binary_file_downloader_html(bin_data, file_label='File', button_label='Download'):
    bin_str = io.BytesIO(bin_data).read()
    # base64モジュールのb64encode関数を使用
    data_url = f"data:application/octet-stream;base64,{base64.b64encode(bin_str).decode()}"
    return f'<a href="{data_url}" download="converted_image.jpg">{button_label}</a>'


if __name__ == "__main__":
    main()
