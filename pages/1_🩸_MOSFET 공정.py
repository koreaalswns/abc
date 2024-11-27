import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components


st.sidebar.title("MOSFET 공정 시뮬레이션")
st.sidebar.write("각 공정 단계를 순서대로 확인하세요.")

# 버튼 상태 관리
if 'step' not in st.session_state:
    st.session_state['step'] = 0

    # 각 공정 단계에 대한 설명 텍스트
steps_description = [
    "1. 웨이퍼(P-Silicon) 준비",
    "2. 산화막 형성",
    "3. 포토레지스트(PR) 층 추가",
    "4. 소스/드레인 마스크, 노광 공정",
    "5. 현상(develope)",
    "6. 식각(etching)을 통해 산화막 제거",
    "7. 애싱(ashing)을 통해 PR 제거",
    "8. Gate 산화막 형성",
    "9. Poly-Si 형성",
    "10. PR 도포",
    "11. Mask 추가 후 노광 공정",
    "12. 현상",
    "13. 식각(etching)을 통해 산화막과 Poly-Si 제거",
    "14. 애싱(ashing)을 통해 PR 제거",
    "15. 이온 주입후 확산",
    "16. ILD(SiO2) 증착 후 CMP",
    "17. PR 도포",
    "18. Mask 추가 후 노광 공정",
    "19. 현상",
    "20. 식각(etching)을 통해 ILD 제거",
    "21. 애싱(ashing)을 통해 PR 제거",
    "22. Metal(Al) 증착 후 CMP",
    "23. PR 도포",
    "24. Mask 추가 후 노광 공정",
    "25. 현상",
    "26. 식각(etching)을 통해 Metal 제거",
    "27. 애싱(ashing)을 통해 PR 제거",
    ]

