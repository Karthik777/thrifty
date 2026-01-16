from fastcore.xml import Html, Head, Style, Body, H1, H2, Div, Label, Select, Input, Span, Button
from fasthtml.xtend import Script
from fasthtml.core import serve, FastHTML
import json
from models import get_models

app = FastHTML()
rt = app.route

@app.get("/")
def get():
    models = get_models()
    providers = sorted(set(m.provider for m in models.values()))
    
    return Html(
        Head(
            Style("""
                body { font-family: system-ui, -apple-system, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
                .container { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 20px; }
                .form-section { background: #f8f9fa; padding: 20px; border-radius: 8px; }
                .result-section { background: #e8f4f8; padding: 20px; border-radius: 8px; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: 500; }
                input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
                .cost-display { font-size: 2em; font-weight: bold; color: #2563eb; margin: 20px 0; }
                .breakdown { margin-top: 15px; }
                .breakdown-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e0e0e0; }
                .btn-group { margin-top: 20px; display: flex; gap: 10px; }
                button { padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: 500; }
                .btn-primary { background: #2563eb; color: white; }
                .btn-secondary { background: #6b7280; color: white; }
                .info-text { color: #6b7280; font-size: 0.9em; margin-top: 5px; }
                @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
            """)
        ),
        Body(
            H1("AI Cost Calculator", style="text-align: center; color: #1e293b;"),
            Div(
                Div(
                    H2("Configuration", style="margin-top: 0;"),
                    Div(
                        Label("Provider"),
                        Select(
                            id="provider-select",
                            onchange="updateModels()"
                        ),
                        cls="form-group"
                    ),
                    Div(
                        Label("Model"),
                        Select(id="model-select", onchange="updateModelSpecs()"),
                        cls="form-group"
                    ),
                    Div(
                        Label("Number of Agents"),
                        Input(type="number", id="agents", value="1", min="1", oninput="calculate()"),
                        cls="form-group"
                    ),
                    Div(
                        Label("Iterations"),
                        Input(type="number", id="iterations", value="1", min="1", oninput="calculate()"),
                        cls="form-group"
                    ),
                    Div(
                        Label("Input Tokens per Iteration"),
                        Input(type="number", id="input-tokens", value="1000", min="1", oninput="calculate()"),
                        Span(id="input-info", cls="info-text"),
                        cls="form-group"
                    ),
                    Div(
                        Label("Output Tokens per Iteration"),
                        Input(type="number", id="output-tokens", value="500", min="1", oninput="calculate()"),
                        Span(id="output-info", cls="info-text"),
                        cls="form-group"
                    ),
                    cls="form-section"
                ),
                Div(
                    H2("Cost Estimate", style="margin-top: 0;"),
                    Div(id="cost-display", cls="cost-display", children="$0.00"),
                    Div(id="breakdown", cls="breakdown"),
                    Div(
                        Button("Export CSV", id="export-csv", cls="btn-primary", onclick="exportCSV()"),
                        Button("Export JSON", id="export-json", cls="btn-secondary", onclick="exportJSON()"),
                        cls="btn-group"
                    ),
                    cls="result-section"
                ),
                cls="container"
            ),
            Script("""
                const models = """ + json.dumps({k: {
                    "name": v.name,
                    "provider": v.provider,
                    "context_window": v.context_window,
                    "max_output": v.max_output,
                    "price_input": v.price_input,
                    "price_output": v.price_output
                } for k, v in models.items()}) + """;
                const providers = """ + json.dumps(providers) + """;
                
                // Initialize provider dropdown
                function initProviders() {
                    const providerSelect = document.getElementById('provider-select');
                    providerSelect.innerHTML = '';
                    providers.forEach(provider => {
                        const opt = document.createElement('option');
                        opt.value = provider;
                        opt.textContent = provider;
                        providerSelect.appendChild(opt);
                    });
                    if (providers.length > 0) {
                        updateModels();
                    }
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
                    if (!modelId) return;
                    const model = models[modelId];
                    const ctxWindow = model.context_window;
                    const maxOut = model.max_output;
                    
                    document.getElementById('input-tokens').max = ctxWindow;
                    document.getElementById('output-tokens').max = Math.min(maxOut, ctxWindow);
                    
                    const inputInfo = document.getElementById('input-info');
                    inputInfo.textContent = `Max: ${ctxWindow.toLocaleString()} tokens`;
                    
                    const outputInfo = document.getElementById('output-info');
                    outputInfo.textContent = `Max: ${Math.min(maxOut, ctxWindow).toLocaleString()} tokens`;
                    
                    // Set defaults: 20% of context window for output, rest for input
                    const defaultOut = Math.min(Math.floor(ctxWindow * 0.2), maxOut);
                    const defaultIn = Math.floor(ctxWindow * 0.3);
                    
                    document.getElementById('input-tokens').value = defaultIn;
                    document.getElementById('output-tokens').value = defaultOut;
                    
                    calculate();
                }
                
                function calculate() {
                    const modelId = document.getElementById('model-select').value;
                    if (!modelId) return;
                    
                    const model = models[modelId];
                    const agents = parseInt(document.getElementById('agents').value) || 1;
                    const iterations = parseInt(document.getElementById('iterations').value) || 1;
                    const inputTokens = parseInt(document.getElementById('input-tokens').value) || 0;
                    const outputTokens = parseInt(document.getElementById('output-tokens').value) || 0;
                    
                    // Validate
                    if (inputTokens + outputTokens > model.context_window) {
                        document.getElementById('cost-display').textContent = 'Error: Exceeds context window';
                        document.getElementById('breakdown').innerHTML = '';
                        return;
                    }
                    
                    const totalIn = inputTokens * agents * iterations;
                    const totalOut = outputTokens * agents * iterations;
                    const costIn = (totalIn / 1000000) * model.price_input;
                    const costOut = (totalOut / 1000000) * model.price_output;
                    const totalCost = costIn + costOut;
                    
                    document.getElementById('cost-display').textContent = '$' + totalCost.toFixed(2);
                    
                    const breakdown = document.getElementById('breakdown');
                    breakdown.innerHTML = `
                        <div class="breakdown-item">
                            <span>Input Tokens:</span>
                            <span>${totalIn.toLocaleString()} ($${costIn.toFixed(4)})</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Output Tokens:</span>
                            <span>${totalOut.toLocaleString()} ($${costOut.toFixed(4)})</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Cost per Agent:</span>
                            <span>$${(totalCost / agents).toFixed(4)}</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Cost per Iteration:</span>
                            <span>$${(totalCost / iterations).toFixed(4)}</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Model:</span>
                            <span>${model.name}</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Input Rate:</span>
                            <span>$${model.price_input.toFixed(2)} / 1M tokens</span>
                        </div>
                        <div class="breakdown-item">
                            <span>Output Rate:</span>
                            <span>$${model.price_output.toFixed(2)} / 1M tokens</span>
                        </div>
                    `;
                    
                    window.calcResult = {
                        model: model.name,
                        provider: model.provider,
                        agents, iterations, inputTokens, outputTokens,
                        totalIn, totalOut, costIn, costOut, totalCost,
                        timestamp: new Date().toISOString()
                    };
                }
                
                function exportCSV() {
                    if (!window.calcResult) return;
                    const r = window.calcResult;
                    const csv = `Model,Provider,Agents,Iterations,Input Tokens,Output Tokens,Total Input Tokens,Total Output Tokens,Input Cost,Output Cost,Total Cost,Timestamp
${r.model},${r.provider},${r.agents},${r.iterations},${r.inputTokens},${r.outputTokens},${r.totalIn},${r.totalOut},${r.costIn.toFixed(4)},${r.costOut.toFixed(4)},${r.totalCost.toFixed(4)},${r.timestamp}`;
                    const blob = new Blob([csv], { type: 'text/csv' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `ai-cost-${Date.now()}.csv`;
                    a.click();
                }
                
                function exportJSON() {
                    if (!window.calcResult) return;
                    const json = JSON.stringify(window.calcResult, null, 2);
                    const blob = new Blob([json], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `ai-cost-${Date.now()}.json`;
                    a.click();
                }
                
                // Initialize on page load
                if (document.readyState === 'loading') {
                    document.addEventListener('DOMContentLoaded', initProviders);
                } else {
                    initProviders();
                }
            """)
        )
    )

if __name__ == "__main__": serve()
