from chromhydra.doctor.diagnose import diagnose
from chromhydra.doctor.render.compare_text import compare_text
from chromhydra.doctor.render.markdown import markdown
from chromhydra.doctor.render.report_text import report_text
from chromhydra.doctor.render.verdict import verdict
from chromhydra.doctor.score import score


def results(load):
    return {"SeleniumBase": diagnose(load("vanilla_headless")), "Chromhydra": diagnose(load("hydra_headless"))}


def test_score_ignores_skips(load):
    assert score(diagnose(load("vanilla_headless"))) == (8, 10)


def test_verdicts(load):
    assert verdict(diagnose(load("hydra_headless"))) == "🐉 all 11 heads healthy"
    assert verdict(diagnose(load("vanilla_headless"))) == "🩸 8/10 heads healthy"


def test_report_text_shows_fix(load):
    text = report_text(diagnose(load("vanilla_headless")), "SeleniumBase")
    assert "↳ fix: chromhydra.install()" in text


def test_compare_text_has_both_labels(load):
    text = compare_text(results(load))
    assert "SeleniumBase vs Chromhydra" in text
    assert text.count("\n") > 11


def test_markdown_table(load):
    text = markdown(results(load))
    assert "| Check | SeleniumBase | Chromhydra |" in text
    assert "| Client Hints | ❌ | ✅ |" in text
    assert "**SeleniumBase**" in text
    assert "**Chromhydra**" not in text
