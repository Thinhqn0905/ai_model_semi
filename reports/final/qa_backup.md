# ReGenATE — Judge Q&A backup

Each answer is bounded by the cited evidence. Simulation is not site validation; financial assumptions are not investment approval.

## Positioning and physics

1. **ReGenATE là gì? / What is ReGenATE?**
   - VI: Giải pháp phối hợp năng lượng và lịch kiểm thử trong một cell. [Mentor](../../Instruction/Mentor_Feedback.md) — SOURCE_REPORTED.
   - EN: It coordinates energy and test schedules within one cell. [Mentor](../../Instruction/Mentor_Feedback.md) — SOURCE_REPORTED.
2. **AI tạo ra năng lượng tiết kiệm? / Does AI create the saving?**
   - VI: Không; phần cứng tái sinh thu hồi năng lượng, lịch quyết định khả năng ghép nguồn và tải. [Mentor](../../Instruction/Mentor_Feedback.md) — SOURCE_REPORTED.
   - EN: No; regeneration hardware recovers energy and scheduling affects source–sink matching. [Mentor](../../Instruction/Mentor_Feedback.md) — SOURCE_REPORTED.
3. **Chỉ số chính là gì? / What is the primary KPI?**
   - VI: Điện năng lưới giảm thêm tại M0 so với B1, cùng điều kiện và độ trễ. [Traceability](../../docs/traceability.md) — SOURCE_REPORTED.
   - EN: Incremental grid energy saved at M0 versus B1, under matched conditions and tardiness. [Traceability](../../docs/traceability.md) — SOURCE_REPORTED.
4. **Vì sao không chỉ dùng tái sinh sang AC? / Why not just regen-to-AC?**
   - VI: Đó là baseline cần vượt; liên kết DC chỉ đáng xét nếu giảm tổn hao chuyển đổi hoặc đem lại giá trị khác sau chi phí. [D001](../../docs/decisions.md) — ANALYTIC_UNIT_TEST; giá trị tại site NOT_VERIFIED.
   - EN: That is the baseline to beat; shared DC is justified only if it reduces conversion losses or adds other value after costs. [D001](../../docs/decisions.md) — ANALYTIC_UNIT_TEST; site value NOT_VERIFIED.
5. **Điều gì thay đổi sau slide 23/11? / What changed since the 23/11 deck?**
   - VI: Kill test chỉ ra burn-in bộ chuyển đổi không có nguồn dư sau tái sử dụng nội bộ; cần cell hai chiều có pha nguồn/tải tách biệt. [D001](../../docs/decisions.md); [audit](../../reports/audit/metric_audit.md) — ANALYTIC_UNIT_TEST; số slide cũ NOT_VERIFIED.
   - EN: The kill test found no residual source after in-rack reuse for converter burn-in; the candidate shifts to bidirectional cells with separated source/sink phases. [D001](../../docs/decisions.md); [audit](../../reports/audit/metric_audit.md) — ANALYTIC_UNIT_TEST; old deck figures NOT_VERIFIED.
6. **Vì sao chọn cell hai chiều? / Why a bidirectional cell?**
   - VI: Pha xả và nạp có thể tạo nguồn dư để trạm khác dùng; lựa chọn cuối cùng thuộc người dùng. [D001](../../docs/decisions.md); [traceability](../../docs/traceability.md) — ANALYTIC_UNIT_TEST; site NOT_VERIFIED.
   - EN: Separate discharge and charge phases can provide residual energy to other stations; the user must choose the final cell. [D001](../../docs/decisions.md); [traceability](../../docs/traceability.md) — ANALYTIC_UNIT_TEST; site NOT_VERIFIED.
7. **Baseline nào công bằng? / Which baseline is fair?**
   - VI: So sánh cùng instance, profile, giới hạn bus và tardiness; thêm B1p tối ưu để kiểm tra lợi ích DC thực sự. [Report](../../reports/final/report_draft.md) — SIM_ASSUMED_PROFILE.
   - EN: Match instances, profiles, bus limits and tardiness; include optimized B1p to isolate the shared-DC increment. [Report](../../reports/final/report_draft.md) — SIM_ASSUMED_PROFILE.
