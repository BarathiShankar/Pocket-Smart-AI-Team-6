/**
 * PocketSmart AI — Client Application Engine
 * Luxury Black & Gold Theme • Gemini Flash Pro • Multi-Planner Architecture
 */

// Dynamic Backend URL resolution
const getBaseUrl = () => {
  if (window.location.protocol === 'file:') {
    return 'http://127.0.0.1:5000';
  }
  return window.location.origin;
};

const BASE_URL = getBaseUrl();

// Global Application State
const state = {
  currentView: 'landing-view',
  activePlanner: 'home',
  currentPlanResult: null,
  recommendationFilter: 'all',
  selectedImageFile: null,
  currency: localStorage.getItem('pocketsmart_currency') || 'INR',
  currencyRate: 1.0, // 1 INR = 1 INR, or 1 USD = ~85 INR for display conversion
  user: null,
  history: [],
  savedItems: []
};

// ==========================================================================
// INITIALIZATION & EVENT LISTENERS
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  initDropzone();
  checkAuthStatus();
  fetchHistory();
  updateCurrencyDisplay();
});

// ==========================================================================
// VIEW NAVIGATION & ROUTING
// ==========================================================================
function switchView(viewId) {
  state.currentView = viewId;
  document.querySelectorAll('.view-container').forEach(el => {
    el.classList.remove('active');
  });

  const target = document.getElementById(viewId);
  if (target) {
    target.classList.add('active');
  }

  // Update navbar links active state
  document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
  const navMap = {
    'landing-view': 'nav-landing',
    'dashboard-view': 'nav-dashboard',
    'home-planner-view': 'nav-home',
    'party-planner-view': 'nav-party',
    'jewelry-planner-view': 'nav-jewelry',
    'history-view': 'nav-history'
  };
  if (navMap[viewId]) {
    const navLink = document.getElementById(navMap[viewId]);
    if (navLink) navLink.classList.add('active');
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });

  // If entering dashboard or history, refresh data
  if (viewId === 'dashboard-view' || viewId === 'history-view') {
    fetchHistory();
  }
}

function openPlanner(type) {
  state.activePlanner = type;
  if (type === 'home') {
    resetWizard('home');
    switchView('home-planner-view');
  } else if (type === 'party') {
    resetWizard('party');
    updateGuestBudgetPreview();
    switchView('party-planner-view');
  } else if (type === 'jewelry') {
    resetWizard('jewelry');
    switchView('jewelry-planner-view');
  }
}

function openActivePlannerAgain() {
  if (state.activePlanner) {
    openPlanner(state.activePlanner);
  } else {
    openPlanner('home');
  }
}

// ==========================================================================
// WIZARD STEPPERS (HOME, PARTY, JEWELRY)
// ==========================================================================
function wizardNext(planner, currentStep, nextStep) {
  // Validate current step inputs
  const currentContent = document.getElementById(`${planner}-step-${currentStep}`);
  const requiredInputs = currentContent.querySelectorAll('input[required], select[required]');
  for (let input of requiredInputs) {
    if (!input.value.trim()) {
      showToast(`Please fill out the required field: ${input.previousElementSibling?.innerText || 'Input'}`, 'warning');
      input.focus();
      return;
    }
  }

  // Switch content
  document.getElementById(`${planner}-step-${currentStep}`).classList.remove('active');
  document.getElementById(`${planner}-step-${nextStep}`).classList.add('active');

  // Update indicators
  const currentInd = document.getElementById(`${planner}-step-indicator-${currentStep}`);
  const nextInd = document.getElementById(`${planner}-step-indicator-${nextStep}`);
  if (currentInd) {
    currentInd.classList.remove('active');
    currentInd.classList.add('completed');
  }
  if (nextInd) {
    nextInd.classList.add('active');
  }
}

function wizardPrev(planner, currentStep, prevStep) {
  document.getElementById(`${planner}-step-${currentStep}`).classList.remove('active');
  document.getElementById(`${planner}-step-${prevStep}`).classList.add('active');

  const currentInd = document.getElementById(`${planner}-step-indicator-${currentStep}`);
  const prevInd = document.getElementById(`${planner}-step-indicator-${prevStep}`);
  if (currentInd) currentInd.classList.remove('active');
  if (prevInd) {
    prevInd.classList.remove('completed');
    prevInd.classList.add('active');
  }
}

