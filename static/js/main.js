// ==========================================================================
// Main Client Controller (State & Elements)
// ==========================================================================
const state = {
    parsedResume: null, // Complete parsed resume JSON payload
    activeSkillCategory: null, // The active category shown in the Skill tab
    sampleJds: [] // Pre-loaded corporate job descriptions
};

// Elements cache
const el = {
    // Navigation Tabs
    navItems: document.querySelectorAll('.nav-item'),
    tabPanels: document.querySelectorAll('.tab-panel'),
    
    // Upload Zone
    dropZone: document.getElementById('dropZone'),
    fileInput: document.getElementById('fileInput'),
    filePreview: document.getElementById('filePreview'),
    fileName: document.getElementById('fileName'),
    fileSize: document.getElementById('fileSize'),
    removeFileBtn: document.getElementById('removeFileBtn'),
    uploadForm: document.getElementById('uploadForm'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    
    // Core Layout loaders & notifications
    loadingOverlay: document.getElementById('loadingOverlay'),
    toast: document.getElementById('toast'),
    
    // Tab 1: ATS scorecard outputs
    resultsGrid: document.getElementById('resultsGrid'),
    gaugeCircle: document.getElementById('gaugeProgressCircle'),
    scoreText: document.getElementById('scoreText'),
    scoreTier: document.getElementById('scoreTier'),
    downloadPdfBtn: document.getElementById('downloadPdfBtn'),
    resName: document.getElementById('resName'),
    resEmail: document.getElementById('resEmail'),
    resPhone: document.getElementById('resPhone'),
    resLinkedin: document.getElementById('resLinkedin'),
    resGithub: document.getElementById('resGithub'),
    recommendationList: document.getElementById('recommendationList'),
    categoriesStrip: document.getElementById('categoriesStrip'),
    skillBadgesContainer: document.getElementById('skillBadgesContainer'),
    previewFileName: document.getElementById('previewFileName'),
    previewPageCount: document.getElementById('previewPageCount'),
    previewTextContent: document.getElementById('previewTextContent'),
    
    // Tab 2: Job Description Matcher
    sampleJdSelect: document.getElementById('sampleJdSelect'),
    jdTextArea: document.getElementById('jdTextArea'),
    compareBtn: document.getElementById('compareBtn'),
    matcherResults: document.getElementById('matcherResults'),
    matchBarFill: document.getElementById('matchBarFill'),
    matchScoreText: document.getElementById('matchScoreText'),
    matchTier: document.getElementById('matchTier'),
    matchDesc: document.getElementById('matchDesc'),
    semanticSimVal: document.getElementById('semanticSimVal'),
    skillCovVal: document.getElementById('skillCovVal'),
    matchingSkillsBox: document.getElementById('matchingSkillsBox'),
    missingSkillsBox: document.getElementById('missingSkillsBox'),
    
    // Tab 3: Career Pathways
    predictedCategoryText: document.getElementById('predictedCategoryText'),
    predictionSummaryText: document.getElementById('predictionSummaryText'),
    careerCardsContainer: document.getElementById('careerCardsContainer'),
    
    // Tab 4: Skill Browser
    taxonomyGrid: document.getElementById('taxonomyGrid')
};

// ==========================================================================
// 1. Client-Side SPA Navigation Tabs
// ==========================================================================
el.navItems.forEach(item => {
    item.addEventListener('click', () => {
        const targetTab = item.getAttribute('data-tab');
        
        // Update active sidebar tab class
        el.navItems.forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        
        // Update active tab panel display
        el.tabPanels.forEach(panel => {
            if (panel.id === targetTab) {
                panel.classList.add('active');
            } else {
                panel.classList.remove('active');
            }
        });
    });
});

// ==========================================================================
// 2. Drag & Drop File Upload Manager
// ==========================================================================

// Dragover highlights
['dragenter', 'dragover'].forEach(eventName => {
    el.dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        el.dropZone.classList.add('dragover');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    el.dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        el.dropZone.classList.remove('dragover');
    }, false);
});

// File dropped event
el.dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        handleFileSelection(files[0]);
    }
});

// Browse click event
el.fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
    }
});

