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

st.caption(" 🚀")

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Probability Calculator", layout="wide", page_icon="🎲")
st.title("🧮 Probability Events Calculator")
st.markdown("**Explore randomness in practice!** Simulations + Theory + Beautiful graphs")

st.sidebar.title("Choose Experiment")
experiment = st.sidebar.radio(
    "Experiment",
    [
        "1. Birthday Paradox",
        "2. Monty Hall Problem",
        "3. Monte Carlo Pi Estimation",
        "4. Bayesian Disease Test",
        "5. Gambler's Ruin",
        "6. Markov Chain Weather",
        "7. Law of Large Numbers (Coin Flips)",
        "About the Project"
    ]
)

# 1. Birthday Paradox
if experiment == "1. Birthday Paradox":
    st.header("🎂 Birthday Paradox")
    col1, col2 = st.columns([1, 2])
    with col1:
        n_people = st.slider("Number of people", 2, 100, 23)
        n_sim = st.slider("Number of simulations", 1000, 50000, 10000, 1000)
        if st.button("Run Simulation", type="primary"):
            birthdays = np.random.randint(1, 365, size=(n_sim, n_people))
            has_match = np.array([len(np.unique(row)) < len(row) for row in birthdays])
            prob_sim = has_match.mean()
            prob_theory = 1 - np.prod(1 - np.arange(1, n_people) / 365)
            st.success(f"Simulation: **{prob_sim:.1%}** | Theory: **{prob_theory:.1%}**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[n_people], y=[prob_sim], mode='markers', name='Simulation', marker=dict(size=15, color='red')))
            fig.add_trace(go.Scatter(x=list(range(2,81)), y=[1 - np.prod(1 - np.arange(1,k)/365) for k in range(2,81)], mode='lines', name='Theory'))
            fig.update_layout(title="Probability of shared birthday", xaxis_title="People", yaxis_title="Probability")
            st.plotly_chart(fig, use_container_width=True)

# 2. Monty Hall
elif experiment == "2. Monty Hall Problem":
    st.header("🚪 Monty Hall Problem")
    col1, col2 = st.columns([1, 2])
    with col1:
        n_games = st.slider("Number of games", 1000, 100000, 10000, 1000)
        strategy = st.radio("Strategy", ["Switch door", "Stay"])
        if st.button("Run Simulation", type="primary"):
            wins = 0
            for _ in range(n_games):
                doors = [0,0,1]; np.random.shuffle(doors)
                choice = np.random.randint(0,3)
                monty = next(i for i in range(3) if i != choice and doors[i]==0)
                if strategy == "Switch door":
                    new = next(i for i in range(3) if i != choice and i != monty)
                    if doors[new] == 1: wins += 1
                else:
                    if doors[choice] == 1: wins += 1
            prob = wins / n_games
            st.success(f"Win probability: **{prob:.1%}**")
            st.info("Theory: Switch = 66.7%, Stay = 33.3%")

# 3. Monte Carlo Pi
elif experiment == "3. Monte Carlo Pi Estimation":
    st.header("🎯 Monte Carlo: Estimating π")
    n_points = st.slider("Number of points", 100, 20000, 5000, 100)
    if st.button("Run Simulation", type="primary"):
        x = np.random.uniform(-1, 1, n_points)
        y = np.random.uniform(-1, 1, n_points)
        inside = (x**2 + y**2) <= 1
        pi_est = 4 * np.sum(inside) / n_points
        st.success(f"Estimated π: **{pi_est:.4f}** (true value 3.1416)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x[inside], y=y[inside], mode='markers', marker=dict(color='green', size=3), name='Inside circle'))
        fig.add_trace(go.Scatter(x=x[~inside], y=y[~inside], mode='markers', marker=dict(color='red', size=3), name='Outside'))
        fig.update_layout(title=f"Monte Carlo π ({n_points} points)", xaxis_range=[-1,1], yaxis_range=[-1,1], width=700, height=700)
        st.plotly_chart(fig, use_container_width=True)

# 4. Bayesian Test
elif experiment == "4. Bayesian Disease Test":
    st.header("🦠 Bayesian Disease Test")
    prevalence = st.slider("Disease prevalence (%)", 0.1, 20.0, 1.0) / 100
    sensitivity = st.slider("Test sensitivity (%)", 70, 100, 95) / 100
    specificity = st.slider("Test specificity (%)", 70, 100, 95) / 100
    if st.button("Calculate", type="primary"):
        prior = prevalence
        likelihood_pos = sensitivity
        false_pos = 1 - specificity
        posterior = (likelihood_pos * prior) / (likelihood_pos * prior + false_pos * (1 - prior))
        st.success(f"Probability of disease after positive test: **{posterior:.1%}**")
        st.info("Intuition fails! Even with a good test, result is often false positive.")

# 5. Gambler's Ruin
elif experiment == "5. Gambler's Ruin":
    st.header("💰 Gambler's Ruin")
    capital = st.slider("Your starting capital", 10, 100, 50)
    total = st.slider("Casino capital", 50, 500, 200)
    p_win = st.slider("Win probability per round (%)", 40, 60, 49) / 100
    if st.button("Simulate 1000 games", type="primary"):
        ruins = 0
        for _ in range(1000):
            money = capital
            while 0 < money < total:
                money += 1 if np.random.random() < p_win else -1
            if money == 0: ruins += 1
        prob_ruin = ruins / 1000
        st.success(f"Probability of ruin: **{prob_ruin:.1%}**")
        st.info("If p < 50% you almost always go bankrupt over time!")

# 6. Markov Chain Weather
elif experiment == "6. Markov Chain Weather":
    st.header("☀️ Weather Forecast (Markov Chain)")
    today = st.selectbox("Today", ["Sunny", "Rainy"])
    if st.button("Simulate 30 days", type="primary"):
        states = ["Sunny", "Rainy"]
        trans = [[0.8, 0.2], [0.3, 0.7]]
        current = 0 if today == "Sunny" else 1
        days = [states[current]]
        for _ in range(29):
            current = np.random.choice([0,1], p=trans[current])
            days.append(states[current])
        sunny_days = days.count("Sunny")
        st.success(f"In 30 days sunny: {sunny_days} times ({sunny_days/30:.1%})")
        st.line_chart([1 if d=="Sunny" else 0 for d in days])

# 7. NEW: Law of Large Numbers
elif experiment == "7. Law of Large Numbers (Coin Flips)":
    st.header("📈 Law of Large Numbers — Coin Flips")
    st.markdown("How many flips needed for the frequency to approach 50%?")
    n_flips = st.slider("Number of coin flips", 10, 10000, 1000, 10)
    if st.button("Run Simulation", type="primary"):
        flips = np.random.choice([0, 1], size=n_flips)  # 0 = tails, 1 = heads
        cum_mean = np.cumsum(flips) / np.arange(1, n_flips + 1)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(1, n_flips+1)), y=cum_mean, mode='lines', name='Running probability of heads'))
        fig.add_hline(y=0.5, line_dash="dash", line_color="red", annotation_text="True probability 50%")
        fig.update_layout(title="Convergence to 50%", xaxis_title="Number of flips", yaxis_title="Proportion of heads")
        st.plotly_chart(fig, use_container_width=True)
        st.success(f"Final proportion after {n_flips} flips: **{cum_mean[-1]:.1%}**")

else:
    st.header("About the Project")
    st.markdown("""
    **Interactive Probability Research Dashboard**  
    - 7 real experiments with simulations vs theory  
    - Built with Streamlit + Plotly + NumPy  
    - Perfect for portfolio, university, or just fun!  
    """)
    st.balloons()

st.caption("Made with ❤️ | Probability Research Project")