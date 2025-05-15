// Open modal function
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "block";
        setTimeout(() => {
            modal.style.display = "none";
        }, 3000);
    }
}

// Close modal function
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "none";
}

// Close modal on outside click
window.onclick = function (event) {
    const modals = ['resumeModal', 'jdModal', 'submitModal', 'resumeNotSelected', 'JDNotSelected'];
    modals.forEach(id => {
        const modal = document.getElementById(id);
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
};

// Event listeners
document.addEventListener("DOMContentLoaded", function () {
    const resumeInput = document.getElementById('resume-upload');
    const jdInput = document.getElementById('jobdesc-upload');
    const form = document.getElementById("resume-form");

    if (form) form.reset();

    // Resume file selected
    resumeInput.addEventListener('change', function () {
        if (resumeInput.files.length > 0) {
            openModal('resumeModal');
        }
    });

    // JD file selected
    jdInput.addEventListener('change', function () {
        if (jdInput.files.length > 0) {
            openModal('jdModal');
        }
    });

    // Form submit validation
    form.addEventListener("submit", function (event) {
        const hasResume = resumeInput.files.length > 0;
        const hasJD = jdInput.files.length > 0 || document.getElementById("jobdesc-textarea").value.trim() !== "";

        if (!hasResume) {
            event.preventDefault();
            openModal('resumeNotSelected');
            return;
        }

        if (!hasJD) {
            event.preventDefault();
            openModal('JDNotSelected');
            return;
        }

        
        openModal('submitModal').reset();
    });
});
window.onpageshow = function (event) {
    if (event.persisted || window.performance.getEntriesByType("navigation")[0].type === "back_forward") {
        const form = document.getElementById("resume-form");
        if (form) form.reset();
    }
};