8. **Oracle chứng minh gì? / What does the oracle establish?**
   - VI: Nó ước lượng mức trần trong mô hình và điều kiện giải đã nêu, không phải hiệu năng vận hành thực tế. [Report](../../reports/final/report_draft.md) — SIM_ASSUMED_PROFILE; site NOT_VERIFIED.
   - EN: It estimates an upper bound within the stated model and solve conditions, not operational site performance. [Report](../../reports/final/report_draft.md) — SIM_ASSUMED_PROFILE; site NOT_VERIFIED.
9. **Nếu không có linh hoạt thì sao? / What if no scheduling flexibility exists?**
   - VI: Mô phỏng S3 vẫn có lợi ích topology; mức thực tế phụ thuộc nguồn dư, trùng thời gian và tổn hao. [Sensitivity](../../reports/sensitivity/sens_v1.md) — SIM_ASSUMED_PROFILE.
   - EN: Simulated S3 retains a topology benefit; actual benefit depends on residual energy, overlap and losses. [Sensitivity](../../reports/sensitivity/sens_v1.md) — SIM_ASSUMED_PROFILE.
10. **Tổn hao quan trọng thế nào? / How important are losses?**
   - VI: Hiệu suất AFE và liên kết ảnh hưởng trực tiếp lợi ích; cần đường cong hiệu suất đo được tại site. [Sensitivity](../../reports/sensitivity/sens_v1.md); [Mentor](../../Instruction/Mentor_Feedback.md) — SIM_ASSUMED_PROFILE; site NOT_VERIFIED.
   - EN: AFE and link efficiencies directly affect the benefit; site-measured efficiency curves are needed. [Sensitivity](../../reports/sensitivity/sens_v1.md); [Mentor](../../Instruction/Mentor_Feedback.md) — SIM_ASSUMED_PROFILE; site NOT_VERIFIED.

## AI and evidence

11. **Vì sao AI không thắng P0? / Why does AI not beat P0?**
   - VI: P0 đã tái lập lịch theo sự kiện, khoảng trống dự báo hoàn hảo nhỏ; nguyên nhân làm mượt chuyển pha chỉ là giả thuyết. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE.
   - EN: P0 already replans as jobs end, leaving little perfect-forecast headroom; transition smoothing is an unverified hypothesis. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE.
12. **Kết quả AI âm cụ thể? / What is the actual negative AI result?**
   - VI: Các biến thể dự báo dùng nhiều điện hơn P0 khoảng 0,2–0,3% trong DS06; CI chênh lệch kWh loại trừ 0. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE.
   - EN: Forecast variants used about 0.2–0.3% more energy than P0 in DS06; paired kWh intervals exclude zero. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE.
13. **Dự báo chính xác hơn có đủ? / Is better forecasting accuracy sufficient?**
   - VI: Không; phải chứng minh tác động downstream trên lịch, năng lượng hoặc đỉnh công suất. [DS06](../../reports/ai/ai_exp12_ds06.md); [Branch C](../../reports/ai/branch_C_ds05.md) — SIM_DATA_PROFILE; LOCAL_RUN on MEASURED data.
   - EN: No; a downstream scheduling, energy or peak benefit must be demonstrated. [DS06](../../reports/ai/ai_exp12_ds06.md); [Branch C](../../reports/ai/branch_C_ds05.md) — SIM_DATA_PROFILE; LOCAL_RUN on MEASURED data.
14. **Có nên giữ AI? / Should AI be retained?**
   - VI: Khuyến nghị P0 cho năng lượng; chỉ giữ AI nếu thử nghiệm phù hợp chứng minh thêm giá trị. [D004](../../docs/decisions.md) — SIM_DATA_PROFILE; lợi ích AI bổ sung NOT_VERIFIED.
   - EN: Recommend P0 for energy; retain AI only if an appropriate experiment demonstrates added value. [D004](../../docs/decisions.md) — SIM_DATA_PROFILE; further AI benefit NOT_VERIFIED.
