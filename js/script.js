/* =========================
   CropGuard AI - script.js
   Complete Frontend Logic
========================= */




// ========================
// IMAGE PREVIEW FUNCTION
// ========================

function previewImage(event) {

    const preview = document.getElementById('preview');
    const file = event.target.files[0];

    if (file) {

        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };

        reader.readAsDataURL(file);
    }
}




// ========================
// DETECTION PAGE LOGIC
// ========================

if (document.getElementById('analyzeBtn')) {

    document.getElementById('analyzeBtn').addEventListener('click', analyzeImage);
}




async function analyzeImage() {

    const fileInput       = document.getElementById('cropImage');
    const cropSelect      = document.getElementById('cropType');
    const loading         = document.getElementById('loading');
    const resultSection   = document.getElementById('resultSection');


    // Get the selected crop type value from dropdown
    const cropType = cropSelect.value;


    // Validate image uploaded
    if (!fileInput.files[0]) {
        alert('Please upload a crop image first.');
        return;
    }


    // Validate crop type selected
    if (!cropType || cropType === '') {
        alert('Please select a crop type.');
        return;
    }


    // Show loading and hide old result
    loading.style.display = 'block';
    resultSection.style.display = 'none';


    // Prepare form data
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('crop_type', cropType);


    try {

        // Send to Flask backend
        const response = await fetch('https://cropguard-ai-backend.onrender.com', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Hide loading
        loading.style.display = 'none';

        // Check for error
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        // Display result with correct crop type
        displayResult(data, cropType);

        // Save to localStorage for dashboard
        saveScanRecord(data, cropType);


    } catch (error) {

        loading.style.display = 'none';
        alert('Connection error. Make sure backend server is running on http://localhost:5000');
        console.error('Fetch error:', error);
    }
}




// ========================
// DISPLAY RESULT FUNCTION
// Fixed: Shows correct crop name
// ========================

function displayResult(data, cropType) {

    const resultSection      = document.getElementById('resultSection');
    const cropResult         = document.getElementById('cropResult');
    const healthResult       = document.getElementById('healthResult');
    const confidenceResult   = document.getElementById('confidenceResult');
    const adviceText         = document.getElementById('adviceText');


    // Show result section
    resultSection.style.display = 'block';


    // Capitalize crop name properly
    // wheat -> Wheat
    // sugarcane -> Sugarcane
    let cropName = '';

    if (cropType === 'wheat') {
        cropName = 'Wheat';
    } else if (cropType === 'sugarcane') {
        cropName = 'Sugarcane';
    } else {
        cropName = cropType.charAt(0).toUpperCase() + cropType.slice(1);
    }


    // Set crop name
    cropResult.textContent = 'Crop: ' + cropName;


    // Set disease or healthy status
    if (data.health === 'Healthy') {
        healthResult.textContent = 'Status: Healthy';
        healthResult.style.color = '#2e7d32';
    } else {
        healthResult.textContent = 'Status: ' + data.status + ' (Diseased)';
        healthResult.style.color = '#c62828';
    }


    // Set confidence
    confidenceResult.textContent = 'Confidence: ' + data.confidence + '%';


    // Set advice
    adviceText.textContent = data.advice;


    // Scroll to result smoothly
    resultSection.scrollIntoView({ behavior: 'smooth' });
}




// ========================
// SAVE SCAN TO LOCALSTORAGE
// Fixed: Saves correct crop name
// ========================

function saveScanRecord(data, cropType) {

    // Get existing records from storage
    const records = JSON.parse(localStorage.getItem('scanRecords')) || [];


    // Build crop display name
    let cropName = '';

    if (cropType === 'wheat') {
        cropName = 'Wheat';
    } else if (cropType === 'sugarcane') {
        cropName = 'Sugarcane';
    } else {
        cropName = cropType.charAt(0).toUpperCase() + cropType.slice(1);
    }


    // Create scan record
    const record = {
        crop       : cropName,
        status     : data.health === 'Healthy' ? 'Healthy' : data.status,
        health     : data.health,
        confidence : data.confidence,
        advice     : data.advice,
        date       : new Date().toLocaleDateString(),
        time       : new Date().toLocaleTimeString()
    };


    // Add to beginning of array
    records.unshift(record);


    // Keep only last 50 records
    if (records.length > 50) {
        records.splice(50);
    }


    // Save back to localStorage
    localStorage.setItem('scanRecords', JSON.stringify(records));
}




// ========================
// DASHBOARD PAGE LOGIC
// ========================

if (document.getElementById('totalScans')) {

    loadDashboard();
}




function loadDashboard() {

    const records = JSON.parse(localStorage.getItem('scanRecords')) || [];


    // Calculate statistics
    const totalScans    = records.length;
    const healthyCount  = records.filter(r => r.health === 'Healthy').length;
    const diseasedCount = records.filter(r => r.health === 'Diseased').length;


    // Update stat cards
    document.getElementById('totalScans').textContent    = totalScans;
    document.getElementById('healthyCrops').textContent   = healthyCount;
    document.getElementById('diseasedCrops').textContent  = diseasedCount;


    // Update chart bars
    updateChartBars(healthyCount, diseasedCount);


    // Load recent activity
    loadActivity(records);


    // Load history table
    loadHistoryTable(records);
}




// ========================
// UPDATE CHART BARS
// ========================

function updateChartBars(healthy, diseased) {

    const total = healthy + diseased;

    if (total === 0) return;

    const healthyBar = document.querySelector('.bar.healthy');
    const diseaseBar = document.querySelector('.bar.disease');

    if (healthyBar && diseaseBar) {

        const healthyPercent  = Math.round((healthy / total) * 100);
        const diseasedPercent = Math.round((diseased / total) * 100);

        healthyBar.style.width = Math.max(healthyPercent, 5) + '%';
        diseaseBar.style.width = Math.max(diseasedPercent, 5) + '%';

        healthyBar.querySelector('span').textContent =
            'Healthy - ' + healthyPercent + '% (' + healthy + ')';

        diseaseBar.querySelector('span').textContent =
            'Diseased - ' + diseasedPercent + '% (' + diseased + ')';
    }
}




// ========================
// LOAD RECENT ACTIVITY
// Fixed: Shows correct crop name
// ========================

function loadActivity(records) {

    const activityList = document.getElementById('activityList');

    if (records.length === 0) {
        activityList.innerHTML = '<li>No scans available yet.</li>';
        return;
    }

    // Show last 5 activities
    const recentRecords = records.slice(0, 5);

    activityList.innerHTML = recentRecords.map(function (record) {

        // Color based on health status
        let statusColor = '#2e7d32';
        let statusText  = 'Healthy';

        if (record.health === 'Diseased') {
            statusColor = '#c62828';
            statusText  = record.status;
        }

        return '<li>' +
            record.crop + ' scan - ' +
            '<strong style="color: ' + statusColor + '">' +
                statusText +
            '</strong>' +
            ' (' + record.confidence + '%) - ' +
            record.date + ' ' + (record.time || '') +
        '</li>';

    }).join('');
}




// ========================
// LOAD HISTORY TABLE
// Fixed: Shows correct crop name
// ========================

function loadHistoryTable(records) {

    const historyTable = document.getElementById('historyTable');

    if (records.length === 0) {

        historyTable.innerHTML =
            '<tr>' +
                '<td colspan="4">No records found</td>' +
            '</tr>';
        return;
    }


    historyTable.innerHTML = records.map(function (record) {

        // Color based on health
        let statusColor = '#2e7d32';
        let statusText  = 'Healthy';

        if (record.health === 'Diseased') {
            statusColor = '#c62828';
            statusText  = record.status;
        }

        return '<tr>' +
            '<td>' + record.crop + '</td>' +
            '<td style="color: ' + statusColor + '; font-weight: bold;">' +
                statusText +
            '</td>' +
            '<td>' + record.confidence + '%</td>' +
            '<td>' + record.date + '</td>' +
        '</tr>';

    }).join('');
}




// ========================
// NAVBAR ACTIVE LINK
// ========================

const navLinks = document.querySelectorAll('.navbar ul li a');

navLinks.forEach(function (link) {

    // Get current page file name
    const currentPage = window.location.pathname.split('/').pop();
    const linkPage    = link.getAttribute('href');

    if (linkPage === currentPage) {
        link.style.color      = '#a5d6a7';
        link.style.fontWeight = 'bold';
    }
});