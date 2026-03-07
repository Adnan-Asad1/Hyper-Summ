/* ============================================================
   HyperSumm — New UI JavaScript (2026)
   ============================================================ */

/* ============================================================
   PARTICLE BACKGROUND
   ============================================================ */
function initParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W, H, particles;

    function resize() {
        W = canvas.width = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }

    function createParticles() {
        const count = Math.floor((W * H) / 18000);
        particles = [];
        for (let i = 0; i < count; i++) {
            particles.push({
                x: Math.random() * W,
                y: Math.random() * H,
                r: Math.random() * 1.2 + 0.3,
                vx: (Math.random() - 0.5) * 0.22,
                vy: (Math.random() - 0.5) * 0.22,
                alpha: Math.random() * 0.5 + 0.15,
                gold: Math.random() > 0.75,
            });
        }
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.gold
                ? `rgba(212,168,83,${p.alpha})`
                : `rgba(180,185,210,${p.alpha * 0.5})`;
            ctx.fill();

            // Connect nearby gold particles
            if (p.gold) {
                for (let j = i + 1; j < particles.length; j++) {
                    const q = particles[j];
                    if (!q.gold) continue;
                    const dx = p.x - q.x, dy = p.y - q.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(q.x, q.y);
                        ctx.strokeStyle = `rgba(212,168,83,${0.08 * (1 - dist / 120)})`;
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                    }
                }
            }

            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0) p.x = W;
            if (p.x > W) p.x = 0;
            if (p.y < 0) p.y = H;
            if (p.y > H) p.y = 0;
        }
        requestAnimationFrame(draw);
    }

    resize();
    createParticles();
    draw();
    window.addEventListener('resize', () => { resize(); createParticles(); });
}

/* ============================================================
   ALGORITHM DATA
   ============================================================ */
const algoData = {
    textrank_seq: {
        desc: 'Graph-based ranking that identifies key sentences through semantic similarity. Processes sequentially for reliable, reproducible results.',
        label: 'TextRank · Sequential',
    },
    textrank_par: {
        desc: 'Graph-based TextRank with parallel execution — similarity matrix is computed across multiple threads for faster throughput on large texts.',
        label: 'TextRank · Parallel ⚡',
    },
    tfidf_seq: {
        desc: 'Statistical TF-IDF scoring ranks sentences by term importance across the document corpus. Sequential processing.',
        label: 'TF-IDF · Sequential',
    },
    tfidf_par: {
        desc: 'TF-IDF with parallelized sentence scoring — vectorization workload distributed across threads for high-performance summarization.',
        label: 'TF-IDF · Parallel ⚡',
    },
};

/* ============================================================
   SAMPLE TEXT
   ============================================================ */
const sampleText = `Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines that mimic cognitive functions that humans associate with the human mind, such as learning and problem solving.

As machines become increasingly capable, tasks considered to require intelligence are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology. Modern machine learning capabilities for computer vision and natural language processing are often considered AI.

Artificial intelligence was founded as an academic discipline in 1956, and in the years since has experienced several waves of optimism, followed by disappointment and the loss of funding, known as an AI winter, followed by new approaches, success and renewed funding. AI research has tried and discarded many different approaches during its lifetime, including simulating the brain, modeling human problem solving, formal logic, large databases of knowledge and imitating animal behavior.

The various sub-fields of AI research are centered around particular goals and the use of particular tools. The traditional goals of AI research include reasoning, knowledge representation, planning, learning, natural language processing, perception and the ability to move and manipulate objects. General intelligence is among the field's long-term goals. Many tools are used in AI, including versions of search and mathematical optimization, artificial neural networks, and methods based on statistics, probability and economics.`;

/* ============================================================
   STATE
   ============================================================ */
let selectedAlgo = 'textrank_seq';

/* ============================================================
   DOM REFS
   ============================================================ */
const form = document.getElementById('summarizerForm');
const inputText = document.getElementById('inputText');
const wordCountEl = document.getElementById('wordCount');
const charCountEl = document.getElementById('charCount');
const clearBtn = document.getElementById('clearBtn');
const sampleTextBtn = document.getElementById('sampleTextBtn');
const algoPills = document.querySelectorAll('.algo-pill');
const algoDesc = document.getElementById('algorithmDescription');
const submitBtn = document.getElementById('submitBtn');

const idleState = document.getElementById('idleState');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const resultsState = document.getElementById('resultsState');
const errorText = document.getElementById('errorText');

const metricTime = document.getElementById('metricTime');
const metricCompression = document.getElementById('metricCompression');
const metricMemory = document.getElementById('metricMemory');
const metricSentences = document.getElementById('metricSentences');

const summaryText = document.getElementById('summaryText');
const summaryWordCount = document.getElementById('summaryWordCount');
const originalText = document.getElementById('originalText');
const originalWordCount = document.getElementById('originalWordCount');
const algorithmBadge = document.getElementById('algorithmBadge');
const copyBtn = document.getElementById('copyBtn');

/* ============================================================
   OUTPUT STATE MANAGER
   ============================================================ */
function showState(name) {
    idleState.classList.toggle('hidden', name !== 'idle');
    loadingState.classList.toggle('hidden', name !== 'loading');
    errorState.classList.toggle('hidden', name !== 'error');
    resultsState.classList.toggle('hidden', name !== 'results');
}

/* ============================================================
   WORD / CHAR COUNT
   ============================================================ */
