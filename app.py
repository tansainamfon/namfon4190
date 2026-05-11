import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Integrated CD Planner", layout="wide")

# --- ส่วนของการเก็บข้อมูล (Session State) ---
if 'ip_data' not in st.session_state:
    st.session_state.ip_data = pd.DataFrame(columns=['ประเด็น', 'Importance', 'Performance'])

# --- Sidebar: Navigation ---
step = st.sidebar.radio("ขั้นตอนการทำงาน", [
    "Step 1: IP Matrix (ปัจจัยภายใน)",
    "Step 2: Policy Alignment (ความเชื่อมโยง)",
    "Step 3: SWOT Analysis",
    "Step 4: TOWS Matrix & Strategy",
    "Step 7: Value Chain Summary"
])

# --- STEP 1: IP MATRIX ---
if step == "Step 1: IP Matrix (ปัจจัยภายใน)":
    st.header("📍 ขั้นตอนที่ 1: วิเคราะห์งานพัฒนาชุมชน (IP Matrix)")
    
    with st.form("ip_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        topic = col1.text_input("ประเด็นการพัฒนา (เช่น กลุ่มอาชีพ, กองทุนหมู่บ้าน)")
        imp = col2.slider("Importance (ความสำคัญ)", 1, 5, 3)
        perf = col3.slider("Performance (ผลงาน)", 1, 5, 3)
        submit = st.form_submit_button("เพิ่มข้อมูล")
        
        if submit and topic:
            new_data = pd.DataFrame({'ประเด็น': [topic], 'Importance': [imp], 'Performance': [perf]})
            st.session_state.ip_data = pd.concat([st.session_state.ip_data, new_data], ignore_index=True)

    if not st.session_state.ip_data.empty:
        fig = px.scatter(st.session_state.ip_data, x="Performance", y="Importance", text="ประเด็น",
                         range_x=[0, 6], range_y=[0, 6], title="แผนภูมิ IP Matrix")
        fig.add_hline(y=3, line_dash="dash", line_color="red")
        fig.add_vline(x=3, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
        st.write("*(จุดที่ Importance สูงแต่ Performance ต่ำ จะถูกส่งต่อไปเป็นจุดอ่อนในขั้นตอนถัดไป)*")

# --- STEP 2: POLICY ALIGNMENT ---
elif step == "Step 2: Policy Alignment (ความเชื่อมโยง)":
    st.header("🔗 ขั้นตอนที่ 2: ความเชื่อมโยงกับแผนระดับต่างๆ")
    if st.session_state.ip_data.empty:
        st.warning("กรุณากรอกข้อมูลใน Step 1 ก่อน")
    else:
        for index, row in st.session_state.ip_data.iterrows():
            with st.expander(f"ประเด็น: {row['ประเด็น']}"):
                st.write(f"✅ **ระดับอำเภอ:** สอดคล้องกับแผนพัฒนาอำเภอ ด้าน{row['ประเด็น']}")
                st.write(f"🏢 **ระดับจังหวัด:** สนับสนุนตัวชี้วัดจังหวัด (KPI: รายได้ครัวเรือน)")
                st.write(f"🇹🇭 **ระดับชาติ:** ยุทธศาสตร์ชาติ ด้านการสร้างโอกาสและความเสมอภาคทางสังคม")

# --- STEP 4: TOWS MATRIX ---
elif step == "Step 4: TOWS Matrix & Strategy":
    st.header("🧠 ขั้นตอนที่ 4: การจัดทำแผนกลยุทธ์ (TOWS Matrix)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("🎯 SO Strategy (เชิงรุก)")
        st.text_area("กลยุทธ์ที่ใช้จุดแข็งคู่กับโอกาส", placeholder="เช่น ยกระดับสินค้า OTOP สู่ตลาดออนไลน์ระดับสากล")
    with col2:
        st.info("🛠️ WO Strategy (เชิงแก้ไข)")
        st.text_area("กลยุทธ์ที่ใช้โอกาสเพื่อลดจุดอ่อน", placeholder="เช่น อบรมทักษะดิจิทัลให้กับกลุ่มตกเกณฑ์ จปฐ.")

    with col1:
        st.warning("🛡️ ST Strategy (เชิงป้องกัน)")
        st.text_area("กลยุทธ์ที่ใช้จุดแข็งรับมืออุปสรรค", placeholder="เช่น สร้างเครือข่ายความมั่นคงทางอาหารรับมือวิกฤตเศรษฐกิจ")
    with col2:
        st.error("⚠️ WT Strategy (เชิงรับ)")
        st.text_area("กลยุทธ์ที่ลดจุดอ่อนและเลี่ยงอุปสรรค", placeholder="เช่น การปรับโครงสร้างกลุ่มออมทรัพย์ที่ขาดสภาพคล่อง")

# --- STEP 7: VALUE CHAIN ---
elif step == "Step 7: Value Chain Summary":
    st.header("🏗️ ขั้นตอนที่ 7: ร่างแผนพัฒนาชุมชนเชิงพื้นที่ (Value Chain)")
    st.image("https://via.placeholder.com/800x400.png?text=Integrated+Value+Chain+Diagram") # จำลองภาพ Value Chain
    st.markdown("""
    ### สรุปแผนบูรณาการ
    *   **ต้นน้ำ (Input):** ทุนชุมชนและปราชญ์ชาวบ้าน จากผลวิเคราะห์ IP Matrix
    *   **กลางน้ำ (Process):** โครงการสำคัญ (Flagship Projects) ที่วิเคราะห์จาก TOWS
    *   **ปลายน้ำ (Output/Outcome):** เป้าหมาย 'ฮ่องสอน ฮอมฮัก' องค์กรแห่งความสุขอย่างยั่งยืน
    """)
    if st.button("Export แผนพัฒนา (PDF)"):
        st.write("ระบบกำลังประมวลผลไฟล์... (จำลอง)")
