import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from math import comb

# ====================== ПЕРЕКЛЮЧАТЕЛЬ ЯЗЫКА ======================
if "lang" not in st.session_state:
    st.session_state.lang = "Русский"

lang = st.sidebar.selectbox("🌍 Язык / Language", ["Русский", "English"], 
                            index=0 if st.session_state.lang == "Русский" else 1)
st.session_state.lang = lang
is_ru = lang == "Русский"

# ====================== ТЕКСТЫ ======================
title = "🧮 Калькулятор вероятностей событий" if is_ru else "🧮 Probability Events Calculator"
desc = "**Исследуй случайность на практике!** Симуляции + теория + красивые графики" if is_ru else "**Explore randomness in practice!** Simulations + Theory + Beautiful graphs"
sidebar_label = "Выбери эксперимент" if is_ru else "Choose Experiment"

experiments = [
    "1. Парадокс дней рождения" if is_ru else "1. Birthday Paradox",
    "2. Проблема Монти Холла" if is_ru else "2. Monty Hall Problem",
    "3. Метод Монте-Карло (π)" if is_ru else "3. Monte Carlo Pi Estimation",
    "4. Байесовский тест на болезнь" if is_ru else "4. Bayesian Disease Test",
    "5. Разорение игрока" if is_ru else "5. Gambler's Ruin",
    "6. Марковская цепь — погода" if is_ru else "6. Markov Chain Weather",
    "7. Закон больших чисел (монетка)" if is_ru else "7. Law of Large Numbers (Coin Flips)",
    "8. Симулятор лотереи 6 из 36" if is_ru else "8. Lottery 6/36 Simulator",
    "О проекте" if is_ru else "About the Project"
]

st.set_page_config(page_title="Probability Calculator", layout="wide", page_icon="🎲")
st.title(title)
st.markdown(desc)

experiment = st.sidebar.radio(sidebar_label, experiments)

# ====================== 1. ПАРАДОКС ДНЕЙ РОЖДЕНИЯ ======================
if experiment.startswith("1."):
    st.header("🎂 Парадокс дней рождения" if is_ru else "🎂 Birthday Paradox")
    col1, col2 = st.columns([1, 2])
    with col1:
        n_people = st.slider("Количество людей" if is_ru else "Number of people", 2, 100, 23)
        n_sim = st.slider("Количество симуляций" if is_ru else "Number of simulations", 1000, 50000, 10000, 1000)
        if st.button("Запустить симуляцию" if is_ru else "Run Simulation", type="primary"):
            birthdays = np.random.randint(1, 365, size=(n_sim, n_people))
            has_match = np.array([len(np.unique(row)) < len(row) for row in birthdays])
            prob_sim = has_match.mean()
            prob_theory = 1 - np.prod(1 - np.arange(1, n_people) / 365)
            st.success(f"Симуляция: **{prob_sim:.1%}** | Теория: **{prob_theory:.1%}**" if is_ru else f"Simulation: **{prob_sim:.1%}** | Theory: **{prob_theory:.1%}**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[n_people], y=[prob_sim], mode='markers', name='Симуляция' if is_ru else 'Simulation', marker=dict(size=15, color='red')))
            fig.add_trace(go.Scatter(x=list(range(2,81)), y=[1 - np.prod(1 - np.arange(1,k)/365) for k in range(2,81)], mode='lines', name='Теория' if is_ru else 'Theory'))
            fig.update_layout(title="Вероятность совпадения дней рождения" if is_ru else "Probability of shared birthday", xaxis_title="Люди" if is_ru else "People", yaxis_title="Вероятность" if is_ru else "Probability")
            st.plotly_chart(fig, use_container_width=True)

# ====================== 2. МОНТИ ХОЛЛ ======================
elif experiment.startswith("2."):
    st.header("🚪 Проблема Монти Холла" if is_ru else "🚪 Monty Hall Problem")
    col1, col2 = st.columns([1, 2])
    with col1:
        n_games = st.slider("Количество игр" if is_ru else "Number of games", 1000, 100000, 10000, 1000)
        strategy = st.radio("Стратегия" if is_ru else "Strategy", ["Менять дверь", "Оставаться"] if is_ru else ["Switch door", "Stay"])
        if st.button("Запустить симуляцию" if is_ru else "Run Simulation", type="primary"):
            wins = 0
            for _ in range(n_games):
                doors = [0,0,1]; np.random.shuffle(doors)
                choice = np.random.randint(0,3)
                monty = next(i for i in range(3) if i != choice and doors[i]==0)
                if strategy == ("Менять дверь" if is_ru else "Switch door"):
                    new = next(i for i in range(3) if i != choice and i != monty)
                    if doors[new] == 1: wins += 1
                else:
                    if doors[choice] == 1: wins += 1
            prob = wins / n_games
            st.success(f"Вероятность выиграть: **{prob:.1%}**" if is_ru else f"Win probability: **{prob:.1%}**")
            st.info("Теория: менять = 66.7%, оставаться = 33.3%" if is_ru else "Theory: Switch = 66.7%, Stay = 33.3%")

# ====================== 3. МОНТЕ-КАРЛО π ======================
elif experiment.startswith("3."):
    st.header("🎯 Метод Монте-Карло (π)" if is_ru else "🎯 Monte Carlo: Estimating π")
    n_points = st.slider("Количество точек" if is_ru else "Number of points", 100, 20000, 5000, 100)
    if st.button("Запустить симуляцию" if is_ru else "Run Simulation", type="primary"):
        x = np.random.uniform(-1, 1, n_points)
        y = np.random.uniform(-1, 1, n_points)
        inside = (x**2 + y**2) <= 1
        pi_est = 4 * np.sum(inside) / n_points
        st.success(f"Оценка π: **{pi_est:.4f}**" if is_ru else f"Estimated π: **{pi_est:.4f}**")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x[inside], y=y[inside], mode='markers', marker=dict(color='green', size=3), name='Внутри' if is_ru else 'Inside'))
        fig.add_trace(go.Scatter(x=x[~inside], y=y[~inside], mode='markers', marker=dict(color='red', size=3), name='Снаружи' if is_ru else 'Outside'))
        fig.update_layout(title="Монте-Карло π" if is_ru else "Monte Carlo π", xaxis_range=[-1,1], yaxis_range=[-1,1])
        st.plotly_chart(fig, use_container_width=True)

