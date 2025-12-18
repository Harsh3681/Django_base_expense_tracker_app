const API = "/api";

let RATES = null;           // { USD: 1, INR: 91.02, ... }
let BASE_CCY = "USD";
let PIE = null;

function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  setTimeout(() => toast.remove(), 3500);
}


const categoryColors = {
  Food: "#ef4444",
  Transport: "#3b82f6",
  Entertainment: "#8b5cf6",
  Bills: "#f59e0b",
  Healthcare: "#10b981",
  Shopping: "#ec4899",
  Other: "#6b7280",
};

document.getElementById("addExpenseForm").addEventListener("submit", async e => {
  e.preventDefault();

  const form = e.target;
  const payload = {
    note: form.note.value,
    amount: form.amount.value,
    category: form.category.value,
    currency: "INR",
    created_at: form.date.value, 
  };

  const res = await fetch("/api/expenses/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    showToast("Failed to add expense", "error");
    return;
  }

  closeModal();
  form.reset();

  await loadDashboard(); // 🔥 live refresh everything
});


async function loadDashboard() {
  await ensureRates();

  const form = new FormData(document.getElementById("filtersForm"));
  const params = new URLSearchParams(form).toString();

  const expenses = await fetch(`/api/expenses/?${params}`).then(r => r.json());

  renderTotal(expenses);
  renderTable(expenses);
  renderCharts(expenses);
}


function renderTotal(expenses) {
  const total = expenses.reduce((s, e) => s + Number(e.amount), 0);
  document.getElementById("totalAmount").textContent = `₹${total.toLocaleString()}`;
}

function renderTable(expenses) {
  const tbody = document.getElementById("expensesTable");
  tbody.innerHTML = "";

  expenses.forEach(e => {
    const rowId = `row-${e.id}`;
    const defaultTo = "USD";

    tbody.innerHTML += `
      <tr id="${rowId}" class="border-t">
        <td class="p-3">${e.created_at.slice(0,10)}</td>
        <td class="p-3">
          <span class="view">${escapeHtml(e.note || "")}</span>
          <input class="edit hidden border rounded px-2 py-1 w-full" name="note" value="${escapeAttr(e.note || "")}">
        </td>
        <td class="p-3">
          <span class="view">
            <span class="px-2 py-1 rounded text-white" style="background:${categoryColors[e.category] || "#6b7280"}">
              ${e.category}
            </span>
          </span>
          <select class="edit hidden border rounded px-2 py-1 w-full" name="category">
            ${categoryOptions(e.category)}
          </select>
        </td>
        <td class="p-3">
          <span class="view">₹${Number(e.amount).toLocaleString()}</span>
          <input class="edit hidden border rounded px-2 py-1 w-32" type="number" step="0.01" name="amount" value="${e.amount}">
        </td>

        <td class="p-3">
          <div class="flex gap-2 items-center">
            <div class="relative w-44">
              <input class="border rounded-lg px-2 py-1 w-full text-sm"
                     placeholder="Search currency..."
                     oninput="filterCurrencyList(${e.id}, this.value)" />
              <select id="ccy-${e.id}"
                      class="border rounded-lg px-2 py-1 w-full mt-2 text-sm"
                      onchange="updateWorldwide(${e.id})">
                ${currencyOptions(defaultTo)}
              </select>
            </div>
            <div class="text-sm font-semibold" id="world-${e.id}">—</div>
          </div>
        </td>

        <td class="p-3 text-right whitespace-nowrap">
          <button class="text-blue-600 hover:underline" onclick="startEdit(${e.id})">Edit</button>
          <button class="text-red-600 hover:underline ml-4" onclick="deleteExpense(${e.id})">Delete</button>
          <button class="text-green-600 hover:underline ml-4 hidden" id="save-${e.id}" onclick="saveEdit(${e.id})">Save</button>
          <button class="text-gray-500 hover:underline ml-2 hidden" id="cancel-${e.id}" onclick="cancelEdit(${e.id})">Cancel</button>
        </td>
      </tr>
    `;

    // compute first worldwide value after row inserted
    setTimeout(() => updateWorldwide(e.id), 0);
  });
}