// File validation and layout transition
function handleFileSelection(file) {
    if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
        showToast('Only PDF resumes are supported', 'error');
        clearFileInput();
        return;
    }
    
    // Display preview details
    el.fileName.textContent = file.name;
    el.fileSize.textContent = formatBytes(file.size);
    
    el.dropZone.classList.add('hidden');
    el.filePreview.classList.remove('hidden');
    el.analyzeBtn.disabled = false;
    
    showToast('Resume selected successfully', 'success');
}

// Clear active file selection
el.removeFileBtn.addEventListener('click', () => {
    clearFileInput();
});

function clearFileInput() {
    el.fileInput.value = '';
    el.dropZone.classList.remove('hidden');
    el.filePreview.classList.add('hidden');
    el.analyzeBtn.disabled = true;
}

// File size bytes formater
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// ==========================================================================
// 3. API Handlers & Form Submissions
// ==========================================================================

// Parse Resume Upload
el.uploadForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const files = el.fileInput.files;
    if (files.length === 0) return;
    
    const formData = new FormData();
    formData.append('resume', files[0]);
    
    // Append student/fresher toggle state
    const fresherToggle = document.getElementById('fresherToggle');
    const isFresher = fresherToggle ? fresherToggle.checked : false;
    formData.append('is_fresher', isFresher);
    
    // Show spinner loader
    el.loadingOverlay.classList.remove('hidden');
    
    fetch('/api/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => { throw new Error(data.error || 'Server error'); });
        }
        return response.json();
    })
    .then(data => {
        state.parsedResume = data;
        renderAtsResults();
        renderCareerRoadmaps();
        showToast('Resume analyzed successfully', 'success');
        
        // Smooth scroll to results
        setTimeout(() => {
            el.resultsGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    })
    .catch(err => {
        console.error(err);
        showToast(err.message || 'Failed to analyze resume', 'error');
    })
    .finally(() => {
        el.loadingOverlay.classList.add('hidden');
    });
});

// Job Description similarity compare handler
el.compareBtn.addEventListener('click', () => {
    if (!state.parsedResume) {
        showToast('Please upload and score your resume first!', 'error');
        return;
    }
    
    const jdText = el.jdTextArea.value.trim();
    if (!jdText) {
        showToast('Please enter a target job description', 'error');
        return;
    }
    
    el.loadingOverlay.classList.remove('hidden');
    
    fetch('/api/match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            resume_text: state.parsedResume.resume_text,
            jd_text: jdText
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => { throw new Error(data.error || 'Server error'); });
        }
        return response.json();
    })
    .then(data => {
        renderMatcherResults(data);
        showToast('Compatibility match calculated', 'success');
        
        // Scroll down
        setTimeout(() => {
            el.matcherResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 150);
    })
    .catch(err => {
        console.error(err);
        showToast(err.message || 'Failed to compare job description', 'error');
    })
    .finally(() => {
        el.loadingOverlay.classList.add('hidden');
    });
});