# ====================== 4. БАЙЕС ======================
elif experiment.startswith("4."):
    st.header("🦠 Байесовский тест на болезнь" if is_ru else "🦠 Bayesian Disease Test")
    prevalence = st.slider("Распространённость болезни (%)" if is_ru else "Disease prevalence (%)", 0.1, 20.0, 1.0) / 100
    sensitivity = st.slider("Чувствительность теста (%)" if is_ru else "Test sensitivity (%)", 70, 100, 95) / 100
    specificity = st.slider("Специфичность теста (%)" if is_ru else "Test specificity (%)", 70, 100, 95) / 100
    if st.button("Рассчитать" if is_ru else "Calculate", type="primary"):
        prior = prevalence
        likelihood_pos = sensitivity
        false_pos = 1 - specificity
        posterior = (likelihood_pos * prior) / (likelihood_pos * prior + false_pos * (1 - prior))
        st.success(f"Вероятность болезни после положительного теста: **{posterior:.1%}**" if is_ru else f"Probability of disease after positive test: **{posterior:.1%}**")
        st.info("Интуиция обманывает!" if is_ru else "Intuition fails!")

# ====================== 5. РАЗОРЕНИЕ ======================
elif experiment.startswith("5."):
    st.header("💰 Разорение игрока" if is_ru else "💰 Gambler's Ruin")
    capital = st.slider("Твой стартовый капитал" if is_ru else "Your starting capital", 10, 100, 50)
    total = st.slider("Капитал казино" if is_ru else "Casino capital", 50, 500, 200)
    p_win = st.slider("Вероятность выиграть раунд (%)" if is_ru else "Win probability per round (%)", 40, 60, 49) / 100
    if st.button("Симулировать 1000 игр" if is_ru else "Simulate 1000 games", type="primary"):
        ruins = 0
        for _ in range(1000):
            money = capital
            while 0 < money < total:
                money += 1 if np.random.random() < p_win else -1
            if money == 0: ruins += 1
        prob_ruin = ruins / 1000
        st.success(f"Вероятность разорения: **{prob_ruin:.1%}**" if is_ru else f"Probability of ruin: **{prob_ruin:.1%}**")

# ====================== 6. МАРКОВ ======================
elif experiment.startswith("6."):
    st.header("☀️ Марковская цепь — погода" if is_ru else "☀️ Markov Chain Weather")
    today = st.selectbox("Сегодня" if is_ru else "Today", ["Солнечно", "Дождливо"] if is_ru else ["Sunny", "Rainy"])
    if st.button("Симулировать 30 дней" if is_ru else "Simulate 30 days", type="primary"):
        states = ["Солнечно", "Дождливо"] if is_ru else ["Sunny", "Rainy"]
        trans = [[0.8, 0.2], [0.3, 0.7]]
        current = 0 if today in ["Солнечно", "Sunny"] else 1
        days = [states[current]]
        for _ in range(29):
            current = np.random.choice([0,1], p=trans[current])
            days.append(states[current])
        sunny = days.count(states[0])
        st.success(f"Солнечно было {sunny} раз ({sunny/30:.1%})" if is_ru else f"Sunny: {sunny} times ({sunny/30:.1%})")
        st.line_chart([1 if d == states[0] else 0 for d in days])

