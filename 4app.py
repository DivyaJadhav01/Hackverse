import streamlit as st
import numpy as np
import pickle

# Define variable descriptions
variable_descriptions = {
    "G1": "First Semester Grade (G1) - Numeric: from 0 to 20",
    "G2": "Second Semester Grade (G2) - Numeric: from 0 to 20",
    "absences": "Number of Absences - Numeric: from 0 to 93",
    "failures": "Number of Past Class Failures - Numeric: n if 1<=n<3, else 4",
    "Fedu": "Father's Education Level - Numeric: 0 to 4",
    "freetime": "Free Time after School - Numeric: from 1 (very low) to 5 (very high)",
    "goout": "Outings with Friends - Numeric: from 1 (very low) to 5 (very high)",
    "guardian": "Guardian - Nominal: 'Mother', 'Father', or 'Other'",
    "school": "School Attended - Nominal: 'GP' or 'LVA'"
}

def load_model():
    return pickle.load(open("C:/Users/wezhi/OneDrive/Desktop/DEAV_CODE/logreg_model.pkl", 'rb'))

def main():
    st.title("🎓 Student Grade Predictor")

    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Predict your academic performance based on key academic and lifestyle factors!</p>', unsafe_allow_html=True)

    # Sidebar for Quick Instructions and Overview
    with st.sidebar:
        st.header("📝 How to Use")
        st.write("1. Fill in the required information in each section.")
        st.write("2. Click 'Predict Overall Score' at the bottom.")

    # Collapsible sections for different categories of inputs
    with st.container():
        with st.expander("📊 Academic Records", expanded=True):
            G1 = st.slider('First Semester Grade (G1)', 0, 20, 10, help=variable_descriptions["G1"])
            G2 = st.slider('Second Semester Grade (G2)', 0, 20, 10, help=variable_descriptions["G2"])
            absences = st.slider('Number of Absences', 0, 93, 5, help=variable_descriptions["absences"])
            failures = st.slider('Number of Past Class Failures', 0, 3, 0, help=variable_descriptions["failures"])

        with st.expander("👪 Family & Lifestyle"):
            Fedu = st.select_slider('Father\'s Education Level', options=[0, 1, 2, 3, 4], format_func=lambda x: 'Level ' + str(x), help=variable_descriptions["Fedu"])
            freetime = st.select_slider('Free Time after School', options=range(1, 6), help=variable_descriptions["freetime"])
            goout = st.select_slider('Outings with Friends', options=range(1, 6), help=variable_descriptions["goout"])
            guardian = st.radio('Guardian', ['Mother', 'Father', 'Other'], help=variable_descriptions["guardian"])

        with st.expander("🏫 School Details"):
            school = st.radio('School Attended', ['GP', 'LVA'], help=variable_descriptions["school"])

    # Prediction Button
    if st.button('🎓 Predict Overall Score'):
        school_GP = 1 if school == 'GP' else 0
        school_LVA = 1 if school == 'LVA' else 0
        guardian_other = 1 if guardian == 'Other' else 0

        feature_list = [G2, G1, school_LVA, absences, failures, Fedu, freetime, guardian_other, school_GP, goout]
        features = np.array(feature_list).reshape(1, -1)

        model = load_model()
        prediction = model.predict(features)
        st.balloons()
        st.success(f"Predicted Overall Score: {prediction[0]}")

if __name__ == '__main__':
    main()