function resetWizard(planner) {
  for (let i = 1; i <= 3; i++) {
    const stepEl = document.getElementById(`${planner}-step-${i}`);
    const indEl = document.getElementById(`${planner}-step-indicator-${i}`);
    if (stepEl) {
      if (i === 1) stepEl.classList.add('active');
      else stepEl.classList.remove('active');
    }
    if (indEl) {
      indEl.classList.remove('completed');
      if (i === 1) indEl.classList.add('active');
      else indEl.classList.remove('active');
    }
  }
}

function updateGuestBudgetPreview() {
  const budget = parseFloat(document.getElementById('partyBudget')?.value || 0);
  const guests = parseInt(document.getElementById('partyGuests')?.value || 1);
  const display = document.getElementById('partyPerGuestDisplay');
  if (display) {
    const perGuest = budget / Math.max(1, guests);
    display.innerText = `${formatCurrency(perGuest)} / guest`;
  }
}

// ==========================================================================
// DRAG & DROP MULTIMODAL IMAGE UPLOAD (FOR JEWELRY)
// ==========================================================================
function initDropzone() {
  const dropzone = document.getElementById('jewelryDropzone');
  if (!dropzone) return;

  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add('dragover');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove('dragover');
    }, false);
  });

  dropzone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length) {
      handleImageFile(files[0]);
    }
  });
}

function handleImageSelected(input) {
  if (input.files && input.files[0]) {
    handleImageFile(input.files[0]);
  }
}

function handleImageFile(file) {
  if (!file.type.startsWith('image/')) {
    showToast('Please upload a valid image file (PNG, JPG, WebP)', 'error');
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    showToast('Image size exceeds 10MB limit', 'error');
    return;
  }

  state.selectedImageFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    const previewBox = document.getElementById('imagePreviewBox');
    const previewImg = document.getElementById('imagePreviewImg');
    const dropzone = document.getElementById('jewelryDropzone');
    if (previewBox && previewImg) {
      previewImg.src = e.target.result;
      previewBox.style.display = 'block';
      if (dropzone) dropzone.style.display = 'none';
      showToast('Outfit photo attached for Gemini Multimodal Analysis', 'success');
    }
  };
  reader.readAsDataURL(file);
}

function clearSelectedImage() {
  state.selectedImageFile = null;
  const fileInput = document.getElementById('jewelryImageInput');
  if (fileInput) fileInput.value = '';
  const previewBox = document.getElementById('imagePreviewBox');
  const dropzone = document.getElementById('jewelryDropzone');
  if (previewBox) previewBox.style.display = 'none';
  if (dropzone) dropzone.style.display = 'block';
}

// ==========================================================================
// SUBMIT PLANNERS (API INTEGRATION)
// ==========================================================================
function getCustomApiKeyHeader() {
  const customKey = localStorage.getItem('pocketsmart_gemini_key');
  return customKey ? { 'X-Gemini-Key': customKey } : {};
}