# ====================== 7. ЗАКОН БОЛЬШИХ ЧИСЕЛ ======================
elif experiment.startswith("7."):
    st.header("📈 Закон больших чисел (монетка)" if is_ru else "📈 Law of Large Numbers (Coin Flips)")
    n_flips = st.slider("Количество бросков" if is_ru else "Number of coin flips", 10, 10000, 1000, 10)
    if st.button("Запустить симуляцию" if is_ru else "Run Simulation", type="primary"):
        flips = np.random.choice([0, 1], size=n_flips)
        cum_mean = np.cumsum(flips) / np.arange(1, n_flips + 1)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(1, n_flips+1)), y=cum_mean, mode='lines', name='Доля орлов' if is_ru else 'Proportion of heads'))
        fig.add_hline(y=0.5, line_dash="dash", line_color="red", annotation_text="50%" if is_ru else "50%")
        fig.update_layout(title="Сходимость к 50%" if is_ru else "Convergence to 50%", xaxis_title="Броски" if is_ru else "Flips", yaxis_title="Доля" if is_ru else "Proportion")
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"Финальная доля: **{cum_mean[-1]:.1%}**" if is_ru else f"Final proportion: **{cum_mean[-1]:.1%}**")

# ====================== 8. ЛОТЕРЕЯ 6 ИЗ 36 ======================
elif experiment.startswith("8."):
    st.header("🎟️ Симулятор лотереи 6 из 36" if is_ru else "🎟️ Lottery 6/36 Simulator")
    st.markdown("Выбери свои 6 чисел и посмотри, как часто ты бы выигрывал!" if is_ru else "Choose your 6 numbers and see how often you would win!")

    col1, col2 = st.columns([2, 1])
    with col1:
        user_numbers = st.multiselect(
            "Твои 6 чисел (1–36)" if is_ru else "Your 6 numbers (1–36)",
            options=range(1, 37),
            max_selections=6,
            default=[1, 2, 3, 4, 5, 6]
        )
    with col2:
        n_draws = st.slider("Количество розыгрышей" if is_ru else "Number of simulated draws", 10000, 1000000, 100000, step=10000)

    if len(user_numbers) == 6:
        user_set = set(user_numbers)
        sorted_user = sorted(user_numbers)
        st.info(f"**Твой билет:** {sorted_user}" if is_ru else f"**Your ticket:** {sorted_user}")

        if st.button("Запустить симуляцию" if is_ru else "Run Simulation", type="primary"):
            wins = {k: 0 for k in range(3, 7)}
            total_comb = comb(36, 6)
            progress_bar = st.progress(0)

            for i in range(n_draws):
                draw = set(np.random.choice(range(1, 37), 6, replace=False))
                matches = len(user_set & draw)
                if matches >= 3:
                    wins[matches] += 1
                if i % 10000 == 0:
                    progress_bar.progress((i + 1) / n_draws)

            progress_bar.empty()

            st.subheader("Результаты: теория vs симуляция" if is_ru else "Results: Theory vs Simulation")
            data = []
            for m in range(6, 2, -1):
                ways = comb(6, m) * comb(30, 6 - m)
                p_theory = ways / total_comb
                p_sim = wins[m] / n_draws
                data.append({
                    "Совпадений" if is_ru else "Matches": m,
                    "Выигрышей" if is_ru else "Your wins": wins[m],
                    "Симуляция %" if is_ru else "Simulated %": f"{p_sim:.6%}",
                    "Теория %" if is_ru else "Theoretical %": f"{p_theory:.6%}",
                    "1 к" if is_ru else "1 in": f"1 к {int(1/p_theory):,}" if is_ru else f"1 in {int(1/p_theory):,}"
                })

            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            fig = go.Figure()
            fig.add_trace(go.Bar(x=[f"{m} совпадений" if is_ru else f"{m} matches" for m in range(6,2,-1)],
                                y=[wins[m] for m in range(6,2,-1)],
                                text=[f"{wins[m]}" for m in range(6,2,-1)],
                                textposition="auto"))
            fig.update_layout(title="Количество выигрышей" if is_ru else "Number of wins in simulation", xaxis_title="Совпадений" if is_ru else "Matches", yaxis_title="Раз" if is_ru else "Times won")
            st.plotly_chart(fig, use_container_width=True)

            if wins[6] > 0:
                st.balloons()
                st.success(f"🎉 ДЖЕКПОТ! {wins[6]} раз!" if is_ru else f"🎉 JACKPOT! {wins[6]} times!")

    else:
        st.warning("Выбери ровно 6 чисел" if is_ru else "Please select exactly 6 numbers")

# ====================== О ПРОЕКТЕ ======================
else:
    st.header("О проекте" if is_ru else "About the Project")
    st.markdown("""
    **Интерактивный дашборд по вероятностям**  
    • 8 экспериментов  
    • Переключение языка  
    • Streamlit + Plotly + NumPy  
    """ if is_ru else """
    **Interactive Probability Research Dashboard**  
    • 8 experiments  
    • Real-time language switch  
    • Streamlit + Plotly + NumPy  
    """)
    st.balloons()

st.caption("Made with ❤️ | Исследование вероятностей" if is_ru else "Made with ❤️ | Probability Research Project")