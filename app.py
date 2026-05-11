import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Integrated CD Planner", layout="wide")

# --- ส่วนของการเก็บข้อมูล (Session State) ---
if 'ip_data' not in st.session_state:
    st.session_state.ip_data = pd.DataFrame(columns=['ประเด็น', 'Importance', 'Performance'])

# เก็บข้อมูลปัจจัยภายนอก O และ T
if 'opps' not in st.session_state:
    st.session_state.opps = ""
if 'threats' not in st.session_state:
    st.session_state.threats = ""

# --- Sidebar: Navigation ---
st.sidebar.title("ระบบแผนพัฒนาชุมชน")
step = st.sidebar.radio("เลือกขั้นตอนการทำงาน", [
    "Step 1: IP Matrix (ปัจจัยภายใน)",
    "Step 2: Policy Alignment (ความเชื่อมโยง)",
    "Step 3: SWOT Analysis (วิเคราะห์อัตโนมัติ)",
    "Step 4: TOWS Matrix & Strategy",
    "Step 7: Value Chain Summary"
])

# --- STEP 1: IP MATRIX ---
if step == "Step 1: IP Matrix (ปัจจัยภายใน)":
    st.header("📍 ขั้นตอนที่ 1: วิเคราะห์งานพัฒนาชุมชน (IP Matrix)")
    st.write("กรอกประเด็นการพัฒนา เพื่อให้ระบบประเมินว่าสิ่งใดคือ **จุดแข็ง** หรือ **จุดอ่อน**")
    
    with st.form("ip_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        topic = col1.text_input("ประเด็นการพัฒนา (เช่น กลุ่มอาชีพ, กองทุนหมู่บ้าน, สัมมาชีพ)")
        imp = col2.slider("Importance (ความสำคัญ)", 1, 5, 3)
        perf = col3.slider("Performance (ผลงานที่ทำได้)", 1, 5, 3)
        submit = st.form_submit_button("เพิ่มข้อมูล")
        
        if submit and topic:
            new_data = pd.DataFrame({'ประเด็น': [topic], 'Importance': [imp], 'Performance': [perf]})
            st.session_state.ip_data = pd.concat([st.session_state.ip_data, new_data], ignore_index=True)

    if not st.session_state.ip_data.empty:
        fig = px.scatter(st.session_state.ip_data, x="Performance", y="Importance", text="ประเด็น",
                         range_x=[0, 6], range_y=[0, 6], title="แผนภูมิ IP Matrix")
        fig.add_hline(y=3.0, line_dash="dash", line_color="red")
        fig.add_vline(x=3.0, line_dash="dash", line_color="red")
        
        # ปรับสีจุดกราฟ
        fig.update_traces(marker=dict(size=15, color='#1f77b4'), textposition='top center')
        st.plotly_chart(fig, use_container_width=True)

# --- STEP 2: POLICY ALIGNMENT ---
elif step == "Step 2: Policy Alignment (ความเชื่อมโยง)":
    st.header("🔗 ขั้นตอนที่ 2: ความเชื่อมโยงกับแผนระดับต่างๆ")
    if st.session_state.ip_data.empty:
        st.warning("กรุณากรอกข้อมูลใน Step 1 ก่อนครับ")
    else:
        for index, row in st.session_state.ip_data.iterrows():
            with st.expander(f"ประเด็น: {row['ประเด็น']}"):
                st.write(f"✅ **ระดับอำเภอ:** สอดคล้องกับแผนพัฒนาอำเภอ ด้าน{row['ประเด็น']}")
                st.write(f"🏢 **ระดับจังหวัด:** สนับสนุนตัวชี้วัดจังหวัดแม่ฮ่องสอน (ยกระดับคุณภาพชีวิต)")
                st.write(f"🇹🇭 **ระดับชาติ:** ยุทธศาสตร์ชาติ ด้านการสร้างโอกาสและความเสมอภาคทางสังคม")

# --- STEP 3: SWOT ANALYSIS ---
elif step == "Step 3: SWOT Analysis (วิเคราะห์อัตโนมัติ)":
    st.header("🔍 ขั้นตอนที่ 3: วิเคราะห์สภาพแวดล้อม (SWOT Analysis)")
    st.write("ระบบทำการดึงข้อมูลจาก **ขั้นตอนที่ 1** มาคัดกรองจุดแข็งและจุดอ่อนให้อัตโนมัติ")
    
    # ระบบตรรกะคัดกรอง S และ W จากคะแนน IP Matrix
    strengths = []
    weaknesses = []
    
    if not st.session_state.ip_data.empty:
        for index, row in st.session_state.ip_data.iterrows():
            # กฎ: ถ้าความสำคัญสูง (>=3) และ ผลงานดี (>=3) = จุดแข็ง
            if row['Importance'] >= 3 and row['Performance'] >= 3:
                strengths.append(row['ประเด็น'])
            # กฎ: ถ้าความสำคัญสูง (>=3) แต่ ผลงานยังน้อย (<3) = จุดอ่อนที่ต้องเร่งแก้
            elif row['Importance'] >= 3 and row['Performance'] < 3:
                weaknesses.append(row['ประเด็น'])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💪 จุดแข็ง (Strengths)")
        st.caption("ดึงจากประเด็นที่คะแนนความสำคัญสูง และผลงานดี")
        if strengths:
            for s in strengths:
                st.success(f"✔️ {s}")
        else:
            st.info("ยังไม่มีข้อมูล (ระบบวิเคราะห์จาก Importance >= 3, Performance >= 3)")

    with col2:
        st.subheader("⚠️ จุดอ่อน (Weaknesses)")
        st.caption("ดึงจากประเด็นที่คะแนนความสำคัญสูง แต่ผลงานยังต้องปรับปรุง")
        if weaknesses:
            for w in weaknesses:
                st.error(f"❌ {w}")
        else:
            st.info("ยังไม่มีข้อมูล (ระบบวิเคราะห์จาก Importance >= 3, Performance < 3)")

    st.markdown("---")
    st.subheader("🌍 ปัจจัยภายนอก (External Factors)")
    st.write("ส่วนนี้ให้เจ้าหน้าที่กรอกเพิ่มเติม เนื่องจากเป็นปัจจัยนอกเหนือการควบคุมของพื้นที่")
    
    col3, col4 = st.columns(2)
    with col3:
        st.session_state.opps = st.text_area("🌟 โอกาส (Opportunities) เช่น นโยบายรัฐ, เทรนด์ใหม่", value=st.session_state.opps, height=150)
    with col4:
        st.session_state.threats = st.text_area("🔥 อุปสรรค (Threats) เช่น ภัยธรรมชาติ, เศรษฐกิจ", value=st.session_state.threats, height=150)

# --- STEP 4: TOWS MATRIX ---
elif step == "Step 4: TOWS Matrix & Strategy":
    st.header("🧠 ขั้นตอนที่ 4: การจัดทำแผนกลยุทธ์ (TOWS Matrix)")
    st.write("นำจุดแข็ง จุดอ่อน โอกาส และอุปสรรค มาไขว้กันเพื่อสร้างกลยุทธ์ (Cross-Impact Analysis)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("🎯 SO Strategy (กลยุทธ์เชิงรุก)")
        st.text_area("ใช้จุดแข็ง (S) คว้าโอกาส (O)", placeholder="เช่น นำจุดแข็งเรื่อง... ไปขยายผลร่วมกับนโยบาย...", height=100)
    with col2:
        st.info("🛠️ WO Strategy (กลยุทธ์เชิงแก้ไข)")
        st.text_area("ใช้โอกาส (O) เพื่อลดจุดอ่อน (W)", placeholder="เช่น ขอรับงบประมาณสนับสนุนจาก... เพื่อแก้ปัญหา...", height=100)

    with col1:
        st.warning("🛡️ ST Strategy (กลยุทธ์เชิงป้องกัน)")
        st.text_area("ใช้จุดแข็ง (S) รับมืออุปสรรค (T)", placeholder="เช่น ใช้ความเข้มแข็งของเครือข่าย เพื่อรับมือกับวิกฤต...", height=100)
    with col2:
        st.error("⚠️ WT Strategy (กลยุทธ์เชิงรับ)")
        st.text_area("ลดจุดอ่อน (W) และเลี่ยงอุปสรรค (T)", placeholder="เช่น ปรับโครงสร้าง หรือชะลอโครงการบางส่วน...", height=100)

# --- STEP 7: VALUE CHAIN ---
elif step == "Step 7: Value Chain Summary":
    st.header("🏗️ ขั้นตอนที่ 7: ร่างแผนพัฒนาชุมชนเชิงพื้นที่ (Value Chain)")
    st.image("https://via.placeholder.com/1000x300.png?text=Community+Development+Value+Chain") 
    st.markdown("""
    ### สรุปแผนบูรณาการ
    *   **ต้นน้ำ (Input):** ทุนชุมชนและปราชญ์ชาวบ้าน จากผลวิเคราะห์ IP Matrix
    *   **กลางน้ำ (Process):** โครงการสำคัญ (Flagship Projects) ที่วิเคราะห์จาก TOWS
    *   **ปลายน้ำ (Output/Outcome):** เป้าหมายชุมชนเข้มแข็งและยั่งยืน
    """)
    if st.button("Export แผนพัฒนา (PDF)"):
        st.success("ระบบจำลองการสร้างไฟล์ PDF เรียบร้อยแล้ว!")
