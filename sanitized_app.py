import streamlit as st
import pandas as pd
from chat_handler import ChatHandler
from financial_tools import FinancialCalculator
import plotly.graph_objects as go
from utils import initialize_session_state

def main():
    st.set_page_config(page_title="CashBot", page_icon="💰")

    initialize_session_state()

    st.title("CashBot 💰")
    st.subheader("Your AI-Powered Financial Assistant")

    # Sidebar with financial tools
    with st.sidebar:
        st.header("Financial Tools")
        tool_choice = st.selectbox(
            "Select a tool:",
            ["Chat Assistant", "Investment Calculator", "Risk Analysis"]
        )

        # Add helper text based on selected tool
        if tool_choice == "Chat Assistant":
            st.info("Try asking questions like:\n"
                   "- What's a good investment strategy for beginners?\n"
                   "- How should I start saving for retirement?\n"
                   "- What are the pros and cons of index funds?")
        elif tool_choice == "Investment Calculator":
            st.info("Use this calculator to project your investment growth over time.")
        else:
            st.info("Analyze your risk tolerance and get personalized investment recommendations.")

    if tool_choice == "Chat Assistant":
        display_chat_interface_demo()
    elif tool_choice == "Investment Calculator":
        display_investment_calculator_demo()
    else:
        display_risk_analysis_demo()

def display_chat_interface_demo():
    # Get API key from session state or sidebar
    if "openai_api_key" not in st.session_state:
        with st.sidebar:
            st.session_state.openai_api_key = st.text_input("Enter OpenAI API Key:", type="password")
            
    if not st.session_state.openai_api_key:
        st.warning("Please enter your OpenAI API key to continue.")
        return
    
    # Use the key from session state
    os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
    chat_handler = ChatHandler()
    
    

def display_chat_interface_demo():
    chat_handler = ChatHandler()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about financial advice..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_handler.get_response(prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

def display_investment_calculator_demo():
    calc = FinancialCalculator()

    st.header("Investment Calculator")
    st.markdown("""
    This calculator helps you project your investment growth over time. 
    Try different scenarios by adjusting the values below.
    """)

    col1, col2 = st.columns(2)
    with col1:
        initial_investment = st.number_input(
            "Initial Investment ($)",
            min_value=0.0,
            value=1000.0,
            help="The amount you start with"
        )
        monthly_contribution = st.number_input(
            "Monthly Contribution ($)",
            min_value=0.0,
            value=100.0,
            help="How much you'll add each month"
        )

    with col2:
        years = st.number_input(
            "Investment Period (Years)",
            min_value=1,
            value=10,
            help="How long you plan to invest"
        )
        rate = st.number_input(
            "Expected Annual Return (%)",
            min_value=0.0,
            value=7.0,
            help="Average yearly return (historically, stock market returns ~7-10%)"
        )

    if st.button("Calculate", help="Click to see your potential investment growth"):
        future_value = calc.calculate_investment_growth(
            initial_investment,
            monthly_contribution,
            rate / 100,
            years
        )

        # Create visualization
        years_range = range(years + 1)
        values = [calc.calculate_investment_growth(
            initial_investment,
            monthly_contribution,
            rate / 100,
            year
        ) for year in years_range]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(years_range),
            y=values,
            mode='lines+markers',
            name='Investment Growth'
        ))

        fig.update_layout(
            title='Investment Growth Over Time',
            xaxis_title='Years',
            yaxis_title='Value ($)',
            showlegend=True
        )

        st.plotly_chart(fig)

        total_contributions = initial_investment + (monthly_contribution * 12 * years)
        earnings = future_value - total_contributions

        st.success(f"After {years} years, your investment could grow to: ${future_value:,.2f}")
        st.markdown(f"""
        **Breakdown:**
        - Total Contributions: ${total_contributions:,.2f}
        - Investment Earnings: ${earnings:,.2f}
        - Return on Investment: {calc.calculate_roi(total_contributions, future_value):.1f}%
        """)

def display_risk_analysis_demo():
    st.header("Risk Analysis")
    st.markdown("""
    Determine your investment risk profile by answering the question below.
    This will help generate personalized investment recommendations.
    """)

    risk_score = st.slider(
        "What's your risk tolerance? (1-10)",
        1, 10, 5,
        help="1 = Very Conservative, 10 = Very Aggressive"
    )

    st.markdown("""
    **Risk Score Guide:**
    - 1-3: Conservative
    - 4-7: Moderate
    - 8-10: Aggressive
    """)

    if st.button("Analyze Risk Profile"):
        with st.spinner("Analyzing..."):
            chat_handler = ChatHandler()
            analysis = chat_handler.get_risk_profile(risk_score)
            st.write(analysis)

if __name__ == "__main__":
    main()

def display_chat_interface_demo():
    st.header("Chat Assistant (Demo)")
    st.write("💬 This is a simulated chat with an AI advisor.")
    st.write("**User:** What's a good investment strategy?")
    st.write("**AI Advisor:** Diversify your investments across asset classes to manage risk effectively.")

def display_investment_calculator_demo():
    st.header("Investment Calculator (Demo)")
    st.write("📈 This tool simulates how your investments might grow.")
    st.write("**Initial Investment:** ₹10,000")
    st.write("**Monthly Contribution:** ₹2,000")
    st.write("**Duration:** 10 years")
    st.write("**Projected Growth:** ₹3,00,000 (Dummy Output)")

def display_risk_analysis_demo():
    st.header("Risk Analysis (Demo)")
    st.write("🧠 This tool analyzes your risk profile.")
    st.write("**Input:** Moderate Risk Appetite")
    st.write("**AI Recommendation:** Consider a mix of equity and debt instruments for balanced growth.")