// PDF Report Download Handler
el.downloadPdfBtn.addEventListener('click', () => {
    if (!state.parsedResume) return;
    
    el.loadingOverlay.classList.remove('hidden');
    
    fetch('/api/download-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            candidate_name: state.parsedResume.candidate_name,
            contact_info: state.parsedResume.contact_info,
            ats_results: state.parsedResume.ats_results,
            recommender_results: state.parsedResume.recommender_results
        })
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to generate PDF');
        return response.blob();
    })
    .then(blob => {
        // Create dynamic anchor link to download blob stream
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const name = state.parsedResume.candidate_name.replace(/\s+/g, '_');
        a.download = `ATS_Scorecard_${name}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        showToast('PDF scorecard downloaded successfully', 'success');
    })
    .catch(err => {
        console.error(err);
        showToast('Could not compile PDF report', 'error');
    })
    .finally(() => {
        el.loadingOverlay.classList.add('hidden');
    });
});

// ==========================================================================
// 4. Client Side HTML Rendering Engine
// ==========================================================================

// Populate Tab 1: ATS Scoring outputs
function renderAtsResults() {
    const res = state.parsedResume;
    if (!res) return;
    
    el.resultsGrid.classList.remove('hidden');
    
    // Populate Resume Preview Panel
    const files = el.fileInput.files;
    if (files && files.length > 0) {
        el.previewFileName.textContent = files[0].name;
    } else {
        el.previewFileName.textContent = "Uploaded_Resume.pdf";
    }
    
    const pages = res.page_count || 1;
    el.previewPageCount.textContent = pages + (pages === 1 ? " Page" : " Pages");
    
    if (res.resume_text) {
        el.previewTextContent.textContent = res.resume_text.slice(0, 350) + (res.resume_text.length > 350 ? "..." : "");
    } else {
        el.previewTextContent.textContent = "No text content extracted.";
    }
    
    // 1. Overall Score SVG Meter
    const score = res.ats_results.overall_score;
    el.scoreText.textContent = `${score}%`;
    
    // Set circle offset stroke dash (circumference = 2 * PI * r = 2 * 3.14159 * 70 = 439.82)
    const circumference = 439.82;
    const strokeDashOffset = circumference - (circumference * score / 100);
    el.gaugeCircle.style.strokeDashoffset = strokeDashOffset;
    
    // Set circle stroke color depending on score boundaries
    if (score >= 80) {
        el.gaugeCircle.style.stroke = 'var(--accent-emerald)';
        el.gaugeCircle.style.filter = 'drop-shadow(0 0 6px var(--accent-emerald-glow))';
        el.scoreTier.className = 'text-emerald';
        el.scoreTier.textContent = 'Tier: Excellent Match';
    } else if (score >= 60) {
        el.gaugeCircle.style.stroke = 'var(--accent-indigo)';
        el.gaugeCircle.style.filter = 'drop-shadow(0 0 6px var(--accent-indigo-glow))';
        el.scoreTier.className = 'text-indigo';
        el.scoreTier.textContent = 'Tier: Strong Match';
    } else if (score >= 40) {
        el.gaugeCircle.style.stroke = 'var(--accent-amber)';
        el.gaugeCircle.style.filter = 'drop-shadow(0 0 6px var(--accent-amber-glow))';
        el.scoreTier.className = 'text-amber';
        el.scoreTier.textContent = 'Tier: Moderate Match';
    } else {
        el.gaugeCircle.style.stroke = 'var(--accent-rose)';
        el.gaugeCircle.style.filter = 'drop-shadow(0 0 6px var(--accent-rose-glow))';
        el.scoreTier.className = 'text-rose';
        el.scoreTier.textContent = 'Tier: Low Match';
    }
    
    // 2. Personal contact metadata
    el.resName.textContent = res.candidate_name;
    el.resEmail.textContent = res.contact_info.email || 'Not found';
    el.resPhone.textContent = res.contact_info.phone || 'Not found';
    
    if (res.contact_info.linkedin) {
        el.resLinkedin.href = res.contact_info.linkedin.startsWith('http') ? res.contact_info.linkedin : 'https://' + res.contact_info.linkedin;
        el.resLinkedin.textContent = 'linkedin.com/in/profile';
        el.resLinkedin.classList.remove('hidden');
    } else {
        el.resLinkedin.removeAttribute('href');
        el.resLinkedin.textContent = 'Not found';
    }
    
    if (res.contact_info.github) {
        el.resGithub.href = res.contact_info.github.startsWith('http') ? res.contact_info.github : 'https://' + res.contact_info.github;
        el.resGithub.textContent = 'github.com/profile';
        el.resGithub.classList.remove('hidden');
    } else {
        el.resGithub.removeAttribute('href');
        el.resGithub.textContent = 'Not found';
    }
    
    // 3. Actionable Checklist Bullet Points
    el.recommendationList.innerHTML = '';
    res.ats_results.recommendations.forEach(rec => {
        const li = document.createElement('li');
        
        // Clean double asterisks markdown format
        const cleanText = rec.replace(/\*\*/g, '');
        li.innerHTML = cleanText;
        
        // Choose list icon class based on keywords
        if (cleanText.toLowerCase().includes('missing section') || cleanText.toLowerCase().includes('missing email') || cleanText.toLowerCase().includes('missing phone')) {
            li.classList.add('error');
        } else if (cleanText.toLowerCase().includes('outstanding') || cleanText.toLowerCase().includes('excellent')) {
            li.classList.add('success');
        } else if (cleanText.toLowerCase().includes('increase') || cleanText.toLowerCase().includes('reduce') || cleanText.toLowerCase().includes('action verbs')) {
            li.classList.add('warn');
        } else {
            li.classList.add('info');
        }
        
        el.recommendationList.appendChild(li);
    });
    
    // 4. Populate Skill category buttons
    el.categoriesStrip.innerHTML = '';
    el.skillBadgesContainer.innerHTML = '';
    
    const categories = Object.keys(res.extracted_skills);
    if (categories.length > 0) {
        state.activeSkillCategory = categories[0];
        
        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = 'cat-tab' + (cat === state.activeSkillCategory ? ' active' : '');
            btn.textContent = `${cat} (${res.extracted_skills[cat].length})`;
            btn.addEventListener('click', () => {
                state.activeSkillCategory = cat;
                document.querySelectorAll('.cat-tab').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderSkillBadges();
            });
            el.categoriesStrip.appendChild(btn);
        });
        
        renderSkillBadges();
    } else {
        el.skillBadgesContainer.innerHTML = '<span class="text-muted">No taxonomic skills detected.</span>';
    }
}

// Dynamic skill tab badges renderer
function renderSkillBadges() {
    el.skillBadgesContainer.innerHTML = '';
    const res = state.parsedResume;
    if (!res || !state.activeSkillCategory) return;
    
    const skills = res.extracted_skills[state.activeSkillCategory] || [];
    skills.forEach(skill => {
        const span = document.createElement('span');
        span.className = 'skill-badge';
        span.textContent = skill;
        el.skillBadgesContainer.appendChild(span);
    });
}

// Populate Tab 2: Job description match results
function renderMatcherResults(data) {
    el.matcherResults.classList.remove('hidden');
    
    const matchScore = data.overall_match_percentage;
    el.matchScoreText.textContent = `${matchScore}%`;
    el.matchBarFill.style.width = `${matchScore}%`;
    
    // Class tier overrides
    el.matchTier.textContent = `Tier: ${data.compatibility_tier}`;
    el.matchDesc.textContent = data.compatibility_description;
    
    if (matchScore >= 80) {
        el.matchTier.className = 'text-emerald';
        el.matchBarFill.style.background = 'linear-gradient(90deg, var(--accent-indigo) 0%, var(--accent-emerald) 100%)';
    } else if (matchScore >= 60) {
        el.matchTier.className = 'text-indigo';
        el.matchBarFill.style.background = 'linear-gradient(90deg, var(--accent-indigo) 0%, var(--accent-cyan) 100%)';
    } else if (matchScore >= 40) {
        el.matchTier.className = 'text-amber';
        el.matchBarFill.style.background = 'linear-gradient(90deg, var(--accent-indigo) 0%, var(--accent-amber) 100%)';
    } else {
        el.matchTier.className = 'text-rose';
        el.matchBarFill.style.background = 'linear-gradient(90deg, var(--accent-indigo) 0%, var(--accent-rose) 100%)';
    }
    
    // Mini values
    el.semanticSimVal.textContent = `${data.semantic_similarity}%`;
    el.skillCovVal.textContent = `${data.skill_coverage_percentage}%`;
    
    // Populating green overlapping badges
    el.matchingSkillsBox.innerHTML = '';
    if (data.matching_skills.length > 0) {
        data.matching_skills.forEach(s => {
            const span = document.createElement('span');
            span.className = 'match-item-badge positive';
            span.textContent = s;
            el.matchingSkillsBox.appendChild(span);
        });
    } else {
        el.matchingSkillsBox.innerHTML = '<span class="text-muted">No overlapping skills found in job description.</span>';
    }
    
    // Populating red missing badges
    el.missingSkillsBox.innerHTML = '';
    if (data.missing_skills.length > 0) {
        data.missing_skills.forEach(s => {
            const span = document.createElement('span');
            span.className = 'match-item-badge negative';
            span.textContent = s;
            el.missingSkillsBox.appendChild(span);
        });
    } else {
        el.missingSkillsBox.innerHTML = '<span class="text-emerald">Perfect technical coverage! You possess all required skills.</span>';
    }
}

// Populate Tab 3: Career pathways and dynamic roadmaps
function renderCareerRoadmaps() {
    const res = state.parsedResume;
    if (!res) return;
    
    const recs = res.recommender_results;
    
    // predicted header info
    el.predictedCategoryText.textContent = recs.predicted_category;
    el.predictionSummaryText.innerHTML = `${recs.prediction_summary}`;
    
    // recommended accordion rows
    el.careerCardsContainer.innerHTML = '';
    
    recs.top_recommendations.forEach((rec, idx) => {
        const accordion = document.createElement('div');
        accordion.className = 'career-accordion' + (idx === 0 ? ' expanded' : ''); // Expand first by default
        
        // Progress tag color class
        let tagClass = 'low';
        if (rec.match_percentage >= 70) tagClass = 'high';
        else if (rec.match_percentage >= 40) tagClass = 'med';
        
        // Match lists layout
        const matchingList = rec.matching_skills.map(s => `<span class="match-item-badge positive">${s}</span>`).join('') || '<span class="text-muted">None</span>';
        const missingList = rec.missing_skills.map(s => `<span class="match-item-badge negative">${s}</span>`).join('') || '<span class="text-emerald">Complete coverage</span>';
        
        // Timeline roadmaps
        const paths = recs.learning_paths[rec.role] || [];
        const roadmapTimeline = paths.map(p => {
            const cleanText = p.replace(/\*\*/g, '');
            return `<div class="roadmap-step">${cleanText}</div>`;
        }).join('') || '<div class="roadmap-step text-emerald">🎉 Congratulations! You have no missing skill roadmaps required for this role. Let\'s practice coding interview sheets.</div>';
        
        // Market Insights details
        const insights = rec.insights || {};
        const avgSalary = insights.avg_salary || 'N/A';
        const growthTrend = insights.growth_trend || 'N/A';
        const skillsInDemand = (insights.skills_in_demand || []).join(', ') || 'N/A';

        const insightsHtml = `
            <div class="career-insights-block">
                <h5><i class="fa-solid fa-chart-bar text-indigo"></i> Job Market Demand & Salary Insights</h5>
                <div class="insights-grid">
                    <div class="insight-card">
                        <span class="insight-icon"><i class="fa-solid fa-money-bill-wave text-emerald"></i></span>
                        <div class="insight-details">
                            <span class="insight-title">Average Salary</span>
                            <span class="insight-value">${avgSalary} / yr</span>
                        </div>
                    </div>
                    <div class="insight-card">
                        <span class="insight-icon"><i class="fa-solid fa-arrow-trend-up text-cyan"></i></span>
                        <div class="insight-details">
                            <span class="insight-title">Growth Trend</span>
                            <span class="insight-value">${growthTrend}</span>
                        </div>
                    </div>
                    <div class="insight-card">
                        <span class="insight-icon"><i class="fa-solid fa-fire text-amber"></i></span>
                        <div class="insight-details">
                            <span class="insight-title">Trending Skills</span>
                            <span class="insight-value">${skillsInDemand}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        accordion.innerHTML = `
            <div class="career-accordion-header">
                <div class="accordion-title-block">
                    <span class="mini-progress-pill ${tagClass}">${rec.match_percentage}% Match</span>
                    <h4>${idx+1}. ${rec.role}</h4>
                </div>
                <i class="fa-solid fa-chevron-down accordion-chevron"></i>
            </div>
            
            <div class="career-accordion-body">
                <p class="career-desc">${rec.description}</p>
                
                <div class="career-skills-matrix">
                    <div class="matrix-col">
                        <h5>Possessed Skills</h5>
                        <div>${matchingList}</div>
                    </div>
                    <div class="matrix-col">
                        <h5>Missing Requirements</h5>
                        <div>${missingList}</div>
                    </div>
                </div>
                
                ${insightsHtml}
                
                <div class="career-roadmap-block">
                    <h5>🗺️ Recommended Upskilling Roadmap</h5>
                    <div class="roadmap-timeline">
                        ${roadmapTimeline}
                    </div>
                </div>
            </div>
        `;
        
        // Accordion click toggle
        const header = accordion.querySelector('.career-accordion-header');
        header.addEventListener('click', () => {
            accordion.classList.toggle('expanded');
        });
        
        el.careerCardsContainer.appendChild(accordion);
    });
}

