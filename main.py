from fastcore.xml import Html, Head, Style, Body, H1, H2, Div, Label, Select, Input, Span, Button, Option, A, P, Nav, Meta
from fasthtml.xtend import Script
from fasthtml.core import serve, FastHTML
import json
from models import get_models
from platforms import get_all_platforms, get_use_case_templates

app = FastHTML()
rt = app.route

def get_common_styles():
    return """
        * { box-sizing: border-box; }
        body { font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 0; background: #f5f7fa; }
        .header { background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); color: white; padding: 20px 40px; }
        .header h1 { margin: 0; font-size: 1.8em; }
        .header p { margin: 5px 0 0 0; opacity: 0.9; font-size: 0.95em; }
        .nav { display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap; }
        .nav a { color: white; text-decoration: none; padding: 8px 16px; border-radius: 6px; background: rgba(255,255,255,0.15); transition: background 0.2s; font-size: 0.9em; }
        .nav a:hover, .nav a.active { background: rgba(255,255,255,0.3); }
        .main-content { max-width: 1400px; margin: 0 auto; padding: 30px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
        .card h2 { margin-top: 0; color: #1e293b; font-size: 1.3em; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .card h3 { margin-top: 0; color: #334155; font-size: 1.1em; }
        .form-group { margin-bottom: 18px; }
        label { display: block; margin-bottom: 6px; font-weight: 500; color: #374151; font-size: 0.9em; }
        input, select { width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.95em; }
        input:focus, select:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
        .cost-display { font-size: 2.5em; font-weight: bold; color: #2563eb; margin: 15px 0; }
        .cost-display.monthly { color: #059669; }
        .cost-label { font-size: 0.9em; color: #6b7280; margin-bottom: 5px; }
        .breakdown { margin-top: 15px; }
        .breakdown-item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb; font-size: 0.9em; }
        .breakdown-item:last-child { border-bottom: none; }
        .btn { padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 0.9em; transition: all 0.2s; }
        .btn-primary { background: #2563eb; color: white; }
        .btn-primary:hover { background: #1d4ed8; }
        .btn-secondary { background: #6b7280; color: white; }
        .btn-secondary:hover { background: #4b5563; }
        .btn-success { background: #059669; color: white; }
        .btn-success:hover { background: #047857; }
        .btn-warning { background: #d97706; color: white; }
        .btn-group { display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
        .info-text { color: #6b7280; font-size: 0.85em; margin-top: 4px; }
        .tag { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.75em; font-weight: 500; margin: 2px; }
        .tag-blue { background: #dbeafe; color: #1e40af; }
        .tag-green { background: #d1fae5; color: #065f46; }
        .tag-purple { background: #e9d5ff; color: #6b21a8; }
        .tag-orange { background: #fed7aa; color: #c2410c; }
        .tag-gray { background: #e5e7eb; color: #374151; }
        .platform-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
        .platform-card h4 { margin: 0 0 8px 0; color: #1e293b; }
        .platform-card p { margin: 0 0 10px 0; color: #64748b; font-size: 0.9em; }
        .pros-cons { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px; }
        .pros li { color: #059669; }
        .cons li { color: #dc2626; }
        .pros, .cons { padding-left: 20px; margin: 0; font-size: 0.85em; }
        .comparison-table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
        .comparison-table th, .comparison-table td { padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }
        .comparison-table th { background: #f8fafc; font-weight: 600; color: #374151; }
        .comparison-table tr:hover { background: #f8fafc; }
        .delta-positive { color: #059669; font-weight: 500; }
        .delta-negative { color: #dc2626; font-weight: 500; }
        .scenario-card { border: 2px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 12px; cursor: pointer; transition: all 0.2s; }
        .scenario-card:hover { border-color: #2563eb; background: #f8fafc; }
        .scenario-card.selected { border-color: #2563eb; background: #eff6ff; }
        .scenario-card h4 { margin: 0 0 5px 0; }
        .scenario-card p { margin: 0; color: #6b7280; font-size: 0.85em; }
        .tco-summary { background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); color: white; border-radius: 12px; padding: 24px; margin-bottom: 25px; }
        .tco-summary h2 { color: white; border-bottom-color: rgba(255,255,255,0.3); }
        .tco-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 15px; }
        .tco-item { text-align: center; }
        .tco-item .value { font-size: 1.8em; font-weight: bold; }
        .tco-item .label { font-size: 0.85em; opacity: 0.9; }
        .section-tabs { display: flex; gap: 5px; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; }
        .section-tab { padding: 10px 20px; cursor: pointer; border: none; background: none; font-size: 0.95em; color: #64748b; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all 0.2s; }
        .section-tab:hover { color: #2563eb; }
        .section-tab.active { color: #2563eb; border-bottom-color: #2563eb; font-weight: 500; }
        .hidden { display: none; }
        @media (max-width: 1024px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } .tco-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 768px) { .tco-grid { grid-template-columns: 1fr; } .header { padding: 15px 20px; } .main-content { padding: 15px; } }
    """

def serialize_models(models):
    return {k: {
        "name": v.name,
        "provider": v.provider,
        "context_window": v.context_window,
        "max_output": v.max_output,
        "price_input": v.price_input,
        "price_output": v.price_output
    } for k, v in models.items()}

def serialize_platforms(platforms_dict):
    result = {}
    for category, platforms in platforms_dict.items():
        result[category] = {}
        for key, p in platforms.items():
            result[category][key] = {
                "name": p.name,
                "category": p.category,
                "description": p.description,
                "pros": p.pros,
                "cons": p.cons,
                "pricing_model": p.pricing_model,
                "estimated_monthly_base": p.estimated_monthly_base,
                "estimated_per_request": p.estimated_per_request,
                "best_for": p.best_for,
                "scale_fit": [s.value for s in p.scale_fit],
                "complexity_fit": [c.value for c in p.complexity_fit],
                "url": p.url
            }
    return result

