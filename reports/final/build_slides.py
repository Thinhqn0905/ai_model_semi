from pathlib import Path
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/final'
INDEX = 'reports/figures/INDEX.md'
MENTOR = 'Instruction/Mentor_Feedback.md'
DEC = 'docs/decisions.md'
AI = 'reports/ai/ai_exp12_ds06.md'
SENS = 'reports/sensitivity/sens_v1.md'
BIZ = 'reports/economics/business_case_v1.md'
REPORT = 'reports/final/report_draft.md'
# Each slide carries its own evidence references; numbers are checked against these files.
slides = [
('ReGenATE', ['Intelligent energy coordination for regenerative test', 'Prove incremental value in shadow operation'], [MENTOR], None, 'LOCAL_RUN', 'Định vị giải pháp điều phối năng lượng; phần cứng tái sinh đã có sẵn. Giá trị tăng thêm cần được chứng minh ở chế độ giám sát.'),
('Context: the opportunity', ['Regenerative equipment already returns energy', 'Coordinate eligible tests to increase useful reuse', 'Primary measure: incremental grid energy at the cell meter versus existing regeneration'], [MENTOR, REPORT], None, 'LOCAL_RUN', 'Lợi ích cần so với thiết bị tái sinh hiện có tại đồng hồ của cell, không phải so với tải điện trở.'),
('The gap', ['Source and sink phases must overlap', 'Start-time flexibility and conversion losses determine the opportunity', 'Production priority and test integrity are hard constraints'], [MENTOR], None, 'LOCAL_RUN', 'Độ linh hoạt thực tế và tổn hao quyết định giá trị; không đánh đổi chất lượng lấy năng lượng.'),
('Choose the right cell', ['Converter burn-in: no residual source after in-rack reuse under the stated conditions', 'Shared-link incremental saving is 0 under equal efficiency and no cap', 'Storage or bidirectional cycling can create separate source and sink phases'], [DEC], None, 'SIM_ASSUMED_PROFILE', 'Kết quả bằng không là hệ quả vật lý dưới các giả định nêu rõ. Việc chọn cell vẫn chờ quyết định và dữ liệu thực tế.'),
('System architecture', ['Read-only meters and production constraints → forecast and scheduler', 'Energy ledger → bus twin → engineer approval → eligible start times', 'Independent protection remains outside the optimizer'], [MENTOR, REPORT], None, 'LOCAL_RUN', 'Hệ thống đọc dữ liệu, đề xuất lịch và kiểm tra bus; kỹ sư phê duyệt. Bảo vệ phần cứng hoạt động độc lập.'),
('Data and provenance', ['DS01: scheduling context • DS02: LVDC observations', 'DS03: equipment specifications • DS04: manufacturing forecasts', 'DS05: measured battery cycles; transfer to a site remains unverified'], [REPORT, INDEX], None, 'LOCAL_RUN / VENDOR_REPORTED', 'Mỗi bộ dữ liệu có vai trò khác nhau. Chu kỳ pin đo được không phải dữ liệu cell bán dẫn tại hiện trường.'),
('Method and matched comparison', ['Cell-meter energy ledger; exact small-instance MILP oracle', 'Rolling nominal and forecast-assisted plans; bus twin screens plans', 'Match instances, profile, bus limits and tardiness; report paired intervals'], [REPORT, MENTOR], None, 'SIM_ASSUMED_PROFILE', 'So sánh phải cùng bộ bài toán, hồ sơ công suất, giới hạn bus và độ trễ. Khoảng tin cậy được tính theo cặp.'),
('Baseline ladder', ['No recovery → regeneration → in-rack reuse → shared DC', 'Static optimization → rolling nominal → forecast-assisted → oracle', 'The figure shows assumed-profile simulation; it is not a site result'], [INDEX, REPORT], 'F08', 'SIM_ASSUMED_PROFILE', 'Thang cơ sở tách lợi ích phần cứng, liên kết DC, tối ưu và dự báo. Không diễn giải biểu đồ là kết quả tại nhà máy.'),
('Go / No-Go map', ['Converter cell: NO-GO against optimized in-rack reuse', 'Cycling cell: conditional GO; flexibility and loss assumptions matter', 'Solver gaps limit interpretation; cycle-scale cases above the supported range failed'], [DEC, SENS, INDEX], 'F10', 'SIM_ASSUMED_PROFILE', 'Cell converter không có nguồn dư; cell cycling có tiềm năng theo mô phỏng. Sai số giải và dữ liệu đo thực tế vẫn là giới hạn.'),
('Forecast accuracy comes first', ['Measured-data forecasting benchmarks demonstrate predictive skill', 'Accuracy alone does not establish downstream energy savings', 'Calibration and transfer to the target cell remain open'], [REPORT, INDEX], 'F03', 'LOCAL_RUN', 'Nêu kết quả dự báo riêng biệt trước khi xét hiệu quả của lịch. Độ chính xác dự báo không tự động tạo ra tiết kiệm điện.'),
('Forecast domains and uncertainty', ['Cross-domain comparisons use distinct measured datasets', 'Forecast uncertainty and deployment calibration need validation'], [INDEX, REPORT], 'F04', 'LOCAL_RUN', 'Các miền dữ liệu khác nhau không thể coi là tương đương. Cần hiệu chuẩn trên dữ liệu cell mục tiêu.'),
('Downstream AI result', ['Measured cycles with assumed station scaling and windows', 'Forecast variants are 0.2-0.3 % worse than nominal rolling optimization', 'Recommend nominal optimization for energy; peak-aware AI evaluation pending'], [AI, INDEX], 'F09', 'SIM_DATA_PROFILE', 'Các biến thể dự báo làm xấu chỉ tiêu năng lượng so với tối ưu không dự báo. Giữ kết quả âm và chọn giải pháp đơn giản hơn.'),
('Peak and oracle headroom', ['P0 peak: 11.34 kW; optimized in-rack baseline: 14.23 kW', 'Oracle energy headroom over P0: 0.094 kWh [0.077, 0.112]', 'Peak-aware forecast experiment remains pending'], [AI], None, 'SIM_DATA_PROFILE', 'Công suất đỉnh và khoảng cách tới oracle thuộc mô phỏng dùng chu kỳ đo nhưng cửa sổ và quy mô trạm giả định.'),
('Business case', ['Base case: alpha=1, behind-meter credit; assumed costs and duty cycle', 'S3 shared-link plus nominal plan: 9.65 [9.19, 10.12] kWh per instance vs regeneration', 'Payback 61.72 years [58.90, 64.82]; demand-charge dependence is assumed'], [BIZ], None, 'SIM_ASSUMED_PROFILE', 'Trường hợp cơ sở chưa hấp dẫn về kinh tế. Phí công suất, chi phí lắp đặt và tái thẩm định cần xác minh tại địa điểm.'),
('Safety, roadmap and ask', ['Failure injection and twin are simulation screens, not hardware proof', 'Shadow: measure profiles, flexibility, quality and incremental energy', 'Pilot only after engineering acceptance, protection and economic gates', 'Ask: select a cycling cell and provide metering and operational constraints'], [REPORT, MENTOR], None, 'SIM_ASSUMED_PROFILE', 'Đề nghị chọn cell phù hợp và cung cấp dữ liệu đo. Chỉ chuyển sang pilot khi đạt các cổng an toàn, chất lượng và kinh tế.'),
('Backup: uncertainty and calibration', ['Measured-cycle forecast diagnostics; calibration requires further validation'], [INDEX, REPORT], 'F12', 'LOCAL_RUN', 'Biểu đồ hỗ trợ thảo luận về độ bất định; chưa chứng minh giá trị vận hành.'),
('Backup: paired kill test', ['Optimized in-rack to oracle: 1.094 [1.037, 1.148] kWh', 'Measured-cycle simulation, with assumed scaling and operating windows'], [AI], None, 'SIM_DATA_PROFILE', 'Đây là chênh lệch theo cặp so với in-rack tối ưu, không phải so với tái sinh cơ sở.'),
('Backup: economics limits', ['Demand charges and representative monthly peaks are assumed', 'Installation, operating and requalification costs are unknown', 'No base option has positive net present value under modeled assumptions'], [BIZ], None, 'SIM_ASSUMED_PROFILE', 'Các giả định tài chính có thể thay đổi kết luận; chi phí chưa biết không được coi là bằng không.'),
('Backup: measurement and quality', ['Measure station profiles, movable windows, efficiency and cell import/export', 'Track throughput, matching ratio, bus excursions and test integrity', 'Water is a separate workstream pending direct metering'], [MENTOR, REPORT], None, 'LOCAL_RUN', 'Thu thập hồ sơ công suất và giới hạn vận hành, đồng thời theo dõi chất lượng và an toàn bus. Chưa định lượng nước.'),
]
prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
notes = ['# Speaker notes\n']
for i, (title, lines, sources, figure, boundary, note) in enumerate(slides, 1):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill; bg.solid(); bg.fore_color.rgb = RGBColor.from_string('0D1B2A')
    def box(text, x, y, w, h, size, color, bold=False):
        sh = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = sh.text_frame; tf.word_wrap = True
        tf.text = text
        for p in tf.paragraphs:
            p.font.name = 'Aptos'; p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = RGBColor.from_string(color)
        return sh
    box(title, .55, .3, 12, .7, 29, 'FFFFFF', True)
    width = 5.25 if figure else 11.9
    for j, line in enumerate(lines): box('• ' + line, .65, 1.35 + j * .85, width, .77, 20, 'DCE7EF')
    if figure:
        p = ROOT / 'reports/figures' / (figure + '.png')
        if not p.exists(): raise FileNotFoundError(p)
        slide.shapes.add_picture(str(p), Inches(6.1), Inches(1.18), width=Inches(6.65), height=Inches(4.9))
    box('Boundary: ' + boundary + ' | Sources: ' + '; '.join(sources), .5, 6.7, 12.4, .65, 9, 'B5C8D8')
    notes.append(f'## {title}\n\n{note}\n')