// Render Tab 4: Supported skills explorer folders
function renderTaxonomyBrowser(taxonomy) {
    el.taxonomyGrid.innerHTML = '';
    
    Object.keys(taxonomy).forEach(cat => {
        const accordion = document.createElement('div');
        accordion.className = 'folder-accordion';
        
        const skillsList = taxonomy[cat].map(s => `<span class="folder-badge">${s}</span>`).join('');
        
        accordion.innerHTML = `
            <div class="folder-header">
                <span class="folder-title">
                    <i class="fa-regular fa-folder-open"></i>
                    ${cat}
                </span>
                <span class="mini-progress-pill">${taxonomy[cat].length} Skills</span>
            </div>
            <div class="folder-body">
                ${skillsList}
            </div>
        `;
        
        // Folder click toggle
        const header = accordion.querySelector('.folder-header');
        header.addEventListener('click', () => {
            accordion.classList.toggle('expanded');
        });
        
        el.taxonomyGrid.appendChild(accordion);
    });
}

// ==========================================================================
// 5. Utility UI functions & Pre-loaders
// ==========================================================================

// Global Toast notifications
function showToast(message, type = 'success') {
    el.toast.className = `toast ${type}`;
    
    // Choose icons
    let icon = '<i class="fa-solid fa-circle-check"></i>';
    if (type === 'error') icon = '<i class="fa-solid fa-circle-exclamation"></i>';
    else if (type === 'warn') icon = '<i class="fa-solid fa-triangle-exclamation"></i>';
    
    el.toast.innerHTML = `${icon} <span>${message}</span>`;
    el.toast.classList.remove('hidden');
    
    // Reset timer
    if (window.toastTimeout) clearTimeout(window.toastTimeout);
    
    window.toastTimeout = setTimeout(() => {
        el.toast.classList.add('hidden');
    }, 4000);
}

