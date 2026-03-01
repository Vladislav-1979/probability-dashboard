import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="🧪 Вероятностный Калькулятор", layout="wide", page_icon="🎲")
st.title("🧮 Калькулятор Вероятностей Событий")
st.markdown("**Исследуй случайность на практике!** 6 крутых экспериментов с симуляциями и теорией")

st.sidebar.title("Выбери эксперимент")
experiment = st.sidebar.radio(
    "Эксперимент",
    [
        "1. Парадокс дней рождения",
        "2. Проблема Монти Холла",
        "3. Метод Монте-Карло (оценка π)",
        "4. Байесовский тест на болезнь",
        "5. Разорение игрока",
        "6. Марковская цепь — погода",
        "О проекте"
    ]
)

# 1. Парадокс дней рождения
if experiment == "1. Парадокс дней рождения":
    st.header("🎂 Парадокс дней рождения")
    col1, col2 = st.columns([1, 2])
    with col1:
        n_people = st.slider("Количество людей", 2, 100, 23)
        n_sim = st.slider("Симуляций", 1000, 50000, 10000, 1000)
        if st.button("Запустить", type="primary"):
            birthdays = np.random.randint(1, 365, size=(n_sim, n_people))
            has_match = np.array([len(np.unique(row)) < len(row) for row in birthdays])
            prob_sim = has_match.mean()
            prob_theory = 1 - np.prod(1 - np.arange(1, n_people) / 365)
            st.success(f"Симуляция: **{prob_sim:.1%}** | Теория: **{prob_theory:.1%}**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[n_people], y=[prob_sim], mode='markers', name='Симуляция', marker=dict(size=15, color='red')))
            fig.add_trace(go.Scatter(x=list(range(2,81)), y=[1 - np.prod(1 - np.arange(1,k)/365) for k in range(2,81)], mode='lines', name='Теория'))
            fig.update_layout(title="Вероятность совпадения дней рождения", xaxis_title="Люди", yaxis_title="Вероятность")
            st.plotly_chart(fig, use_container_width=True)

# 2. Монти Холл
elif experiment == "2. Проблема Монти Холла":
    st.header("🚪 Проблема Монти Холла")
    col1, col2 = st.columns([1, 2])
    with col1:
        n_games = st.slider("Игр", 1000, 100000, 10000, 1000)
        strategy = st.radio("Стратегия", ["Менять дверь", "Оставаться"])
        if st.button("Запустить", type="primary"):
            wins = 0
            for _ in range(n_games):
                doors = [0,0,1]; np.random.shuffle(doors)
                choice = np.random.randint(0,3)
                monty = next(i for i in range(3) if i != choice and doors[i]==0)
                if strategy == "Менять дверь":
                    new = next(i for i in range(3) if i != choice and i != monty)
                    if doors[new] == 1: wins += 1
                else:
                    if doors[choice] == 1: wins += 1
            prob = wins / n_games
            st.success(f"Выигрыш: **{prob:.1%}**")
            st.info("Теория: менять = 66.7%, оставаться = 33.3%")

# 3. Монте-Карло π
elif experiment == "3. Метод Монте-Карло (оценка π)":
    st.header("🎯 Монте-Карло: считаем π")
    n_points = st.slider("Точек", 100, 20000, 5000, 100)
    if st.button("Запустить", type="primary"):
        x = np.random.uniform(-1, 1, n_points)
        y = np.random.uniform(-1, 1, n_points)
        inside = (x**2 + y**2) <= 1
        pi_est = 4 * np.sum(inside) / n_points
        st.success(f"Оценка π: **{pi_est:.4f}** (настоящее 3.1416)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x[inside], y=y[inside], mode='markers', marker=dict(color='green', size=3), name='Внутри круга'))
        fig.add_trace(go.Scatter(x=x[~inside], y=y[~inside], mode='markers', marker=dict(color='red', size=3), name='Снаружи'))
        fig.update_layout(title=f"Монте-Карло π ({n_points} точек)", xaxis_range=[-1,1], yaxis_range=[-1,1], width=700, height=700)
        st.plotly_chart(fig, use_container_width=True)

# 4. Байесовский тест
elif experiment == "4. Байесовский тест на болезнь":
    st.header("🦠 Байес: тест на болезнь")
    prevalence = st.slider("Распространённость болезни (%)", 0.1, 20.0, 1.0) / 100
    sensitivity = st.slider("Чувствительность теста (%)", 70, 100, 95) / 100
    specificity = st.slider("Специфичность теста (%)", 70, 100, 95) / 100
    if st.button("Рассчитать", type="primary"):
        prior = prevalence
        likelihood_pos = sensitivity
        false_pos = 1 - specificity
        posterior = (likelihood_pos * prior) / (likelihood_pos * prior + false_pos * (1 - prior))
        st.success(f"Вероятность болезни после положительного теста: **{posterior:.1%}**")
        st.info("Интуиция обманывает! Даже при хорошем тесте результат часто ложноположительный.")

# 5. Разорение игрока
elif experiment == "5. Разорение игрока":
    st.header("💰 Разорение игрока (Gambler’s Ruin)")
    capital = st.slider("Твой стартовый капитал", 10, 100, 50)
    total = st.slider("Капитал казино", 50, 500, 200)
    p_win = st.slider("Вероятность выиграть раунд (%)", 40, 60, 49) / 100
    if st.button("Симулировать 1000 игр", type="primary"):
        ruins = 0
        for _ in range(1000):
            money = capital
            while 0 < money < total:
                money += 1 if np.random.random() < p_win else -1
            if money == 0: ruins += 1
        prob_ruin = ruins / 1000
        st.success(f"Вероятность разорения: **{prob_ruin:.1%}**")
        st.info("При p < 50% ты почти всегда разоришься со временем!")

# 6. Марковская цепь — погода
elif experiment == "6. Марковская цепь — погода":
    st.header("☀️ Погода завтра (Марковская цепь)")
    today = st.selectbox("Сегодня", ["Солнечно", "Дождливо"])
    if st.button("Симулировать 30 дней", type="primary"):
        states = ["Солнечно", "Дождливо"]
        trans = [[0.8, 0.2], [0.3, 0.7]]  # Солнечно → Солнечно/Дождь
        current = 0 if today == "Солнечно" else 1
        days = [states[current]]
        for _ in range(29):
            current = np.random.choice([0,1], p=trans[current])
            days.append(states[current])
        sunny_days = days.count("Солнечно")
        st.success(f"За 30 дней солнечно было {sunny_days} раз ({sunny_days/30:.1%})")
        st.line_chart([1 if d=="Солнечно" else 0 for d in days])

else:
    st.header("О проекте")
    st.markdown("""
    **Готово!** У тебя теперь полноценный интерактивный дашборд.
    - Сравнение симуляций и теории
    - Красивые графики Plotly
    - Можно добавлять свои эксперименты
    
    **Дальше:**
    - Сохрани код (Ctrl+S)
    - Закрой Блокнот
    - В PowerShell выполни: `streamlit run app.py`
    """)
    st.balloons()

st.caption("Сделано специально для тебя в Киеве | 2026 🚀")