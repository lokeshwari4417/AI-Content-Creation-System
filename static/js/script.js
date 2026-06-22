// ============================================================
// script.js — AI Content Creation System Frontend Logic
// Handles form submission, API calls, copy, and export
// ============================================================

document.addEventListener('DOMContentLoaded', () => {

  // ── Element References ──────────────────────────────────
  const form           = document.getElementById('content-form');
  if (!form) return;   // Guard: only run on the index page

  const generateBtn    = document.getElementById('generate-btn');
  const btnText        = document.getElementById('btn-text');
  const btnLoader      = document.getElementById('btn-loader');
  const alertBox       = document.getElementById('alert-box');
  const outputSection  = document.getElementById('output-section');
  const contentBody    = document.getElementById('generated-content');
  const outType        = document.getElementById('out-type');
  const outTopic       = document.getElementById('out-topic');
  const copyBtn        = document.getElementById('copy-btn');
  const exportBtn      = document.getElementById('export-btn');
  const promptPreview  = document.getElementById('prompt-preview');

  // Track the record id returned by the server for the export link
  let currentRecordId = null;

  // ── Form Submit ─────────────────────────────────────────
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearAlert();
    hideOutput();

    // Collect form values
    const contentType = document.getElementById('content_type').value.trim();
    const topic       = document.getElementById('topic').value.trim();
    const audience    = document.getElementById('audience').value.trim();
    const tone        = document.getElementById('tone').value.trim();
    const length      = getSelectedLength();

    // ── Client-side validation ──────────────────────────
    if (!contentType) { showAlert('Please select a Content Type.', 'error'); return; }
    if (!topic)       { showAlert('Please enter a Topic.', 'error'); return; }
    if (!audience)    { showAlert('Please enter a Target Audience.', 'error'); return; }
    if (!tone)        { showAlert('Please select a Tone.', 'error'); return; }
    if (!length)      { showAlert('Please select a Content Length.', 'error'); return; }

    // ── Show loading state ──────────────────────────────
    setLoading(true);

    // ── API Call ────────────────────────────────────────
    try {
      const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content_type: contentType, topic, audience, tone, length }),
      });

      const data = await response.json();

      if (data.success) {
        // Populate output card
        outType.textContent       = contentType;
        outTopic.textContent      = `"${topic}"`;
        contentBody.textContent   = data.content;
        promptPreview.textContent = data.prompt_used || '';
        currentRecordId           = data.record_id;

        // Show download button only if we have a record id
        if (currentRecordId) {
          exportBtn.classList.remove('hidden');
          exportBtn.onclick = () => {
            window.location.href = `/export/${currentRecordId}`;
          };
        }

        showOutput();
        showAlert('Content generated and saved!', 'success');

        // Smooth scroll to output
        setTimeout(() => {
          outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

      } else {
        showAlert(data.error || 'Generation failed. Please try again.', 'error');
      }

    } catch (err) {
      showAlert('Network error — please check your connection and try again.', 'error');
      console.error('Generate error:', err);
    } finally {
      setLoading(false);
    }
  });

  // ── Copy to Clipboard ───────────────────────────────────
  copyBtn.addEventListener('click', async () => {
    const text = contentBody.textContent;
    if (!text) return;

    try {
      await navigator.clipboard.writeText(text);
      const original = copyBtn.textContent;
      copyBtn.textContent = '✓ Copied!';
      copyBtn.style.color = 'var(--success)';
      setTimeout(() => {
        copyBtn.textContent = original;
        copyBtn.style.color = '';
      }, 2000);
    } catch {
      // Fallback for older browsers
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      copyBtn.textContent = '✓ Copied!';
      setTimeout(() => { copyBtn.textContent = '📋 Copy'; }, 2000);
    }
  });

  // ── Helper: get selected radio value ───────────────────
  function getSelectedLength() {
    const radios = document.querySelectorAll('input[name="length"]');
    for (const r of radios) {
      if (r.checked) return r.value;
    }
    return '';
  }

  // ── Helper: show / hide loading state ──────────────────
  function setLoading(isLoading) {
    generateBtn.disabled = isLoading;
    btnText.classList.toggle('hidden', isLoading);
    btnLoader.classList.toggle('hidden', !isLoading);
  }

  // ── Helper: alert banner ────────────────────────────────
  function showAlert(message, type = 'error') {
    alertBox.textContent = message;
    alertBox.className = `alert ${type}`;
    alertBox.classList.remove('hidden');
    // Auto-dismiss success alerts after 4 s
    if (type === 'success') {
      setTimeout(clearAlert, 4000);
    }
  }
  function clearAlert() {
    alertBox.className = 'alert hidden';
    alertBox.textContent = '';
  }

  // ── Helper: show / hide output section ─────────────────
  function showOutput() {
    outputSection.classList.remove('hidden');
  }
  function hideOutput() {
    outputSection.classList.add('hidden');
    currentRecordId = null;
    exportBtn.classList.add('hidden');
  }

});