async function submitHomePlan() {
  const budget = parseFloat(document.getElementById('homeBudget').value);
  if (!budget || budget <= 0) {
    showToast('Please enter a valid budget', 'warning');
    return;
  }

  const payload = {
    budget: budget,
    location: document.getElementById('homeLocation').value,
    room_type: document.getElementById('homeRoomType').value,
    num_rooms: document.getElementById('homeNumRooms').value,
    style: document.getElementById('homeStyle').value,
    colors: document.getElementById('homeColors').value,
    furniture: document.getElementById('homeFurniture').value,
    lighting: document.getElementById('homeLighting').value,
    decor: document.getElementById('homeDecor').value,
    storage_flooring: document.getElementById('homeStorageFlooring').value,
    priorities: document.getElementById('homePriorities').value
  };

  showLoading('Synthesizing Interior Architectural Models & Pricing...');

  try {
    const res = await fetch(`${BASE_URL}/api/planner/home`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getCustomApiKeyHeader()
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    hideLoading();

    if (data.success && data.data) {
      state.currentPlanResult = data.data;
      renderResultsView(data.data, 'Home Interior');
      showToast('AI Interior Plan Generated Successfully!', 'success');
    } else {
      showToast(data.error || 'Failed to generate interior plan', 'error');
    }
  } catch (err) {
    hideLoading();
    showToast(`Connection error: ${err.message}`, 'error');
  }
}

async function submitPartyPlan() {
  const budget = parseFloat(document.getElementById('partyBudget').value);
  const guests = parseInt(document.getElementById('partyGuests').value);
  if (!budget || budget <= 0 || !guests || guests <= 0) {
    showToast('Please enter valid budget and guest count', 'warning');
    return;
  }

  const payload = {
    budget: budget,
    guests: guests,
    event_type: document.getElementById('partyEventType').value,
    location: document.getElementById('partyLocation').value,
    date: document.getElementById('partyDate').value,
    venue: document.getElementById('partyVenue').value,
    food: document.getElementById('partyFood').value,
    decoration: document.getElementById('partyDecoration').value,
    photography: document.getElementById('partyPhotography').value,
    entertainment: document.getElementById('partyEntertainment').value,
    accommodation: document.getElementById('partyAccommodation').value,
    priorities: document.getElementById('partyPriorities').value
  };

  showLoading('Analyzing Event Logistics, Menus & Catering Platform Bundles...');

  try {
    const res = await fetch(`${BASE_URL}/api/planner/party`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getCustomApiKeyHeader()
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    hideLoading();

    if (data.success && data.data) {
      state.currentPlanResult = data.data;
      renderResultsView(data.data, 'Party & Event');
      showToast('AI Event Plan Generated Successfully!', 'success');
    } else {
      showToast(data.error || 'Failed to generate party plan', 'error');
    }
  } catch (err) {
    hideLoading();
    showToast(`Connection error: ${err.message}`, 'error');
  }
}

async function submitJewelryPlan() {
  const budget = parseFloat(document.getElementById('jewelryBudget').value);
  if (!budget || budget <= 0) {
    showToast('Please enter a valid jewelry budget', 'warning');
    return;
  }

  showLoading('Running Gemini Multimodal Vision & Hallmark Valuation...');

  try {
    let res;
    if (state.selectedImageFile) {
      // Use FormData for multimodal upload
      const formData = new FormData();
      formData.append('budget', budget);
      formData.append('jewelry_category', document.getElementById('jewelryCategory').value);
      formData.append('occasion', document.getElementById('jewelryOccasion').value);
      formData.append('preferred_platform', document.getElementById('jewelryPlatform').value);
      formData.append('metal', document.getElementById('jewelryMetal').value);
      formData.append('gemstone', document.getElementById('jewelryGemstone').value);
      formData.append('style', document.getElementById('jewelryStyle').value);
      formData.append('color', document.getElementById('jewelryColor').value);
      formData.append('notes', document.getElementById('jewelryNotes').value);
      formData.append('image', state.selectedImageFile);

      res = await fetch(`${BASE_URL}/api/planner/jewelry`, {
        method: 'POST',
        headers: {
          ...getCustomApiKeyHeader()
        },
        body: formData
      });
    } else {
      // Standard JSON request
      const payload = {
        budget: budget,
        jewelry_category: document.getElementById('jewelryCategory').value,
        occasion: document.getElementById('jewelryOccasion').value,
        preferred_platform: document.getElementById('jewelryPlatform').value,
        metal: document.getElementById('jewelryMetal').value,
        gemstone: document.getElementById('jewelryGemstone').value,
        style: document.getElementById('jewelryStyle').value,
        color: document.getElementById('jewelryColor').value,
        notes: document.getElementById('jewelryNotes').value
      };

      res = await fetch(`${BASE_URL}/api/planner/jewelry`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getCustomApiKeyHeader()
        },
        body: JSON.stringify(payload)
      });
    }

    const data = await res.json();
    hideLoading();

    if (data.success && data.data) {
      state.currentPlanResult = data.data;
      renderResultsView(data.data, 'Jewelry Styling');
      showToast('AI Jewelry & Styling Plan Generated!', 'success');
    } else {
      showToast(data.error || 'Failed to generate jewelry plan', 'error');
    }
  } catch (err) {
    hideLoading();
    showToast(`Connection error: ${err.message}`, 'error');
  }
}

