document.addEventListener('DOMContentLoaded', () => {
    // --- Theme Management ---
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const htmlElement = document.documentElement;
    
    // Retrieve theme from localStorage or default to dark
    const currentTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-theme', currentTheme);

    themeToggleBtn.addEventListener('click', () => {
        const activeTheme = htmlElement.getAttribute('data-theme');
        const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
        
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // --- Ingestion DOM Elements ---
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const fileInfoCard = document.getElementById('file-info-card');
    const fileNameDisplay = document.getElementById('file-name');
    const fileSizeDisplay = document.getElementById('file-size');
    const removeFileBtn = document.getElementById('remove-file-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadStatus = document.getElementById('upload-status');
    const statusMessage = uploadStatus.querySelector('.status-message');
    const statusIcon = uploadStatus.querySelector('.status-icon');
    const loaderSpinner = uploadStatus.querySelector('.loader-spinner');

    // --- Q&A DOM Elements ---
    const questionInput = document.getElementById('question-input');
    const askBtn = document.getElementById('ask-btn');
    const outputScreen = document.getElementById('output-screen');
    const outputPlaceholder = document.getElementById('output-placeholder');
    const qaResultBox = document.getElementById('qa-result-box');
    const qaLoadingState = document.getElementById('qa-loading-state');
    const responseQuestion = document.getElementById('response-question');
    const responseAnswer = document.getElementById('response-answer');
    const sourceChunksContainer = document.getElementById('source-chunks-container');

    let selectedFile = null;

    // --- Drag and Drop File Handlers ---
    
    // Open file selector when clicking Dropzone
    dropzone.addEventListener('click', () => {
        fileInput.click();
    });

    // Trigger file change when files are selected
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    // Drag-over styling shifts
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

    // Drop file trigger
    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });

    function handleFileSelection(file) {
        if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
            showUploadStatus('Please select a valid PDF document.', 'error');
            resetFileSelection();
            return;
        }

        selectedFile = file;
        fileNameDisplay.textContent = file.name;
        fileSizeDisplay.textContent = formatBytes(file.size);
        
        // UI Transition: Show File Details, Hide Dropzone, Enable Index Button
        fileInfoCard.style.display = 'flex';
        uploadBtn.removeAttribute('disabled');
        hideUploadStatus();
    }

    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Avoid triggering dropzone click
        resetFileSelection();
    });

    function resetFileSelection() {
        selectedFile = null;
        fileInput.value = '';
        fileInfoCard.style.display = 'none';
        uploadBtn.setAttribute('disabled', 'true');
        hideUploadStatus();
    }

    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }

    // --- Upload and Ingest API Request ---
    uploadBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        // UI Upload Loading State
        showUploadStatus('Ingesting PDF and creating FAISS index...', 'loading');
        uploadBtn.setAttribute('disabled', 'true');
        removeFileBtn.setAttribute('disabled', 'true');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showUploadStatus(`Success! Document indexed into ${data.chunks_count} chunks.`, 'success');
                // Enable Q&A Panel
                questionInput.removeAttribute('disabled');
                askBtn.removeAttribute('disabled');
                
                // Transition the output screen from empty-state
                outputScreen.classList.remove('empty-state');
                outputPlaceholder.style.display = 'none';
                
                // Focus on question input
                questionInput.focus();
            } else {
                showUploadStatus(data.detail || 'Failed to process document.', 'error');
                disableQA();
            }
        } catch (error) {
            console.error('Upload error:', error);
            showUploadStatus('Connection error. Server may be down.', 'error');
            disableQA();
        } finally {
            uploadBtn.removeAttribute('disabled');
            removeFileBtn.removeAttribute('disabled');
        }
    });

    // --- UI Status Box Utilities ---
    function showUploadStatus(message, type) {
        uploadStatus.className = 'status-box'; // Reset
        uploadStatus.classList.add(type);
        statusMessage.textContent = message;
        uploadStatus.style.display = 'flex';

        // Set Icons and spinners
        if (type === 'loading') {
            loaderSpinner.style.display = 'block';
            statusIcon.style.display = 'none';
        } else {
            loaderSpinner.style.display = 'none';
            statusIcon.style.display = 'block';
            if (type === 'success') {
                statusIcon.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                    </svg>
                `;
            } else if (type === 'error') {
                statusIcon.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                `;
            }
        }
    }

    function hideUploadStatus() {
        uploadStatus.style.display = 'none';
    }

    function disableQA() {
        questionInput.setAttribute('disabled', 'true');
        askBtn.setAttribute('disabled', 'true');
        outputScreen.classList.add('empty-state');
        outputPlaceholder.style.display = 'flex';
        qaResultBox.style.display = 'none';
        qaLoadingState.style.display = 'none';
    }

    // --- Q&A API Request ---
    askBtn.addEventListener('click', triggerQuestionQuery);

    // Support submitting by pressing Enter key
    questionInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            triggerQuestionQuery();
        }
    });

    async function triggerQuestionQuery() {
        const question = questionInput.value.trim();
        if (!question) return;

        // UI Query Loading State
        qaResultBox.style.display = 'none';
        qaLoadingState.style.display = 'flex';
        outputScreen.classList.remove('empty-state');
        
        questionInput.setAttribute('disabled', 'true');
        askBtn.setAttribute('disabled', 'true');

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });

            const data = await response.json();

            if (response.ok) {
                // Hide loader and display result fields
                qaLoadingState.style.display = 'none';
                qaResultBox.style.display = 'flex';
                
                responseQuestion.textContent = data.question;
                responseAnswer.textContent = data.answer;
                
                // Generate chunk accordion items
                renderSources(data.retrieved_chunks);
                
                // Scroll output screen to top
                outputScreen.scrollTop = 0;
            } else {
                qaLoadingState.style.display = 'none';
                qaResultBox.style.display = 'flex';
                responseQuestion.textContent = question;
                responseAnswer.innerHTML = `<span style="color: #ff5c5c;"><strong>Error:</strong> ${data.detail || 'Failed to get answer from Gemini.'}</span>`;
                sourceChunksContainer.innerHTML = '';
                
                questionInput.removeAttribute('disabled');
                askBtn.removeAttribute('disabled');
                questionInput.focus();
            }
        } catch (error) {
            console.error('Q&A error:', error);
            qaLoadingState.style.display = 'none';
            qaResultBox.style.display = 'flex';
            responseQuestion.textContent = question;
            responseAnswer.innerHTML = `<span style="color: #ff5c5c;"><strong>Error:</strong> Connection error. Failed to reach server.</span>`;
            sourceChunksContainer.innerHTML = '';
            
            questionInput.removeAttribute('disabled');
            askBtn.removeAttribute('disabled');
            questionInput.focus();
        } finally {
            questionInput.removeAttribute('disabled');
            askBtn.removeAttribute('disabled');
            questionInput.focus();
        }
    }

    function renderSources(chunks) {
        sourceChunksContainer.innerHTML = ''; // Clear previous

        if (!chunks || chunks.length === 0) {
            sourceChunksContainer.innerHTML = '<p class="text-tertiary">No sources were retrieved.</p>';
            return;
        }

        chunks.forEach((chunk, index) => {
            const accordionItem = document.createElement('div');
            accordionItem.className = 'accordion-item';

            accordionItem.innerHTML = `
                <div class="accordion-header">
                    <div class="accordion-header-left">
                        <span class="source-badge">Chunk #${index + 1}</span>
                        <span>Source Segment</span>
                    </div>
                    <svg class="accordion-chevron" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 12 15 18 9"/>
                    </svg>
                </div>
                <div class="accordion-content">
                    <div class="accordion-content-inner">${escapeHtml(chunk)}</div>
                </div>
            `;

            // Expand / Collapse Events
            const header = accordionItem.querySelector('.accordion-header');
            const content = accordionItem.querySelector('.accordion-content');

            header.addEventListener('click', () => {
                const isOpen = accordionItem.classList.contains('open');
                
                // Close all other items first (optional, makes it an accordion)
                document.querySelectorAll('.accordion-item').forEach(item => {
                    item.classList.remove('open');
                    item.querySelector('.accordion-content').style.maxHeight = '0px';
                });

                if (!isOpen) {
                    accordionItem.classList.add('open');
                    content.style.maxHeight = content.scrollHeight + 'px';
                }
            });

            sourceChunksContainer.appendChild(accordionItem);
        });
    }

    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
});
