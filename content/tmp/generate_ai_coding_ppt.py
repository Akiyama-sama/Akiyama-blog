from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

NAVY = RGBColor(9, 18, 34)
INK = RGBColor(23, 31, 43)
COBALT = RGBColor(46, 109, 246)
CYAN = RGBColor(78, 201, 240)
CORAL = RGBColor(255, 99, 72)
AMBER = RGBColor(255, 179, 64)
IVORY = RGBColor(248, 246, 240)
WHITE = RGBColor(255, 255, 255)
MUTED = RGBColor(109, 118, 132)
BORDER = RGBColor(221, 227, 236)
PALE_BLUE = RGBColor(235, 243, 255)
PALE_YELLOW = RGBColor(255, 246, 214)
PALE_CORAL = RGBColor(255, 235, 229)
PALE_NAVY = RGBColor(230, 235, 244)

LEFT = Inches(0.72)
TOP = Inches(0.52)
CONTENT_W = Inches(11.9)


def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def textbox(slide, x, y, w, h, text="", size=20, color=INK, bold=False,
            font="Aptos", align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    return box


def paragraph_box(slide, x, y, w, h, paragraphs, size=18, color=INK, bullet=False):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, item in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(10)
        text = f"• {item}" if bullet else item
        r = p.add_run()
        r.text = text
        r.font.name = "Aptos"
        r.font.size = Pt(size)
        r.font.color.rgb = color
    return box


def footer(slide, n, dark=False):
    color = RGBColor(184, 191, 203) if dark else RGBColor(144, 152, 164)
    textbox(slide, Inches(12.1), Inches(6.96), Inches(0.55), Inches(0.25),
            str(n), size=12, color=color, align=PP_ALIGN.RIGHT)


def kicker(slide, text, dark=False):
    color = RGBColor(193, 201, 214) if dark else MUTED
    textbox(slide, LEFT, TOP, Inches(5.5), Inches(0.3), text, size=14, color=color)


def bar(slide, color=COBALT):
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, LEFT, Inches(0.72), Inches(1.24), Inches(0.06))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def title(slide, text, sub=None, dark=False, y=Inches(0.98)):
    c = WHITE if dark else INK
    s = RGBColor(197, 203, 214) if dark else MUTED
    size = 34 if len(text) < 20 else 29
    textbox(slide, LEFT, y, Inches(10.9), Inches(0.9), text, size=size, color=c, bold=True)
    if sub:
        textbox(slide, LEFT, y + Inches(0.72), Inches(10.6), Inches(0.45), sub, size=16, color=s)


def card(slide, x, y, w, h, heading, body, fill=WHITE, line=BORDER,
         head_color=INK, body_color=MUTED, head_size=21, body_size=16, radius=True):
    shape_type = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(1.2)
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    r1 = p1.add_run()
    r1.text = heading
    r1.font.name = "Aptos Display"
    r1.font.size = Pt(head_size)
    r1.font.bold = True
    r1.font.color.rgb = head_color
    if body:
        p2 = tf.add_paragraph()
        p2.space_before = Pt(10)
        r2 = p2.add_run()
        r2.text = body
        r2.font.name = "Aptos"
        r2.font.size = Pt(body_size)
        r2.font.color.rgb = body_color
    return shape


def stat_card(slide, x, y, w, h, value, label, fill=WHITE, accent=COBALT, dark_text=False):
    body = INK if dark_text else WHITE
    muted = MUTED if dark_text else RGBColor(210, 218, 231)
    line = accent if fill == WHITE else fill
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(1.4)
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.LEFT
    r1 = p1.add_run()
    r1.text = value
    r1.font.name = "Aptos Display"
    r1.font.size = Pt(30)
    r1.font.bold = True
    r1.font.color.rgb = accent if fill == WHITE else body
    p2 = tf.add_paragraph()
    p2.space_before = Pt(8)
    r2 = p2.add_run()
    r2.text = label
    r2.font.name = "Aptos"
    r2.font.size = Pt(15)
    r2.font.color.rgb = muted
    return shape


def divider(slide, x, y, w, color=BORDER):
    line = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, x, y, w, Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()


def big_quote(slide, text, note=None, dark=False):
    c = WHITE if dark else INK
    s = RGBColor(189, 196, 208) if dark else MUTED
    textbox(slide, LEFT, Inches(2.15), Inches(10.8), Inches(2.0), f"“{text}”", size=28, color=c, bold=True)
    if note:
        textbox(slide, LEFT, Inches(4.6), Inches(10.4), Inches(0.55), note, size=16, color=s)