# CSS와 HTML을 사용하여 스타일 설정
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .stTitle { color: #34495e; font-weight: bold; font-size: 26px; text-align: center; margin-top: 10px; margin-bottom: 10px; }
        .button-container { display: flex; justify-content: space-between; align-items: center; padding: 5px 80px; margin-top: -10px; margin-bottom: 10px; }
        .stButton button { background-color: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 14px; font-weight: bold; cursor: pointer; transition: background-color 0.3s; }
        .stButton button:hover { background-color: #2980b9; }
        .step-display { text-align: center; font-size: 16px; color: #444444; font-weight: bold; margin-top: 5px; }
        .three-js-container { display: flex; justify-content: center; border-radius: 10px; background-color: #ffffff; padding: 5px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); margin-top: 10px; margin-bottom: 10px; }
        .description-box { background-color: #ecf0f1; border-radius: 10px; padding: 15px; font-size: 16px; color: #2c3e50; margin-top: 10px; text-align: left; }
    </style>
""", unsafe_allow_html=True)
# Three.js 애니메이션 스크립트
three_js_script_template = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
    let scene, camera, renderer, controls;

    // 전역 변수로 객체 선언
    let wafer = null, oxide = null, pr = null;
    let leftPart = null, rightPart = null, middlePart = null, topPart = null;

    function init() {{
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);

        // 초기 카메라 위치
        camera.position.set(5, 5, 10);
        camera.lookAt(0, 0, 0);

        renderer = new THREE.WebGLRenderer({{ alpha: true }});
        renderer.setSize(500, 350);
        document.getElementById('3d-simulation').appendChild(renderer.domElement);

        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // 객체 생성 함수 (테두리 포함)
        function createLayer(geometry, color, position) {{
            const material = new THREE.MeshBasicMaterial({{ color: color, opacity: 1, transparent: true }});
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(...position);

            // 테두리 추가
            const edges = new THREE.EdgesGeometry(geometry);
            const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({{ color: 0x000000 }}));
            mesh.add(line);

            return mesh;
        }}

        // 단계별 객체 관리
        if ({step} >= 0) {{
            // 1단계: 웨이퍼 생성
            if (!wafer) {{
                wafer = createLayer(new THREE.BoxGeometry(4, 1, 3), 0x87CEFA, [0, -0.5, 0]);
                scene.add(wafer);
            }}
        }}

        if ({step} >= 1) {{
            // 2단계: 산화막 추가
            if (!oxide) {{
                oxide = createLayer(new THREE.BoxGeometry(4, 0.5, 3), 0xA9A9A9, [0, 0.25, 0]);
                scene.add(oxide);
            }}
        }}

        if ({step} >= 2) {{
            // 3단계: PR 추가
            if (!pr) {{
                pr = createLayer(new THREE.BoxGeometry(4, 0.2, 3), 0xFF0000, [0, 0.6, 0]);
                scene.add(pr);
            }}
        }}

        if ({step} >= 3) {{
            // 4단계: 소스/드레인 마스크 추가
            if (!leftPart && !rightPart && !middlePart && !topPart) {{
                leftPart = createLayer(new THREE.BoxGeometry(0.5, 0.2, 3), 0x000000, [-1.75, 1, 0]);
                rightPart = createLayer(new THREE.BoxGeometry(0.5, 0.2, 3), 0x000000, [1.75, 1, 0]);
                topPart = createLayer(new THREE.BoxGeometry(4, 0.2, 1.2), 0x000000, [0, 1, -0.9]);

                 scene.add(leftPart);
                scene.add(rightPart);
                scene.add(topPart);
            }}
        }}

        if ({step} >= 4) {{
            // 5단계: 현상
            if (pr) {{
                scene.remove(pr);
                pr = null;
            }}

            if (leftPart) {{
                scene.remove(leftPart);
                leftPart = null;
            }}
            if (rightPart) {{
                scene.remove(rightPart);
                rightPart = null;
            }}
            if (topPart) {{
                scene.remove(topPart);
                topPart = null;
            }}

            if (!pr) {{
                leftPartp = createLayer(new THREE.BoxGeometry(0.5, 0.2, 3), 0xFF0000, [-1.75, 0.6, 0]);
                rightPartp = createLayer(new THREE.BoxGeometry(0.5, 0.2, 3), 0xFF0000, [1.75, 0.6, 0]);
                topPartp = createLayer(new THREE.BoxGeometry(4, 0.2, 1.2), 0xFF0000, [0, 0.6, -0.9]);

                scene.add(leftPartp);
                scene.add(rightPartp);
                scene.add(topPartp);
            }}
        }}

        if ({step} >= 5) {{
            // 6단계: 애칭
            if (oxide) {{
                scene.remove(oxide);
                oxide = null;
            }}
            if (!oxide) {{
                leftParto = createLayer(new THREE.BoxGeometry(0.5, 0.5, 3), 0xA9A9A9, [-1.75, 0.25, 0]);
                rightParto = createLayer(new THREE.BoxGeometry(0.5, 0.5, 3), 0xA9A9A9, [1.75, 0.25, 0]);
                topParto = createLayer(new THREE.BoxGeometry(4, 0.5, 1.2), 0xA9A9A9, [0, 0.25, -0.9]);

                scene.add(leftParto);
                scene.add(rightParto);
                scene.add(topParto);
            }}
        }}

        if ({step} >= 6) {{
            // 7단계: 애싱
            if (leftPartp) {{
                scene.remove(leftPartp);
                leftPartp = null;
            }}
            if (rightPartp) {{
                scene.remove(rightPartp);
                rightPartp = null;
            }}
            if (topPartp) {{
                scene.remove(topPartp);
                topPartp = null;
            }}
        }}        
        if ({step} >= 7) {{
            // 8단계: 산화막 형성
            if (wafer) {{
                leftParto8 = createLayer(new THREE.BoxGeometry(0.5, 0.25, 3), 0x7F7F7F, [-1.75, 0.625, 0]);
                rightParto8 = createLayer(new THREE.BoxGeometry(0.5, 0.25, 3), 0x7F7F7F, [1.75, 0.625, 0]);
                topParto8 = createLayer(new THREE.BoxGeometry(4, 0.25, 1.2), 0x7F7F7F, [0, 0.625, -0.9]);
                middleParto8 = createLayer(new THREE.BoxGeometry(3, 0.25, 1.8), 0x7F7F7F, [0, 0.125, 0.6]);


                scene.add(leftParto8);
                scene.add(rightParto8);
                scene.add(topParto8);
                scene.add(middleParto8);
            }}
        }}
        if ({step} >= 8) {{
            // 9단계: Poly-Si 형성
            if (wafer) {{
                leftPartp9 = createLayer(new THREE.BoxGeometry(0.5, 0.25, 3), 0x0000FF, [-1.75, 0.875, 0]);
                rightPartp9 = createLayer(new THREE.BoxGeometry(0.5, 0.25, 3), 0x0000FF, [1.75, 0.875, 0]);
                topPartp9 = createLayer(new THREE.BoxGeometry(4, 0.25, 1.2), 0x0000FF, [0, 0.875, -0.9]);
                middlePartp9 = createLayer(new THREE.BoxGeometry(3, 0.25, 1.8), 0x0000FF, [0, 0.375, 0.6]);


                scene.add(leftPartp9);
                scene.add(rightPartp9);
                scene.add(topPartp9);
                scene.add(middlePartp9);
            }}  
        }}
        if ({step} >= 9) {{
            // 10단계: PR 도포
            if (wafer) {{
                leftPartp10 = createLayer(new THREE.BoxGeometry(0.5, 0.1, 3), 0xFF0000, [-1.75, 1.05, 0]);
                rightPartp10 = createLayer(new THREE.BoxGeometry(0.5, 0.1, 3), 0xFF0000, [1.75, 1.05, 0]);
                topPartp10 = createLayer(new THREE.BoxGeometry(4, 0.1, 1.2), 0xFF0000, [0, 1.05, -0.9]);
                middlePartp10 = createLayer(new THREE.BoxGeometry(3, 0.1, 1.8), 0xFF0000, [0, 0.55, 0.6]);


                scene.add(leftPartp10);
                scene.add(rightPartp10);
                scene.add(topPartp10);
                scene.add(middlePartp10);
            }}  
        }}
        if ({step} >= 10) {{
            // 11단계: Mask 추가 후 노광 공정
            if (wafer) {{
                mask11 = createLayer(new THREE.BoxGeometry(1, 0.2, 1.8), 0x000000, [0, 1.3, 0.6]);

                scene.add(mask11);
            }}  
        }}
        if ({step} >= 11) {{
            // 12단계: 현상
            if (mask11) {{
                scene.remove(mask11);
                mask11 = null;

                scene.remove(leftPartp10);
                leftPartp10 = null;
                scene.remove(rightPartp10);
                rightPartp10 = null;
                scene.remove(topPartp10);
                topPartp10 = null;
                scene.remove(middlePartp10);
                middlePartp10 = null;

                PR12 = createLayer(new THREE.BoxGeometry(1, 0.1, 1.8), 0xFF0000, [0, 0.55, 0.6]);

                scene.add(PR12);
            }}  
        }}                 
        if ({step} >= 12) {{
            // 13단계: 식각(etching)을 통해 산화막과 Poly-Si 제거
        if (PR12){{
                scene.remove(leftParto8);
                leftParto8 = null;
                scene.remove(rightParto8);
                rightParto8 = null;
                scene.remove(topParto8);
                topParto8 = null;
                scene.remove(middleParto8);
                middleParto8 = null;

                scene.remove(leftPartp9);
                leftPartp9 = null;
                scene.remove(rightPartp9);
                rightPartp9 = null;
                scene.remove(topPartp9);
                topPartp9 = null;
                scene.remove(middlePartp9);
                middlePartp9 = null;

                Si12 = createLayer(new THREE.BoxGeometry(1, 0.25, 1.8), 0x7F7F7F, [0, 0.125, 0.6]);
                Poly12 = createLayer(new THREE.BoxGeometry(1, 0.25, 1.8), 0x0000FF, [0, 0.375, 0.6]);
                    
                scene.add(Si12);
                scene.add(Poly12);
        }}
        }}                 
        if ({step} >= 13) {{
            // 14단계: 애싱(ashing)을 통해 PR 제거
            if (PR12) {{
                scene.remove(PR12);
                PR2 = null;
                }}
        }}       
        if ({step} >= 14) {{
            // 15단계: 이온 주입후 확산
            if (wafer) {{
                scene.remove(wafer);
                wafer = null;
            }}
            if(!wafer) {{
                waferunder = createLayer(new THREE.BoxGeometry(4, 0.5, 3), 0x87CEFA, [0, -0.75, 0]);
                scene.add(waferunder);                
            }}
            if(!wafer) {{
                waferleft = createLayer(new THREE.BoxGeometry(0.25, 0.5, 3), 0x87CEFA, [-1.875, -0.25, 0]);
                scene.add(waferleft);
                waferright = createLayer(new THREE.BoxGeometry(0.25, 0.5, 3), 0x87CEFA, [1.875, -0.25, 0]);
                scene.add(waferright);
                wafertop = createLayer(new THREE.BoxGeometry(4, 0.5, 1), 0x87CEFA, [0, -0.25, -1]);
                scene.add(wafertop);
                wafermiddle = createLayer(new THREE.BoxGeometry(0.5, 0.5, 3), 0x87CEFA, [0, -0.25, 0]);
                scene.add(wafermiddle);                       
            }}
            if(!wafer) {{
                doppingNP = createLayer(new THREE.BoxGeometry(1.5, 0.5, 2), 0x4682B4, [-1, -0.25, 0.5]);
                scene.add(doppingNP);
                doppingN = createLayer(new THREE.BoxGeometry(1.5, 0.5, 2), 0x4682B4, [1, -0.25, 0.5]);
                scene.add(doppingN);                      
            }}
        }}               
        if ({step} >= 15) {{
            // 16단계: ILD(SiO2) 증착 후 CMP
            if(!wafer) {{
                ILDL = createLayer(new THREE.BoxGeometry(1, 0.5, 1.8), 0x8F8F8F, [-1, 0.25, 0.6]);
                scene.add(ILDL);
                ILDR = createLayer(new THREE.BoxGeometry(1, 0.5, 1.8), 0x8F8F8F, [1, 0.25, 0.6]);
                scene.add(ILDR); 
                ILD = createLayer(new THREE.BoxGeometry(4, 1, 3), 0x8F8F8F, [0, 1, 0]);
                scene.add(ILD);                   
            }}
        }} 
        if ({step} >= 16) {{
            // 17단계: PR 도포
            if(!wafer) {{
                PR17 = createLayer(new THREE.BoxGeometry(4, 0.2, 3), 0xFF0000, [0, 1.6, 0]);
                scene.add(PR17);
            }}
        }}     
        if ({step} >= 17) {{
            // 18단계: Mask 추가 후 노광 공정
            if(!wafer) {{
                ML18 = createLayer(new THREE.BoxGeometry(0.6, 0.2, 3), 0x000000, [-1.7, 2, 0]);
                MR18 = createLayer(new THREE.BoxGeometry(0.6, 0.2, 3), 0x000000, [1.7, 2, 0]);
                MML18 = createLayer(new THREE.BoxGeometry(0.2, 0.2, 3), 0x000000, [-0.5, 2, 0]);
                MMR18 = createLayer(new THREE.BoxGeometry(0.2, 0.2, 3), 0x000000, [0.5, 2, 0]);
                MT18 = createLayer(new THREE.BoxGeometry(4, 0.2, 1.2), 0x000000, [0, 2, -0.9]);

                scene.add(ML18);
                scene.add(MR18);
                scene.add(MML18);
                scene.add(MMR18);
                scene.add(MT18);
            }}
        }}             
        if ({step} >= 18) {{
            // 19단계: 현상
            if(!wafer) {{
                scene.remove(ML18);
                scene.remove(MR18);
                scene.remove(MML18);
                scene.remove(MMR18);
                scene.remove(MT18);
                
                ML18 = null;
                MR18 = null;
                MML18 = null;
                MMR18 = null;
                MT18 = null;

                scene.remove(PR17);
                PR17 = null;

                ML19 = createLayer(new THREE.BoxGeometry(0.6, 0.2, 3), 0xFF0000, [-1.7, 1.6, 0]);
                MR19 = createLayer(new THREE.BoxGeometry(0.6, 0.2, 3), 0xFF0000, [1.7, 1.6, 0]);
                MML19 = createLayer(new THREE.BoxGeometry(0.2, 0.2, 3), 0xFF0000, [-0.5, 1.6, 0]);
                MMR19 = createLayer(new THREE.BoxGeometry(0.2, 0.2, 3), 0xFF0000, [0.5, 1.6, 0]);
                MT19 = createLayer(new THREE.BoxGeometry(4, 0.2, 1.2), 0xFF0000, [0, 1.6, -0.9]);

                scene.add(ML19);
                scene.add(MR19);
                scene.add(MML19);
                scene.add(MMR19);
                scene.add(MT19);
            }}
        }}
        if ({step} >= 19) {{
            // 20단계: 식각(etching)을 통해 ILD 제거
            if(!wafer) {{
                scene.remove(ILDL);
                ILDL = null;
                scene.remove(ILDR);
                ILDR = null;
                scene.remove(ILD);
                ILD = null;

                ILDL19 = createLayer(new THREE.BoxGeometry(0.6, 1, 3), 0x8F8F8F, [-1.7, 1, 0]);
                ILDR19 = createLayer(new THREE.BoxGeometry(0.6, 1, 3), 0x8F8F8F, [1.7, 1, 0]);
                ILDT19 = createLayer(new THREE.BoxGeometry(4, 1, 1.2), 0x8F8F8F, [0, 1, -0.9]);
                ILDML19 = createLayer(new THREE.BoxGeometry(0.2, 1, 3), 0x8F8F8F, [-0.5, 1, 0]);
                ILDMR19 = createLayer(new THREE.BoxGeometry(0.2, 1, 3), 0x8F8F8F, [0.5, 1, 0]);

                scene.add(ILDL19);
                scene.add(ILDR19);
                scene.add(ILDT19);
                scene.add(ILDML19);
                scene.add(ILDMR19);

                ILDUL = createLayer(new THREE.BoxGeometry(0.1, 0.5, 1.8), 0x8F8F8F, [-1.45, 0.25, 0.6]);
                ILDUR = createLayer(new THREE.BoxGeometry(0.1, 0.5, 1.8), 0x8F8F8F, [1.45, 0.25, 0.6]);
                ILDUML = createLayer(new THREE.BoxGeometry(0.1, 0.5, 1.8), 0x8F8F8F, [-0.55, 0.25, 0.6]);
                ILDUMR = createLayer(new THREE.BoxGeometry(0.1, 0.5, 1.8), 0x8F8F8F, [0.55, 0.25, 0.6]);

                scene.add(ILDUL);
                scene.add(ILDUR);
                scene.add(ILDUML);
                scene.add(ILDUMR);
            }}
        }}     
        if ({step} >= 20) {{
            // 21단계: 애싱(ashing)을 통해 PR 제거
            if (!wafer) {{
                scene.remove(ML19);
                ML19 = null;
                scene.remove(MR19);
                MR19 = null;
                scene.remove(MML19);
                MML9 = null;
                scene.remove(MMR19);
                MMR19 = null;
                scene.remove(MT19);
                MT19 = null;
            }}             
        }}
        if ({step} >= 21) {{
            // 22단계: Metal(Al) 증착 후 CMP
            if (!wafer) {{
                ML22 = createLayer(new THREE.BoxGeometry(0.8, 1.5, 1.8), 0x800080, [-1, 0.75, 0.6]);
                MR22 = createLayer(new THREE.BoxGeometry(0.8, 1.5, 1.8), 0x800080, [1, 0.75, 0.6]);
                MM22 = createLayer(new THREE.BoxGeometry(0.8, 1, 1.8), 0x800080, [0, 1, 0.6]);
                M22 = createLayer(new THREE.BoxGeometry(4, 0.4, 3), 0x800080, [0, 1.7, 0]);
                scene.add(ML22);
                scene.add(MR22);
                scene.add(MM22);
                scene.add(M22);
            }}             
        }}
        if ({step} >= 22) {{
            // 23단계: PR 도포
            if (!wafer) {{
                PR23 = createLayer(new THREE.BoxGeometry(4, 0.2, 3), 0xFF0000, [0, 2, 0]);
                scene.add(PR23);
            }}             
        }}
        if ({step} >= 23) {{
            // 24단계: Mask 추가 후 노광 공정
            if (!wafer) {{
                ML24 = createLayer(new THREE.BoxGeometry(0.3, 0.2, 3), 0x000000, [-1.85, 2.4, 0]);
                MR24 = createLayer(new THREE.BoxGeometry(0.3, 0.2, 3), 0x000000, [1.85, 2.4, 0]);
                MML24 = createLayer(new THREE.BoxGeometry(0.1, 0.2, 3), 0x000000, [-0.5, 2.4, 0]);
                MMR24 = createLayer(new THREE.BoxGeometry(0.1, 0.2, 3), 0x000000, [0.5, 2.4, 0]);
                MT24 = createLayer(new THREE.BoxGeometry(4, 0.2, 1.2), 0x000000, [0, 2.4, -0.9]);
                scene.add(ML24);
                scene.add(MR24);
                scene.add(MML24);
                scene.add(MMR24);
                scene.add(MT24);
            }}             
        }}
        if ({step} >= 24) {{
            // 25단계: 현상
            if (!wafer) {{
                scene.remove(ML24);
                scene.remove(MR24);
                scene.remove(MML24);
                scene.remove(MMR24);
                scene.remove(MT24);
                ML24 = null;
                MR24 = null;
                MML24 = null;
                MMR24 = null;
                MR24 = null;

                scene.remove(PR23);
                PR23 = null;

                PRL25 = createLayer(new THREE.BoxGeometry(1.15, 0.2, 1.8), 0xFF0000, [-1.125, 2, 0.6]);
                PRR25 = createLayer(new THREE.BoxGeometry(1.15, 0.2, 1.8), 0xFF0000, [1.125, 2, 0.6]);
                PRM25 = createLayer(new THREE.BoxGeometry(0.9, 0.2, 1.8), 0xFF0000, [0, 2, 0.6]);
                scene.add(PRL25);
                scene.add(PRR25);
                scene.add(PRM25);
            }}             
        }}
        if ({step} >= 25) {{
            // 26단계: 식각(etching)을 통해 Metal 제거
            if (M22) {{
                scene.remove(M22);
                M22 = null;

                ML25 = createLayer(new THREE.BoxGeometry(1.15, 0.4, 1.8), 0x800080, [-1.125, 1.7, 0.6]);
                MR25 = createLayer(new THREE.BoxGeometry(1.15, 0.4, 1.8), 0x800080, [1.125, 1.7, 0.6]);
                MM25 = createLayer(new THREE.BoxGeometry(0.9, 0.4, 1.8), 0x800080, [0, 1.7, 0.6]);
                scene.add(ML25);
                scene.add(MR25);
                scene.add(MM25);
            }}             
        }}
        if ({step} >= 26) {{
            // 27단계: 애싱(ashing)을 통해 PR 제거
            if (!wafer) {{
                scene.remove(PRL25);
                PRL25 = null;
                scene.remove(PRR25);
                PRR25 = null;
                scene.remove(PRM25);
                PRM25 = null;

            }}             
        }}

        animate();
            function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
    }}

    init();
}});
</script>

<!-- 3D 시뮬레이션 화면 -->
<div class="three-js-container">
    <div id="3d-simulation" style="width: 100%; height: 350px;"></div>
</div>
"""

# Streamlit에서 HTML 포함
with st.container():
    st.markdown("<div class='stTitle'>MOSFET 3D 공정 시뮬레이션</div>", unsafe_allow_html=True)

    # 버튼 영역 생성
    st.write('<div class="button-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("이전"):
            if st.session_state['step'] > 0:
                st.session_state['step'] -= 1
                st.experimental_rerun()

    with col3:
        if st.button("다음"):
            if st.session_state['step'] < len(steps_description) - 1:
                st.session_state['step'] += 1
                st.experimental_rerun()

    st.write('</div>', unsafe_allow_html=True)

    # 현재 단계 표시 및 단계별 설명 박스
    st.write(f'<div class="step-display">현재 단계: {st.session_state["step"] + 1}</div>', unsafe_allow_html=True)
    st.write(f'<div class="description-box">{steps_description[st.session_state["step"]]}</div>', unsafe_allow_html=True)

    # 3D 시뮬레이션 HTML 삽입
    components.html(three_js_script_template.format(step=st.session_state['step']), height=400)