// Load static Job Descriptions dropdown and Skill taxonomy on page mount
document.addEventListener('DOMContentLoaded', () => {
    // 1. Fetch sample JDs
    fetch('/api/sample-jds')
    .then(res => res.json())
    .then(data => {
        state.sampleJds = data;
        
        data.forEach(jd => {
            const opt = document.createElement('option');
            opt.value = jd.id;
            opt.textContent = `${jd.company} - ${jd.title}`;
            el.sampleJdSelect.appendChild(opt);
        });
    })
    .catch(err => console.error('Error fetching sample JDs:', err));
    
    // 2. Fetch Skill database
    fetch('/api/skill-taxonomy')
    .then(res => res.json())
    .then(data => {
        renderTaxonomyBrowser(data);
    })
    .catch(err => console.error('Error fetching skill database:', err));
});

// Dropdown change auto-fills text area
el.sampleJdSelect.addEventListener('change', (e) => {
    const val = e.target.value;
    if (!val) {
        el.jdTextArea.value = '';
        return;
    }
    
    const jd = state.sampleJds.find(j => j.id === val);
    if (!jd) return;
    
    let text = `Title: ${jd.title}\nCompany: ${jd.company}\nExperience: ${jd.experience}\n\nDescription:\n${jd.description}\n\nRequired Skills:\n` + jd.skills.join(', ');
    if (jd.preferred_skills && jd.preferred_skills.length > 0) {
        text += `\n\nPreferred Skills:\n` + jd.preferred_skills.join(', ');
    }
    if (jd.responsibilities && jd.responsibilities.length > 0) {
        text += `\n\nResponsibilities:\n` + jd.responsibilities.map(r => `- ${r}`).join('\n');
    }
    
    el.jdTextArea.value = text;
});