def process_row(slide, labels, colors, y):
    x = LEFT
    widths = [Inches(2.0), Inches(1.7), Inches(2.25), Inches(1.8), Inches(1.3)]
    for i, label in enumerate(labels):
        shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, y, widths[i], Inches(0.86))
        shape.fill.solid()
        shape.fill.fore_color.rgb = colors[i]
        shape.line.color.rgb = colors[i] if colors[i] != WHITE else BORDER
        tf = shape.text_frame
        tf.clear()
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        r = tf.paragraphs[0].add_run()
        r.text = label
        r.font.name = "Aptos"
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = WHITE if colors[i] in (COBALT, CORAL, NAVY) else INK
        x += widths[i] + Inches(0.14)
        if i < len(labels) - 1:
            textbox(slide, x - Inches(0.1), y + Inches(0.18), Inches(0.14), Inches(0.2), "→", size=16, color=MUTED)


def lane(slide, x, y, label):
    textbox(slide, x, y, Inches(1.6), Inches(0.3), label, size=16, color=MUTED)
    specs = [
        ("Explore", PALE_NAVY, INK),
        ("Implement", COBALT, WHITE),
        ("Verify", PALE_BLUE, INK),
        ("Review", PALE_CORAL, INK),
    ]
    cy = y + Inches(0.42)
    for title_txt, fill, color in specs:
        shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, cy, Inches(2.25), Inches(0.52))
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
        shape.line.color.rgb = fill if fill in (COBALT,) else BORDER
        tf = shape.text_frame
        tf.clear()
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        r = tf.paragraphs[0].add_run()
        r.text = title_txt
        r.font.name = "Aptos"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = color
        cy += Inches(0.64)