// ==========================================================================
// RENDER PLAN RESULTS & RECOMMENDATIONS
// ==========================================================================
function renderResultsView(plan, plannerTitle) {
  state.recommendationFilter = 'all';

  // Set titles
  document.getElementById('resultsPlannerBadge').innerText = `${plannerTitle} Plan`;
  document.getElementById('resultsTitle').innerText = `${plannerTitle} Smart Allocation & Recommendations`;

  const summary = plan.budget_summary || {};
  document.getElementById('resultsVerdict').innerText = summary.financial_verdict || 'Plan optimized for high-value allocation within constraints.';

  // Render KPI cards
  document.getElementById('resTotalBudget').innerText = formatCurrency(summary.total_budget || 0);
  document.getElementById('resEstimatedSpend').innerText = formatCurrency(summary.estimated_spend || summary.allocated_total || 0);
  document.getElementById('resContingency').innerText = `${formatCurrency(summary.contingency_reserve || 0)} (${summary.contingency_percentage || 10}%)`;
  document.getElementById('resRemaining').innerText = formatCurrency(summary.remaining_unallocated || 0);

  // Render Stacked Allocations Bar & Legend
  renderAllocationsBar(plan.allocation || []);

  // Multimodal Vision Spotlight (if jewelry and image available)
  const spotlightBox = document.getElementById('multimodalSpotlightCard');
  if (plan.image_analysis && (plan.uploaded_image_url || state.selectedImageFile)) {
    spotlightBox.style.display = 'block';
    const previewImg = document.getElementById('multimodalResultImg');
    if (plan.uploaded_image_url) {
      previewImg.src = `${BASE_URL}${plan.uploaded_image_url}`;
    } else if (state.selectedImageFile) {
      previewImg.src = document.getElementById('imagePreviewImg')?.src || '';
    }
    document.getElementById('multimodalOutfitDetails').innerHTML = `<strong>Outfit Characteristics:</strong> ${plan.image_analysis.outfit_detected || ''}`;
    document.getElementById('multimodalHarmonyDetails').innerHTML = `<strong>Metal & Style Match:</strong> ${plan.image_analysis.complementary_metals || ''} • ${plan.image_analysis.style_harmony || ''}`;
  } else {
    spotlightBox.style.display = 'none';
  }

  // Render Recommendations Cards
  renderRecommendationCards(plan.recommendations || []);

  // Render Tips & Warnings
  const tipsList = document.getElementById('tipsList');
  tipsList.innerHTML = (plan.tips || [
    "Always inspect BIS Hallmarking and verify HUID numbers on fine jewelry.",
    "Allocate at least 10% safety contingency reserve for unexpected delivery or installation overhead."
  ]).map(t => `<li><i class="fa-solid fa-check text-gold"></i> <span>${t}</span></li>`).join('');

  const warningsList = document.getElementById('warningsList');
  warningsList.innerHTML = (plan.warnings || [
    "Verify seasonal vendor availability and lock pricing quotes at least 2 weeks in advance."
  ]).map(w => `<li><i class="fa-solid fa-triangle-exclamation" style="color: var(--accent-amber);"></i> <span>${w}</span></li>`).join('');

  // Switch to results view
  switchView('results-view');
}

function renderAllocationsBar(allocations) {
  const barContainer = document.getElementById('allocStackedBar');
  const legendContainer = document.getElementById('allocLegend');
  if (!barContainer || !legendContainer) return;

  const colors = ['#C8A24A', '#E6C766', '#10B981', '#06B6D4', '#F59E0B', '#8B5CF6', '#EC4899'];
  barContainer.innerHTML = '';
  legendContainer.innerHTML = '';

  const totalAlloc = allocations.reduce((acc, a) => acc + (a.allocated_amount || 0), 0) || 1;

  allocations.forEach((alloc, idx) => {
    const color = colors[idx % colors.length];
    const pct = Math.max(5, Math.round(((alloc.allocated_amount || 0) / totalAlloc) * 100));

    // Bar segment
    const seg = document.createElement('div');
    seg.className = 'alloc-segment';
    seg.style.width = `${pct}%`;
    seg.style.backgroundColor = color;
    seg.title = `${alloc.category}: ${formatCurrency(alloc.allocated_amount)} (${pct}%)`;
    barContainer.appendChild(seg);

    // Legend item
    const leg = document.createElement('div');
    leg.className = 'legend-item';
    leg.innerHTML = `
      <div class="legend-color" style="background-color: ${color};"></div>
      <span><strong>${alloc.category}</strong>: ${formatCurrency(alloc.allocated_amount)} (${alloc.percentage || pct}%)</span>
    `;
    legendContainer.appendChild(leg);
  });
}