15. **Vì sao tin dữ liệu tổng hợp? / Why should we believe synthetic data?**
   - VI: Không coi đó là bằng chứng tiết kiệm tại site; dùng để kiểm tra cơ chế và độ nhạy, rồi đối chiếu profile đo thực tế. [Mentor](../../Instruction/Mentor_Feedback.md); [Sensitivity](../../reports/sensitivity/sens_v1.md) — SIM_ASSUMED_PROFILE; site NOT_VERIFIED.
   - EN: It is not evidence of site savings; use it to test mechanisms and sensitivity, then validate against measured site profiles. [Mentor](../../Instruction/Mentor_Feedback.md); [Sensitivity](../../reports/sensitivity/sens_v1.md) — SIM_ASSUMED_PROFILE; site NOT_VERIFIED.
16. **DS06 có phải dữ liệu nhà máy? / Is DS06 factory data?**
   - VI: Không; chu kỳ pin DS05 là đo thực, nhưng số trạm, scaling và cửa sổ vận hành là giả định. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE.
   - EN: No; DS05 battery cycles are measured, but station count, scaling and operating windows are assumed. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE.
17. **Có rò rỉ dữ liệu train/test? / Is there train/test leakage?**
   - VI: Báo cáo DS06 nêu chỉ dùng chu kỳ test chưa dùng huấn luyện; khả năng chuyển sang site vẫn chưa xác minh. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE; site NOT_VERIFIED.
   - EN: DS06 reports use of held-out cycles excluded from forecaster training; site transfer is unverified. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE; site NOT_VERIFIED.
18. **Kết quả kill test DS06? / What is the DS06 kill-test result?**
   - VI: Oracle giảm trung bình 1,094 kWh so với B1p-OPT, CI 95% [1,037; 1,148], trên 100 cặp mô phỏng. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE.
   - EN: Oracle saves a mean 1.094 kWh versus B1p-OPT, 95% CI [1.037, 1.148], over 100 paired simulations. [DS06](../../reports/ai/ai_exp12_ds06.md) — SIM_DATA_PROFILE.
19. **Khoảng tin cậy có đủ chứng minh? / Does a confidence interval prove deployment value?**
   - VI: Không; CI mô tả bất định giữa instance, không bao gồm sai lệch mô hình và dữ liệu site thiếu. [Sensitivity](../../reports/sensitivity/sens_v1.md); [Report](../../reports/final/report_draft.md) — SIM_ASSUMED_PROFILE.
   - EN: No; the interval captures instance variation, not model error or missing site evidence. [Sensitivity](../../reports/sensitivity/sens_v1.md); [Report](../../reports/final/report_draft.md) — SIM_ASSUMED_PROFILE.
20. **Số liệu deck cũ dùng được không? / Can old deck figures be reused?**
   - VI: Không làm bằng chứng kết quả: liên kết run chưa xác lập và audit không tái tạo được các số đó. [Audit](../../reports/audit/metric_audit.md); [legacy audit](../../reports/audit/legacy_results.md) — NOT_VERIFIED.
   - EN: Not as results evidence: the run binding is missing and the audit could not reproduce those figures. [Audit](../../reports/audit/metric_audit.md); [legacy audit](../../reports/audit/legacy_results.md) — NOT_VERIFIED.
21. **Còn đỉnh công suất? / What about peak demand?**
   - VI: DS06 báo cáo P0 giảm đỉnh so với B1p-OPT trong mô phỏng; chưa suy ra hóa đơn nhu cầu thực. [DS06](../../reports/ai/ai_exp12_ds06.md); [business case](../../reports/economics/business_case_v1.md) — SIM_DATA_PROFILE; ASSUMED.
   - EN: DS06 reports a simulated P0 peak reduction versus B1p-OPT; this does not establish a real demand-charge saving. [DS06](../../reports/ai/ai_exp12_ds06.md); [business case](../../reports/economics/business_case_v1.md) — SIM_DATA_PROFILE; ASSUMED.

