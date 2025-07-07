#group 37
#ran out of time but have future plans to add more options to calculate their future investments through tax deductions, 
#     if their married status and children are part of their financial gain or loss
#add more styling so that it looks more presentable for the real world market
#create multiple scripts that can run along side so that it is more readable and clean
#fixing that double click button is a MUST!!!!
#hopfully using a better model if we had more time, we're not use to using styling anymore but hope to be better at it for the next time

#4/5/2025 --> this project was completed at UTD FInHack 2025


import streamlit as st


#the page configuration + styles..........
st.set_page_config(page_title="Investor Profile", layout="centered")
st.markdown(
    """
    <style>
    /*hide Streamlit's top menu and footer(annoying) */
    #MainMenu, header, footer {visibility: hidden;}

    /*background and global styling <------------- */
    .stApp {
        background: linear-gradient(to top right, #1a0033, #6a0dad, #3b0a65);
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-size: cover;
        color: white;
    }

    /*text shadow for headers and paragraphs <---------------*/
    h1, h2, h3, h4, h5, h6, p {
        text-shadow: 1px 1px 2px black;
    }

    /*global button styling <-----------------*/
    button
    {
        background-color: #4b6cb7 !important;
        color: white !important;
        font-weight: bold;
        border: 2px solid black !important;
        border-radius: 12px !important;
        height: 100px !important;
        width: 100% !important;
        font-size: 16px !important;
    }
    button:hover
    {
        background-color: #6e85d3 !important;
    }

    /*label styling <--------------------*/
    label
    {
        color: white !important;
        font-weight: bold;
    }

    /*clean number input styling <------------------------*/
    input[type=number]
    {
        border-radius: 6px;
        padding-right: 2.5em;
        -moz-appearance: textfield;
    }
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button
    {
        -webkit-appearance: none;
        margin: 0;
    }
    .stNumberInput input
    {
        border-radius: 6px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

#session state initialization...........
default_keys = [
    "user_info_collected",
    "riskToleranceChoice",
    "investmentTimeline",
    "financialGoal",
    "adjustedRiskPercent",
]
for key in default_keys:
    if key not in st.session_state:
        st.session_state[key] = None

#input Forms & buttons.......
if not st.session_state.user_info_collected:
    st.markdown("### Let's get started... Tell us about yourself")
    with st.form("user_info_form"):
        st.session_state.name = st.text_input("What is your name?")
        st.session_state.age = st.number_input("How old are you?", min_value=0, max_value=120, step=1)
        st.session_state.marital_status = st.text_input("What is your marital status?")
        st.session_state.employment_status = st.radio(
            "What is your employment status?",
            options=["Part Time", "Full Time", "Student"],
            horizontal=True
        )

        submitted = st.form_submit_button("continue")
        if submitted:
            st.session_state.user_info_collected = True

if st.session_state.user_info_collected and not st.session_state.riskToleranceChoice:
    st.title("What is your risk tolerance?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Low"):
            st.session_state.riskToleranceChoice = "Low"
            st.session_state.riskPercent = 20
    with col2:
        if st.button("Medium"):
            st.session_state.riskToleranceChoice = "Medium"
            st.session_state.riskPercent = 50
    with col3:
        if st.button("High"):
            st.session_state.riskToleranceChoice = "High"
            st.session_state.riskPercent = 80

if st.session_state.riskToleranceChoice and not st.session_state.investmentTimeline:
    st.markdown("### What is your timeline for return on investment?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("0-1 years"):
            st.session_state.investmentTimeline = "0-1 years"
            st.session_state.adjustedRiskPercent = max(0, st.session_state.riskPercent - 5)
    with col2:
        if st.button("1-5 years"):
            st.session_state.investmentTimeline = "1-5 years"
            st.session_state.adjustedRiskPercent = st.session_state.riskPercent
    with col3:
        if st.button("5+ years"):
            st.session_state.investmentTimeline = "5+ years"
            st.session_state.adjustedRiskPercent = min(100, st.session_state.riskPercent + 5)

if st.session_state.investmentTimeline and not st.session_state.financialGoal:
    st.markdown("### What are your financial goals?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Education"):
            st.session_state.financialGoal = "Education"
        if st.button("Retirement"):
            st.session_state.financialGoal = "Retirement"
            st.session_state.adjustedRiskPercent = min(100, st.session_state.adjustedRiskPercent + 10)
    with col2:
        if st.button("Significant Event"):
            st.session_state.financialGoal = "Significant Event"
        if st.button("Becoming a Homeowner"):
            st.session_state.financialGoal = "Becoming a Homeowner"
    with col3:
        if st.button("Donation to Charity"):
            st.session_state.financialGoal = "Donation to Charity"
            st.session_state.adjustedRiskPercent = min(100, st.session_state.adjustedRiskPercent + 10)
        if st.button("Future Wealth Transfer"):
            st.session_state.financialGoal = "Future Wealth Transfer"
            st.session_state.adjustedRiskPercent = min(100, st.session_state.adjustedRiskPercent + 10)

if st.session_state.financialGoal and "debt_Income_ratio" not in st.session_state:
    st.markdown("### What is your monthly debt-to-income ratio?")
    with st.form("debt_income_form"):
        monthly_debt = st.number_input("Enter your total **monthly debt** ($):", min_value=0.0, step=50.0, format="%.2f")
        monthly_income = st.number_input("Enter your **gross monthly income** ($):", min_value=0.0, step=50.0, format="%.2f")
        submitted = st.form_submit_button("Calculate")
        if submitted:
            if monthly_income > 0:
                st.session_state.monthly_income = monthly_income
                st.session_state.monthly_debt = monthly_debt
                dti = (monthly_debt / monthly_income) * 100
                st.session_state.debt_Income_ratio = round(dti, 2)
                #adjust risk based on debt-to-income ratio....
                if dti > 50:
                    st.session_state.adjustedRiskPercent = max(0, st.session_state.adjustedRiskPercent - 20)
                elif dti < 25:
                    st.session_state.adjustedRiskPercent = min(100, st.session_state.adjustedRiskPercent + 10)
                st.success(f"Your debt-to-income ratio is **{st.session_state.debt_Income_ratio}%**")
            else:
                st.error("Income must be greater than 0 to calculate the ratio.")

if "debt_Income_ratio" in st.session_state and "investmentProduct" not in st.session_state:
    st.markdown("### Do you have financial knowledge?")
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("Yes"):
            st.session_state.investmentProduct = "mutual funds"
    with col_no:
        if st.button("No"):
            st.session_state.investmentProduct = "government bond"

if "investmentProduct" in st.session_state and "taxDeferredPreference" not in st.session_state:
    st.markdown("### Do you prefer tax-deferred income?")
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("Yes (Tax-Deferred)"):
            st.session_state.taxDeferredPreference = "Yes"
    with col_no:
        if st.button("No (Taxable Now)"):
            st.session_state.taxDeferredPreference = "No"


#final summary Output......
if st.session_state.financialGoal:
    st.markdown("## Final Summary")
    st.markdown(f"**Risk Tolerance:** {st.session_state.riskToleranceChoice}")
    st.markdown(f"**Investment Timeline:** {st.session_state.investmentTimeline}")
    st.markdown(f"**Financial Goal:** {st.session_state.financialGoal}")
    if "monthly_income" in st.session_state:
        st.markdown(f"**Monthly Income:** ${st.session_state.monthly_income:,.2f}")
    if "monthly_debt" in st.session_state:
        st.markdown(f"**Monthly Debt:** ${st.session_state.monthly_debt:,.2f}")
    if "debt_Income_ratio" in st.session_state:
        st.markdown(f"**Debt-to-Income Ratio:** {st.session_state.debt_Income_ratio}%")
    if "investmentProduct" in st.session_state:
        st.markdown(f"**Recommended Investment Product:** {st.session_state.investmentProduct}")
    if "taxDeferredPreference" in st.session_state:
        st.markdown(f"**Tax-Deferred Income Preference:** {st.session_state.taxDeferredPreference}")
    if st.session_state.adjustedRiskPercent is not None:
        st.markdown(f"**Final Adjusted Risk Score:** {st.session_state.adjustedRiskPercent}%")