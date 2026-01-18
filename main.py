from fasthtml.core import serve, FastHTML
from fastcore.xml import Div
from platforms import get_all_platforms, get_use_case_templates
from ui import (
    base, header, tco_summary, calculator_card, results_card, saved_scenarios_card,
    use_cases_section, platforms_section, comparison_section, delta_modal,
    get_client_script
)

app = FastHTML()
rt = app.route

@app.get("/")
def get():
    all_platforms = get_all_platforms()
    use_cases = get_use_case_templates()

    content = Div(
        tco_summary(),
        Div(
            calculator_card(use_cases),
            Div(
                results_card(),
                saved_scenarios_card(),
            ),
            cls="grid-2"
        ),
        use_cases_section(),
        platforms_section(),
        comparison_section(),
        delta_modal(),
        get_client_script(all_platforms, use_cases)
    )

    return base(content)

if __name__ == "__main__":
    serve()