## Safety and operations

22. **Chất lượng kiểm thử có bị đánh đổi? / Is test integrity traded for energy?**
   - VI: Không theo thiết kế: recipe và tính toàn vẹn là ràng buộc cứng; hồ sơ chất lượng site chưa được kiểm chứng. [Mentor](../../Instruction/Mentor_Feedback.md); [Report](../../reports/final/report_draft.md) — SOURCE_REPORTED; site NOT_VERIFIED.
   - EN: Not by design: recipe and test integrity are hard constraints; site quality records remain unverified. [Mentor](../../Instruction/Mentor_Feedback.md); [Report](../../reports/final/report_draft.md) — SOURCE_REPORTED; site NOT_VERIFIED.
23. **Hệ thống được thay đổi điều gì? / What may the system change?**
   - VI: Thời điểm bắt đầu và trạm đủ điều kiện, không thay recipe hay tốc độ stress. [Audit](../../reports/audit/metric_audit.md) — design scope; site NOT_VERIFIED.
   - EN: Start time and eligible station, not the recipe or stress speed. [Audit](../../reports/audit/metric_audit.md) — design scope; site NOT_VERIFIED.
24. **Twin đã chứng minh bus an toàn? / Has the twin proved bus safety?**
   - VI: Chưa; twin chỉ sàng lọc mô phỏng với tham số giả định và bỏ qua một số khoảng thời gian. [Twin](../../reports/safety/bus_twin.md) — SIM_ASSUMED_PROFILE.
   - EN: No; the twin only screens simulations with assumed parameters and omitted time intervals. [Twin](../../reports/safety/bus_twin.md) — SIM_ASSUMED_PROFILE.
25. **Mất MES hay solver timeout thì sao? / What happens on MES loss or solver timeout?**
   - VI: Mô phỏng ghi nhận giữ kế hoạch hiện có; timeout được phát hiện sau khi callable trả về. [Failure injection](../../reports/safety/failure_injection.md) — SIM_ASSUMED_PROFILE.
   - EN: Simulation records fallback to the existing plan; timeout is detected after the callable returns. [Failure injection](../../reports/safety/failure_injection.md) — SIM_ASSUMED_PROFILE.
26. **Bảo vệ điện nào còn thiếu? / What electrical protection remains?**
   - VI: Cần thiết kế và kiểm chứng độc lập bảo vệ, cách ly, tương thích thiết bị và lỗi thực. [FMEA](../../reports/safety/fmea_v2.md); [Mentor](../../Instruction/Mentor_Feedback.md) — SIM_ASSUMED_PROFILE; hardware NOT_VERIFIED.
   - EN: Independent protection, isolation, equipment compatibility and real fault behavior need engineering and validation. [FMEA](../../reports/safety/fmea_v2.md); [Mentor](../../Instruction/Mentor_Feedback.md) — SIM_ASSUMED_PROFILE; hardware NOT_VERIFIED.
27. **FMEA có phải xác suất hỏng đo được? / Are FMEA scores measured failure probabilities?**
   - VI: Không; các điểm là nhận định kỹ thuật tạm thời cần đánh giá lại tại site. [FMEA](../../reports/safety/fmea_v2.md) — SIM_ASSUMED_PROFILE.
   - EN: No; the scores are provisional engineering judgments requiring site reassessment. [FMEA](../../reports/safety/fmea_v2.md) — SIM_ASSUMED_PROFILE.