def serialize_use_cases(use_cases):
    return {k: {
        "name": v.name,
        "description": v.description,
        "typical_input_tokens": v.typical_input_tokens,
        "typical_output_tokens": v.typical_output_tokens,
        "requests_per_user_day": v.requests_per_user_day,
        "model_tier": v.model_tier,
        "complexity": v.complexity.value
    } for k, v in use_cases.items()}

@app.get("/")
def get():
    models = get_models()
    providers = sorted(set(m.provider for m in models.values()))
    all_platforms = get_all_platforms()
    use_cases = get_use_case_templates()

    return Html(
        Head(
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Style(get_common_styles())
        ),
        Body(
            # Header
            Div(
                H1("Thrifty - AI Platform TCO Calculator"),
                P(
                    Span("Pragmatic recommendations for LLM infrastructure with cost optimization"),
                    Span(" • ", style="opacity: 0.7;"),
                    Span(id="model-count-badge", style="opacity: 0.8;"),
                ),
                Nav(
                    A("Cost Calculator", href="#calculator", cls="active"),
                    A("Use Case Templates", href="#use-cases"),
                    A("Platform Recommendations", href="#platforms"),
                    A("Model Comparison", href="#comparison"),
                    A("TCO Planner", href="#tco"),
                    cls="nav"
                ),
                cls="header"
            ),

            # Main Content
            Div(
                # TCO Summary Dashboard
                Div(
                    H2("Total Cost of Ownership Summary", style="margin-top: 0;"),
                    Div(
                        Div(Div("$0.00", cls="value", id="tco-per-request"), Div("Per Request", cls="label"), cls="tco-item"),
                        Div(Div("$0", cls="value", id="tco-monthly"), Div("Monthly (Est.)", cls="label"), cls="tco-item"),
                        Div(Div("$0", cls="value", id="tco-platform"), Div("Platform Costs", cls="label"), cls="tco-item"),
                        Div(Div("$0", cls="value", id="tco-total"), Div("Total Monthly", cls="label"), cls="tco-item"),
                        cls="tco-grid"
                    ),
                    cls="tco-summary"
                ),

                # Main Calculator Grid
                Div(
                    # Left Column - Configuration
                    Div(
                        H2("Cost Calculator"),

                        # Use Case Quick Select
                        Div(
                            Label("Quick Start: Select Use Case"),
                            Select(
                                Option("Custom Configuration", value=""),
                                *[Option(uc.name, value=k) for k, uc in use_cases.items()],
                                id="use-case-select",
                                onchange="applyUseCase()"
                            ),
                            Div(id="use-case-info", style="margin-top: 10px;"),
                            cls="form-group"
                        ),

                        # Scale Selection
                        Div(
                            Label("Expected Scale"),
                            Select(
                                Option("Startup (< 100K req/mo)", value="startup"),
                                Option("Growth (100K - 1M req/mo)", value="growth"),
                                Option("Scale (1M - 10M req/mo)", value="scale"),
                                Option("Enterprise (10M+ req/mo)", value="enterprise"),
                                id="scale-select",
                                onchange="updateRecommendations()"
                            ),
                            cls="form-group"
                        ),

                        # Complexity Selection
                        Div(
                            Label("Use Case Complexity"),
                            Select(
                                Option("Low - Simple prompt/response", value="low"),
                                Option("Medium - Multi-step, some context", value="medium"),
                                Option("High - Complex agents, tool use", value="high"),
                                id="complexity-select",
                                onchange="updateRecommendations()"
                            ),
                            cls="form-group"
                        ),

                        Div(style="border-top: 1px solid #e5e7eb; margin: 20px 0;"),

                        # Model Selection
                        Div(
                            Label("LLM Provider"),
                            Select(
                                *[Option(p, value=p) for p in providers],
                                id="provider-select",
                                onchange="updateModels()"
                            ),
                            cls="form-group"
                        ),
                        Div(
                            Label("Model"),
                            Select(id="model-select", onchange="updateModelSpecs()"),
                            Span(id="model-info", cls="info-text"),
                            cls="form-group"
                        ),

                        Div(style="border-top: 1px solid #e5e7eb; margin: 20px 0;"),

                        # Token Configuration
                        Div(
                            Label("Input Tokens per Request"),
                            Input(type="number", id="input-tokens", value="1000", min="1", oninput="recalculateAll()"),
                            Span(id="input-info", cls="info-text"),
                            cls="form-group"
                        ),
                        Div(
                            Label("Output Tokens per Request"),
                            Input(type="number", id="output-tokens", value="500", min="1", oninput="recalculateAll()"),
                            Span(id="output-info", cls="info-text"),
                            cls="form-group"
                        ),

                        Div(style="border-top: 1px solid #e5e7eb; margin: 20px 0;"),

                        # Volume Configuration
                        Div(
                            Label("Daily Active Users"),
                            Input(type="number", id="daily-users", value="100", min="1", oninput="recalculateAll()"),
                            cls="form-group"
                        ),
                        Div(
                            Label("Requests per User per Day"),
                            Input(type="number", id="requests-per-user", value="10", min="1", oninput="recalculateAll()"),
                            cls="form-group"
                        ),
                        Div(
                            Label("Agent Iterations per Request"),
                            Input(type="number", id="iterations", value="1", min="1", oninput="recalculateAll()"),
                            Span("For multi-step agents, enter average iterations", cls="info-text"),
                            cls="form-group"
                        ),

                        cls="card"
                    ),

                    # Right Column - Results
                    Div(
                        # Cost Results
                        Div(
                            H2("Cost Breakdown"),
                            Div(
                                Div("LLM Cost Per Request", cls="cost-label"),
                                Div("$0.00", id="cost-per-request", cls="cost-display"),
                            ),
                            Div(
                                Div("LLM Cost Monthly", cls="cost-label"),
                                Div("$0", id="cost-monthly", cls="cost-display monthly"),
                            ),
                            Div(
                                Div("Total Monthly (LLM + Platform)", cls="cost-label"),
                                Div("$0", id="cost-total-monthly", cls="cost-display", style="color: #7c3aed;"),
                            ),
                            Div(id="breakdown", cls="breakdown"),
                            Div(
                                Button("Save Scenario", cls="btn btn-primary", onclick="saveScenario()"),
                                Button("Compare Models", cls="btn btn-secondary", onclick="showComparison()"),
                                Button("Export", cls="btn btn-success", onclick="exportResults()"),
                                cls="btn-group"
                            ),
                            cls="card"
                        ),

                        # Saved Scenarios for Comparison
                        Div(
                            H2("Saved Scenarios"),
                            Div(id="saved-scenarios", children=P("No scenarios saved yet. Save configurations to compare.", style="color: #6b7280; font-size: 0.9em;")),
                            Div(
                                Button("Clear All", cls="btn btn-secondary", onclick="clearScenarios()"),
                                Button("Show Delta", cls="btn btn-warning", onclick="showDelta()"),
                                cls="btn-group"
                            ),
                            cls="card", style="margin-top: 25px;"
                        ),

                    ),
                    cls="grid-2"
                ),

                # Use Case Templates Section
                Div(
                    H2("Use Case Templates", id="use-cases"),
                    P("Click a template to auto-configure the calculator with typical values", style="color: #6b7280; margin-top: -10px;"),
                    Div(id="use-case-templates-grid"),
                    cls="card", style="margin-top: 25px;"
                ),

                # Platform Recommendations Section
                Div(
                    H2("Platform Recommendations", id="platforms"),
                    P("Based on your scale and complexity selections", style="color: #6b7280; margin-top: -10px;"),

                    Div(
                        Button("Agent Frameworks", cls="section-tab active", onclick="showPlatformTab('agent_frameworks')"),
                        Button("Vector Stores", cls="section-tab", onclick="showPlatformTab('vector_stores')"),
                        Button("CI/CD", cls="section-tab", onclick="showPlatformTab('cicd')"),
                        Button("Observability", cls="section-tab", onclick="showPlatformTab('observability')"),
                        Button("Model Registry", cls="section-tab", onclick="showPlatformTab('registries')"),
                        cls="section-tabs"
                    ),

                    Div(id="platform-recommendations"),

                    cls="card", style="margin-top: 25px;"
                ),

                # Model Comparison Table
                Div(
                    H2("Model Cost Comparison", id="comparison"),
                    P("Compare costs across models for your use case", style="color: #6b7280; margin-top: -10px;"),
                    Div(id="model-comparison-table"),
                    cls="card", style="margin-top: 25px;"
                ),

                # Delta Comparison Modal (hidden by default)
                Div(
                    Div(
                        H2("Scenario Delta Comparison"),
                        Div(id="delta-comparison-content"),
                        Button("Close", cls="btn btn-secondary", onclick="hideDelta()"),
                        cls="card", style="max-width: 800px; margin: 50px auto;"
                    ),
                    id="delta-modal",
                    cls="hidden",
                    style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; overflow-y: auto; padding: 20px;"
                ),

                cls="main-content"
            ),

            # JavaScript
            Script("""
                const models = """ + json.dumps(serialize_models(models)) + """;
                const providers = """ + json.dumps(providers) + """;
                const platforms = """ + json.dumps(serialize_platforms(all_platforms)) + """;
                const useCases = """ + json.dumps(serialize_use_cases(use_cases)) + """;
                
                let savedScenarios = [];
                let currentPlatformTab = 'agent_frameworks';
                
                // Initialize
                function init() {
                    const modelCount = Object.keys(models).length;
                    const providerCount = providers.length;
                    console.log(`Loaded ${modelCount} models from ${providerCount} providers`);
                    
                    // Update model count badge in header
                    const badge = document.getElementById('model-count-badge');
                    if (badge) {
                        badge.textContent = `${modelCount} models from ${providerCount} providers (live pricing)`;
                    }
                    
                    if (modelCount === 0) {
                        document.getElementById('model-info').textContent = 'No models loaded - check API connection';
                    }
                    
                    updateModels();
                    renderUseCaseTemplates();
                    updateRecommendations();
                    generateModelComparison();
                }
                
                function updateModels() {
                    const provider = document.getElementById('provider-select').value;
                    const modelSelect = document.getElementById('model-select');
                    modelSelect.innerHTML = '';
                    Object.entries(models).forEach(([id, model]) => {
                        if (model.provider === provider) {
                            const opt = document.createElement('option');
                            opt.value = id;
                            opt.textContent = model.name;
                            modelSelect.appendChild(opt);
                        }
                    });
                    updateModelSpecs();
                }
                
                function updateModelSpecs() {
                    const modelId = document.getElementById('model-select').value;
                    if (!modelId || !models[modelId]) return;
                    const model = models[modelId];
                    
                    document.getElementById('input-tokens').max = model.context_window;
                    document.getElementById('output-tokens').max = model.max_output;
                    
                    document.getElementById('input-info').textContent = `Max: ${model.context_window.toLocaleString()} tokens`;
                    document.getElementById('output-info').textContent = `Max: ${model.max_output.toLocaleString()} tokens`;
                    document.getElementById('model-info').textContent = `$${model.price_input}/1M in, $${model.price_output}/1M out`;
                    
                    recalculateAll();
                }
                
                function applyUseCase() {
                    const ucId = document.getElementById('use-case-select').value;
                    const infoPanel = document.getElementById('use-case-info');
                    
                    if (!ucId || !useCases[ucId]) {
                        infoPanel.innerHTML = '';
                        return;
                    }
                    
                    const uc = useCases[ucId];
                    
                    // Find recommended models based on tier
                    const recommendedModels = getRecommendedModelsForTier(uc.model_tier);
                    
                    // Show use case info panel
                    const tierLabels = { budget: 'Budget-friendly', balanced: 'Balanced', premium: 'Premium' };
                    infoPanel.innerHTML = `
                        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 12px; font-size: 0.9em;">
                            <div style="font-weight: 500; color: #1e40af; margin-bottom: 8px;">${uc.name}</div>
                            <div style="color: #64748b; margin-bottom: 8px;">${uc.description}</div>
                            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                                <span class="tag tag-blue">~${uc.typical_input_tokens} input tokens</span>
                                <span class="tag tag-blue">~${uc.typical_output_tokens} output tokens</span>
                                <span class="tag tag-purple">${uc.requests_per_user_day} req/user/day</span>
                                <span class="tag tag-orange">${uc.complexity} complexity</span>
                                <span class="tag tag-green">${tierLabels[uc.model_tier] || uc.model_tier} tier</span>
                            </div>
                            <div style="margin-top: 8px; font-size: 0.85em; color: #64748b;">
                                <strong>Suggested models:</strong> ${recommendedModels.slice(0, 5).map(m => m.name).join(', ')}
                            </div>
                        </div>
                    `;
                    
                    // Apply values
                    document.getElementById('input-tokens').value = uc.typical_input_tokens;
                    document.getElementById('output-tokens').value = uc.typical_output_tokens;
                    document.getElementById('requests-per-user').value = uc.requests_per_user_day;
                    document.getElementById('complexity-select').value = uc.complexity;
                    
                    // Select the best recommended model
                    if (recommendedModels.length > 0) {
                        const bestModel = recommendedModels[0];
                        document.getElementById('provider-select').value = bestModel.provider;
                        updateModels();
                        document.getElementById('model-select').value = bestModel.id;
                        updateModelSpecs();
                    } else {
                        recalculateAll();
                    }
                    
                    updateRecommendations();
                }
                
                function getRecommendedModelsForTier(tier) {
                    // Get all models sorted by cost
                    const modelList = Object.entries(models).map(([id, m]) => ({
                        id,
                        ...m,
                        totalCost: m.price_input + m.price_output
                    })).filter(m => m.totalCost > 0).sort((a, b) => a.totalCost - b.totalCost);
                    
                    if (modelList.length === 0) return [];
                    
                    // Divide into tiers based on percentiles
                    const tierSize = Math.ceil(modelList.length / 3);
                    
                    switch (tier) {
                        case 'budget':
                            // Cheapest third
                            return modelList.slice(0, tierSize);
                        case 'balanced':
                            // Middle third
                            return modelList.slice(tierSize, tierSize * 2);
                        case 'premium':
                            // Most expensive third
                            return modelList.slice(tierSize * 2);
                        default:
                            return modelList.slice(0, tierSize);
                    }
                }
                
                function renderUseCaseTemplates() {
                    const container = document.getElementById('use-case-templates-grid');
                    
                    const complexityColors = {
                        'low': { bg: '#d1fae5', text: '#065f46' },
                        'medium': { bg: '#fef3c7', text: '#92400e' },
                        'high': { bg: '#fee2e2', text: '#991b1b' }
                    };
                    
                    const tierColors = {
                        'budget': { bg: '#dbeafe', text: '#1e40af' },
                        'balanced': { bg: '#e9d5ff', text: '#6b21a8' },
                        'premium': { bg: '#fce7f3', text: '#9d174d' }
                    };
                    
                    const tierLabels = { budget: 'Budget', balanced: 'Balanced', premium: 'Premium' };
                    
                    let html = '<div class="grid-3" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));">';
                    
                    Object.entries(useCases).forEach(([id, uc]) => {
                        const colors = complexityColors[uc.complexity] || complexityColors.low;
                        const tColors = tierColors[uc.model_tier] || tierColors.budget;
                        const estimatedCost = calculateUseCaseCost(uc);
                        
                        html += `
                            <div class="scenario-card" onclick="selectUseCaseTemplate('${id}')" style="cursor: pointer;">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                                    <h4 style="margin: 0; font-size: 1em;">${uc.name}</h4>
                                    <div>
                                        <span class="tag" style="background: ${colors.bg}; color: ${colors.text};">${uc.complexity}</span>
                                        <span class="tag" style="background: ${tColors.bg}; color: ${tColors.text};">${tierLabels[uc.model_tier] || uc.model_tier}</span>
                                    </div>
                                </div>
                                <p style="margin: 0 0 10px 0; color: #64748b; font-size: 0.85em;">${uc.description}</p>
                                <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px;">
                                    <span class="tag tag-gray">${uc.typical_input_tokens} in</span>
                                    <span class="tag tag-gray">${uc.typical_output_tokens} out</span>
                                    <span class="tag tag-gray">${uc.requests_per_user_day} req/day</span>
                                </div>
                                <div style="font-size: 0.85em; color: #2563eb; font-weight: 500;">
                                    Est. ${estimatedCost}/request (cheapest model)
                                </div>
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                    container.innerHTML = html;
                }
                
                function calculateUseCaseCost(uc) {
                    // Find cheapest model cost for this use case
                    let minCost = Infinity;
                    Object.values(models).forEach(m => {
                        const cost = (uc.typical_input_tokens / 1000000) * m.price_input + 
                                     (uc.typical_output_tokens / 1000000) * m.price_output;
                        if (cost < minCost) minCost = cost;
                    });
                    return '$' + minCost.toFixed(4);
                }
                
                function selectUseCaseTemplate(ucId) {
                    document.getElementById('use-case-select').value = ucId;
                    applyUseCase();
                    // Scroll to calculator
                    document.querySelector('.card').scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
                
                function calculate() {
                    const modelId = document.getElementById('model-select').value;
                    if (!modelId || !models[modelId]) return;
                    
                    const model = models[modelId];
                    const inputTokens = parseInt(document.getElementById('input-tokens').value) || 0;
                    const outputTokens = parseInt(document.getElementById('output-tokens').value) || 0;
                    const dailyUsers = parseInt(document.getElementById('daily-users').value) || 0;
                    const requestsPerUser = parseFloat(document.getElementById('requests-per-user').value) || 0;
                    const iterations = parseInt(document.getElementById('iterations').value) || 1;
                    
                    // Get complexity multiplier (accounts for retries, tool calls, etc.)
                    const complexityMultiplier = getComplexityMultiplier();
                    // Get scale discount (volume pricing)
                    const scaleDiscount = getScaleDiscount();
                    
                    // Calculate per request cost (complexity adds overhead)
                    const effectiveIterations = iterations * complexityMultiplier;
                    const inputCost = (inputTokens * effectiveIterations / 1000000) * model.price_input * scaleDiscount;
                    const outputCost = (outputTokens * effectiveIterations / 1000000) * model.price_output * scaleDiscount;
                    const costPerRequest = inputCost + outputCost;
                    
                    // Calculate monthly cost
                    const dailyRequests = dailyUsers * requestsPerUser;
                    const monthlyRequests = dailyRequests * 30;
                    const monthlyCost = costPerRequest * monthlyRequests;
                    
                    // Get platform costs
                    const platformCost = calculatePlatformCosts();
                    const totalMonthlyCost = monthlyCost + platformCost;
                    
                    // Update displays
                    document.getElementById('cost-per-request').textContent = '$' + costPerRequest.toFixed(4);
                    document.getElementById('cost-monthly').textContent = '$' + monthlyCost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
                    document.getElementById('cost-total-monthly').textContent = '$' + totalMonthlyCost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
                    
                    // Update TCO summary
                    document.getElementById('tco-per-request').textContent = '$' + costPerRequest.toFixed(4);
                    document.getElementById('tco-monthly').textContent = '$' + Math.round(monthlyCost).toLocaleString();
                    document.getElementById('tco-platform').textContent = '$' + Math.round(platformCost).toLocaleString();
                    document.getElementById('tco-total').textContent = '$' + Math.round(totalMonthlyCost).toLocaleString();
                    
                    // Update breakdown
                    const complexity = document.getElementById('complexity-select').value;
                    const scale = document.getElementById('scale-select').value;
                    
                    const breakdown = document.getElementById('breakdown');
                    breakdown.innerHTML = `
                        <div class="breakdown-item"><span>Model</span><span>${model.name}</span></div>
                        <div class="breakdown-item"><span>Complexity</span><span>${complexity} (${complexityMultiplier}x overhead)</span></div>
                        <div class="breakdown-item"><span>Scale Discount</span><span>${scale} (${Math.round((1 - scaleDiscount) * 100)}% off)</span></div>
                        <div class="breakdown-item"><span>Effective Iterations</span><span>${effectiveIterations.toFixed(1)} (${iterations} × ${complexityMultiplier})</span></div>
                        <div class="breakdown-item"><span>Input Cost/Req</span><span>$${inputCost.toFixed(6)}</span></div>
                        <div class="breakdown-item"><span>Output Cost/Req</span><span>$${outputCost.toFixed(6)}</span></div>
                        <div class="breakdown-item"><span>Tokens/Request</span><span>${(inputTokens + outputTokens).toLocaleString()}</span></div>
                        <div class="breakdown-item"><span>Daily Requests</span><span>${dailyRequests.toLocaleString()}</span></div>
                        <div class="breakdown-item"><span>Monthly Requests</span><span>${monthlyRequests.toLocaleString()}</span></div>
                        <div class="breakdown-item"><span>LLM Cost/Month</span><span>$${monthlyCost.toFixed(2)}</span></div>
                        <div class="breakdown-item"><span>Platform Cost/Month</span><span>$${platformCost.toFixed(2)}</span></div>
                        <div class="breakdown-item" style="font-weight: bold; border-top: 2px solid #e5e7eb;"><span>Total Monthly</span><span>$${totalMonthlyCost.toFixed(2)}</span></div>
                    `;
                    
                    // Store current calculation
                    window.currentCalc = {
                        modelId, model: model.name, provider: model.provider,
                        inputTokens, outputTokens, iterations,
                        dailyUsers, requestsPerUser,
                        costPerRequest, monthlyCost, platformCost, totalMonthlyCost,
                        monthlyRequests,
                        scale: document.getElementById('scale-select').value,
                        complexity: document.getElementById('complexity-select').value,
                        timestamp: new Date().toISOString()
                    };
                }
                
                function recalculateAll() {
                    calculate();
                    generateModelComparison();
                }
                
                function calculatePlatformCosts() {
                    // Estimate based on typical selections for scale
                    const scale = document.getElementById('scale-select').value;
                    const baseCosts = {
                        'startup': 50,
                        'growth': 200,
                        'scale': 800,
                        'enterprise': 3000
                    };
                    return baseCosts[scale] || 50;
                }
                
                function getComplexityMultiplier() {
                    // Complexity affects expected iterations/overhead
                    const complexity = document.getElementById('complexity-select').value;
                    const multipliers = {
                        'low': 1.0,
                        'medium': 1.5,
                        'high': 2.5
                    };
                    return multipliers[complexity] || 1.0;
                }
                
                function getScaleDiscount() {
                    // Volume discounts at higher scales
                    const scale = document.getElementById('scale-select').value;
                    const discounts = {
                        'startup': 1.0,
                        'growth': 0.95,
                        'scale': 0.90,
                        'enterprise': 0.85
                    };
                    return discounts[scale] || 1.0;
                }
                
                function updateRecommendations() {
                    const scale = document.getElementById('scale-select').value;
                    const complexity = document.getElementById('complexity-select').value;
                    
                    showPlatformTab(currentPlatformTab);
                    recalculateAll();
                }
                
                function showPlatformTab(category) {
                    currentPlatformTab = category;
                    const scale = document.getElementById('scale-select').value;
                    const complexity = document.getElementById('complexity-select').value;
                    
                    // Update tab styles
                    document.querySelectorAll('.section-tab').forEach(tab => tab.classList.remove('active'));
                    event?.target?.classList.add('active');
                    
                    const container = document.getElementById('platform-recommendations');
                    const categoryPlatforms = platforms[category] || {};
                    
                    let html = '<div class="grid-2">';
                    
                    Object.entries(categoryPlatforms).forEach(([key, p]) => {
                        const isRecommended = p.scale_fit.includes(scale) && p.complexity_fit.includes(complexity);
                        const borderColor = isRecommended ? '#22c55e' : '#e2e8f0';
                        
                        html += `
                            <div class="platform-card" style="border-color: ${borderColor}; ${isRecommended ? 'border-width: 2px;' : ''}">
                                <div style="display: flex; justify-content: space-between; align-items: start;">
                                    <h4>${p.name}</h4>
                                    ${isRecommended ? '<span class="tag tag-green">Recommended</span>' : ''}
                                </div>
                                <p>${p.description}</p>
                                <div style="margin-bottom: 10px;">
                                    <span class="tag tag-blue">${p.pricing_model}</span>
                                    ${p.estimated_monthly_base > 0 ? `<span class="tag tag-orange">~$${p.estimated_monthly_base}/mo base</span>` : ''}
                                </div>
                                <div class="pros-cons">
                                    <div>
                                        <strong style="color: #059669; font-size: 0.85em;">Pros:</strong>
                                        <ul class="pros">${p.pros.map(pro => `<li>${pro}</li>`).join('')}</ul>
                                    </div>
                                    <div>
                                        <strong style="color: #dc2626; font-size: 0.85em;">Cons:</strong>
                                        <ul class="cons">${p.cons.map(con => `<li>${con}</li>`).join('')}</ul>
                                    </div>
                                </div>
                                <div style="margin-top: 10px;">
                                    <strong style="font-size: 0.85em;">Best for:</strong>
                                    <div>${p.best_for.map(b => `<span class="tag tag-gray">${b}</span>`).join('')}</div>
                                </div>
                                ${p.url ? `<a href="${p.url}" target="_blank" style="display: inline-block; margin-top: 10px; font-size: 0.85em; color: #2563eb;">Learn more →</a>` : ''}
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                    container.innerHTML = html;
                }
                
                function generateModelComparison() {
                    const inputTokens = parseInt(document.getElementById('input-tokens').value) || 1000;
                    const outputTokens = parseInt(document.getElementById('output-tokens').value) || 500;
                    const dailyUsers = parseInt(document.getElementById('daily-users').value) || 100;
                    const requestsPerUser = parseFloat(document.getElementById('requests-per-user').value) || 10;
                    const iterations = parseInt(document.getElementById('iterations').value) || 1;
                    const currentModelId = document.getElementById('model-select').value;
                    
                    const complexityMultiplier = getComplexityMultiplier();
                    const scaleDiscount = getScaleDiscount();
                    const effectiveIterations = iterations * complexityMultiplier;
                    const monthlyRequests = dailyUsers * requestsPerUser * 30;
                    
                    let modelCosts = [];
                    let currentModelCost = null;
                    
                    Object.entries(models).forEach(([id, m]) => {
                        const inputCost = (inputTokens * effectiveIterations / 1000000) * m.price_input * scaleDiscount;
                        const outputCost = (outputTokens * effectiveIterations / 1000000) * m.price_output * scaleDiscount;
                        const costPerRequest = inputCost + outputCost;
                        const monthlyCost = costPerRequest * monthlyRequests;
                        
                        const modelData = {
                            id, name: m.name, provider: m.provider,
                            costPerRequest, monthlyCost,
                            priceInput: m.price_input, priceOutput: m.price_output,
                            contextWindow: m.context_window,
                            isCurrent: id === currentModelId
                        };
                        
                        modelCosts.push(modelData);
                        if (id === currentModelId) {
                            currentModelCost = modelData;
                        }
                    });
                    
                    // Sort by monthly cost
                    modelCosts.sort((a, b) => a.monthlyCost - b.monthlyCost);
                    
                    // Find current model rank
                    const currentRank = modelCosts.findIndex(m => m.isCurrent) + 1;
                    const cheapestModel = modelCosts[0];
                    
                    let html = '';
                    
                    // Summary box
                    if (currentModelCost && cheapestModel) {
                        const savings = currentModelCost.monthlyCost - cheapestModel.monthlyCost;
                        const savingsPercent = currentModelCost.monthlyCost > 0 ? (savings / currentModelCost.monthlyCost * 100) : 0;
                        
                        html += `<div style="background: #f8fafc; border-radius: 8px; padding: 15px; margin-bottom: 15px; display: flex; gap: 20px; flex-wrap: wrap;">
                            <div>
                                <div style="font-size: 0.85em; color: #6b7280;">Your model</div>
                                <div style="font-weight: 600; color: #1e293b;">${currentModelCost.name}</div>
                                <div style="font-size: 0.9em; color: #2563eb;">$${currentModelCost.monthlyCost.toFixed(2)}/mo</div>
                            </div>
                            <div>
                                <div style="font-size: 0.85em; color: #6b7280;">Rank</div>
                                <div style="font-weight: 600; color: #1e293b;">#${currentRank} of ${modelCosts.length}</div>
                            </div>
                            ${savings > 0 ? `<div>
                                <div style="font-size: 0.85em; color: #6b7280;">Potential savings</div>
                                <div style="font-weight: 600; color: #059669;">$${savings.toFixed(2)}/mo (${savingsPercent.toFixed(0)}%)</div>
                                <div style="font-size: 0.85em; color: #6b7280;">vs ${cheapestModel.name}</div>
                            </div>` : `<div>
                                <div style="font-size: 0.85em; color: #6b7280;">Status</div>
                                <div style="font-weight: 600; color: #059669;">✓ Cheapest option!</div>
                            </div>`}
                        </div>`;
                    }
                    
                    html += `
                        <table class="comparison-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Model</th>
                                    <th>Provider</th>
                                    <th>$/Request</th>
                                    <th>$/Month</th>
                                    <th>vs Current</th>
                                    <th>Context</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    
                    // Show top 10 cheapest + current model if not in top 10
                    const topModels = modelCosts.slice(0, 10);
                    const showCurrentSeparately = currentRank > 10;
                    
                    topModels.forEach((m, i) => {
                        const rank = i + 1;
                        const isCurrentRow = m.isCurrent;
                        const rowStyle = isCurrentRow ? 'background: #eff6ff; border-left: 3px solid #2563eb;' : 
                                        (rank === 1 ? 'background: #f0fdf4;' : '');
                        
                        const diffFromCurrent = currentModelCost ? (m.monthlyCost - currentModelCost.monthlyCost) : 0;
                        const diffClass = diffFromCurrent < 0 ? 'delta-positive' : (diffFromCurrent > 0 ? 'delta-negative' : '');
                        const diffSign = diffFromCurrent > 0 ? '+' : '';
                        const diffText = isCurrentRow ? '—' : `${diffSign}$${diffFromCurrent.toFixed(2)}`;
                        
                        html += `
                            <tr style="${rowStyle}">
                                <td>${rank}</td>
                                <td>
                                    <strong>${m.name}</strong>
                                    ${rank === 1 ? ' <span class="tag tag-green">Cheapest</span>' : ''}
                                    ${isCurrentRow ? ' <span class="tag tag-blue">Current</span>' : ''}
                                </td>
                                <td>${m.provider}</td>
                                <td>$${m.costPerRequest.toFixed(4)}</td>
                                <td>$${m.monthlyCost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                <td class="${diffClass}">${diffText}</td>
                                <td>${(m.contextWindow / 1000).toFixed(0)}K</td>
                            </tr>
                        `;
                    });
                    
                    // Show current model if not in top 10
                    if (showCurrentSeparately && currentModelCost) {
                        html += `
                            <tr style="border-top: 2px dashed #e5e7eb;">
                                <td colspan="7" style="text-align: center; color: #6b7280; font-size: 0.85em; padding: 5px;">... ${currentRank - 11} models ...</td>
                            </tr>
                            <tr style="background: #eff6ff; border-left: 3px solid #2563eb;">
                                <td>${currentRank}</td>
                                <td><strong>${currentModelCost.name}</strong> <span class="tag tag-blue">Current</span></td>
                                <td>${currentModelCost.provider}</td>
                                <td>$${currentModelCost.costPerRequest.toFixed(4)}</td>
                                <td>$${currentModelCost.monthlyCost.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                <td>—</td>
                                <td>${(currentModelCost.contextWindow / 1000).toFixed(0)}K</td>
                            </tr>
                        `;
                    }
                    
                    html += '</tbody></table>';
                    html += `<p style="font-size: 0.8em; color: #6b7280; margin-top: 10px;">Showing top 10 of ${modelCosts.length} models. Costs based on your configuration: ${inputTokens} input × ${outputTokens} output tokens, ${monthlyRequests.toLocaleString()} requests/month.</p>`;
                    
                    document.getElementById('model-comparison-table').innerHTML = html;
                }
                
                function saveScenario() {
                    if (!window.currentCalc) return;
                    
                    const scenario = {
                        ...window.currentCalc,
                        id: Date.now(),
                        name: `${window.currentCalc.model} - ${new Date().toLocaleTimeString()}`
                    };
                    
                    savedScenarios.push(scenario);
                    renderSavedScenarios();
                }
                
                function renderSavedScenarios() {
                    const container = document.getElementById('saved-scenarios');
                    
                    if (savedScenarios.length === 0) {
                        container.innerHTML = '<p style="color: #6b7280; font-size: 0.9em;">No scenarios saved yet.</p>';
                        return;
                    }
                    
                    let html = '';
                    savedScenarios.forEach((s, i) => {
                        html += `
                            <div class="scenario-card" onclick="loadScenario(${i})">
                                <div style="display: flex; justify-content: space-between;">
                                    <h4 style="margin: 0;">${s.model}</h4>
                                    <button onclick="event.stopPropagation(); removeScenario(${i})" style="background: none; border: none; color: #dc2626; cursor: pointer;">×</button>
                                </div>
                                <p>$${s.costPerRequest.toFixed(4)}/req · $${s.monthlyCost.toFixed(2)}/mo · ${s.monthlyRequests.toLocaleString()} req/mo</p>
                            </div>
                        `;
                    });
                    
                    container.innerHTML = html;
                }
                
                function loadScenario(index) {
                    const s = savedScenarios[index];
                    if (!s) return;
                    
                    document.getElementById('provider-select').value = s.provider;
                    updateModels();
                    document.getElementById('model-select').value = s.modelId;
                    document.getElementById('input-tokens').value = s.inputTokens;
                    document.getElementById('output-tokens').value = s.outputTokens;
                    document.getElementById('iterations').value = s.iterations;
                    document.getElementById('daily-users').value = s.dailyUsers;
                    document.getElementById('requests-per-user').value = s.requestsPerUser;
                    document.getElementById('scale-select').value = s.scale;
                    document.getElementById('complexity-select').value = s.complexity;
                    
                    updateModelSpecs();
                }
                
                function removeScenario(index) {
                    savedScenarios.splice(index, 1);
                    renderSavedScenarios();
                }
                
                function clearScenarios() {
                    savedScenarios = [];
                    renderSavedScenarios();
                }
                
                function showDelta() {
                    if (savedScenarios.length < 2) {
                        alert('Save at least 2 scenarios to compare deltas');
                        return;
                    }
                    
                    const modal = document.getElementById('delta-modal');
                    const content = document.getElementById('delta-comparison-content');
                    
                    // Use first scenario as baseline
                    const baseline = savedScenarios[0];
                    
                    let html = `
                        <p style="color: #6b7280;">Comparing against baseline: <strong>${baseline.model}</strong></p>
                        <table class="comparison-table">
                            <thead>
                                <tr>
                                    <th>Scenario</th>
                                    <th>$/Request</th>
                                    <th>Δ $/Request</th>
                                    <th>$/Month</th>
                                    <th>Δ $/Month</th>
                                    <th>Δ %</th>
                                </tr>
                            </thead>
                            <tbody>
                    `;
                    
                    savedScenarios.forEach((s, i) => {
                        const deltaPerReq = s.costPerRequest - baseline.costPerRequest;
                        const deltaMonthly = s.monthlyCost - baseline.monthlyCost;
                        const deltaPercent = baseline.monthlyCost > 0 ? ((s.monthlyCost - baseline.monthlyCost) / baseline.monthlyCost * 100) : 0;
                        
                        const deltaClass = deltaMonthly > 0 ? 'delta-negative' : (deltaMonthly < 0 ? 'delta-positive' : '');
                        const deltaSign = deltaMonthly > 0 ? '+' : '';
                        
                        html += `
                            <tr ${i === 0 ? 'style="background: #f8fafc;"' : ''}>
                                <td><strong>${s.model}</strong>${i === 0 ? ' (baseline)' : ''}</td>
                                <td>$${s.costPerRequest.toFixed(4)}</td>
                                <td class="${deltaClass}">${i === 0 ? '-' : deltaSign + '$' + deltaPerReq.toFixed(4)}</td>
                                <td>$${s.monthlyCost.toFixed(2)}</td>
                                <td class="${deltaClass}">${i === 0 ? '-' : deltaSign + '$' + deltaMonthly.toFixed(2)}</td>
                                <td class="${deltaClass}">${i === 0 ? '-' : deltaSign + deltaPercent.toFixed(1) + '%'}</td>
                            </tr>
                        `;
                    });
                    
                    html += '</tbody></table>';
                    
                    // Add savings summary
                    const cheapest = savedScenarios.reduce((a, b) => a.monthlyCost < b.monthlyCost ? a : b);
                    const mostExpensive = savedScenarios.reduce((a, b) => a.monthlyCost > b.monthlyCost ? a : b);
                    const savings = mostExpensive.monthlyCost - cheapest.monthlyCost;
                    
                    html += `
                        <div style="margin-top: 20px; padding: 15px; background: #f0fdf4; border-radius: 8px;">
                            <strong style="color: #059669;">Potential Savings:</strong>
                            <p style="margin: 5px 0 0 0;">
                                Switching from <strong>${mostExpensive.model}</strong> to <strong>${cheapest.model}</strong> 
                                saves <strong>$${savings.toFixed(2)}/month</strong> 
                                (${((savings / mostExpensive.monthlyCost) * 100).toFixed(1)}% reduction)
                            </p>
                        </div>
                    `;
                    
                    content.innerHTML = html;
                    modal.classList.remove('hidden');
                }
                
                function hideDelta() {
                    document.getElementById('delta-modal').classList.add('hidden');
                }
                
                function showComparison() {
                    generateModelComparison();
                    document.getElementById('comparison').scrollIntoView({ behavior: 'smooth' });
                }
                
                function exportResults() {
                    if (!window.currentCalc) return;
                    
                    const data = {
                        calculation: window.currentCalc,
                        savedScenarios: savedScenarios,
                        exportedAt: new Date().toISOString()
                    };
                    
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `thrifty-tco-${Date.now()}.json`;
                    a.click();
                }
                
                // Initialize on load
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', init);
                } else {
                    init();
                }
            """)
        )
    )

if __name__ == "__main__":
    serve()
