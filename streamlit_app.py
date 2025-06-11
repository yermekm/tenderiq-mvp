import streamlit as st
import pandas as pd

st.set_page_config(page_title="TenderIQ MVP", layout="wide")

# ────────────────────────────────────────────────────────────
# Заголовок и описание
# ────────────────────────────────────────────────────────────
st.title("TenderIQ — демо-анализ тендеров")
st.markdown(
    """
    **Как пользоваться:**
    1. Загрузите CSV-файл с выгрузкой тендеров *(Goszakup export)*  
       — или вставьте ссылку на карточку тендера (пока заглушка).  
    2. Нажмите **Анализировать** — система присвоит упрощённый Risk Score.  
    3. Скачайте результат как CSV или посмотрите таблицу на экране.
    """
)

# ────────────────────────────────────────────────────────────
# Загрузка данных
# ────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Загрузите CSV", type=["csv"])
url = st.text_input("URL тендера (опционально)")

# ────────────────────────────────────────────────────────────
# Упрощённая логика скоринга для MVP
# ────────────────────────────────────────────────────────────
def dummy_score(row: pd.Series) -> int:
    """Простейший расчёт риска для демонстрации."""
    risk = 0
    # примерные правила
    if "конкурс" in str(row.get("proc_method", "")).lower():
        risk -= 10        # конкурс = меньше риска
    if row.get("single_source", False):
        risk += 30        # единственный источник
    try:
        price = float(row.get("price", 0))
        if price > 1_000_000_000:
            risk += 20    # большие суммы — выше риск
    except ValueError:
        pass
    return max(0, min(100, 50 + risk))

# ────────────────────────────────────────────────────────────
# Обработка
# ────────────────────────────────────────────────────────────
if uploaded:
    df = pd.read_csv(uploaded)
    st.write("### Предпросмотр данных", df.head())

    df["RiskScore"] = df.apply(dummy_score, axis=1)
    st.write("### Результат с упрощённым Risk Score", df)

    csv_out = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Скачать результат CSV",
        data=csv_out,
        file_name="tenderiq_scored.csv",
        mime="text/csv",
    )

elif url:
    st.info("Парсинг URL будет добавлен на следующем этапе 😉")
    st.write(f"Введённый URL: **{url}**")

else:
    st.warning("Загрузите CSV или введите URL для анализа.")