def chapter_slide(prs, no, chapter, text):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    accent = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.22))
    accent.fill.solid()
    accent.fill.fore_color.rgb = COBALT
    accent.line.fill.background()
    textbox(slide, LEFT, Inches(1.75), Inches(3.0), Inches(0.3), chapter, size=18, color=RGBColor(188, 196, 210))
    textbox(slide, LEFT, Inches(2.45), Inches(10.4), Inches(1.4), text, size=40, color=WHITE, bold=True)
    footer(slide, no, dark=True)
    return slide


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    # 1 Cover
    slide = prs.slides.add_slide(blank)
    bg(slide, NAVY)
    band = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(8.6), Inches(0), Inches(4.733), Inches(7.5))
    band.fill.solid()
    band.fill.fore_color.rgb = RGBColor(17, 30, 54)
    band.line.fill.background()
    dot = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.OVAL, Inches(10.45), Inches(1.15), Inches(1.55), Inches(1.55))
    dot.fill.solid()
    dot.fill.fore_color.rgb = COBALT
    dot.line.fill.background()
    textbox(slide, LEFT, Inches(1.1), Inches(4.8), Inches(0.3), "设计模式课程分享", size=18, color=RGBColor(191, 198, 210))
    textbox(slide, LEFT, Inches(1.85), Inches(7.3), Inches(0.8), "AI Coding", size=30, color=CYAN, bold=True)
    textbox(slide, LEFT, Inches(2.55), Inches(8.9), Inches(1.5), "一年实战：\n从效率幻觉到能力进化", size=40, color=WHITE, bold=True)
    textbox(slide, LEFT, Inches(5.25), Inches(7.8), Inches(0.45), "关键词：瓶颈、Spec、验证闭环、并发、能力进化", size=18, color=RGBColor(191, 198, 210))
    footer(slide, 1, dark=True)

    # 2 Thesis
    slide = prs.slides.add_slide(blank)
    bg(slide, IVORY)
    kicker(slide, "01 文章主论点")
    bar(slide)
    title(slide, "这篇文章最重要的，不是工具，而是系统视角", "它把讨论从“快不快”抬到了“瓶颈、流程与能力结构”")
    card(slide, LEFT, Inches(2.0), Inches(3.55), Inches(1.55),
         "局部提速 ≠ 系统提效", "AI 把编码变快，但交付吞吐量受瓶颈约束。", fill=WHITE, line=BORDER, head_size=24, body_size=18)
    card(slide, Inches(4.38), Inches(2.0), Inches(3.55), Inches(1.55),
         "概念澄清很关键", "Spec / Rule / Skill 混在一起，会直接拉低效果。", fill=WHITE, line=BORDER, head_size=24, body_size=18)
    card(slide, Inches(8.04), Inches(2.0), Inches(3.55), Inches(1.55),
         "真正红利是能力升级", "省下来的时间该投向学习、分析和高阶判断。", fill=WHITE, line=BORDER, head_size=24, body_size=18)
    footer(slide, 2)

    # 3 Data paradox
    slide = prs.slides.add_slide(blank)
    bg(slide, WHITE)
    kicker(slide, "02 开篇的反直觉证据")
    bar(slide)
    title(slide, "你以为快了，但实验与组织数据都在泼冷水", "这也是全文最抓人的开场")
    stat_card(slide, LEFT, Inches(2.05), Inches(2.5), Inches(1.6), "慢了 19%", "METR 预注册 RCT：资深开发者使用 AI 后，客观完成时间变慢", fill=WHITE, accent=CORAL, dark_text=True)
    stat_card(slide, Inches(3.55), Inches(2.05), Inches(2.5), Inches(1.6), "快了 20%", "同一批人主观却认为自己更快了，主客观偏差极大", fill=COBALT, accent=COBALT)
    stat_card(slide, Inches(6.3), Inches(2.05), Inches(2.5), Inches(1.6), "90% / 3.1%", "大量开发者在用 AI，但真正高度信任它的人很少", fill=NAVY, accent=NAVY)
    stat_card(slide, Inches(9.05), Inches(2.05), Inches(2.5), Inches(1.6), "PR +154%", "Faros 数据显示个体产出增加，但评审时间也显著拉长", fill=WHITE, accent=AMBER, dark_text=True)
    paragraph_box(slide, LEFT, Inches(4.45), Inches(11.6), Inches(1.55), [
        "文章做得好的地方，在于没有停在“AI 有幻觉”这种泛结论，",
        "而是进一步追问：为什么个体提效，没有转化成组织吞吐量？"
    ], size=19, color=INK)
    footer(slide, 3)

    # 4 bottleneck
    slide = prs.slides.add_slide(blank)
    bg(slide, WHITE)
    kicker(slide, "03 第一层解释：瓶颈")
    bar(slide)
    title(slide, "真正的约束，往往不在编码，而在 review 和验证", "这是文章把局部效率问题提升到系统效率问题的关键一步")
    process_row(slide, ["需求理解", "编码", "Code Review", "测试验证", "交付"],
                [WHITE, COBALT, CORAL, WHITE, WHITE], Inches(2.65))
    paragraph_box(slide, LEFT, Inches(4.15), Inches(6.2), Inches(1.85), [
        "AI 更像把编码工位变成 NCX-10。",
        "如果瓶颈其实在 review，那么更快的生成只会制造更多排队。"
    ], size=22, color=INK)
    big_quote(slide, "系统吞吐量由瓶颈决定，不由最快的环节决定")
    footer(slide, 4)

    # 5 frameworks
    slide = prs.slides.add_slide(blank)
    bg(slide, NAVY)
    kicker(slide, "04 第二层解释：别先纠结框架", dark=True)
    bar(slide, color=CYAN)
    title(slide, "OpenSpec、Superpowers、BMAD、Spec Kit，本质都在做同一件事", "AI Coding 框架之争，有点像当年的 JS Framework Fatigue", dark=True)
    xs = [LEFT, Inches(3.75), Inches(6.78), Inches(9.8)]
    items = [
        ("OpenSpec", "偏系统化\n按 SDLC 阶段组织"),
        ("Superpowers", "偏灵活\n适合个人渐进采用"),
        ("BMAD", "偏流程\n强调协作与步骤"),
        ("Spec Kit", "偏模板\n沉淀规范与文档"),
    ]
    for x, item in zip(xs, items):
        card(slide, x, Inches(3.0), Inches(2.45), Inches(1.8), item[0], item[1],
             fill=RGBColor(19, 33, 58), line=RGBColor(51, 73, 111),
             head_color=WHITE, body_color=RGBColor(201, 209, 222), head_size=22, body_size=16)
    textbox(slide, LEFT, Inches(5.6), Inches(11.7), Inches(0.6),
            "结论：它们的共同目标，是把 SDLC 中重复度高的上下文与提示，沉淀成可复用 Skill。", size=19, color=WHITE)
    footer(slide, 5, dark=True)

    # 6 chapter divider
    chapter_slide(prs, 6, "Part Two", "Spec / Rule / Skill 是全文的方法论核心")

    # 7 spec rule skill
    slide = prs.slides[-1]
    # Need current slide is chapter; add next actual slide.
    slide = prs.slides.add_slide(blank)
    bg(slide, WHITE)
    kicker(slide, "05 方法论核心")
    bar(slide)
    title(slide, "Spec、Rule、Skill 不是同义词", "分不清这三个概念，AI 工作流会直接变形")
    card(slide, LEFT, Inches(2.2), Inches(3.1), Inches(3.0), "Spec", "业务知识\n回答：做什么\n描述当前状态、目标状态、兼容边界", fill=PALE_BLUE, line=COBALT, head_color=COBALT, body_color=INK, head_size=24, body_size=17)
    card(slide, Inches(4.4), Inches(2.2), Inches(3.0), Inches(3.1), "Rule", "工程规范\n回答：约束是什么\n应该短、小、稳定、始终加载", fill=PALE_YELLOW, line=AMBER, head_color=AMBER, body_color=INK, head_size=24, body_size=17)
    card(slide, Inches(8.0), Inches(2.2), Inches(3.0), Inches(3.1), "Skill", "工作流\n回答：怎么做\n按需加载，可带 SOP、示例、脚本", fill=PALE_CORAL, line=CORAL, head_color=CORAL, body_color=INK, head_size=24, body_size=17)
    textbox(slide, LEFT, Inches(5.75), Inches(11.7), Inches(0.45),
            "一句话：Spec 是上下文，Rule 是底线，Skill 是执行器。", size=22, color=INK, bold=True)
    footer(slide, 7)

    # 8 why spec
    slide = prs.slides.add_slide(blank)
    bg(slide, IVORY)
    kicker(slide, "06 为什么 Spec 不能省")
    bar(slide)
    title(slide, "AI 会读代码，但不会自动替你理解业务", "尤其在存量系统、兼容性要求高、规则复杂的场景里")
    paragraph_box(slide, LEFT, Inches(2.15), Inches(5.7), Inches(2.5), [
        "跳过 Spec，模型只能从代码里猜意图。",
        "猜对一次没意义，猜错一次就可能吞掉前面所有提速。",
        "最小可行 Spec 也该说清：当前行为、目标行为、不变项、边界条件。"
    ], size=20, color=INK, bullet=True)
    card(slide, Inches(8.0), Inches(2.45), Inches(3.6), Inches(2.3),
         "作者的关键判断", "Spec 不是给 AI 增负担，\n而是把它的起点从“猜意图”\n抬到“理解业务后做决策”。",
         fill=WHITE, line=COBALT, head_color=COBALT, body_color=INK, head_size=24, body_size=20)
    footer(slide, 8)

    # 9 why skill obeys better
    slide = prs.slides.add_slide(blank)
    bg(slide, WHITE)
    kicker(slide, "07 为什么 Skill 比 Rule 更有效")
    bar(slide)
    title(slide, "因为按需加载，信噪比更高，而且更靠近任务尾部", "这一段把工程实践和 LLM 注意力问题连起来了")
    card(slide, LEFT, Inches(2.25), Inches(4.85), Inches(2.9),
         "长 Rule", "50 条常驻规则里，真正和当前任务相关的可能只有 3 条。\n其余都是噪声。",
         fill=WHITE, line=BORDER, head_color=CORAL, body_color=INK, head_size=24, body_size=18)
    card(slide, Inches(7.05), Inches(2.25), Inches(4.85), Inches(2.9),
         "按需 Skill", "只在当前任务出现，内容高度聚焦。\n还能带 SOP、few-shot、脚本调用，遵循性自然更强。",
         fill=PALE_BLUE, line=COBALT, head_color=COBALT, body_color=INK, head_size=24, body_size=18)
    textbox(slide, Inches(5.88), Inches(3.32), Inches(1.0), Inches(0.3), "VS", size=20, color=MUTED, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, LEFT, Inches(5.72), Inches(11.7), Inches(0.5),
            "文章还引用了 Lost in the Middle / LongPiBench：位置偏差虽缓解，但相关信息间距问题仍然存在。", size=18, color=MUTED)
    footer(slide, 9)

    # 10 verify + swiss cheese
    slide = prs.slides.add_slide(blank)
    bg(slide, NAVY)
    kicker(slide, "08 质量底线：给 AI 一根安灯绳", dark=True)
    bar(slide, color=CYAN)
    title(slide, "生成之后，必须立刻进入 verify 闭环", "安灯绳 + 瑞士奶酪模型，是这一章最好的比喻", dark=True)
    x = LEFT
    steps = [("Generate", RGBColor(23, 38, 68)), ("Verify", COBALT), ("Fix / Log", RGBColor(23, 38, 68))]
    for label, fill in steps:
        card(slide, x, Inches(2.45), Inches(3.2), Inches(1.18), label, "",
             fill=fill, line=fill, head_color=WHITE, body_color=WHITE, head_size=26, body_size=14)
        x += Inches(3.55)
    divider(slide, LEFT, Inches(4.55), Inches(11.7), color=RGBColor(50, 72, 109))
    paragraph_box(slide, LEFT, Inches(4.75), Inches(11.8), Inches(1.25), [
        "Lint 拦基础错误",
        "Unit Test 拦边界条件",
        "E2E 拦流程断裂",
        "Review 拦深层设计问题"
    ], size=19, color=WHITE, bullet=True)
    footer(slide, 10, dark=True)

    # 11 trust mechanism
    slide = prs.slides.add_slide(blank)
    bg(slide, WHITE)
    kicker(slide, "09 信任结构")
    bar(slide)
    title(slide, "你不是在信任 AI 本身，而是在信任拦截机制", "这是文章中最成熟的一层判断")
    card(slide, LEFT, Inches(2.3), Inches(3.9), Inches(2.3),
         "过去", "有人愿意信外包交付，\n并不是因为外包更聪明，\n而是因为后面有 Review 和 QA。", fill=WHITE, line=BORDER, head_size=24, body_size=18)
    card(slide, Inches(4.6), Inches(2.3), Inches(4.1), Inches(2.3),
         "现在", "同一套机制套在 AI 上，信任基础并没有本质区别。\n差别只在于：深层设计判断仍然需要人。", fill=PALE_BLUE, line=COBALT, head_color=COBALT, body_color=INK, head_size=24, body_size=18)
    card(slide, Inches(8.5), Inches(2.3), Inches(2.3), Inches(3.9),
         "角色变化", "工程师不再主要是逐行执行者，\n而更像流程调度员与架构判断者。", fill=PALE_YELLOW, line=AMBER, head_color=AMBER, body_color=INK, head_size=24, body_size=18)
    footer(slide, 11)

    # 12 concurrency
    slide = prs.slides.add_slide(blank)
    bg(slide, IVORY)
    kicker(slide, "10 真正的效率杠杆")
    bar(slide)
    title(slide, "单任务变慢不是关键，能不能并发才是关键", "但前提是：每个任务跑完后，你能快速判断它是否合格")
    lane(slide, LEFT, Inches(2.1), "任务 A")
    lane(slide, Inches(3.9), Inches(2.1), "任务 B")
    lane(slide, Inches(7.08), Inches(2.1), "任务 C")
    card(slide, Inches(10.1), Inches(2.25), Inches(2.5), Inches(2.8),
         "文章的计算逻辑", "如果完整流程让单任务慢 50%，\n并发 2 个仍有 1.33x 产出；\n并发 3 个可接近 2x。",
         fill=WHITE, line=COBALT, head_color=COBALT, body_color=INK, head_size=22, body_size=17)
    footer(slide, 12)

    # 13 WIP
    slide = prs.slides.add_slide(blank)
    bg(slide, WHITE)
    kicker(slide, "11 并发的边界")
    bar(slide)
    title(slide, "并发不是多开窗口，而是受 WIP 限制的并行协作", "否则只会把第一章的问题扩大")
    stat_card(slide, LEFT, Inches(2.15), Inches(3.0), Inches(1.55), "PR 不能太大", "生成端一旦产出巨型 PR，review 端会立刻窒息", fill=WHITE, accent=CORAL, dark_text=True)
    stat_card(slide, Inches(3.55), Inches(2.15), Inches(3.0), Inches(1.55), "并发度 2-3", "文章给出的现实判断，比“无限开 session”更可信", fill=WHITE, accent=AMBER, dark_text=True)
    stat_card(slide, Inches(6.3), Inches(2.15), Inches(3.0), Inches(1.55), "先建 verify", "验证闭环越可靠，越敢脱手，能支持的并发度越高", fill=COBALT, accent=COBALT)
    stat_card(slide, Inches(9.05), Inches(2.15), Inches(3.0), Inches(1.55), "保护 reviewer", "并发加速生成端，WIP 限制保护下游评审端", fill=NAVY, accent=NAVY)
    footer(slide, 13)

    # 14 laundry
    slide = prs.slides.add_slide(blank)
    bg(slide, NAVY)
    kicker(slide, "12 最值得记住的一章", dark=True)
    bar(slide, color=CYAN)
    title(slide, "有了洗衣机，你可能只是在洗更多衣服", "技术提升了效率，也提高了标准；苦差事没有消失，只是换了形式", dark=True)
    card(slide, LEFT, Inches(2.45), Inches(3.55), Inches(2.7),
         "过去的苦差事", "手写样板代码\n重复劳动\n机械搬运", fill=RGBColor(21, 35, 61), line=RGBColor(53, 76, 114), head_color=WHITE, body_color=RGBColor(203, 211, 223), head_size=24, body_size=18)
    card(slide, Inches(4.55), Inches(2.45), Inches(3.15), Inches(3.55),
         "现在的苦差事", "读 AI 代码\n找“差不多对”的 bug\n消化更大的 PR\n管理返工与技术债", fill=RGBColor(22, 40, 69), line=COBALT, head_color=CYAN, body_color=RGBColor(215, 223, 234), head_size=24, body_size=18)
    card(slide, Inches(8.25), Inches(2.45), Inches(3.15), Inches(3.55),
         "真正要避免的陷阱", "如果省下来的时间只用来写更多代码，\n那只是线性提效，不是能力进化。", fill=RGBColor(21, 35, 61), line=RGBColor(53, 76, 114), head_color=WHITE, body_color=RGBColor(203, 211, 223), head_size=24, body_size=18)
    footer(slide, 14, dark=True)

    # 15 capability evolution
    slide = prs.slides.add_slide(blank)
    bg(slide, WHITE)
    kicker(slide, "13 作者真正想落到的地方")
    bar(slide)
    title(slide, "AI 的终点，不是更快写代码，而是做以前做不到的事", "文章用“10 个 Agent 并行拆解报告”的例子，把效率提升拉到了能力提升")
    card(slide, LEFT, Inches(2.35), Inches(3.7), Inches(2.4),
         "以前", "最多精读 1-2 篇报告\n其余只能看二手总结", fill=WHITE, line=BORDER, head_size=24, body_size=18)
    card(slide, Inches(4.55), Inches(2.35), Inches(3.4), Inches(3.7),
         "现在", "用统一框架让多个 Agent 并行拆解报告，\n再由主 Agent 聚合、交叉验证、标注偏见与置信度。", fill=PALE_BLUE, line=COBALT, head_color=COBALT, body_color=INK, head_size=24, body_size=18)
    card(slide, Inches(8.25), Inches(2.35), Inches(3.0), Inches(3.7),
         "能力进化", "你获得的不是“更快摘要”，\n而是对冲突结论、方法论差异、证据质量的判断力。", fill=PALE_YELLOW, line=AMBER, head_color=AMBER, body_color=INK, head_size=24, body_size=18)
    footer(slide, 15)

    # 16 action / q&a
    slide = prs.slides.add_slide(blank)
    bg(slide, IVORY)
    kicker(slide, "14 课堂汇报收束")
    bar(slide)
    title(slide, "如果只带走三句话，我会带走这三句", "也是这篇文章最值得继续实践的三件事")
    paragraph_box(slide, LEFT, Inches(2.2), Inches(11.0), Inches(3.7), [
        "第一，AI 加速的环节必须是瓶颈，否则只会制造堆积。",
        "第二，Spec / Rule / Skill 要分清，验证闭环要先建好。",
        "第三，别把节省下来的时间全部换成更多代码，要换成更高阶的能力。"
    ], size=23, color=INK, bullet=True)
    divider(slide, LEFT, Inches(5.58), Inches(11.9))
    textbox(slide, LEFT, Inches(5.85), Inches(11.2), Inches(0.4), "Q&A", size=30, color=COBALT, bold=True)
    textbox(slide, LEFT, Inches(6.42), Inches(11.0), Inches(0.5),
            "你的团队瓶颈真的在 coding 吗？\n你现在有没有稳定的 verify 闭环？\n你省下来的时间，最后流向了哪里？",
            size=18, color=MUTED)
    footer(slide, 16)

    out = "tmp/AI Coding 一年实战 - v2.pptx"
    prs.save(out)
    print(out)


if __name__ == "__main__":
    build()