OUT.mkdir(parents=True, exist_ok=True)
path = OUT / 'ReGenATE_final.pptx'; prs.save(path)
(OUT / 'slides_notes.md').write_text('\n'.join(notes), encoding='utf-8')
# Validate every numeric token in native slide text against that slide's cited source text.
# Embedded figures are existing image artifacts: their internal labels are not machine checked.
opened = Presentation(path)
assert 18 <= len(opened.slides) <= 20, f'slide count: {len(opened.slides)}'
number = re.compile(r'(?<![\w.])\d+(?:\.\d+)?(?![\w.])')
issues = []
for i, (slide, spec) in enumerate(zip(opened.slides, slides), 1):
    corpus = '\n'.join((ROOT / s).read_text(encoding='utf-8') for s in spec[2])
    for shape in slide.shapes:
        if not shape.has_text_frame: continue
        for token in number.findall(shape.text_frame.text):
            if token not in corpus: issues.append(f'slide {i}: {token}')
if issues: raise ValueError('Unsupported numbers: ' + ', '.join(issues))
check = f'LOCAL_RUN: opened {path.relative_to(ROOT)}\nLOCAL_RUN: slide count {len(opened.slides)} (required 18-20)\nLOCAL_RUN: native text numeric tokens found in cited sources\nNOT_VERIFIED: numeric labels embedded in figure images are not OCR checked\n'
with (OUT / 'slides_notes.md').open('a', encoding='utf-8') as f: f.write('\n## Build check\n\n`	ext\n' + check + '`\n')
print(check)