function renderCharts(expenses) {
  const totals = {};
  expenses.forEach(e => totals[e.category] = (totals[e.category] || 0) + Number(e.amount));

  if (!expenses.length) {
    document.getElementById("chartsSection").classList.add("hidden");
    return;
  }

  document.getElementById("chartsSection").classList.remove("hidden");

  // Bars
  const bars = document.getElementById("bars");
  bars.innerHTML = "";

  const totalSum = Object.values(totals).reduce((a,b)=>a+b,0);

  Object.entries(totals).forEach(([cat, amt]) => {
    const pct = ((amt / totalSum) * 100).toFixed(1);
    bars.innerHTML += `
      <div class="mb-3">
        <div class="flex justify-between text-sm">
          <span>${cat}</span>
          <span>₹${amt} (${pct}%)</span>
        </div>
        <div class="bg-gray-200 h-3 rounded">
          <div class="h-3 rounded" style="width:${pct}%;background:${categoryColors[cat]}"></div>
        </div>
      </div>
    `;
  });

  // Pie
  if (PIE) PIE.destroy(); // 🔥 important

  PIE = new Chart(document.getElementById("pieChart"), {
    type: "pie",
    data: {
      labels: Object.keys(totals),
      datasets: [{
        data: Object.values(totals),
        backgroundColor: Object.keys(totals).map(c => categoryColors[c]),
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        animateRotate: true,
        duration: 700,
      },
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });

}

function resetFilters() {
  const form = document.getElementById("filtersForm");
  form.reset();

  // force category back to "all"
  form.querySelector('select[name="category"]').value = "all";

  loadDashboard();
}


function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

function openAddExpense() {
  document.getElementById("addExpenseModal").classList.remove("hidden");
  document.getElementById("addExpenseModal").classList.add("flex");
}

function closeModal() {
  document.getElementById("addExpenseModal").classList.add("hidden");
  document.getElementById("addExpenseModal").classList.remove("flex");
}

async function ensureRates() {
  if (RATES) return;

  // try to load latest stored rates
  const r1 = await fetch("/api/integrations/rates/");
  const data = await r1.json();

  if (data.rates && Object.keys(data.rates).length > 5) {
    BASE_CCY = data.base;
    RATES = data.rates;
    return;
  }

  // if not available, sync now (base USD)
  await fetch("/api/integrations/exchange-rate/", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ base: "USD" }),
  });

  const r2 = await fetch("/api/integrations/rates/");
  const data2 = await r2.json();
  BASE_CCY = data2.base;
  RATES = data2.rates || {};
}

function convert(amount, from, to) {
  if (!RATES || !RATES[from] || !RATES[to]) return null;

  // RATES are relative to BASE_CCY
  // Convert from -> BASE -> to
  // If your expense currency is INR and BASE=USD:
  // amount_in_usd = amount / RATES["INR"]
  const amountInBase = (from === BASE_CCY) ? amount : (amount / Number(RATES[from] || 1));
  const out = amountInBase * Number(RATES[to]);
  return out;
}


function categoryOptions(selected) {
  const cats = ["Food","Transport","Entertainment","Bills","Healthcare","Shopping","Other"];
  return cats.map(c => `<option ${c===selected?"selected":""} value="${c}">${c}</option>`).join("");
}

function currencyOptions(selected) {
  const codes = Object.keys(RATES || {}).sort();
  return codes.map(c => `<option ${c===selected?"selected":""} value="${c}">${c}</option>`).join("");
}

function filterCurrencyList(id, q) {
  q = (q || "").toUpperCase();
  const sel = document.getElementById(`ccy-${id}`);
  const current = sel.value;
  sel.innerHTML = currencyOptions(current).split("</option>")
    .filter(x => x.includes(`value="`) && x.toUpperCase().includes(q))
    .join("</option>") + "</option>";
}

function updateWorldwide(id) {
  const row = document.getElementById(`row-${id}`);
  const amount = Number(row.querySelector('input[name="amount"]').value || row.querySelector(".view")?.textContent?.replace(/[^\d.]/g,'') || 0);

  // our DB stores currency field too (default INR)
  // If you always use INR, keep it hardcoded:
  const from = "INR";

  const to = document.getElementById(`ccy-${id}`).value;
  const out = convert(amount, from, to);
  document.getElementById(`world-${id}`).textContent =
    out == null ? "—" : `${to} ${out.toFixed(2)}`;
}

// safety helpers
function escapeHtml(s){return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");}
function escapeAttr(s){return escapeHtml(s).replaceAll('"',"&quot;");}



function startEdit(id) {
  const row = document.getElementById(`row-${id}`);
  row.querySelectorAll(".view").forEach(el => el.classList.add("hidden"));
  row.querySelectorAll(".edit").forEach(el => el.classList.remove("hidden"));
  document.getElementById(`save-${id}`).classList.remove("hidden");
  document.getElementById(`cancel-${id}`).classList.remove("hidden");
}

function cancelEdit(id) {
  loadDashboard(); // simplest reset
}

async function saveEdit(id) {
  const row = document.getElementById(`row-${id}`);
  const note = row.querySelector('input[name="note"]').value;
  const amount = row.querySelector('input[name="amount"]').value;
  const category = row.querySelector('select[name="category"]').value;

  const res = await fetch(`/api/expenses/${id}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      // "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ note, amount, category }),
  });

  if (!res.ok) {
    showToast("Update failed", "error");
    return;
  }

  await loadDashboard();
}

async function deleteExpense(id) {
  if (!window.confirm("Delete this expense?")) return;

  const res = await fetch(`/api/expenses/${id}/`, {
    method: "DELETE",
    // headers: { "X-CSRFToken": getCSRFToken() },
    
  });

  if (!res.ok) {
    alert("Delete failed");
    return;
  }

  await loadDashboard();
}

function applyFilters(e) {
  e.preventDefault();        
  loadDashboard();        
}


loadDashboard();