28. **Ai quyết định triển khai lịch? / Who approves a schedule?**
   - VI: Kỹ sư phải chấp thuận trong quy trình đề xuất; từ chối giữ kế hoạch cũ trong mô phỏng. [Failure injection](../../reports/safety/failure_injection.md); [Mentor](../../Instruction/Mentor_Feedback.md) — SIM_ASSUMED_PROFILE; site NOT_VERIFIED.
   - EN: The proposed workflow requires engineer acceptance; simulated rejection retains the existing plan. [Failure injection](../../reports/safety/failure_injection.md); [Mentor](../../Instruction/Mentor_Feedback.md) — SIM_ASSUMED_PROFILE; site NOT_VERIFIED.
29. **Khi nào được pilot? / When can a pilot begin?**
   - VI: Sau shadow mode chứng minh điện giảm thêm sau tổn hao, không vi phạm test integrity, kỹ sư chấp thuận và xử lý bảo vệ, tương thích, kinh tế. [Mentor](../../Instruction/Mentor_Feedback.md); [Report](../../reports/final/report_draft.md) — site NOT_VERIFIED.
   - EN: After shadow mode demonstrates incremental energy after losses, no test-integrity violations, engineer acceptance, and adequate protection, compatibility and economics. [Mentor](../../Instruction/Mentor_Feedback.md); [Report](../../reports/final/report_draft.md) — site NOT_VERIFIED.
30. **Cần dữ liệu đầu tiên nào? / Which data should be collected first?**
   - VI: Công suất từng trạm đồng bộ thời gian, độ linh hoạt, hiệu suất converter, điện tại cell và hồ sơ chất lượng. [Mentor](../../Instruction/Mentor_Feedback.md) — SOURCE_REPORTED; site NOT_VERIFIED.
   - EN: Time-aligned station power, scheduling flexibility, converter efficiencies, cell metering and quality records. [Mentor](../../Instruction/Mentor_Feedback.md) — SOURCE_REPORTED; site NOT_VERIFIED.

## Economics, deployment and water

31. **Hoàn vốn bao lâu? / What is the payback?**
   - VI: Case S3 B1→P0 mô phỏng có hoàn vốn đơn giản 61,72 năm theo giả định cơ sở; chưa phải dự báo site. [Business case](../../reports/economics/business_case_v1.md) — SIM_ASSUMED_PROFILE + ASSUMED.
   - EN: The simulated S3 B1→P0 case has a 61.72-year simple payback under base assumptions; this is not a site forecast. [Business case](../../reports/economics/business_case_v1.md) — SIM_ASSUMED_PROFILE + ASSUMED.
32. **Dự án có đáng đầu tư không? / Is this investable now?**
   - VI: Chưa chứng minh; mọi phương án cơ sở trong báo cáo có NPV 10 năm âm và còn thiếu chi phí thực. [Business case](../../reports/economics/business_case_v1.md) — SIM_ASSUMED_PROFILE + ASSUMED.
   - EN: Not yet established; all reported base cases have negative 10-year NPV and real costs are missing. [Business case](../../reports/economics/business_case_v1.md) — SIM_ASSUMED_PROFILE + ASSUMED.
33. **Chi phí nào còn thiếu? / Which costs are missing?**
   - VI: Lắp đặt, vận hành và tái thẩm định chưa biết; số 0 trong mô hình là giả định lạc quan. [Business case](../../reports/economics/business_case_v1.md) — ASSUMED.
   - EN: Installation, operating and requalification costs are unknown; zero in the model is an optimistic placeholder. [Business case](../../reports/economics/business_case_v1.md) — ASSUMED.
34. **Có thể nhân rộng toàn fab? / Can results be scaled to the entire fab?**
   - VI: Không có cơ sở; trước hết chỉ xét cell được chọn và đo tại chỗ. [Mentor](../../Instruction/Mentor_Feedback.md); [Traceability](../../docs/traceability.md) — site NOT_VERIFIED.
   - EN: There is no basis for fab-wide extrapolation; first assess the chosen cell with site measurements. [Mentor](../../Instruction/Mentor_Feedback.md); [Traceability](../../docs/traceability.md) — site NOT_VERIFIED.