function renderRecommendationCards(recommendations) {
  const grid = document.getElementById('recommendationsGrid');
  if (!grid) return;

  const filtered = recommendations.filter(item => {
    if (state.recommendationFilter === 'all') return true;
    return item.tag === state.recommendationFilter;
  });

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; background: var(--bg-card); border-radius: var(--radius-md);">
        <p style="color: var(--text-muted);">No recommendations found matching filter "${state.recommendationFilter}".</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered.map((item, index) => {
    const tagClass = getTagClass(item.tag);
    const escapedItem = encodeURIComponent(JSON.stringify(item));

    return `
      <div class="recommendation-card">
        <div>
          <div class="rec-header">
            <h4 class="rec-title">${escapeHtml(item.name)}</h4>
            <span class="tag ${tagClass}">${escapeHtml(item.tag || 'Recommended')}</span>
          </div>

          <div class="rec-platform">
            <i class="fa-solid fa-store text-gold"></i>
            <span>${escapeHtml(item.platform || 'Amazon')}</span>
            ${item.platform_badge ? `<span class="badge" style="font-size:0.65rem; background:rgba(200,162,74,0.12); padding:2px 6px; border-radius:10px; color:var(--gold-light);">${escapeHtml(item.platform_badge)}</span>` : ''}
          </div>

          <div class="rec-price">
            ${formatCurrency(item.estimated_price)}
          </div>

          <div class="rec-reason">
            <strong>Why this matches:</strong>
            ${escapeHtml(item.reason || 'Curated to maximize aesthetic harmony and budget efficiency.')}
          </div>
        </div>

        <div class="rec-footer">
          <button class="btn btn-outline-gold btn-sm" onclick="saveItemToFavorites('${escapedItem}')" title="Save to Favorites">
            <i class="fa-regular fa-heart"></i> Save
          </button>
          <a href="${item.link || '#'}" target="_blank" rel="noopener noreferrer" class="btn btn-gold btn-sm">
            <span>View on ${escapeHtml(item.platform || 'Store')}</span>
            <i class="fa-solid fa-arrow-up-right-from-square"></i>
          </a>
        </div>
      </div>
    `;
  }).join('');
}

function filterRecommendations(filterTag) {
  state.recommendationFilter = filterTag;
  document.querySelectorAll('#recommendationFilterChips .filter-chip').forEach(btn => {
    btn.classList.remove('active');
    if (btn.innerText.toLowerCase().includes(filterTag.toLowerCase()) || (filterTag === 'all' && btn.innerText.includes('All'))) {
      btn.classList.add('active');
    }
  });
  if (state.currentPlanResult && state.currentPlanResult.recommendations) {
    renderRecommendationCards(state.currentPlanResult.recommendations);
  }
}

function getTagClass(tag) {
  switch (tag) {
    case 'Best Match': return 'tag-best-match';
    case 'Premium Choice': return 'tag-premium';
    case 'Budget Friendly': return 'tag-budget';
    case 'Luxury Pick': return 'tag-luxury';
    default: return 'tag-ai';
  }
}