function updateCounts() {
    const t = inputText.value.trim();
    const words = t ? t.split(/\s+/).length : 0;
    wordCountEl.textContent = `${words} word${words !== 1 ? 's' : ''}`;
    charCountEl.textContent = `${t.length} char${t.length !== 1 ? 's' : ''}`;
}

/* ============================================================
   ALGORITHM PILLS
   ============================================================ */
algoPills.forEach(pill => {
    pill.addEventListener('click', () => {
        algoPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        selectedAlgo = pill.dataset.value;
        algoDesc.textContent = algoData[selectedAlgo].desc;
    });
});

/* ============================================================
   CLEAR & SAMPLE
   ============================================================ */
clearBtn.addEventListener('click', () => {
    inputText.value = '';
    updateCounts();
    inputText.focus();
});

sampleTextBtn.addEventListener('click', () => {
    inputText.value = sampleText;
    updateCounts();
    sampleTextBtn.style.transform = 'scale(0.94)';
    setTimeout(() => { sampleTextBtn.style.transform = ''; }, 120);
});

inputText.addEventListener('input', updateCounts);

/* ============================================================
   COPY TO CLIPBOARD
   ============================================================ */
copyBtn.addEventListener('click', async () => {
    const text = summaryText.textContent;
    if (!text) return;
    try {
        await navigator.clipboard.writeText(text);
        copyBtn.classList.add('copied');
        copyBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                <path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Copied!`;
        setTimeout(() => {
            copyBtn.classList.remove('copied');
            copyBtn.innerHTML = `
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/>
                    <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                Copy`;
        }, 2200);
    } catch (_) { /* ignore */ }
});

/* ============================================================
   LOADING STEPS ANIMATION
   ============================================================ */
let stepTimer = null;

function startLoadingSteps() {
    const steps = ['step1', 'step2', 'step3', 'step4'];
    let idx = 0;
    steps.forEach(id => {
        const el = document.getElementById(id);
        if (el) { el.classList.remove('active', 'done'); }
    });
    const step0 = document.getElementById('step1');
    if (step0) step0.classList.add('active');

    stepTimer = setInterval(() => {
        const curr = document.getElementById(steps[idx]);
        if (curr) { curr.classList.remove('active'); curr.classList.add('done'); }
        idx++;
        if (idx < steps.length) {
            const next = document.getElementById(steps[idx]);
            if (next) next.classList.add('active');
        } else {
            clearInterval(stepTimer);
        }
    }, 600);
}

function stopLoadingSteps() {
    if (stepTimer) { clearInterval(stepTimer); stepTimer = null; }
}

/* ============================================================
   ANIMATED COUNTER
   ============================================================ */
function animateValue(el, from, to, unit, duration = 600) {
    const start = performance.now();
    function step(now) {
        const t = Math.min((now - start) / duration, 1);
        const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
        const val = from + (to - from) * ease;
        el.textContent = Number.isInteger(to) ? Math.round(val) + unit : val.toFixed(2) + unit;
        if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}

/* ============================================================
   TYPEWRITER EFFECT
   ============================================================ */
function typewriterReveal(el, text, delay = 10) {
    el.textContent = '';
    let i = 0;
    const interval = setInterval(() => {
        el.textContent += text[i];
        i++;
        if (i >= text.length) clearInterval(interval);
    }, delay);
}

/* ============================================================
   DISPLAY RESULTS
   ============================================================ */
function displayResults(data) {
    const m = data.metrics;

    // Metrics — animated counters
    animateValue(metricTime, 0, m.execution_time, 's');
    animateValue(metricCompression, 0, m.compression_ratio, '%');
    animateValue(metricMemory, 0, m.memory_used_mb, ' MB');
    metricSentences.textContent = `${m.num_sentences} → ${m.summary_sentences}`;

    // Badge
    algorithmBadge.textContent = data.algorithm_name;

    // Summary — typewriter reveal
    typewriterReveal(summaryText, data.summary, 12);
    summaryWordCount.textContent = `${data.summary_word_count} words`;

    // Original text
    originalText.textContent = data.original_text;
    originalWordCount.textContent = `${data.original_word_count} words`;

    showState('results');

    // Scroll into view on mobile
    if (window.innerWidth < 1000) {
        setTimeout(() => {
            document.getElementById('outputPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 150);
    }
}

/* ============================================================
   FORM SUBMIT
   ============================================================ */
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const text = inputText.value.trim();
    if (!text) { showError('Please enter some text to summarize.'); return; }
    const words = text.split(/\s+/).length;
    if (words < 10) { showError('Text is too short — please provide at least 10 words.'); return; }

    // Show loading
    submitBtn.disabled = true;
    showState('loading');
    startLoadingSteps();

    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, algorithm: selectedAlgo }),
        });

        const data = await response.json();
        stopLoadingSteps();
        submitBtn.disabled = false;

        if (!response.ok || !data.success) {
            showError(data.error || 'An error occurred while generating the summary.');
            return;
        }

        displayResults(data);

    } catch (err) {
        stopLoadingSteps();
        submitBtn.disabled = false;
        showError('Could not reach the server. Please make sure the Flask app is running.');
        console.error(err);
    }
});

function showError(msg) {
    errorText.textContent = msg;
    showState('error');
}

/* ============================================================
   INIT
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    updateCounts();
    algoDesc.textContent = algoData[selectedAlgo].desc;
    showState('idle');
});