import streamlit as st
import streamlit.components.v1 as components

# Konfiguration der Seite
st.set_page_config(
    page_title="Richter Management Tools",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- HTML INHALTE ALS STRINGS (Zusammengefasst aus deinen Dateien) ---

HTML_PERSONALKOSTEN = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #121212; color: #e5e7eb; font-family: sans-serif; margin: 0; padding: 20px; }
        .card { background: #1e1e1e; border-radius: 12px; border: 1px solid #2d2d2d; padding: 20px; margin-bottom: 20px; }
        input, select { background-color: #2d2d2d !important; border: 1px solid #404040 !important; color: white !important; padding: 8px; border-radius: 6px; width: 100%; }
        .btn-red { background-color: #dc2626; color: white; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; border: none; }
        .btn-red:hover { background-color: #b91c1c; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { text-align: left; color: #9ca3af; border-bottom: 1px solid #2d2d2d; padding: 10px; }
        td { padding: 12px 10px; border-bottom: 1px solid #2d2d2d; }
    </style>
</head>
<body>
    <div class="card">
        <h1 class="text-2xl font-bold text-red-600 mb-6">Personalkosten Richter</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div>
                <label class="block mb-2 text-sm font-medium">Monatlicher Umsatz (€)</label>
                <input type="number" id="revenue" placeholder="z.B. 500000" oninput="calculate()">
            </div>
            <div class="text-center p-4 bg-black/20 rounded-lg">
                <span class="block text-gray-400 text-sm uppercase">Gesamt Personalkosten</span>
                <span id="total-cost" class="text-3xl font-bold text-white">0,00 €</span>
            </div>
            <div class="text-center p-4 bg-black/20 rounded-lg">
                <span class="block text-gray-400 text-sm uppercase">Personalquote</span>
                <span id="quote" class="text-3xl font-bold text-blue-400">0,0 %</span>
            </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 bg-black/30 p-4 rounded-lg">
            <input type="text" id="name" placeholder="Name Mitarbeiter">
            <input type="number" id="salary" placeholder="Bruttogehalt">
            <select id="type">
                <option value="1.21">Vollzeit (+21% AG-Anteil)</option>
                <option value="1.05">Minijob (+5% Pauschale)</option>
                <option value="1.20">Aushilfe (+20% AG-Anteil)</option>
            </select>
            <button class="btn-red" onclick="addEmployee()">Hinzufügen</button>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Mitarbeiter</th>
                    <th>Brutto</th>
                    <th>Typ</th>
                    <th>AG-Kosten (geschätzt)</th>
                    <th>Aktion</th>
                </tr>
            </thead>
            <tbody id="employee-list"></tbody>
        </table>
    </div>

    <script>
        let employees = [];
        function addEmployee() {
            const name = document.getElementById('name').value;
            const salary = parseFloat(document.getElementById('salary').value);
            const factor = parseFloat(document.getElementById('type').value);
            if (!name || isNaN(salary)) return;
            employees.push({ name, salary, factor });
            document.getElementById('name').value = '';
            document.getElementById('salary').value = '';
            render();
        }
        function deleteEmployee(index) {
            employees.splice(index, 1);
            render();
        }
        function render() {
            const list = document.getElementById('employee-list');
            list.innerHTML = '';
            let total = 0;
            employees.forEach((emp, i) => {
                const cost = emp.salary * emp.factor;
                total += cost;
                list.innerHTML += `<tr>
                    <td>${emp.name}</td>
                    <td>${emp.salary.toLocaleString('de-DE')} €</td>
                    <td>${emp.factor > 1.1 ? 'SV-Pflichtig' : 'Minijob'}</td>
                    <td class="font-bold text-white">${cost.toLocaleString('de-DE', {minimumFractionDigits: 2})} €</td>
                    <td><button onclick="deleteEmployee(${i})" style="color:#ef4444">Löschen</button></td>
                </tr>`;
            });
            document.getElementById('total-cost').innerText = total.toLocaleString('de-DE', {minimumFractionDigits: 2}) + ' €';
            const rev = parseFloat(document.getElementById('revenue').value) || 0;
            const quote = rev > 0 ? (total / rev) * 100 : 0;
            document.getElementById('quote').innerText = quote.toFixed(1) + ' %';
            document.getElementById('quote').style.color = quote > 16 ? '#ef4444' : '#60a5fa';
        }
        function calculate() { render(); }
    </script>
</body>
</html>
"""

HTML_KER_ANALYSE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #121212; color: #e5e7eb; font-family: sans-serif; padding: 20px; }
        .card { background: #1e1e1e; border-radius: 12px; border: 1px solid #2d2d2d; padding: 20px; }
        .grid-row { display: grid; grid-template-columns: 1fr 150px 100px; gap: 10px; padding: 8px; border-bottom: 1px solid #2d2d2d; }
        .header-row { font-weight: bold; color: #9ca3af; border-bottom: 2px solid #dc2626; }
        input { background: #2d2d2d; border: 1px solid #404040; color: white; padding: 4px; text-align: right; width: 100%; }
        .total-row { background: #2d2d2d; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1 class="text-2xl font-bold text-red-600 mb-6">KER Analyse Tool</h1>
        <div class="grid-row header-row">
            <div>Bezeichnung</div>
            <div>Wert (€)</div>
            <div>%</div>
        </div>
        <div id="ker-content">
            <!-- Dynamischer Content -->
        </div>
    </div>
    <script>
        const rows = [
            { label: "Umsatzerlöse", val: 540000, isMain: true },
            { label: "Wareneinsatz", val: 380000, isMain: false },
            { label: "Rohertrag", val: 160000, isTotal: true },
            { label: "Personalkosten", val: 85000, isMain: false },
            { label: "Raumkosten", val: 12000, isMain: false },
            { label: "Werbekosten", val: 3500, isMain: false },
            { label: "Sonst. Kosten", val: 15000, isMain: false },
            { label: "Betriebsergebnis", val: 44500, isTotal: true }
        ];

        function render() {
            const container = document.getElementById('ker-content');
            container.innerHTML = '';
            const revenue = rows[0].val;
            
            rows.forEach((row, i) => {
                const perc = revenue > 0 ? (row.val / revenue * 100).toFixed(1) : 0;
                const className = row.isTotal ? 'grid-row total-row' : 'grid-row';
                container.innerHTML += `
                    <div class="${className}">
                        <div>${row.label}</div>
                        <div><input type="number" value="${row.val}" oninput="update(${i}, this.value)"></div>
                        <div class="text-gray-400">${perc}%</div>
                    </div>
                `;
            });
        }
        function update(i, v) {
            rows[i].val = parseFloat(v) || 0;
            // Hier könnte man automatische Berechnungen für Rohertrag etc. einfügen
            render();
        }
        render();
    </script>
</body>
</html>
"""

# --- STREAMLIT UI ---

# Custom CSS um Streamlit "sauber" zu machen
st.markdown("""
    <style>
        .block-container { padding: 0rem; max-width: 100%; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stSidebar"] { background-color: #1e1e1e; }
        [data-testid="stSidebar"] h1 { color: #dc2626 !important; }
        /* Entfernt den grauen Rahmen um Iframes */
        iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("RICHTER TOOLS")
st.sidebar.markdown("---")

selection = st.sidebar.radio(
    "Menü auswählen",
    ["Personalkosten Rechner", "KER Analyse Dashboard"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("v2.0.0 - Integrierte Lösung")

# Logik für die Anzeige
if selection == "Personalkosten Rechner":
    # Wir nutzen eine sehr große Höhe, damit der Iframe selbst nicht scrollt
    # sondern die gesamte Seite genutzt wird.
    components.html(HTML_PERSONALKOSTEN, height=1500, scrolling=False)

elif selection == "KER Analyse Dashboard":
    components.html(HTML_KER_ANALYSE, height=1500, scrolling=False)