// ==========================================================================
// SAVED ITEMS & FAVORITES MANAGEMENT
// ==========================================================================
async function saveItemToFavorites(itemEncoded) {
  try {
    const item = JSON.parse(decodeURIComponent(itemEncoded));
    const payload = {
      name: item.name,
      category: item.category || 'General',
      estimated_price: item.estimated_price || 0,
      platform: item.platform || 'Amazon',
      link: item.link || '',
      tag: item.tag || 'Recommended',
      reason: item.reason || '',
      planner_type: state.activePlanner || 'general',
      plan_id: state.currentPlanResult?.plan_id || null
    };

    const res = await fetch(`${BASE_URL}/api/history/saved-items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (data.success) {
      showToast(`Saved "${item.name}" to favorites!`, 'success');
      fetchHistory();
    } else {
      showToast(data.error || 'Failed to save item', 'error');
    }
  } catch (err) {
    showToast(`Error saving favorite: ${err.message}`, 'error');
  }
}

async function removeSavedItem(itemId) {
  try {
    const res = await fetch(`${BASE_URL}/api/history/saved-items/${itemId}`, {
      method: 'DELETE'
    });
    const data = await res.json();
    if (data.success) {
      showToast('Item removed from favorites', 'success');
      fetchHistory();
    }
  } catch (err) {
    showToast('Failed to delete item', 'error');
  }
}

// ==========================================================================
// HISTORY & DASHBOARD SYNC
// ==========================================================================
async function fetchHistory() {
  try {
    const [historyRes, savedRes] = await Promise.all([
      fetch(`${BASE_URL}/api/history`),
      fetch(`${BASE_URL}/api/history/saved-items`)
    ]);

    const historyData = await historyRes.json();
    const savedData = await savedRes.json();

    if (historyData.success) {
      state.history = historyData.history || [];
      renderHistoryPlans(state.history);
      renderDashboardRecent(state.history);
      updateDashboardKPIs(state.history, savedData.saved_items || []);
    }

    if (savedData.success) {
      state.savedItems = savedData.saved_items || [];
      renderSavedItems(state.savedItems);
    }
  } catch (err) {
    console.warn('Could not load history:', err);
  }
}

function updateDashboardKPIs(historyList, savedList) {
  document.getElementById('statTotalPlans').innerText = historyList.length;
  const totalBudgetSum = historyList.reduce((acc, h) => acc + (h.budget || 0), 0);
  document.getElementById('statTotalBudget').innerText = formatCurrency(totalBudgetSum);
  document.getElementById('statSavedItems').innerText = savedList.length;
  const contingencySum = historyList.reduce((acc, h) => acc + (h.contingency || 0), 0);
  document.getElementById('statContingencySaved').innerText = formatCurrency(contingencySum);
}

function renderDashboardRecent(historyList) {
  const container = document.getElementById('dashboardRecentPlansContainer');
  if (!container) return;

  if (historyList.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px; background: var(--bg-card); border-radius: var(--radius-md); border: 1px dashed var(--gold-border);">
        <p style="color: var(--text-muted);">No plans generated yet. Click "New Plan" above to create your first intelligent budget.</p>
      </div>
    `;
    return;
  }

  const recent = historyList.slice(0, 4);
  container.innerHTML = `
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
      ${recent.map(h => `
        <div class="planner-card" style="padding: 20px; cursor: pointer;" onclick="loadPlanFromHistory(${h.id})">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
            <span class="tag tag-best-match">${h.planner_type.toUpperCase()}</span>
            <span style="font-size: 0.75rem; color: var(--text-muted);">${new Date(h.created_at).toLocaleDateString()}</span>
          </div>
          <h4 style="font-size: 1.05rem; margin-bottom: 6px;">${escapeHtml(h.title)}</h4>
          <p style="font-size: 0.85rem; color: var(--gold-light); font-weight: 700;">Budget: ${formatCurrency(h.budget)}</p>
          <div style="margin-top: 12px; font-size: 0.8rem; color: var(--text-secondary);">
            Allocated: ${formatCurrency(h.allocated_total)} • Safety: ${formatCurrency(h.contingency)}
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderHistoryPlans(historyList) {
  const container = document.getElementById('historyPlansContainer');
  if (!container) return;

  if (historyList.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 60px; background: var(--bg-card); border-radius: var(--radius-lg); border: 1px dashed var(--gold-border);">
        <i class="fa-solid fa-folder-open" style="font-size: 2.5rem; color: var(--gold-light); margin-bottom: 16px;"></i>
        <h3>No Budget Plans Saved Yet</h3>
        <p style="color: var(--text-secondary); margin-bottom: 20px;">Use our AI planners to generate and store optimized allocations.</p>
        <button class="btn btn-gold" onclick="openPlanner('home')">Launch Home Planner</button>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 16px;">
      ${historyList.map(h => `
        <div class="planner-card" style="padding: 24px; display: flex; flex-direction: row; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
          <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
              <span class="tag tag-best-match">${h.planner_type.toUpperCase()}</span>
              <span style="font-size: 0.8rem; color: var(--text-muted);">${new Date(h.created_at).toLocaleString()}</span>
            </div>
            <h3 style="font-size: 1.2rem; margin-bottom: 4px;">${escapeHtml(h.title)}</h3>
            <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0;">
              Total Budget: <strong class="text-gold">${formatCurrency(h.budget)}</strong> |
              Allocated: <strong>${formatCurrency(h.allocated_total)}</strong> |
              Contingency Reserve: <strong style="color: var(--accent-amber);">${formatCurrency(h.contingency)}</strong>
            </p>
          </div>

          <div style="display: flex; gap: 10px;">
            <button class="btn btn-gold btn-sm" onclick="loadPlanFromHistory(${h.id})">
              <i class="fa-solid fa-eye"></i> View Full Plan
            </button>
            <button class="btn btn-secondary btn-sm" onclick="deleteHistoryPlan(${h.id})" title="Delete Plan">
              <i class="fa-regular fa-trash-can"></i>
            </button>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderSavedItems(savedList) {
  const grid = document.getElementById('savedItemsGrid');
  if (!grid) return;

  if (savedList.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 60px; background: var(--bg-card); border-radius: var(--radius-lg); border: 1px dashed var(--gold-border);">
        <i class="fa-regular fa-heart" style="font-size: 2.5rem; color: var(--gold-light); margin-bottom: 16px;"></i>
        <h3>No Favorited Recommendations</h3>
        <p style="color: var(--text-secondary); margin-bottom: 0;">Click "Save" on any AI recommendation to store it here for easy shopping.</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = savedList.map(item => `
    <div class="recommendation-card">
      <div>
        <div class="rec-header">
          <h4 class="rec-title">${escapeHtml(item.item_name)}</h4>
          <span class="tag ${getTagClass(item.tag)}">${escapeHtml(item.tag || 'Saved')}</span>
        </div>

        <div class="rec-platform">
          <i class="fa-solid fa-store text-gold"></i>
          <span>${escapeHtml(item.platform || 'Store')}</span>
        </div>

        <div class="rec-price">
          ${formatCurrency(item.estimated_price)}
        </div>

        <div class="rec-reason">
          ${escapeHtml(item.reason || 'Saved to your personal luxury wishlist.')}
        </div>
      </div>

      <div class="rec-footer">
        <button class="btn btn-secondary btn-sm" onclick="removeSavedItem(${item.id})">
          <i class="fa-solid fa-trash"></i> Remove
        </button>
        <a href="${item.platform_url || '#'}" target="_blank" rel="noopener noreferrer" class="btn btn-gold btn-sm">
          <span>Shop on ${escapeHtml(item.platform || 'Platform')}</span>
          <i class="fa-solid fa-arrow-up-right-from-square"></i>
        </a>
      </div>
    </div>
  `).join('');
}

function switchHistoryTab(tab) {
  const plansContainer = document.getElementById('historyPlansContainer');
  const savedContainer = document.getElementById('historySavedItemsContainer');
  const tabPlans = document.getElementById('tabHistoryPlans');
  const tabSaved = document.getElementById('tabHistorySaved');

  if (tab === 'plans') {
    plansContainer.style.display = 'block';
    savedContainer.style.display = 'none';
    tabPlans.classList.add('active');
    tabSaved.classList.remove('active');
  } else {
    plansContainer.style.display = 'none';
    savedContainer.style.display = 'block';
    tabPlans.classList.remove('active');
    tabSaved.classList.add('active');
  }
}

async function loadPlanFromHistory(planId) {
  try {
    showLoading('Loading saved plan details...');
    const res = await fetch(`${BASE_URL}/api/history/${planId}`);
    const data = await res.json();
    hideLoading();

    if (data.success && data.plan) {
      state.currentPlanResult = data.plan.result;
      state.currentPlanResult.plan_id = data.plan.id;
      renderResultsView(data.plan.result, data.plan.planner_type.toUpperCase());
    }
  } catch (err) {
    hideLoading();
    showToast('Failed to load plan details', 'error');
  }
}

async function deleteHistoryPlan(planId) {
  if (!confirm('Are you sure you want to delete this plan?')) return;
  try {
    const res = await fetch(`${BASE_URL}/api/history/${planId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast('Plan deleted successfully', 'success');
      fetchHistory();
    }
  } catch (err) {
    showToast('Failed to delete plan', 'error');
  }
}

// ==========================================================================
// AUTHENTICATION & USER PROFILE
// ==========================================================================
async function checkAuthStatus() {
  try {
    const res = await fetch(`${BASE_URL}/api/auth/me`);
    const data = await res.json();
    if (data.authenticated && data.user) {
      state.user = data.user;
      updateAuthUI(data.user);
    } else {
      state.user = null;
      updateAuthUI(null);
    }
  } catch (err) {
    console.warn('Auth check error:', err);
  }
}

function updateAuthUI(user) {
  const btnText = document.getElementById('authBtnText');
  const profileEmail = document.getElementById('profileEmailDisplay');
  const profileName = document.getElementById('profileName');
  const profileLoc = document.getElementById('profileLocation');
  const modalTabProfile = document.getElementById('modalTabProfile');

  if (user) {
    btnText.innerText = user.name || 'Account';
    if (profileEmail) profileEmail.innerText = user.email;
    if (profileName) profileName.value = user.name || '';
    if (profileLoc) profileLoc.value = user.location || 'Mumbai, India';
    if (modalTabProfile) modalTabProfile.style.display = 'block';
  } else {
    btnText.innerText = 'Sign In';
    if (modalTabProfile) modalTabProfile.style.display = 'none';
  }
}

function openAuthModal() {
  const modal = document.getElementById('authModal');
  if (!modal) return;
  modal.classList.add('active');

  const customKey = localStorage.getItem('pocketsmart_gemini_key') || '';
  const keyInput = document.getElementById('customGeminiKeyInput');
  if (keyInput) keyInput.value = customKey;

  if (state.user) {
    switchAuthTab('profile');
  } else {
    switchAuthTab('signin');
  }
}

function closeAuthModal() {
  const modal = document.getElementById('authModal');
  if (modal) modal.classList.remove('active');
}

function switchAuthTab(tab) {
  document.getElementById('signInForm').style.display = tab === 'signin' ? 'block' : 'none';
  document.getElementById('signUpForm').style.display = tab === 'signup' ? 'block' : 'none';
  document.getElementById('profileTabContent').style.display = tab === 'profile' ? 'block' : 'none';

  document.getElementById('modalTabSignIn').classList.toggle('active', tab === 'signin');
  document.getElementById('modalTabSignUp').classList.toggle('active', tab === 'signup');
  document.getElementById('modalTabProfile').classList.toggle('active', tab === 'profile');
}

async function handleSignIn(e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;

  try {
    const res = await fetch(`${BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (data.success && data.user) {
      state.user = data.user;
      updateAuthUI(data.user);
      closeAuthModal();
      showToast(`Welcome back, ${data.user.name}!`, 'success');
      fetchHistory();
    } else {
      showToast(data.error || 'Login failed', 'error');
    }
  } catch (err) {
    showToast('Network error during login', 'error');
  }
}

async function quickGuestLogin() {
  document.getElementById('loginEmail').value = 'demo@pocketsmart.ai';
  document.getElementById('loginPassword').value = 'pocketsmart123';
  handleSignIn(new Event('submit'));
}

async function handleSignUp(e) {
  e.preventDefault();
  const name = document.getElementById('regName').value;
  const email = document.getElementById('regEmail').value;
  const password = document.getElementById('regPassword').value;
  const location = document.getElementById('regCity').value;

  try {
    const res = await fetch(`${BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password, location })
    });
    const data = await res.json();
    if (data.success && data.user) {
      state.user = data.user;
      updateAuthUI(data.user);
      closeAuthModal();
      showToast(`Account created for ${data.user.name}!`, 'success');
      fetchHistory();
    } else {
      showToast(data.error || 'Registration failed', 'error');
    }
  } catch (err) {
    showToast('Network error during registration', 'error');
  }
}

async function handleLogout() {
  try {
    await fetch(`${BASE_URL}/api/auth/logout`, { method: 'POST' });
    state.user = null;
    updateAuthUI(null);
    closeAuthModal();
    showToast('Logged out successfully', 'success');
    fetchHistory();
  } catch (err) {
    showToast('Error signing out', 'error');
  }
}

function saveUserProfile() {
  const customKey = document.getElementById('customGeminiKeyInput')?.value.trim() || '';
  if (customKey) {
    localStorage.setItem('pocketsmart_gemini_key', customKey);
  } else {
    localStorage.removeItem('pocketsmart_gemini_key');
  }

  showToast('Settings and API configurations saved!', 'success');
  closeAuthModal();
}

// ==========================================================================
// CURRENCY & FORMATTING HELPERS
// ==========================================================================
function toggleCurrency() {
  state.currency = state.currency === 'INR' ? 'USD' : 'INR';
  localStorage.setItem('pocketsmart_currency', state.currency);
  updateCurrencyDisplay();
  if (state.currentPlanResult) {
    renderResultsView(state.currentPlanResult, state.activePlanner);
  }
  fetchHistory();
}

function updateCurrencyDisplay() {
  const label = document.getElementById('currencyLabel');
  if (label) {
    label.innerText = state.currency === 'INR' ? 'INR (₹)' : 'USD ($)';
  }
}

function formatCurrency(amount) {
  const val = parseFloat(amount || 0);
  if (state.currency === 'USD') {
    const usdVal = val / 85.0; // Conversion display rate
    return `$${usdVal.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
  }
  return `₹${val.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

function exportPlanJSON() {
  if (!state.currentPlanResult) {
    showToast('No active plan to export', 'warning');
    return;
  }
  const blob = new Blob([JSON.stringify(state.currentPlanResult, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `PocketSmart_Plan_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('JSON Plan Exported Successfully', 'success');
}

// ==========================================================================
// TOAST NOTIFICATIONS & LOADING UTILITIES
// ==========================================================================
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  
  let icon = '<i class="fa-solid fa-circle-info text-gold"></i>';
  if (type === 'success') icon = '<i class="fa-solid fa-circle-check" style="color: var(--accent-emerald);"></i>';
  if (type === 'error') icon = '<i class="fa-solid fa-circle-xmark" style="color: var(--accent-rose);"></i>';
  if (type === 'warning') icon = '<i class="fa-solid fa-triangle-exclamation" style="color: var(--accent-amber);"></i>';

  toast.innerHTML = `${icon} <span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function showLoading(msg) {
  const overlay = document.getElementById('globalLoadingOverlay');
  const statusText = document.getElementById('loadingStatusText');
  if (overlay) {
    if (statusText && msg) statusText.innerText = msg;
    overlay.classList.add('active');
  }
}

function hideLoading() {
  const overlay = document.getElementById('globalLoadingOverlay');
  if (overlay) overlay.classList.remove('active');
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
