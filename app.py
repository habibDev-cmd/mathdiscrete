import streamlit as st

from chat_agent import answer_question


st.set_page_config(page_title="Diskrit Lab", page_icon="∴", layout="wide")
st.markdown(
    """
    <style>
    :root { --ink: #182b2b; --muted: #617675; --paper: #f5f8f3; --teal: #087e78; --coral: #e66c4f; }
    .stApp { background: radial-gradient(ellipse at 8% 0%, #e1f2e9 0, transparent 38%), linear-gradient(135deg, #f7f8f2, #eef4f0); color: var(--ink); }
    [data-testid="stSidebar"] { background: #163a39; }
    [data-testid="stSidebar"] * { color: #f2f6ee; }
    .main .block-container { max-width: 920px; padding-top: 2.3rem; padding-bottom: 7rem; }
    .brand { font: 700 2.25rem Georgia, serif; color: var(--ink); margin: .15rem 0 0; }
    .dek { color: var(--muted); font-size: 1rem; margin: .1rem 0 1.1rem; }
    .eyebrow { color: var(--coral); text-transform: uppercase; font-size: .72rem; font-weight: 800; letter-spacing: .12em; }
    [data-testid="stChatMessage"] { border: 1px solid rgba(22,58,57,.09); border-radius: 8px; background: rgba(255,255,255,.74); }
    [data-testid="stChatInput"] { border-color: rgba(8,126,120,.42); }
    div.stButton > button { border-radius: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": "Halo! Kirim soal matematika diskrit, dan saya akan memilih solver yang sesuai.\n\n"
            "Saya bisa menghitung tabel kebenaran, operasi himpunan, kombinasi/permutasi, "
            "graf sederhana, dan sifat relasi. Untuk jenis lain, saya akan bilang jika belum didukung.",
            "table": None,
        }
    ]


def submit_question(question: str) -> None:
    st.session_state.chat_messages.append({"role": "user", "text": question})
    st.session_state.chat_messages.append({"role": "assistant", **answer_question(question)})


with st.sidebar:
    st.markdown("<div style='font:700 1.5rem Georgia,serif'>Diskrit Lab <span style='color:#ff9b77'>∴</span></div>", unsafe_allow_html=True)
    st.caption("Chat agent matematika diskrit")
    st.divider()
    if st.button("＋  Percakapan baru", use_container_width=True):
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "text": "Percakapan baru dimulai. Tanyakan soal matematika diskrit yang ingin kamu hitung.",
                "table": None,
            }
        ]
        st.rerun()
    st.markdown("#### Kemampuan")
    st.markdown("Logika proposisional  \nHimpunan  \nKombinatorika  \nGraf sederhana  \nRelasi hingga")
    st.divider()
    st.caption("Agent lokal berbasis aturan · tidak memakai LLM/API")

st.markdown("<div class='eyebrow'>Tutor diskrit · mode percakapan</div>", unsafe_allow_html=True)
st.markdown("<h1 class='brand'>Diskrit Lab</h1>", unsafe_allow_html=True)
st.markdown("<p class='dek'>Tanyakan soalnya. Saya hitung dengan solver yang bisa diverifikasi.</p>", unsafe_allow_html=True)

if len(st.session_state.chat_messages) == 1:
    st.caption("Coba salah satu contoh")
    examples = [
        "Tabel kebenaran p and not p",
        "Berapa cara memilih 3 dari 8?",
        "Operasi himpunan A={1,2}, B={2,3}",
        "Analisis graf simpul: A, B, C sisi: A-B; B-C",
        "Periksa relasi domain: a, b relasi: (a,a); (b,b); (a,b); (b,a)",
    ]
    columns = st.columns(2)
    selected_example = None
    for index, example in enumerate(examples):
        if columns[index % 2].button(example, use_container_width=True):
            selected_example = example
    if selected_example:
        submit_question(selected_example)
        st.rerun()

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])
        if message.get("table"):
            st.dataframe(message["table"], hide_index=True, use_container_width=True)

if question := st.chat_input("Tulis soal matematika diskrit…"):
    submit_question(question)
    st.rerun()

st.divider()
st.caption("Hasil hanya berlaku untuk format soal yang dikenali. Agent akan menyatakan jika soal belum didukung.")