35. **Tiết kiệm nước bao nhiêu? / How much water is saved?**
   - VI: Chưa xác minh; cần đo lưu lượng, chênh nhiệt, tải nhiệt và nước chiller/tháp giải nhiệt. [Mentor](../../Instruction/Mentor_Feedback.md); [Report](../../reports/final/report_draft.md) — NOT_VERIFIED.
   - EN: Unknown; cooling flow, temperature difference, heat load and chiller/tower water must be measured. [Mentor](../../Instruction/Mentor_Feedback.md); [Report](../../reports/final/report_draft.md) — NOT_VERIFIED.

## Run 2: calibration and electrical sizing

36. **T?i ?u ??nh mang l?i g?? / What does peak-aware optimization add?**
   - VI: Tr?n 50 c?p DS06, b??c t?i ?u ??nh gi?m ??nh P0 trung b?nh 0,449 kW (CI 95% [0,120; 0,830]), kh?ng ??i ?i?n n?ng ??ng k?; kh?ng bi?n th? AI n?o c?i thi?n ??nh v?i CI lo?i tr? 0. [DS06](../../reports/ai/ai_exp12_ds06.md) ? SIM_DATA_PROFILE; site NOT_VERIFIED.
   - EN: Across 50 paired DS06 instances, the peak stage reduced mean P0 peak by 0.449 kW (95% CI [0.120, 0.830]) with no significant energy change; no AI variant improved peak with a CI excluding zero. [DS06](../../reports/ai/ai_exp12_ds06.md) ? SIM_DATA_PROFILE; site NOT_VERIFIED.
37. **CQR c? ??m b?o th?i ?i?m ho?n th?nh? / Does CQR guarantee completion time?**
   - VI: Kh?ng; CQR hi?u chu?n tr?n t?p validation, nh?ng coverage kho?ng 80% cho th?i l??ng c?n l?i ch? ??t 75,5% tr?n test; P90 kh?ng ph?i gi?i h?n b?o ??m. [Branch C](../../reports/ai/branch_C_ds05.md) ? LOCAL_RUN on MEASURED data; site NOT_VERIFIED.
   - EN: No; CQR calibrates on validation, but the nominal 80% remaining-duration interval covers 75.5% on test; P90 is not a guaranteed bound. [Branch C](../../reports/ai/branch_C_ds05.md) ? LOCAL_RUN on MEASURED data; site NOT_VERIFIED.
38. **T?ng k?ch th??c AFE c? ?? ?? bus an to?n? / Is a larger AFE sufficient for bus safety?**
   - VI: Ch?a; m? ph?ng cho th?y l?ch k?ch th??c AFE v? v?n c? qu? d?ng ho?c th?p ?p khi t?ng c?ng su?t. D?ng link, ??ng h?c v? b?o v? ??c l?p c?n ???c thi?t k? v? ki?m ch?ng; c?ng su?t AC ledger ch? l? proxy. [Bus KPI](../../reports/safety/bus_stability_kpi.md) ? SIM_ASSUMED_PROFILE; hardware NOT_VERIFIED.
   - EN: No; the simulation indicates an AFE sizing mismatch and still reports overcurrent or undervoltage with larger capacity. Link current, dynamics and independent protection require design and validation; AC ledger power is only a sizing proxy. [Bus KPI](../../reports/safety/bus_stability_kpi.md) ? SIM_ASSUMED_PROFILE; hardware NOT_VERIFIED.
 
 # #   R u n   2   c i t a t i o n   g a t e   ?   L O C A L _ R U N  
 Q u e s t i o n s :   3 8 ;   b i l i n g u a l   a n s w e r s :   7 6 ;   m i s s i n g   c i t a t i o n   o r   b o u n d a r y :   0 ;   b r o k e n   l i n k s :   0 .  
 R e s u l t :   P A S S .   S c o p e :   d o c u m e n t   s t r u c t u r e   a n d   l o c a l   c i t a t i o n   l i n k s   o n l y ;   u n d e r l y i n g   c l a i m s   r e t a i n   t h e i r   s t a t e d   b o u n d a r i e s .  
 