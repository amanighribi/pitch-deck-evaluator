import streamlit as st
from modules.pdf_parser import extract_text_from_pdf
from modules.evaluator import evaluate_deck
from modules.report import generate_report

st.set_page_config(page_title="PitchLens AI", page_icon="⚡", layout="wide")

st.title("⚡ PitchLens AI")
st.caption("An AI-powered pitch deck evaluator built for investors.")

uploaded_file = st.file_uploader("Upload your pitch deck (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading your deck..."):
        deck_text = extract_text_from_pdf(uploaded_file)

    if not deck_text:
        st.error("Could not extract text from this PDF. Make sure it's not a scanned image.")
        st.stop()

    st.success(f"Deck loaded. Extracted {len(deck_text.split())} words across slides.")

    if st.button("⚡ Evaluate Deck"):
        with st.spinner("Analyzing through an investor lens..."):
            evaluation = evaluate_deck(deck_text)

        if "error" in evaluation:
            st.error(evaluation["error"])
            st.stop()

        report = generate_report(evaluation)

        # Overall Score + Investment Readiness
        st.divider()
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Overall Score", f"{report['overall_score']} / 100")
            st.markdown(f"**Verdict:** :{report['color']}[{report['verdict']}]")
        with col2:
            st.markdown("**Investment Readiness**")
            readiness = report['investment_readiness']
            if "Strong" in readiness:
                  icon = "🟢"
            elif "Potential" in readiness:
                  icon = "🟡"
            else:
                  icon = "🔴"
            st.info(f"{icon} {readiness}\n\n{report['readiness_detail']}")
            st.markdown("**Investor Recommendation**")
            st.info(report["recommendation"])

        # Dimension Scores
        st.divider()
        st.subheader("Evaluation Breakdown")
        c1, c2, c3 = st.columns(3)
        c1.metric("Communication", f"{report['communication']['score']} / 100", "30% weight")
        c2.metric("Narrative", f"{report['narrative']['score']} / 100", "30% weight")
        c3.metric("Problem-Solution Fit", f"{report['problem_solution_fit']['score']} / 100", "40% weight")

        # Dimension Details
        st.divider()
        for dim_key, dim_label in [
            ("communication", "Communication"),
            ("narrative", "Narrative"),
            ("problem_solution_fit", "Problem-Solution Fit")
        ]:
            with st.expander(f"📊 {dim_label} — {report[dim_key]['score']}/100"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Strengths**")
                    for s in report[dim_key]["strengths"]:
                        st.markdown(f"✅ {s}")
                with col_b:
                    st.markdown("**Weaknesses**")
                    for w in report[dim_key]["weaknesses"]:
                        st.markdown(f"❌ {w}")

        # Slide Coverage
        st.divider()
        st.subheader("📋 Slide Coverage")
        coverage = report["slide_coverage"]
        st.metric("Narrative Completeness", f"{coverage['completeness_score']}%")
        cov_col1, cov_col2 = st.columns(2)
        with cov_col1:
            st.markdown("**Detected Sections**")
            for section in coverage["detected"]:
                st.markdown(f"✅ {section}")
        with cov_col2:
            st.markdown("**Missing Sections**")
            if coverage["missing"]:
                for section in coverage["missing"]:
                    st.markdown(f"❌ {section}")
            else:
                st.markdown("✅ All sections present")

        # Missing Investor Signals
        st.divider()
        st.subheader("📉 Missing Investor Signals")
        if report["missing_investor_signals"]:
            for signal in report["missing_investor_signals"]:
                st.markdown(f"❌ {signal}")
            st.warning("Investors may struggle to assess scalability without these signals.")
        else:
            st.success("All key investor signals are present.")

        # Risks and Questions
        st.divider()
        col_r, col_q = st.columns(2)
        with col_r:
            st.subheader("🔴 Top Risks")
            for risk in report["top_risks"]:
                st.markdown(f"- {risk}")
        with col_q:
            st.subheader("💬 Investor Would Ask")
            for q in report["investor_questions"]:
                st.markdown(f"- {q}")