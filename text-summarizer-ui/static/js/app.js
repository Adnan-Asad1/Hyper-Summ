// ===================================
// DOM Elements
// ===================================
const form = document.getElementById('summarizerForm');
const inputText = document.getElementById('inputText');
const algorithmSelect = document.getElementById('algorithm');
const algorithmDescription = document.getElementById('algorithmDescription');
const submitBtn = document.getElementById('submitBtn');
const sampleTextBtn = document.getElementById('sampleTextBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const resultsSection = document.getElementById('resultsSection');
const wordCount = document.getElementById('wordCount');
const charCount = document.getElementById('charCount');

// ===================================
// Algorithm Descriptions
// ===================================
const algorithmDescriptions = {
    'textrank_seq': 'Graph-based ranking algorithm that identifies important sentences based on their relationships. Sequential processing.',
    'textrank_par': 'Graph-based ranking algorithm with parallel processing for improved performance on large texts.',
    'tfidf_seq': 'Statistical approach using Term Frequency-Inverse Document Frequency to score sentence importance. Sequential processing.',
    'tfidf_par': 'TF-IDF algorithm with parallel processing optimization for faster summarization of large documents.'
};

// ===================================
// Sample Text
// ===================================
const sampleText = `Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".

As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology. Modern machine learning capabilities for computer vision and natural language processing are often considered AI, but this wasn't always the case.

Artificial intelligence was founded as an academic discipline in 1956, and in the years since has experienced several waves of optimism, followed by disappointment and the loss of funding (known as an "AI winter"), followed by new approaches, success and renewed funding. AI research has tried and discarded many different approaches during its lifetime, including simulating the brain, modeling human problem solving, formal logic, large databases of knowledge and imitating animal behavior. In the first decades of the 21st century, highly mathematical statistical machine learning has dominated the field, and this technique has proved highly successful, helping to solve many challenging problems throughout industry and academia.

The various sub-fields of AI research are centered around particular goals and the use of particular tools. The traditional goals of AI research include reasoning, knowledge representation, planning, learning, natural language processing, perception and the ability to move and manipulate objects. General intelligence is among the field's long-term goals. Approaches include statistical methods, computational intelligence, and traditional symbolic AI. Many tools are used in AI, including versions of search and mathematical optimization, artificial neural networks, and methods based on statistics, probability and economics. The AI field draws upon computer science, information engineering, mathematics, psychology, linguistics, philosophy, and many other fields.`;

// ===================================
// Event Listeners
// ===================================

// Update character and word count
inputText.addEventListener('input', updateCharCount);

// Update algorithm description
algorithmSelect.addEventListener('change', () => {
    algorithmDescription.textContent = algorithmDescriptions[algorithmSelect.value];
});

// Load sample text
sampleTextBtn.addEventListener('click', () => {
    inputText.value = sampleText;
    updateCharCount();

    // Add visual feedback
    sampleTextBtn.style.transform = 'scale(0.95)';
    setTimeout(() => {
        sampleTextBtn.style.transform = 'scale(1)';
    }, 100);
});

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await generateSummary();
});

// ===================================
// Functions
// ===================================

/**
 * Update character and word count
 */
function updateCharCount() {
    const text = inputText.value.trim();
    const words = text ? text.split(/\s+/).length : 0;
    const chars = text.length;

    wordCount.textContent = `${words} word${words !== 1 ? 's' : ''}`;
    charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
}

/**
 * Show error message
 */
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
    loadingSpinner.classList.add('hidden');
    resultsSection.classList.add('hidden');

    // Scroll to error
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.classList.add('hidden');
}

/**
 * Show loading state
 */
function showLoading() {
    hideError();
    loadingSpinner.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.6';
    submitBtn.style.cursor = 'not-allowed';

    // Scroll to loading spinner
    loadingSpinner.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingSpinner.classList.add('hidden');
    submitBtn.disabled = false;
    submitBtn.style.opacity = '1';
    submitBtn.style.cursor = 'pointer';
}

/**
 * Display results
 */
function displayResults(data) {
    // Update metrics
    document.getElementById('metricTime').textContent = `${data.metrics.execution_time}s`;
    document.getElementById('metricCompression').textContent = `${data.metrics.compression_ratio}%`;
    document.getElementById('metricMemory').textContent = `${data.metrics.memory_used_mb} MB`;
    document.getElementById('metricSentences').textContent =
        `${data.metrics.num_sentences} → ${data.metrics.summary_sentences}`;

    // Update text comparison
    document.getElementById('originalText').textContent = data.original_text;
    document.getElementById('summaryText').textContent = data.summary;
    document.getElementById('originalWordCount').textContent = `${data.original_word_count} words`;
    document.getElementById('summaryWordCount').textContent = `${data.summary_word_count} words`;
    document.getElementById('algorithmBadge').textContent = data.algorithm_name;

    // Show results section
    resultsSection.classList.remove('hidden');

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Generate summary via API
 */
async function generateSummary() {
    const text = inputText.value.trim();
    const algorithm = algorithmSelect.value;

    // Validate input
    if (!text) {
        showError('Please enter some text to summarize.');
        return;
    }

    const words = text.split(/\s+/).length;
    if (words < 10) {
        showError('Text is too short. Please provide at least 10 words.');
        return;
    }

    // Show loading state
    showLoading();

    try {
        // Make API request
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                algorithm: algorithm
            })
        });

        const data = await response.json();

        // Hide loading
        hideLoading();

        // Check for errors
        if (!response.ok || !data.success) {
            showError(data.error || 'An error occurred while generating the summary.');
            return;
        }

        // Display results
        displayResults(data);

    } catch (error) {
        hideLoading();
        showError('Failed to connect to the server. Please make sure the server is running.');
        console.error('Error:', error);
    }
}

// ===================================
// Initialize
// ===================================
document.addEventListener('DOMContentLoaded', () => {
    updateCharCount();
    algorithmDescription.textContent = algorithmDescriptions[algorithmSelect.value];

    console.log('Text Summarizer UI initialized');
});
