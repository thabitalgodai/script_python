# -*- coding: utf-8 -*-
import streamlit as st
import subprocess, os, tempfile
from pathlib import Path

# 1. إعدادات واجهة التطبيق
st.set_page_config(page_title="Vocal Remover - هاتفك", page_icon="🎤")
st.title("🎤 إزالة صوت الفنان")
st.markdown("ارفع ملف فيديو أو صوت، وسأقوم بإزالة الغناء أو الكلام منه.")

# 2. خيار رفع الملف
uploaded_file = st.file_uploader("اختر الملف", type=['mp4', 'avi', 'mov', 'mp3', 'wav'])

# 3. خيارات المعالجة
output_type = st.radio("نوع المخرج:", ["🎵 صوت فقط (MP3)", "🎬 فيديو (MP4)"])

# 4. زر التشغيل
if st.button("ابدأ المعالجة 🚀"):
    if uploaded_file is None:
        st.error("الرجاء رفع ملف أولاً")
    else:
        with st.spinner('جاري المعالجة... قد تستغرق دقيقة'):
            # حفظ الملف المؤقت
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                input_file = tmp.name

            # تشغيل أمر الفصل (نفس الكود القديم)
            os.system(f'demucs --two-stems=vocals "{input_file}"')
            base_name = Path(input_file).stem
            music_file = f"separated/htdemucs/{base_name}/no_vocals.wav"

            # تجهيز المخرج
            if output_type == "🎵 صوت فقط (MP3)":
                output_file = "output.mp3"
                os.system(f'ffmpeg -i "{music_file}" -b:a 192k -y "{output_file}"')
                with open(output_file, "rb") as f:
                    st.audio(f, format='audio/mp3')
                    st.download_button("تحميل الملف", f, file_name=output_file)
            else:
                output_file = "output.mp4"
                os.system(f'ffmpeg -i "{input_file}" -i "{music_file}" -c:v copy -map 0:v:0 -map 1:a:0 -shortest -y "{output_file}"')
                with open(output_file, "rb") as f:
                    st.video(f)
                    st.download_button("تحميل الفيديو", f, file_name=output_file)

            # تنظيف
            os.system("rm -rf separated")
